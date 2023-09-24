import logging
import time
import traceback
import uuid
from enum import Enum, auto
from functools import total_ordering
from typing import Any, Callable, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Extra, Field

from .devices import TimeAwareModel, VirtualDevice
from .errors import DeviceReadError, DeviceScanError, \
    DeviceUpdateError, DeviceWriteError
from .rpn import RPNCalc
from ..controls.pv import PVOptions, WriteResponse
from ..utils.pydantic import JSON_ENCODERS

__all__ = ['TRIG', 'SignalContext', 'EchoDevice', 'EchoDeviceOptions', 'GenericDevice',
           'GenericDeviceOptions', 'ProxyDevice', 'ProxyDeviceOptions', 'EPICSDevice',
           'EPICSDeviceOptions']

logger = logging.getLogger(__name__)


class TRIG(Enum):
    PROPAGATE = 1
    IGNORE = 2


DataT = Union[float, str, int, None]


class DS(Enum):
    CREATED = 0
    ENABLED = 1
    PAUSED = 2
    ENABLED_AND_SCANNING = 3
    ERROR_DEPENDENCIES = 4
    ERROR_UPDATE = 5
    STARTING_UP = 6
    ERROR_NOT_STARTED = 7
    ERROR_INTERNAL = 8
    ERROR_ENABLE = 9
    ERROR_WRITE = 10
    ERROR_READ = 11


class OP(Enum):
    UPDATE = auto()
    READ = auto()
    READ_NOW = auto()
    WRITE = auto()
    SCAN = auto()
    ENABLE = auto()
    PAUSE = auto()
    UPDATE_PROP = auto()
    UPDATE_PUSH = auto()


@total_ordering
class Event:
    def __init__(self,
                 op: OP,
                 dn: str,
                 txid: int,
                 t_event: float,
                 data: dict[str, DataT] = None,
                 root: Optional[int] = None,
                 source: Optional[int] = None,
                 cb: Callable = None
                 ):
        self.op: OP = op
        self.dn: str = dn
        self.txid: int = txid
        self.t_event: float = t_event
        self.t_process: float = None
        self.data: dict[str, DataT] = data
        self.root: Optional[int] = root if root is not None else txid
        self.source: Optional[int] = source if source is not None else txid
        self._cb: Callable = cb  # if cb is not None else lambda *args: None

    def __eq__(self, other):
        return self.txid == other.txid

    def __lt__(self, other):
        return self.root < other.root

    def cb(self, *args, **kwargs):
        if self._cb is not None:
            self._cb(*args, **kwargs)

    def set_cb(self, cb):
        assert self._cb is None
        self._cb = cb

    @property
    def uuid(self):
        return f'E{self.txid}:{self.source}:{self.root}'


class Result:
    def __init__(self, t: float, data: Any, success: bool, **kwargs):
        self.t = t
        self.data = data
        self.success = success
        self.metadata = {}
        self.metadata.update(**kwargs)

    def __repr__(self):
        return f'Result ({self.data}) at ({self.t}) ({self.metadata=})'


class SignalContext:
    def __init__(self, se):
        from .core import SimulationEngine
        self.se: SimulationEngine = se
        self.add_device = self.se.add_device

    def issue_update(self, device: "EngineDevice", data: dict[str, DataT]):
        assert isinstance(data, dict)
        self.se.push_update(device, data)

    def time(self):
        return self.se.time()


class DeviceOptions(BaseModel):
    name: str = Field(description='Device name')
    scan_period: float = Field(0.0, description='refresh_period')
    editable_fields: list[str] = Field([])
    model_config = ConfigDict(extra='forbid')


