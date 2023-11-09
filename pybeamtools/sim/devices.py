import abc
import logging
import time
from enum import Enum, auto
from typing import Literal, Optional

import numpy as np
from pydantic import BaseModel, Extra, NonNegativeFloat, validator
from ..utils.pydantic import JSON_ENCODERS

logger = logging.getLogger(__name__)


class WriteResult:
    def __init__(self) -> None:
        pass


class Device(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        # self.time = time_fun or time.time
        pass

    @abc.abstractmethod
    def read(self, t):
        pass

    @abc.abstractmethod
    def write(self, value, t):
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
    def read_exact(self, t):
        pass


class TRIGSPEC(Enum):
    PROPAGATE = 1
    IGNORE = 2


# class MagnetEngineDevice(EngineDevice):
#     DEVICE_TYPE = 'Generic magnet'
#
#     def __init__(self, name: str,
#                  read_channel: str,
#                  exact_read_channel: str,
#                  initial_value=0.0,
#                  now: float = 0.0,
#                  low=None, high=None,
#                  noise=None, resolution=None,
#                  measurement_period=None,
#                  model='instant', pmodel_kwargs=None
#                  ) -> None:
#         if high is not None and low is not None:
#             assert high > low
#         assert noise is None or noise >= 0.0
#         assert resolution is None or resolution > 0.0
#
#         self.raw_value = self.setpoint = initial_value
#         self.read_channel = read_channel
#         self.exact_read_channel = exact_read_channel
#         self.time_last_update = now
#         self.time_last_write = now
#         self.time_last_read = now
#         self.noise = noise
#         self.resolution = resolution
#         self.low = low
#         self.high = high
#         self.model = model
#         self.measurement_period = measurement_period
#         self.pmodel_kwargs = pmodel_kwargs or {'decay_constant': 2}
#         self._update_value(now)
#
#         channel_map = {read_channel: {}, exact_read_channel: {}}
#         self.params = {'low': low,
#                        'high': high,
#                        'resolution': resolution,
#                        'model': model,
#                        'noise': noise
#                        }
#         super().__init__(name=name,
#                          update_fun=self._update_fun,
#                          read_fun=self._read_fun,
#                          write_fun=self._write_fun,
#                          channel_map=channel_map)
#
#     def _read_fun(self, t_sched, t_run, channel_name) -> float:
#         self.time_last_read = t_run
#         if channel_name == self.read_channel:
#             return self.value
#         elif channel_name == self.exact_read_channel:
#             return self.raw_value
#         else:
#             raise Exception(f'Unknown channel {channel_name}')
#
#     def _write_fun(self, t_sched, t_run, value_dict):
#         self.time_last_write = t_run
#         if self.exact_read_channel in value_dict:
#             raise Exception(f'Cannot write exact channel')
#         if self.read_channel not in value_dict:
#             raise Exception(f'Device {self.name} requires channel {self.read_channel}')
#         value = value_dict[self.read_channel]
#         if self.low and value < self.low:
#             raise ValueError(f'Value {value} below bounds ({self.low}|{self.high})')
#             # return False
#         if self.high and value > self.high:
#             raise ValueError(f'Value {value} above bounds ({self.low}|{self.high})')
#             # return False
#         self.setpoint = value
#
#     def _update_fun(self, t_sched, t_run, data):
#         self.time_last_update = t_run
#         self._update_value(t_run)
#         raw_read = self.raw_value
#         if self.noise is not None and self.noise != 0.0:
#             noise = float(np.random.normal(0, self.noise, 1))
#             raw_read += noise
#         if self.resolution is not None and self.resolution != 0.0:
#             raw_read = int(raw_read / self.resolution) * self.resolution
#         self.value = raw_read
#         return {self.read_channel: self.value,
#                 self.exact_read_channel: self.raw_value
#                 }
#
#     def _update_value(self, t: float):
#         if self.model == 'exponential':
#             # For exp, N(t) = N0 exp(-lambda*T)
#             decay_constant = self.pmodel_kwargs['decay_constant']
#             delta = t - self.time_last_update
#             output_delta = self.value - self.setpoint
#             new_value = self.setpoint - output_delta * np.exp(-decay_constant * delta)
#             self.raw_value = new_value
#             # self.time_last_update = now
#         elif self.model == 'instant':
#             self.raw_value = self.setpoint
#             # self.time_last_update = now
#         else:
#             raise Exception(f'Unknown model {self.model}')
#
#
# class ModelEngineDevice(EngineDevice):
#     DEVICE_TYPE = 'Model wrapper'
#
#     def __init__(self,
#                  device: VirtualDevice
#                  ):
#         self.device = device
#         self.data = {}
#         self.params = {'wrapped_device': str(device)}
#         channel_map = {device.name: {}}
#         super().__init__(name=device.name,
#                          update_fun=self._update_fun,
#                          read_fun=self._read_fun,
#                          write_fun=self._write_fun,
#                          channel_map=channel_map)
#
#     def _update_fun(self, t_sched, t_run, data):
#         self.device.update(t_run)
#         self.data[self.device.name] = self.device.read(t_run)
#         return self.data.copy()
#
#     def _read_fun(self, t_sched, t_run, channel_name):
#         assert channel_name == self.device.name
#         return self.data[channel_name]
#
#     def _write_fun(self, t_sched, t_run, value_dict):
#         assert len(value_dict) == 1 and self.device.name in value_dict
#         self.device.write(t_run, value_dict[self.device.name])


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

    def write(self, value, t) -> bool:
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

    def write(self, value, t) -> bool:
        raise NotImplementedError()

    def update(self, t):
        self.time_last_update = time.time()
        self.raw_value = self.time_last_update - self.time_start


class TimeModel(VirtualDevice):
    def __init__(self, name: str, t: float):
        self.raw_value = t
        super().__init__(name)

    def read(self, t) -> float:
        return t

    def read_exact(self, t) -> float:
        return t

    def write(self, value, t) -> bool:
        raise NotImplementedError()

    def update(self, t):
        self.raw_value = t


# class DeviceGroup:
#     def __init__(self, *args):
#         assert all(isinstance(el, (Device, DeviceGroup)) for el in args)
#         self.devices = args
#
#     def __contains__(self, item):
#         return item in self.devices


# class GenericOutput(VirtualDevice):
#     def __init__(self, name: str, eval_fn, update_fn=None, *args, **kwargs) -> None:
#         self.eval_fn = eval_fn
#         self.update_fn = update_fn
#         self.args = args
#         self.kwargs = kwargs
#         super().__init__(name)
#
#     def read(self) -> Measurement:
#         return self.eval_fn(*self.args, **self.kwargs)
#
#     def read_exact(self) -> Measurement:
#         return self.read()
#
#     def write(self, value):
#         self.setpoint = value
#         self.time_setpoint = time.time()
#
#     def update(self):
#         return self.update_fn() if self.update_fn else None


# class GenericInput(VirtualDevice):
#     def __init__(self, name: str, eval_fn, update_fn=None, *args, **kwargs) -> None:
#         self.eval_fn = eval_fn
#         self.update_fn = update_fn
#         self.args = args
#         self.kwargs = kwargs
#         super().__init__(name)
#
#     def read(self) -> Measurement:
#         return self.eval_fn(*self.args, **self.kwargs)
#
#     def read_exact(self) -> Measurement:
#         return self.read()
#
#     def write(self, value):
#         raise Exception('Setting generic input is not allowed')
#
#     def update(self):
#         return self.update_fn() if self.update_fn else None
#
#
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


#
#
# class StaticOutputDevice(VirtualDevice):
#     def __init__(self, name: str, value=0.0) -> None:
#         self.value = value
#         super().__init__(name)
#
#     def read(self) -> float:
#         return self.value
#
#     def read_exact(self) -> float:
#         return self.value
#
#     def write(self, value):
#         raise Exception('Setting not allowed')
#
#     def update(self):
#         raise Exception('Update not allowed')


class ModelOptions(BaseModel):
    class Config:
        extra = Extra.forbid
        json_encoders = JSON_ENCODERS


class MTYPE(Enum):
    INSTANT = auto()
    EXPONENTIAL = auto()


class RealisticModelOptions(ModelOptions):
    name: str
    value: float = None
    low: float = None
    high: float = None
    noise: NonNegativeFloat = None
    resolution: NonNegativeFloat = None
    model: Literal['instant', 'exponential', 'underdamped'] = 'instant'
    pmodel_kwargs: dict = {}
    # setpoint params
    setpoint_update_rate: float = None

    #
    readback_update_rate: float = None
    event_threshold: float = None

    @validator('low', 'high')
    def check_limits(cls, v):
        low, high = v
        if high is not None and low is not None:
            assert high > low

    @validator('pmodel_kwargs', always=True)
    def check_model_opts(cls, kw, values):
        if values['model'] == 'exponential':
            kw.update({'decay_constant': 2})
        elif values['model'] == 'underdamped':
            kw.update({'decay_constant': 5, 'c': 0.9})
        return kw


class TimeAwareModel(VirtualDevice):
    @abc.abstractmethod
    def get_next_event(self, t) -> tuple:
        pass

    @abc.abstractmethod
    def read_setpoint(self, t) -> float:
        pass


class RealisticModel(TimeAwareModel):
    def __init__(self, o: RealisticModelOptions, t: float) -> None:
        self.o = o
        super().__init__(o.name)
        self.raw_value = self.value = o.value
        self.last_setpoint = self.setpoint = o.value
        self.time_last_update = t
        self.time_last_write = t
        self.time_last_read = t
        self.time_last_setpoint_event = t
        self.time_last_readback_event = t
        self._time_last_call = t
        self.last_known_t = t

    def check_t(self, t):
        if t < self.last_known_t:
            raise ValueError(f'Time went backwards from {self.last_known_t} to {t}')

    @property
    def time_last_call(self):
        return self._time_last_call

    @time_last_call.setter
    def time_last_call(self, t):
        if t < self.last_known_t:
            raise ValueError(f'Time went backwards!')
        self._time_last_call = self.last_known_t = t

    def read(self, t: float) -> float:
        self.check_t(t)
        self.update(t)
        self.time_last_read = t
        return self.value

    def read_exact(self, t: float) -> float:
        self.check_t(t)
        self.update(t)
        self.time_last_read = t
        return self.raw_value

    def read_setpoint(self, t: float) -> float:
        self.check_t(t)
        self.update(t)
        self.time_last_read = t
        return self.setpoint

    def write(self, setpoint: float, t: float):
        self.check_t(t)
        assert self.time_last_update == t, f'Write time {t=} different from update ' \
                                           f'{self.time_last_update=}'
        if self.o.low and setpoint < self.o.low:
            raise ValueError(f'Value {setpoint} below ({self.o.low}|{self.o.high})')
        if self.o.high and setpoint > self.o.high:
            raise ValueError(f'Value {setpoint} above {self.o.low}|{self.o.high})')
        self.last_setpoint = self.value
        self.setpoint = setpoint
        self.time_last_write = self.time_last_call = t
        self.update(t)

    def update(self, t: float):
        self.check_t(t)
        self._update_raw_value(t)
        self.time_last_update = self.time_last_call = t

    def _update_raw_value(self, t: float):
        if self.o.model == 'exponential':
            # For exp, N(t) = N0 exp(-lambda*T)
            decay_constant = self.o.pmodel_kwargs['decay_constant']
            delta_t = t - self.time_last_update
            delta_v = self.raw_value - self.setpoint
            new_value = self.setpoint + delta_v * np.exp(-decay_constant * delta_t)
            self.raw_value = new_value
            # self.time_last_update = now
        elif self.o.model == 'underdamped':
            # N(t) = N0 exp(-w*c*T) exp(+- i*w*sqrt(1-c**2)*T)
            # = N0 exp(-w*c*T) cos(w*sqrt(1-c**2)*T)
            dc = self.o.pmodel_kwargs['decay_constant']
            c = self.o.pmodel_kwargs['c']

            delta_t = t - self.time_last_update
            delta_t_abs = t - self.time_last_write
            delta_v = self.raw_value - self.setpoint
            delta_v_abs = self.last_setpoint - self.setpoint
            factor = np.exp(-dc * c * delta_t_abs) * np.cos(dc * np.sqrt(1 - c * c) * delta_t_abs)
            new_value = self.setpoint + delta_v_abs * factor
            self.raw_value = new_value
            # self.time_last_update = now
        elif self.o.model == 'instant':
            self.raw_value = self.setpoint
            # self.time_last_update = now
        else:
            raise Exception

        value = self.raw_value
        if self.o.noise is not None and self.o.noise != 0.0:
            noise = np.random.normal(0, self.o.noise, 1)
            value += float(noise)
        if self.o.resolution is not None and self.o.resolution != 0.0:
            value = int(value / self.o.resolution) * self.o.resolution
        self.value = value

    # def advance_time(self, t: float) -> list:
    #     if self.o.readback_update_rate is None:
    #         return []
    #     # now = self.time_last_call
    #     now = self.time_last_readback_event
    #     step = self.o.readback_update_rate
    #     events = []
    #     while True:
    #         t_next = now + step
    #         if t_next > t:
    #             break
    #         self.logger.debug(f'Model {self.o.name}: advancing {now} -> {t_next}')
    #         if t_next - self.time_last_readback_event >= self.o.readback_update_rate:
    #             self.update(t_next)
    #             events.append((t_next, self.value))
    #             self.time_last_readback_event = t_next
    #         now = t_next
    #     self.update(t)
    #     self.time_last_call = t
    #     return events

    def advance_direct_to_time(self, t: float) -> list:
        """ Advance all the way to new time, only producing latest result if any """
        if self.o.readback_update_rate is None:
            return []
        tl = self.time_last_call
        self.update(t)
        if t - self.time_last_readback_event >= self.o.readback_update_rate:
            logger.debug(f'Model {self.o.name}: ({tl}) -> ({t}) | {self.value:.5f} (TRIG, next in '
                         f'{self.o.readback_update_rate:.5f})')
            result = [(t, self.value)]
            self.time_last_readback_event = t
            return result
        else:
            until_update = t - self.time_last_readback_event
            logger.debug(f'Model {self.o.name}: ({tl}) -> ({t}) | ({until_update:.5f}) until '
                         f'next update, last at ({self.time_last_readback_event:.5f})')
            return []

    def get_next_event(self, t: float) -> Optional[float]:
        events = self.advance_direct_to_time(t)
        if len(events) > 0:
            if len(events) > 1:
                logger.warning(f'Multiple scan events detected - reduce step')
            return events[-1][1]
        else:
            return None


class RealisticMagnet(VirtualDevice):
    def __init__(self, name: str, value: float = 0.0, t: float = None,
                 low=None, high=None,
                 noise=None, resolution=None,
                 measurement_period=None,
                 model='instant', pmodel_kwargs=None
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
        self.pmodel_kwargs = pmodel_kwargs or {'decay_constant': 2}

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
            # decay_constant = self.pmodel_kwargs['decay_constant']
            # delta = t - self.time_last_update
            # output_delta = self.value - self.setpoint
            # new_value = self.setpoint - output_delta * np.exp(-decay_constant * delta)
            # self.raw_value = new_value

            decay_constant = self.pmodel_kwargs['decay_constant']
            delta_t = t - self.time_last_update
            delta_v = self.value - self.setpoint
            new_value = self.setpoint + delta_v * np.exp(-decay_constant * delta_t)
            self.raw_value = new_value

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
