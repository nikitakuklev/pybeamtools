class SimulationError(Exception):
    pass


class DeviceError(SimulationError):
    pass


class DeviceWriteError(DeviceError):
    pass


class DeviceReadError(DeviceError):
    pass


class MissingDependencyError(SimulationError):
    pass