class EngineDevice:
    device_type: str = 'device'

    def __init__(self,
                 options: DeviceOptions,
                 ctx: SignalContext = None,
                 update_fun: Callable = None,
                 read_fun: Callable = None,
                 read_now_fun: Callable = None,
                 write_fun: Callable = None,
                 scan_fun: Callable = None,
                 enable_fun: Callable = None,
                 disable_fun: Callable = None,
                 channel_map: dict = None
                 ):
        self.ctx = ctx
        self.options = options
        self.deps = set()
        self.aux_data = {}

        assert isinstance(channel_map, dict)
        for output, deps_dict in channel_map.items():
            assert isinstance(output, str)
            assert isinstance(deps_dict, dict), f'{deps_dict}'
            for dep, spec in deps_dict.items():
                assert isinstance(dep, str)
                assert isinstance(spec, TRIG), f'Spec {spec} bad'
                self.deps.add(dep)
        assert self.device_type != 'device'
        self.channel_map = channel_map or {}
        self.channels = set(self.channel_map.keys())
        self.name: str = options.name or uuid.uuid4()[:12]
        if len(self.deps) > 0:
            # We need to handle incoming update
            assert update_fun is not None
        self.update_fun = update_fun
        self.read_fun = read_fun
        self.read_now_fun = read_now_fun
        self.write_fun = write_fun
        self.scan_fun = scan_fun
        self.enable_fun = enable_fun
        self.disable_fun = disable_fun
        self.stats = {'update': 0, 'read': 0, 'read_now': 0, 'write': 0,
                      'scan': 0, 'enable': 0, 'disable': 0
                      }

        self.state = DS.CREATED
        # if ctx is not None:
        #    ctx.add_device(self)

    def __str__(self):
        return f'{self.device_type} with {self.options=}'

    def update(self, ev: Event, aux_dict: dict[str, DataT]) -> dict[str, DataT]:
        self.stats['update'] += 1
        if aux_dict is not None:
            set_provided = set(aux_dict.keys())
            assert set_provided.issubset(self.deps), f'Bad aux data keys {set_provided}'
        self.aux_data.update(aux_dict)
        if self.update_fun is not None:
            result = self.update_fun(ev, aux_dict)
            if result is not None:
                assert isinstance(result, dict)
                assert set(result.keys()).issubset(self.channels)
                return result
        else:
            raise DeviceUpdateError(f'Device {self.name} has no update function')

    def read(self, ev: Event, channel_name: str) -> dict[str, DataT]:
        """ Request last available read from device """
        self.stats['read'] += 1
        if channel_name not in self.channel_map:
            raise Exception(f'Unknown channel {channel_name}')
        if self.read_fun is not None:
            return self.read_fun(ev, channel_name)
        else:
            raise Exception(f'No read function defined for C({channel_name})')

    def read_now(self, ev: Event, channel_name: str) -> DataT:
        """ Request a fresh read from device """
        self.stats['read_now'] += 1
        if channel_name not in self.channel_map:
            raise Exception(f'Unknown channel {channel_name}')
        if self.read_now_fun is not None:
            return self.read_now_fun(ev, channel_name)
        else:
            raise Exception(f'No read_now function defined for C({channel_name})')

    def write(self, ev: Event, value_dict: dict[str, DataT],
              aux_dict: dict[str, DataT]
              ) -> dict[str, DataT]:
        """ Return updated values of channels """
        self.stats['write'] += 1
        if aux_dict is not None:
            set_provided = set(aux_dict.keys())
            assert set_provided.issubset(self.deps), f'Bad aux data keys {set_provided}'
        self.aux_data.update(aux_dict)
        for k, v in value_dict.items():
            if k not in self.channel_map:
                raise DeviceWriteError(f'Unknown channel ({k})')

        if self.write_fun is not None:
            result = self.write_fun(ev, value_dict, aux_dict)
            return result
        else:
            raise DeviceWriteError(f'Device ({self.name}) does not support writes')

    def scan(self, ev: Event) -> dict[str, DataT]:
        self.stats['scan'] += 1
        if self.scan_fun is not None:
            result = self.scan_fun(ev)
            assert isinstance(result, dict)
            return result
        else:
            raise DeviceScanError(f'Device ({self.name}) does not support scans')

    def enable(self, ev: Event) -> dict[str, DataT]:
        """ Enable device, allowing all other operations """
        self.stats['enable'] += 1
        if self.enable_fun is not None:
            result = self.enable_fun(ev)
            if result is not None:
                assert isinstance(result, dict)
                assert set(result.keys()).issubset(self.channels)
                return result
        else:
            # logger.warning(f'Device {self.name} has no enable, skipping')
            pass

    def disable(self, ev: Event):
        """ Disable device """
        self.stats['disable'] += 1
        if self.disable_fun is not None:
            result = self.disable_fun(ev)
            if result is not None:
                assert isinstance(result, dict)
                assert set(result.keys()).issubset(self.channels)
                return result
        else:
            logger.warning(f'Device {self.name} has no disable, skipping')

    def issue_full_update(self):
        t_run = self.ctx.time()
        data = {k: self.read(t_run, k) for k in self.channel_map}
        if self.ctx.se.TRACE:
            logger.debug(f'{self.name} full update:  {data}')
        self.ctx.issue_update(self, data)

    def is_ready_to_write(self):
        return True


