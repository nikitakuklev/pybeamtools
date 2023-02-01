import abc
import time
import random
import uuid
from typing import Callable, Any
from enum import Enum
import numpy as np
from pydantic import BaseModel

from .errors import SimulationError, DeviceError
from .rpn import RPNCalc


class Measurement:
    def __init__(self, value) -> None:
        self.value = value


class WriteResult:
    def __init__(self) -> None:
        pass


class Device(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        # self.time = time_fun or time.time
        pass

    @abc.abstractmethod
    def read(self, t) -> Measurement:
        pass

    @abc.abstractmethod
    def write(self, t, value) -> WriteResult:
        pass

    @abc.abstractmethod
    def update(self, t):
        pass


class VirtualDevice(Device):
    def __init__(self, name: str):
        super().__init__()
        if ' ' in name:
            raise ValueError(f'Whitespace is not allowed in device name')
        self.name = name

    @abc.abstractmethod
    def read_exact(self, t) -> Measurement:
        pass


class TRIGSPEC(Enum):
    PROPAGATE = 1
    IGNORE = 2


class EngineDevice:
    DEVICE_TYPE = 'Generic'

    def __init__(self,
                 # device: Device,
                 name: str = None,
                 update_fun: Callable = None,
                 read_fun: Callable = None,
                 write_fun: Callable = None,
                 channel_map: dict = None
                 ):
        # self.device = device
        assert isinstance(channel_map, dict)
        for output, deps_dict in channel_map.items():
            assert isinstance(output, str)
            assert isinstance(deps_dict, dict), f'{deps_dict}'
            for dep, spec in deps_dict.items():
                assert isinstance(dep, str)
                assert isinstance(spec, TRIGSPEC)
        self.channel_map = channel_map or {}
        self.name = name or uuid.uuid4()[:12]
        self.update_fun = update_fun
        self.read_fun = read_fun
        self.write_fun = write_fun
        if not hasattr(self, 'params'):
            self.params = {}

    def update(self, t_sched: float, t_run: float, data: dict[str, Any]):
        if self.update_fun is not None:
            return self.update_fun(t_sched, t_run, data)
        else:
            raise Exception(f'No update function defined')

    def read(self, t_sched: float, t_run: float, channel_name: str):
        if channel_name not in self.channel_map:
            raise Exception(f'Unknown channel {channel_name}')
        if self.read_fun is not None:
            value = self.read_fun(t_sched, t_run, channel_name)
        else:
            raise Exception(f'No read function defined for {channel_name=}')
        return value

    def write(self, t_sched: float, t_run: float, value_dict: dict[str, Any]):
        for k, v in value_dict:
            if k not in self.channel_map:
                raise Exception(f'Unknown channel {k}')

        if self.write_fun is not None:
            return self.write_fun(t_sched, t_run, value_dict)
        else:
            raise SimulationError(f'Device {self.name} does not support writes')


class MagnetEngineDevice(EngineDevice):
    DEVICE_TYPE = 'Generic magnet'

    def __init__(self, name: str,
                 read_channel: str,
                 exact_read_channel: str,
                 initial_value=0.0,
                 now: float = 0.0,
                 low=None, high=None,
                 noise=None, resolution=None,
                 measurement_period=None,
                 model='instant', model_kwargs=None
                 ) -> None:
        if high is not None and low is not None:
            assert high > low
        assert noise is None or noise >= 0.0
        assert resolution is None or resolution > 0.0

        self.raw_value = self.setpoint = initial_value
        self.read_channel = read_channel
        self.exact_read_channel = exact_read_channel
        self.time_last_update = now
        self.time_last_write = now
        self.time_last_read = now
        self.noise = noise
        self.resolution = resolution
        self.low = low
        self.high = high
        self.model = model
        self.measurement_period = measurement_period
        self.model_kwargs = model_kwargs or {'decay_constant': 2}
        self._update_value(now)

        channel_map = {read_channel: {}, exact_read_channel: {}}
        self.params = {'low': low,
                       'high': high,
                       'resolution': resolution,
                       'model': model,
                       'noise': noise
                       }
        super().__init__(name=name,
                         update_fun=self._update_fun,
                         read_fun=self._read_fun,
                         write_fun=self._write_fun,
                         channel_map=channel_map)

    def _read_fun(self, t_sched, t_run, channel_name) -> float:
        self.time_last_read = t_run
        if channel_name == self.read_channel:
            return self.value
        elif channel_name == self.exact_read_channel:
            return self.raw_value
        else:
            raise Exception(f'Unknown channel {channel_name}')

    def _write_fun(self, t_sched, t_run, value_dict):
        self.time_last_write = t_run
        if self.exact_read_channel in value_dict:
            raise Exception(f'Cannot write exact channel')
        if self.read_channel not in value_dict:
            raise Exception(f'Device {self.name} requires channel {self.read_channel}')
        value = value_dict[self.read_channel]
        if self.low and value < self.low:
            raise ValueError(f'Value {value} below bounds ({self.low}|{self.high})')
            # return False
        if self.high and value > self.high:
            raise ValueError(f'Value {value} above bounds ({self.low}|{self.high})')
            # return False
        self.setpoint = value

    def _update_fun(self, t_sched, t_run, data):
        self.time_last_update = t_run
        self._update_value(t_run)
        raw_read = self.raw_value
        if self.noise is not None and self.noise != 0.0:
            noise = float(np.random.normal(0, self.noise, 1))
            raw_read += noise
        if self.resolution is not None and self.resolution != 0.0:
            raw_read = int(raw_read / self.resolution) * self.resolution
        self.value = raw_read
        return {self.read_channel: self.value,
                self.exact_read_channel: self.raw_value
                }

    def _update_value(self, t: float):
        if self.model == 'exponential':
            # For exp, N(t) = N0 exp(-lambda*T)
            decay_constant = self.model_kwargs['decay_constant']
            delta = t - self.time_last_update
            output_delta = self.value - self.setpoint
            new_value = self.setpoint - output_delta * np.exp(-decay_constant * delta)
            self.raw_value = new_value
            # self.time_last_update = now
        elif self.model == 'instant':
            self.raw_value = self.setpoint
            # self.time_last_update = now
        else:
            raise Exception(f'Unknown model {self.model}')


class ModelEngineDevice(EngineDevice):
    DEVICE_TYPE = 'Model wrapper'

    def __init__(self,
                 device: VirtualDevice
                 ):
        self.device = device
        self.data = {}
        self.params = {'wrapped_device': str(device)}
        channel_map = {device.name: {}}
        super().__init__(name=device.name,
                         update_fun=self._update_fun,
                         read_fun=self._read_fun,
                         write_fun=self._write_fun,
                         channel_map=channel_map)

    def _update_fun(self, t_sched, t_run, data):
        self.device.update(t_run)
        self.data[self.device.name] = self.device.read(t_run)
        return self.data.copy()

    def _read_fun(self, t_sched, t_run, channel_name):
        assert channel_name == self.device.name
        return self.data[channel_name]

    def _write_fun(self, t_sched, t_run, value_dict):
        assert len(value_dict) == 1 and self.device.name in value_dict
        self.device.write(t_run, value_dict[self.device.name])


# class ModelEngineDevice(EngineDevice):
#     def __init__(self,
#                  name: str,
#                  devices: list[VirtualDevice]):
#         self.devices = devices
#         self.device_names = [d.name for d in devices]
#         self.devices_map = {d.name: d for d in devices}
#         self.data = {}
#         channel_map = {}
#         for dev in devices:
#             channel_map[dev.name] = {}
#         super().__init__(name=name,
#                          update_fun=self._update_fun,
#                          read_fun=self._read_fun,
#                          write_fun=self._write_fun,
#                          channel_map=channel_map)
#
#     def _update_fun(self, t_sched, t_run, data):
#         for dev in self.devices:
#             dev.update(t_run)
#             self.data[dev.name] = dev.read(t_run)
#         return self.data.copy()
#
#     def _read_fun(self, t_sched, t_run, channel_name):
#         assert channel_name in self.device_names
#         return self.data[channel_name]
#
#     def _write_fun(self, t_sched, t_run, value_dict):
#         for k, v in value_dict.items():
#             assert k in self.device_names
#             self.devices_map[k].write(v)


class Oscillator(VirtualDevice):
    def __init__(self,
                 name: str,
                 period: float,
                 amplitude: float,
                 now: float = 0.0
                 ):
        self.time_last_update = self.t_start = now
        self.period = period
        self.amplitude = np.array([amplitude])
        self.raw_value = 0.0
        super().__init__(name)

    def read(self, t) -> float:
        return self.raw_value

    def read_exact(self, t) -> float:
        return self.raw_value

    def write(self, t, value) -> bool:
        raise NotImplementedError('Oscillator is a read-only device')

    def update(self, t):
        self.raw_value = float(
                self.amplitude * np.sin(2 * np.pi * (t - self.t_start) / self.period))
        self.time_last_update = t


class UNIXTimer(VirtualDevice):
    def __init__(self, name: str):
        self.time_start = self.time_last_update = time.time()
        self.raw_value = 0.0
        super().__init__(name)

    def read(self, t) -> float:
        return self.raw_value

    def read_exact(self, t) -> float:
        return self.raw_value

    def write(self, t, value) -> bool:
        raise NotImplementedError()

    def update(self, t):
        self.time_last_update = time.time()
        self.raw_value = self.time_last_update - self.time_start


class DeviceGroup:
    def __init__(self, *args):
        assert all(isinstance(el, (Device, DeviceGroup)) for el in args)
        self.devices = args

    def __contains__(self, item):
        return item in self.devices


class GenericOutput(VirtualDevice):
    def __init__(self, name: str, eval_fn, update_fn=None, *args, **kwargs) -> None:
        self.eval_fn = eval_fn
        self.update_fn = update_fn
        self.args = args
        self.kwargs = kwargs
        super().__init__(name)

    def read(self) -> Measurement:
        return self.eval_fn(*self.args, **self.kwargs)

    def read_exact(self) -> Measurement:
        return self.read()

    def write(self, value):
        self.setpoint = value
        self.time_setpoint = time.time()

    def update(self):
        return self.update_fn() if self.update_fn else None


class GenericInput(VirtualDevice):
    def __init__(self, name: str, eval_fn, update_fn=None, *args, **kwargs) -> None:
        self.eval_fn = eval_fn
        self.update_fn = update_fn
        self.args = args
        self.kwargs = kwargs
        super().__init__(name)

    def read(self) -> Measurement:
        return self.eval_fn(*self.args, **self.kwargs)

    def read_exact(self) -> Measurement:
        return self.read()

    def write(self, value):
        raise Exception('Setting generic input is not allowed')

    def update(self):
        return self.update_fn() if self.update_fn else None


class StaticInputDevice():
    def __init__(self, name: str, value=0.0) -> None:
        self.value = self.setpoint = value
        self.name = name

    def read(self, t=None) -> float:
        return self.value

    def read_exact(self, t=None) -> float:
        return self.value

    def write(self, value, t=None):
        self.value = self.setpoint = value

    def update(self, t=None):
        pass


class StaticOutputDevice(VirtualDevice):
    def __init__(self, name: str, value=0.0) -> None:
        self.value = value
        super().__init__(name)

    def read(self) -> float:
        return self.value

    def read_exact(self) -> float:
        return self.value

    def write(self, value):
        raise Exception('Setting not allowed')

    def update(self):
        raise Exception('Update not allowed')


class RealisticMagnet(VirtualDevice):
    def __init__(self, name: str, value: float = 0.0, t: float = None,
                 low=None, high=None,
                 noise=None, resolution=None,
                 measurement_period=None,
                 model='instant', model_kwargs=None
                 ) -> None:
        if high is not None and low is not None:
            assert high > low
        assert noise is None or noise >= 0.0
        assert resolution is None or resolution > 0.0
        super().__init__(name)
        self.raw_value = self.value = value
        self.setpoint = value
        now = t or time.time()
        self.time_last_update = now
        self.time_last_write = now
        self.time_last_read = now
        self.noise = noise
        self.resolution = resolution
        self.low = low
        self.high = high
        self.model = model
        self.measurement_period = measurement_period
        self.model_kwargs = model_kwargs or {'decay_constant': 2}

    def read(self, t: float = None) -> float:
        self.time_last_read = t or time.time()
        self._update_value(self.time_last_read)
        raw_read = self.raw_value
        if self.noise is not None and self.noise != 0.0:
            noise = np.random.normal(0, self.noise, 1)
            raw_read += float(noise)
        if self.resolution is not None and self.resolution != 0.0:
            raw_read = int(raw_read / self.resolution) * self.resolution
        self.value = raw_read
        return raw_read
        # return self.value

    def read_exact(self, t: float = None) -> float:
        # self._update_value()
        # return self.raw_value
        return self.raw_value

    def read_setpoint(self) -> float:
        return self.setpoint

    def write(self, value, t: float = None):
        self.time_last_write = t or time.time()

        if self.low and value < self.low:
            raise ValueError(f'Value {value} below bounds ({self.low}|{self.high})')
            # return False
        if self.high and value > self.high:
            raise ValueError(f'Value {value} above bounds ({self.low}|{self.high})')
            # return False
        self.setpoint = value

    def update(self, t: float):
        self.time_last_update = t or time.time()

        self._update_value(t)
        raw_read = self.raw_value
        if self.noise is not None and self.noise != 0.0:
            noise = np.random.normal(0, self.noise, 1)
            raw_read += float(noise)
        if self.resolution is not None and self.resolution != 0.0:
            raw_read = int(raw_read / self.resolution) * self.resolution
        self.value = raw_read

    def _update_value(self, t: float):
        if self.model == 'exponential':
            # For exp, N(t) = N0 exp(-lambda*T)
            decay_constant = self.model_kwargs['decay_constant']
            delta = t - self.time_last_update
            output_delta = self.value - self.setpoint
            new_value = self.setpoint - output_delta * np.exp(-decay_constant * delta)
            self.raw_value = new_value
            # self.time_last_update = now
        elif self.model == 'instant':
            self.raw_value = self.setpoint
            # self.time_last_update = now
        else:
            raise Exception


class EchoDevice(VirtualDevice):
    def __init__(self, name: str, value=0.0, t: float = None) -> None:
        super().__init__(name)
        self.value = value
        now = t or time.time()
        self.time_last_update = now
        self.time_last_write = now
        self.time_last_read = now

    def read(self, t: float = None) -> float:
        self.time_last_read = t or time.time()
        return self.value

    def read_exact(self, t: float) -> float:
        return self.read()

    def write(self, value, t: float = None):
        self.time_last_write = t or time.time()
        self.value = value

    def update(self, t: float):
        self.time_last_update = t or time.time()
