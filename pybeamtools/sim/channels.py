from typing import Callable, Union, Any

from .devices import VirtualDevice
from .errors import SimulationError
from .rpn import RPNCalc


class ChannelMap:
    def __init__(self,
                 devices: list[VirtualDevice],
                 channels: list[str],
                 read_fun: Callable,
                 write_fun: Callable = None
                 ):
        self.map_type = 'custom'
        self.devices = devices
        self.channels = channels
        self.read_fun = read_fun
        self.write_fun = write_fun

    def process_read(self) -> dict[str, Union[str, int, float]]:
        # assert channel_name in self.channels
        read_dict = self.read_fun(self, self.devices, self.channels)
        assert set(read_dict.keys()) == set(self.channels), \
            f'{read_dict=} {self.channels=}'
        return read_dict  # [channel_name]

    def process_write(self, value_dict: dict[str, Any]):
        if self.write_fun is None:
            raise SimulationError(
                f'Channel map ({self.channels}) -> ({self.devices}) does not support writes')
        return self.write_fun(self, self.devices, self.channels, value_dict)


class RPNMap(ChannelMap):
    def __init__(self,
                 devices: list[VirtualDevice],
                 channels: list[str],
                 rpn_expression: str
                 ):
        assert len(channels) == 1
        rpn = RPNCalc()
        missing_tokens = rpn.validate_expression(rpn_expression)
        device_names = [d.name for d in devices]
        if not set(missing_tokens).issubset(set(device_names)):
            raise ValueError(f'Unknown tokens ({missing_tokens=} vs {device_names=})')
        super().__init__(devices, channels, read_fun=self.eval_rpn)
        self.map_type = 'rpn'
        self.rpn_expression = rpn_expression

    def eval_rpn(self):
        rpn = RPNCalc()
        device_values = {d: d.read(t=None) for d in self.devices}
        rpn.add_variables(device_values)
        rpn.push(self.rpn_expression)