class EchoDeviceOptions(DeviceOptions):
    device_type: Literal['echo'] = 'echo'
    data: dict[str, Any]


class EchoDevice(EngineDevice):
    device_type: str = 'echo'

    def __init__(self, options: EchoDeviceOptions, ctx: SignalContext = None):
        self.options = options
        channel_map = {k: {} for k in options.data.keys()}
        super().__init__(options,
                         ctx,
                         update_fun=self._update_fun,
                         read_fun=self._read_fun,
                         read_now_fun=self._read_now_fun,
                         write_fun=self._write_fun,
                         scan_fun=self._scan_fun,
                         channel_map=channel_map)

    def _update_fun(self, event, aux_dict):
        return self.options.data

    def _read_fun(self, ev, channel_name):
        return self.options.data[channel_name]

    def _read_now_fun(self, ev, channel_name):
        return self._read_fun(ev, channel_name)

    def _write_fun(self, ev, value_dict, aux_dict):
        assert len(aux_dict) == 0
        changed_dict = {}
        for k, v in value_dict.items():
            if k not in self.options.data:
                raise DeviceWriteError(f'Channel ({k}) unknown')
            else:
                self.options.data[k] = v
                changed_dict[k] = v
        return changed_dict

    def _scan_fun(self, ev):
        # assert self.options.scan_period > 0.0
        return self.options.data

    # def _edit_fun(self, t_run, options_dict):
    #     for k, v in options_dict.items():
    #         if k not in self.options.editable_fields:
    #             raise DeviceError(f'Field {k} not editable')
    #     current_opt_dict = self.options.dict()
    #     new_opt_dict = current_opt_dict.update(options_dict)
    #     new_opt = self.options.parse_obj(new_opt_dict)
    #
    #     # validation passed, so modify current one now
    #     for k, v in options_dict.items():
    #         setattr(self.options, k, v)


class CounterDeviceOptions(DeviceOptions):
    device_type: Literal['counter'] = 'counter'
    data: dict[str, Any]
    increment_on: list[str] = ['scan']


class CounterDevice(EngineDevice):
    device_type: str = 'counter'
    options: CounterDeviceOptions

    def __init__(self, options: CounterDeviceOptions, ctx: SignalContext = None):
        self.options = options
        channel_map = {k: {} for k in options.data.keys()}
        super().__init__(options,
                         ctx,
                         update_fun=self._update_fun,
                         read_fun=self._read_fun,
                         write_fun=self._write_fun,
                         scan_fun=self._scan_fun,
                         channel_map=channel_map)

    def _update_fun(self, event, aux_dict):
        data = self.options.data.copy()
        if 'update' in self.options.increment_on:
            for k in self.options.data:
                self.options.data[k] += 1
        return data

    def _read_fun(self, ev, channel_name):
        return self.options.data[channel_name]

    def _write_fun(self, ev, value_dict, aux_dict):
        assert len(aux_dict) == 0
        changed_dict = {}
        for k, v in value_dict.items():
            if k not in self.options.data:
                raise DeviceWriteError(f'Channel ({k}) unknown')
            else:
                self.options.data[k] = v
                changed_dict[k] = v
        return changed_dict

    def _scan_fun(self, ev):
        assert self.options.scan_period > 0.0
        data = self.options.data.copy()
        if 'scan' in self.options.increment_on:
            for k in self.options.data:
                self.options.data[k] += 1
        return data


