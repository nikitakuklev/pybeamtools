import logging
import uuid
from enum import Enum
from typing import Any, Callable, Literal, Optional, Union

from pydantic import BaseModel

from .errors import DeviceError, DeviceWriteError
from .rpn import RPNCalc
from ..controls.pv import PVOptions
from ..utils.pydantic import SignatureModel

__all__ = ['TRIGSPEC', 'SignalContext', 'EchoDevice', 'EchoDeviceOptions', 'GenericDevice',
           'GenericDeviceOptions', 'ProxyDevice', 'ProxyDeviceOptions', 'EPICSDevice',
           'EPICSDeviceOptions']

logger = logging.getLogger(__name__)


class TRIGSPEC(Enum):
    PROPAGATE = 1
    IGNORE = 2


class DeviceOptions(BaseModel):
    name: str
    # update_fun: Callable
    # read_fun: Callable
    # write_fun: Callable
    # channel_map: dict


class SignalContext:
    def __init__(self, se):
        from .core import SimulationEngine
        self.se: SimulationEngine = se
        self.add_device = self.se.add_device

    def issue_update(self, channel_name: str):
        self.se.notify_update_available(channel_name)


class EngineDevice:
    DEVICE_TYPE = 'Generic'

    def __init__(self,
                 ctx,
                 options,
                 update_fun: Callable = None,
                 read_fun: Callable = None,
                 write_fun: Callable = None,
                 channel_map: dict = None
                 ):
        # self.device = device
        self.ctx = ctx
        self.options = options
        assert isinstance(channel_map, dict)
        for output, deps_dict in channel_map.items():
            assert isinstance(output, str)
            assert isinstance(deps_dict, dict), f'{deps_dict}'
            for dep, spec in deps_dict.items():
                assert isinstance(dep, str)
                assert isinstance(spec, TRIGSPEC)
        self.channel_map = channel_map or {}
        self.name: str = options.name or uuid.uuid4()[:12]
        self.update_fun = update_fun
        self.read_fun = read_fun
        self.write_fun = write_fun
        if not hasattr(self, 'params'):
            self.params = {}

    def update(self, t_sched: Optional[float], t_run: float, data: dict[str, Any]):
        if self.update_fun is not None:
            return self.update_fun(t_sched, t_run, data)
        else:
            raise Exception(f'No update function defined')

    def read(self, t_sched: Optional[float], t_run: float, channel_name: str):
        if channel_name not in self.channel_map:
            raise Exception(f'Unknown channel {channel_name}')
        if self.read_fun is not None:
            value = self.read_fun(t_sched, t_run, channel_name)
        else:
            raise Exception(f'No read function defined for {channel_name=}')
        return value

    def write(self, t_sched: Optional[float], t_run: float, value_dict: dict[str, Any]):
        for k, v in value_dict.items():
            if k not in self.channel_map:
                raise DeviceWriteError(f'Unknown channel ({k})')

        if self.write_fun is not None:
            return self.write_fun(t_sched, t_run, value_dict)
        else:
            raise DeviceWriteError(f'Device ({self.name}) does not support writes')


class EchoDeviceOptions(DeviceOptions):
    device_type: Literal['echo'] = 'echo'
    data: dict[str, Any]


class EchoDevice(EngineDevice):
    DEVICE_TYPE = 'Echo'

    def __init__(self, ctx: SignalContext, options: EchoDeviceOptions):
        self.options = options
        channel_map = {k: {} for k in options.data.keys()}
        super().__init__(ctx,
                         options=options,
                         update_fun=self._update_fun,
                         read_fun=self._read_fun,
                         write_fun=self._write_fun,
                         channel_map=channel_map)

    def _update_fun(self, t_sched, t_run, data):
        return self.options.data.copy()

    def _read_fun(self, t_sched, t_run, channel_name):
        return self.options.data[channel_name]

    def _write_fun(self, t_sched, t_run, value_dict):
        for k, v in value_dict.items():
            if k not in self.options.data:
                raise DeviceWriteError()
            else:
                self.options.data[k] = v


class ProxyDeviceOptions(DeviceOptions):
    device_type: Literal['proxy'] = 'proxy'
    channel_map: dict[str, dict[str, TRIGSPEC]]


class ProxyDevice(EngineDevice):
    DEVICE_TYPE = 'Proxy'

    def __init__(self, ctx, options: ProxyDeviceOptions):
        self._channel_map = options.channel_map
        self.data = {}
        channel_map = {k: v for k, v in self._channel_map.items()}
        super().__init__(ctx,
                         options=options,
                         update_fun=self._update_fun,
                         read_fun=self._read_fun,
                         write_fun=self._write_fun,
                         channel_map=channel_map)
        if ctx is not None:
            ctx.add_device(self)

    def _update_fun(self, t_sched, t_run, data):
        for ch_out, dep_dict in self._channel_map.items():
            dep_keys = list(dep_dict.keys())
            self.data[ch_out] = data[dep_keys[0]]
        return self.data.copy()

    def _read_fun(self, t_sched, t_run, channel_name):
        return self.data[channel_name]

    def _write_fun(self, t_sched, t_run, value_dict):
        pass


class EPICSDeviceOptions(DeviceOptions):
    pv_config: PVOptions

    @property
    def pv_name(self):
        return self.pv_config.name


