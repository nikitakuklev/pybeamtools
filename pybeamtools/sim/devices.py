import abc
import time
import random
import numpy as np


class Measurement:
    def __init__(self, value) -> None:
        self.value = value


class WriteResult:
    def __init__(self) -> None:
        pass


class Device(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def read(self) -> Measurement:
        pass

    @abc.abstractmethod
    def write(self, value) -> WriteResult:
        pass

    @abc.abstractmethod
    def update(self):
        pass


class VirtualDevice(Device):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    @abc.abstractmethod
    def read_exact(self) -> Measurement:
        pass


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


class StaticInputDevice(VirtualDevice):
    def __init__(self, name: str, value=0.0) -> None:
        self.value = value
        super().__init__(name)

    def read(self) -> float:
        return self.value

    def read_exact(self) -> float:
        return self.value

    def write(self, value):
        self.setpoint = value
        self.time_setpoint = time.time()

    def update(self):
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


class Oscillator(VirtualDevice):
    def __init__(self, name: str, period: float, amplitude: float):
        self.time_start = time.time()
        self.time_last_update = self.time_start
        self.period = period
        self.amplitude = np.array([amplitude])
        super().__init__(name)

    def read(self) -> float:
        self._update_value()
        raw_read = self.raw_value
        return raw_read

    def read_exact(self) -> float:
        self._update_value()
        return self.raw_value

    def write(self, value) -> bool:
        raise NotImplementedError('Oscillator is a read-only device')

    def update(self):
        pass

    def _update_value(self):
        now = time.time()
        self.raw_value = self.amplitude * np.sin(2 * np.pi * (now - self.time_start)/self.period)
        self.time_last_update = now


class RealisticMagnet(VirtualDevice):
    def __init__(self, name: str, value=0.0, low=None, high=None, noise=None, resolution=None,
                 measurement_period=None,
                 model='instant', model_kwargs=None) -> None:
        if high is not None and low is not None:
            assert high > low
        assert noise is None or noise >= 0.0
        assert resolution is None or resolution > 0.0
        super().__init__(name)
        self.raw_value = self.value = value
        self.setpoint = value
        self.time_last_update = time.time()
        self.time_setpoint = time.time()
        self.noise = noise
        self.resolution = resolution
        self.low = low
        self.high = high
        self.model = model
        self.measurement_period = measurement_period
        self.model_kwargs = model_kwargs or {'decay_constant': 2}

    def read(self) -> float:
        self._update_value()
        raw_read = self.raw_value
        if self.noise is not None and self.noise != 0.0:
            noise = np.random.normal(0, self.noise, 1)
            raw_read += noise
        if self.resolution is not None and self.resolution != 0.0:
            raw_read = int(raw_read / self.resolution) * self.resolution
        self.value = raw_read
        return raw_read

    def read_exact(self) -> float:
        self._update_value()
        return self.raw_value

    def read_setpoint(self) -> float:
        return self.setpoint

    def write(self, value) -> bool:
        if self.low and value < self.low:
            raise ValueError(f'Value {value} below permitted bounds ({self.low}|{self.high})')
            # return False
        if self.high and value > self.high:
            raise ValueError(f'Value {value} above permitted bounds ({self.low}|{self.high})')
            # return False
        self.setpoint = value
        self.time_setpoint = time.time()
        return True

    def update(self):
        pass

    def _update_value(self):
        now = time.time()
        if self.model == 'exponential':
            # For exp, N(t) = N0 exp(-lambda*T)
            decay_constant = self.model_kwargs['decay_constant']
            delta = now - self.time_last_update
            output_delta = self.value - self.setpoint
            new_value = self.setpoint - output_delta * np.exp(-decay_constant * delta)
            self.raw_value = new_value
            self.time_last_update = now
        elif self.model == 'instant':
            self.raw_value = self.setpoint
            self.time_last_update = now
        else:
            raise Exception

# class CurrentMonitor(VirtualDevice):