class ProxyDeviceOptions(DeviceOptions):
    device_type: Literal['proxy'] = 'proxy'
    channel_map: dict[str, dict[str, TRIG]]


class ProxyDevice(EngineDevice):
    device_type: str = 'Proxy'
    options: ProxyDeviceOptions

    def __init__(self, options: ProxyDeviceOptions, ctx: SignalContext = None):
        self._channel_map = options.channel_map
        self.all_deps = set()
        for k, v in self._channel_map.items():
            self.all_deps.update(set(v.keys()))
        self.data = {}
        super().__init__(options,
                         ctx,
                         update_fun=self._update_fun,
                         read_fun=self._read_fun,
                         # write_fun=self._write_fun,
                         channel_map=options.channel_map)

    def _update_fun(self, event, aux_dict):
        for cn, cval in aux_dict.items():
            assert cn in self.all_deps
        # Get new data
        changed_data = {}
        for ch_out, dep_dict in self._channel_map.items():
            dep_key = list(dep_dict.keys())[0]
            if dep_dict[dep_key] == TRIG.IGNORE:
                pass
            else:
                assert dep_dict[dep_key] == TRIG.PROPAGATE
                self.data[ch_out] = changed_data[ch_out] = aux_dict[dep_key]
        return changed_data

    def _read_fun(self, event, channel_name):
        return self.data[channel_name]

    # def _write_fun(self, t_run, value_dict, aux_dict):
    #     raise DeviceWriteError(f'Writes are not allowed')


class EPICSDeviceOptions(DeviceOptions):
    device_type: Literal['epics_ca'] = 'epics_ca'
    connection: Literal['dummy', 'epics'] = 'epics'
    pv_to_ch_map: dict[str, str]
    pv_config: PVOptions
    wait: bool = False

    @property
    def pv_name(self):
        return self.pv_config.name