class EPICSDevice(EngineDevice):
    def __init__(self, ctx, options: EPICSDeviceOptions, acc_context):
        from ..controls import Accelerator
        from ..controls.pv import EPICSPV, PVAccess, PVOptions

        self.acc_context: Accelerator = acc_context
        self.data = {}
        self.response_data = {}
        self.pv = EPICSPV(options=options.pv_config)
        self._channel_map = {options.name: {}}

        self.acc_context.add_pv_object([self.pv])

        def callback(sub, response):
            pv_name = sub.pv.name
            assert pv_name == self.options.pv_name
            self.data[options.name] = response.data[0]
            self.response_data[options.name] = response
            ctx.issue_update(options.name)

        self.acc_context.cm.subscribe_custom(self.pv, callback)

        super().__init__(ctx,
                         options=options,
                         update_fun=self._update_fun,
                         read_fun=self._read_fun,
                         write_fun=self._write_fun,
                         channel_map=self._channel_map.copy())

        if ctx is not None:
            ctx.add_device(self)

        logger.debug(f'EPICS device created: {self._channel_map}')

    def _update_fun(self, t_sched, t_run, data):
        return self.data.copy()

    def _read_fun(self, t_sched, t_run, channel_name):
        return self.data[channel_name]

    def _write_fun(self, t_sched, t_run, value_dict):
        name = self.options.name
        assert name in value_dict
        self.pv.write(value_dict[name])


class RPNDeviceOptions(DeviceOptions):
    rpn_expression: str


class RPNEngineDevice(EngineDevice):
    DEVICE_TYPE = 'RPN'

    def __init__(self, ctx, options: RPNDeviceOptions):
        self.output_name = options.name
        rpn_expression = options.rpn_expression
        self.data = {}

        rpn = RPNCalc()
        missing_tokens = rpn.validate_expression(rpn_expression)
        # if not set(missing_tokens).issubset(set(channels)):
        #    raise ValueError(f'Unknown tokens ({missing_tokens=} vs {channels=})')
        channel_map = {self.output_name: {k: TRIGSPEC.PROPAGATE for k in missing_tokens}}
        self.missing_tokens = missing_tokens
        self._channel_map: dict[str, dict[str, TRIGSPEC]] = channel_map
        self.params = {'rpn_expression': rpn_expression,
                       'required_token': self.missing_tokens
                       }

        super().__init__(ctx,
                         options=options,
                         update_fun=self._update_fun,
                         read_fun=self._read_fun,
                         write_fun=self._write_fun,
                         channel_map=channel_map)

    def _update_fun(self, t_sched, t_run, data):
        for k in self.missing_tokens:
            assert k in data, f'RPN ({self.options.rpn_expression}) requires channel ({k})'
        rpn = RPNCalc()
        extra_variables = {k: data[k] for k in self.missing_tokens}
        rpn.add_variables(extra_variables)
        rpn.push(self.options.rpn_expression)
        assert (len(rpn.stack) == 1), f'RPN length incorrect'
        self.value = rpn.stack[0]
        return {self.output_name: self.value}

    def _read_fun(self, t_sched, t_run, channel_name):
        assert channel_name == self.output_name
        return self.value

    def _write_fun(self, t_sched, t_run, value_dict):
        raise DeviceError(f'RPN does not support writes')


class GenericDeviceOptions(DeviceOptions):
    update_fun: Callable
    read_fun: Callable
    write_fun: Optional[Callable] = None
    startup_fun: Optional[Callable] = None
    channel_map: dict[str, Union[str, dict]]


class GenericDevice(EngineDevice):
    DEVICE_TYPE = 'generic'

    def __init__(self,
                 ctx: Optional[SignalContext],
                 options: GenericDeviceOptions
                 ):
        self.ctx = ctx
        wf = self._write_fun if options.write_fun is not None else None
        super().__init__(ctx,
                         options=options,
                         update_fun=self._update_fun,
                         read_fun=self._read_fun,
                         write_fun=wf,
                         channel_map=options.channel_map)
        if ctx is not None:
            ctx.add_device(self)
        if self.options.startup_fun is not None:
            self.options.startup_fun(self)

    def _update_fun(self, t_sched, t_run, data):
        return self.options.update_fun(t_sched, t_run, data, self)

    def _read_fun(self, t_sched, t_run, channel_name):
        assert channel_name in self.options.channel_map
        return self.options.read_fun(t_sched, t_run, channel_name, self)

    def _write_fun(self, t_sched, t_run, value_dict):
        for k in value_dict.keys():
            assert k in self.options.channel_map
        self.options.write_fun(t_sched, t_run, value_dict, self)


class ScriptDeviceOptions(DeviceOptions):
    script_read: Callable
    script_write: Callable
    signature_read: SignatureModel
    signature_write: SignatureModel
    channel_map: dict[str, Union[str, dict]]


class ScriptDevice(EngineDevice):
    DEVICE_TYPE = 'Script wrapper'

    def __init__(self,
                 ctx,
                 options: ScriptDeviceOptions
                 ):
        channel_map = {options.name: {}}
        self.last_results = {}
        super().__init__(ctx,
                         options=options,
                         update_fun=self._update_fun,
                         read_fun=self._read_fun,
                         write_fun=self._write_fun,
                         channel_map=channel_map)

    def _update_fun(self, t_sched, t_run, data):
        results = self.options.script_read(data)
        for k, v in self.options.channel_map:
            self.last_results[k] = results[k]
        return self.last_results.copy()

    def _read_fun(self, t_sched, t_run, channel_name):
        assert channel_name in self.options.channel_map
        return self.last_results[channel_name]

    def _write_fun(self, t_sched, t_run, value_dict):
        for k in value_dict.keys():
            assert k in self.options.channel_map
        self.options.script_write(value_dict)


ALL_DEVICE_CLASS_TYPE = Union[EchoDevice, ProxyDevice]

ALL_DEVICE_OPTIONS_CLASS_TYPE = Union[EchoDeviceOptions, ProxyDeviceOptions]

DEVICE_CLASS_MAP = {'echo': EchoDeviceOptions,
                    'proxy': ProxyDeviceOptions
                    }
