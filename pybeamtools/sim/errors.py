class SimulationError(Exception):
    pass


class ReadError(SimulationError):
    pass


class ReadTimeoutError(SimulationError):
    pass


class WriteError(SimulationError):
    pass


class WriteReadbackError(SimulationError):
    pass


class WriteTimeoutError(SimulationError):
    pass


class DeviceError(SimulationError):
    pass


class DeviceUpdateError(DeviceError):
    pass


class DeviceWriteError(DeviceError):
    pass


class DeviceWriteTimeout(DeviceError):
    pass


class DeviceEventTimeout(DeviceError):
    pass


class DeviceReadError(DeviceError):
    pass


class DeviceScanError(DeviceError):
    pass

class DeviceEnableError(DeviceError):
    pass

class DeviceDisabledError(DeviceError):
    pass


class DeviceDependencyError(DeviceError):
    pass


class MissingDependencyError(SimulationError):
    pass