class EPICSDevice(EngineDevice):
    device_type: str = 'epics_ca'
    options: EPICSDeviceOptions

    def __init__(self, options: EPICSDeviceOptions,
                 ctx: Optional[SignalContext],
                 acc_context
                 ):
        from ..controls import Accelerator
        self.acc: Accelerator = acc_context
        self.response_data = {}
        # self.pv = None
        if options.connection == 'epics':
            from ..controls.pv import EPICSPV
            logger.debug(f'Creating EPICSPV with {options.pv_config}')
            self.pv = EPICSPV(options=options.pv_config)
        else:
            from ..controls.pv import SimPV
            logger.debug(f'Creating SimPV with {options.pv_config}')
            self.pv = SimPV(options=options.pv_config)
        self._channel_map = {n: {} for n in options.pv_to_ch_map.values()}
        self.data = {options.pv_to_ch_map[options.pv_name]: None}
        self.success = False
        # self.acc_context.add_pv_object([self.pv])

        super().__init__(options,
                         ctx,
                         update_fun=self._update_fun,
                         read_fun=self._read_fun,
                         read_now_fun=self._read_now_fun,
                         write_fun=self._write_fun,
                         enable_fun=self._enable_fun,
                         channel_map=self._channel_map.copy())

        # logger.debug(f'EPICS device created: {self._channel_map}')

    def is_connected(self):
        return self.acc.cm.is_connected(self.pv.name)

    def is_ready_to_write(self):
        return self.is_connected()

    def _get_caproto_pv(self):
        return self.acc.cm.pv_caproto_map[self.pv.name]

    def _update_fun(self, ev, aux_dict):
        return self.data.copy()

    def _read_fun(self, ev, channel_name):
        ready = self.is_connected()
        if not ready:
            raise DeviceReadError(
                    f'PV {self.options.pv_name} not connected')  # -> {self._get_caproto_pv()}
        return self.data[channel_name]

    def _read_now_fun(self, ev, channel_name):
        ready = self.is_connected()
        if not ready:
            raise DeviceReadError(f'PV {self.options.pv_name} not connected')
        response = self.pv.read()
        pv_name = self.options.pv_name
        cn = self.options.pv_to_ch_map[pv_name]
        assert cn == channel_name
        try:
            r = self.extract_data(response)
            self.data[cn] = r
            self.response_data[cn] = response
            self.success = self.extract_status(response)
            # logger.debug(f'EPICS read now: ({cn})=({response})')
            return r
        except Exception as ex:
            logger.warning(f'EPICS read now ({cn})=({response}) failed, {ex}')
            logger.warning(f'{traceback.format_exc()}')
            raise ex

    def _write_fun(self, ev, value_dict, aux_dict):
        def status(response):
            if self.options.connection == 'epics':
                return response.status.success == 1
            else:
                assert isinstance(response, WriteResponse)
                return True

        pv_name = self.options.pv_name
        ch_name = self.options.pv_to_ch_map[pv_name]
        value = value_dict[ch_name]
        assert len(value_dict) == 1
        assert next(iter(value_dict)) == ch_name
        assert all(k in self.options.pv_to_ch_map.values() for k in value_dict)

        # ready = self.acc.cm.pv_caproto_map[self.pv.name].channel_ready.is_set()
        # if not ready:
        #    raise Exception(
        #            f'PV {self.pv.name} not ready -> {self.acc.cm.pv_caproto_map[self.pv.name]}')
        assert self.is_connected()
        t1 = time.perf_counter()
        if self.options.wait:
            result = self.pv.write(value, wait=True)
        else:
            result = self.pv.write(value, wait=False)
        t2 = time.perf_counter()
        logger.debug(
            f'PV ({self.pv.name})=({value}) write in ({t2 - t1:.3f}) ({self.options.wait=})')
        if self.options.wait:
            if not status(result):
                raise Exception(f'PV write failed - {result=}')
            return {ch_name: value}
        else:
            return {}

    def extract_name(self, sub):
        if self.options.connection == 'epics':
            return sub.pv.name
        else:
            return sub.name

    def extract_data(self, response):
        if self.options.connection == 'epics':
            return response.data[0]
        else:
            return response

    def extract_status(self, response):
        if self.options.connection == 'epics':
            return response.status.success == 1
        else:
            return True

    def callback(self, sub, response):
        # logger.debug(f'EPICS callback ({sub=}) ({response=})')
        try:
            pv_name = self.extract_name(sub)
            assert pv_name == self.options.pv_name
            cn = self.options.pv_to_ch_map[pv_name]
            r = self.extract_data(response)
            # logger.debug(f'EPICS callback ({cn})=({r})')
            self.data[cn] = r
            self.response_data[cn] = response
            self.success = self.extract_status(response)
            if self.ctx is not None:
                # logger.debug(f'EPICS callback ({cn})=({r}) ISSUE')
                self.ctx.issue_update(self, {cn: r})
            # logger.debug(f'EPICS callback ({cn})=({r}) END')
        except Exception as ex:
            logger.error(f'EPICS callback ({sub=}) ({response=}) failed, {ex}')
            logger.error(f'{traceback.format_exc()}')

    def _enable_fun(self, ev):
        # from ..controls.pv import EPICSPV, SimPV
        # if self.pv is None:
        #     if self.options.connection == 'epics':
        #         logger.debug(f'Creating EPICSPV with {self.options.pv_config}')
        #         self.pv = EPICSPV(options=self.options.pv_config)
        #     else:
        #         logger.debug(f'Creating SimPV with {self.options.pv_config}')
        #         self.pv = SimPV(options=self.options.pv_config)
        self.acc.add_pv_object([self.pv])
        self.acc.cm.subscribe_custom(self.pv, self.callback)
        # logger.debug(f'EPICS device ({self.pv.name}) enabled')


class RPNDeviceOptions(DeviceOptions):
    device_type: Literal['rpn'] = 'rpn'
    rpn_expression: str


class RPNEngineDevice(EngineDevice):
    device_type: str = 'RPN'
    options: RPNDeviceOptions

    def __init__(self, options: RPNDeviceOptions, ctx: Optional[SignalContext]):
        rpn_expression = options.rpn_expression
        self.data = {}

        rpn = RPNCalc()
        missing_tokens = rpn.validate_expression(rpn_expression)
        # if not set(missing_tokens).issubset(set(channels)):
        #    raise ValueError(f'Unknown tokens ({missing_tokens=} vs {channels=})')
        channel_map = {options.name: {k: TRIG.PROPAGATE for k in missing_tokens}}
        self.missing_tokens = missing_tokens
        self._channel_map: dict[str, dict[str, TRIG]] = channel_map

        super().__init__(options,
                         ctx,
                         update_fun=self._update_fun,
                         read_fun=self._read_fun,
                         channel_map=channel_map)

    def _update_fun(self, event, aux_dict):
        rpn_exp = self.options.rpn_expression
        for k in self.missing_tokens:
            if k not in aux_dict:
                raise DeviceUpdateError(f'RPN ({rpn_exp}) requires ({k})')
            assert aux_dict[k] is not None
        rpn = RPNCalc()
        extra_variables = {k: aux_dict[k] for k in self.missing_tokens}
        rpn.add_variables(extra_variables)
        rpn.push(rpn_exp)
        assert (len(rpn.stack) == 1), f'RPN length incorrect'
        self.value = rpn.stack[0]
        return {self.options.name: self.value}

    def _read_fun(self, event, channel_name):
        assert channel_name == self.options.name
        return self.value


class GenericDeviceOptions(DeviceOptions):
    device_type: Literal['generic'] = 'generic'
    update_fun: Callable
    read_fun: Callable
    scan_fun: Optional[Callable] = None
    write_fun: Optional[Callable] = None
    startup_fun: Optional[Callable] = None
    channel_map: dict[str, Union[str, dict]]


class GenericDevice(EngineDevice):
    device_type: str = 'generic'
    options: GenericDeviceOptions

    def __init__(self, options: GenericDeviceOptions,
                 ctx: SignalContext = None
                 ):
        self.ctx = ctx
        wf = self._write_fun if options.write_fun is not None else None
        sf = self._scan_fun if options.scan_fun is not None else None
        super().__init__(options,
                         ctx,
                         update_fun=self._update_fun,
                         read_fun=self._read_fun,
                         write_fun=wf,
                         scan_fun=sf,
                         channel_map=options.channel_map)
        if options.startup_fun is not None:
            options.startup_fun(self)

    def _update_fun(self, ev, aux_dict):
        return self.options.update_fun(ev, aux_dict, self)

    def _read_fun(self, ev, channel_name):
        return self.options.read_fun(ev, channel_name, self)

    def _write_fun(self, ev, value_dict, aux_dict):
        return self.options.write_fun(ev, value_dict, aux_dict, self)
        # self.issue_full_update()
        # new_data = {k: self._read_fun(t_run, k) for k in self.options.channel_map}
        # self.ctx.issue_update(self, new_data)

    def _scan_fun(self, ev):
        return self.options.scan_fun(ev, self)


class ModelDeviceOptions(DeviceOptions):
    device_type: Literal['model_wrapper'] = 'model_wrapper'
    device: VirtualDevice

    class Config:
        arbitrary_types_allowed = True


class ModelDevice(EngineDevice):
    device_type: str = 'Model wrapper'
    options: ModelDeviceOptions

    def __init__(self,
                 options: ModelDeviceOptions, ctx: SignalContext = None
                 ):
        self.data = {}
        channel_map = {options.name: {}}
        super().__init__(options,
                         ctx,
                         update_fun=self._update_fun,
                         read_fun=self._read_fun,
                         write_fun=self._write_fun,
                         channel_map=channel_map)

    def _update_fun(self, ev, aux_dict):
        self.options.device.update(ev.t_event)
        self.data[self.options.name] = self.options.device.read(ev.t_event)
        return self.data

    def _read_fun(self, ev, channel_name):
        return self.data[channel_name]

    def _write_fun(self, ev, value_dict, aux_dict):
        assert len(value_dict) == 1
        value = list(value_dict.values())[0]
        self.options.device.update(ev.t_event)
        self.options.device.write(value, ev.t_event)
        self.data[self.options.name] = value
        return {self.options.name: value}


class ModelPairDeviceOptions(DeviceOptions):
    device_type: Literal['model_pair_wrapper'] = 'model_pair_wrapper'
    device: TimeAwareModel
    variable_name: str
    readback_name: str

    class Config:
        arbitrary_types_allowed = True


class ModelPairDevice(EngineDevice):
    """ Model a setpoint/readback pair of channels """
    device_type: str = 'Model pair wrapper'
    options: ModelPairDeviceOptions

    def __init__(self,
                 options: ModelPairDeviceOptions, ctx: SignalContext = None
                 ):
        self.data = {}
        assert hasattr(options.device, 'setpoint')
        channel_map = {options.variable_name: {}, options.readback_name: {}}
        super().__init__(options,
                         ctx,
                         update_fun=self._update_fun,
                         read_fun=self._read_fun,
                         read_now_fun=self._read_now_fun,
                         write_fun=self._write_fun,
                         scan_fun=self._scan_fun,
                         channel_map=channel_map)

    def _update_fun(self, ev, aux_dict):
        assert len(aux_dict) == 0
        self.options.device.update(ev.t_event)
        rb = self.options.device.read(ev.t_event)
        rb_exact = self.options.device.read_setpoint(ev.t_event)
        self.data[self.options.variable_name] = rb_exact
        self.data[self.options.readback_name] = rb
        return self.data

    def _read_fun(self, ev, channel_name):
        return self.data[channel_name]

    def _read_now_fun(self, ev, channel_name):
        return self.data[channel_name]

    def _write_fun(self, ev, value_dict, aux_dict):
        assert len(value_dict) == 1
        k = list(value_dict.keys())[0]
        value = list(value_dict.values())[0]
        if k == self.options.readback_name:
            raise DeviceWriteError('Readback cannot be written')
        else:
            assert k == self.options.variable_name
            self.options.device.update(ev.t_event)
            self.options.device.write(value, ev.t_event)
            self.options.device.update(ev.t_event)
            self.data[self.options.variable_name] = self.options.device.read_setpoint(ev.t_event)
            self.data[self.options.readback_name] = self.options.device.read(ev.t_event)
            return self.data

    def _scan_fun(self, ev):
        scan_rb = self.options.device.get_next_event(ev.t_event)
        if scan_rb is not None:
            self.data[self.options.readback_name] = scan_rb
            return {self.options.readback_name: scan_rb}
        else:
            return {}


# class ScriptDeviceOptions(DeviceOptions):
#     device_type: Literal['script'] = 'script'
#     script_read: Callable
#     script_write: Callable
#     signature_read: SignatureModel
#     signature_write: SignatureModel
#     channel_map: dict[str, Union[str, dict]]
#
#
# class ScriptDevice(EngineDevice):
#     DEVICE_TYPE = 'Script wrapper'
#
#     def __init__(self,
#                  ctx,
#                  options: ScriptDeviceOptions
#                  ):
#         channel_map = {options.name: {}}
#         self.last_results = {}
#         super().__init__(ctx,
#                          options=options,
#                          update_fun=self._update_fun,
#                          read_fun=self._read_fun,
#                          write_fun=self._write_fun,
#                          channel_map=channel_map)
#
#     def _update_fun(self, t_sched, t_run, data):
#         results = self.options.script_read(data)
#         for k, v in self.options.channel_map:
#             self.last_results[k] = results[k]
#         return self.last_results.copy()
#
#     def _read_fun(self, t_sched, t_run, channel_name):
#         assert channel_name in self.options.channel_map
#         return self.last_results[channel_name]
#
#     def _write_fun(self, t_sched, t_run, value_dict):
#         for k in value_dict.keys():
#             assert k in self.options.channel_map
#         self.options.script_write(value_dict)


ALL_DEVICE_CLASS_TYPE = Union[EchoDevice, ProxyDevice]

AllOptionsT = Union[EchoDeviceOptions,
ProxyDeviceOptions, EPICSDeviceOptions, RPNDeviceOptions, GenericDeviceOptions]

DEVICE_CLASS_MAP = {'echo': EchoDeviceOptions,
                    'proxy': ProxyDeviceOptions
                    }
