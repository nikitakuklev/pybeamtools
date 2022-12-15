import collections
import json
import logging
import time
import uuid
from abc import abstractmethod
from enum import Enum
from typing import Callable, Union, Optional, Any, Literal

import caproto
import caproto.threading.client
import numpy as np

from ..sim.core import SimulationEngine
from ..utils.pydantic import to_sdds
from .errors import SecurityError, ControlLibException, InvalidWriteError
from pydantic import BaseModel


class PVAccess(Enum):
    READONLY = 1
    #    WRITE = 2
    READWRITE = 3

class WriteResponse:
    def __init__(self, ts, data):
        self.timestamp = ts
        self.data = data

class PVOptions(BaseModel):
    name: str
    low: Union[float, int] = None
    high: Union[float, int] = None
    monitor: bool = True
    security: PVAccess = PVAccess.READONLY
    read_timeout: float = 2.0
    write_timeout: float = 5.0

    class Config:
        extra = 'forbid'

    def sdds(self):
        return to_sdds(json.loads(self.json()))


class PV:
    def __init__(self, options: PVOptions):
        self.uuid = str(uuid.uuid4())
        self.name = options.name
        self.options = options

    @abstractmethod
    def read(self, *, wait=True, callback=None,
             timeout=None, data_type=None, data_count=None, notify=True):
        pass

    def __str__(self):
        return f'{self.__class__.__name__} {self.options}'

    def __repr__(self):
        return self.__str__()

    def _check_proposed_write(self, data):
        if isinstance(data, (float, int)):
            if self.options.low and data < self.options.low:
                raise InvalidWriteError(f'Value {data} below bounds ({self.options.low}|{self.options.high})')
                # return False
            if self.options.high and data > self.options.high:
                raise InvalidWriteError(f'Value {data} above bounds ({self.options.low}|{self.options.high})')
        elif isinstance(data, str):
            pass
        else:
            raise ControlLibException(f'Unrecognized value  ({data=}) ({type(data)=})')


class EPICSPV(PV):
    def __init__(self, options: PVOptions):
        self.cm: Optional[EPICSConnectionManager] = None
        self.lower_ctrl_limit = self.upper_ctrl_limit = None
        super().__init__(options)

    @property
    def caproto(self) -> Optional[caproto.threading.client.PV]:
        if self.cm is None:
            return None
        else:
            return self.cm.pv_caproto_map[self.name]

    def read(self, *, wait=True, callback=None,
             timeout=None, data_type=None, data_count=None, notify=True):
        cm = self.caproto
        if cm is None:
            raise ControlLibException(f'PV is not bound to a connection manager')
        return self.caproto.read(wait=wait, callback=callback,
                                 timeout=self.options.read_timeout if timeout is None else timeout,
                                 data_type=data_type, data_count=data_count, notify=notify)

    def write(self, data, *, wait=True, callback=None,
              timeout=None, notify=None, data_type=None, data_count=None):
        # Check access
        if self.options.security != PVAccess.READWRITE:
            raise SecurityError(f'Writes on PV {self.name} are forbidden')
        # Propose a write - any issues will raise an Exception
        self.cm.acc.propose_writes(self.name, data)
        # Perform write
        return self.caproto.write(data, wait=wait, callback=callback,
                                  timeout=self.options.write_timeout if timeout is None else timeout,
                                  notify=notify, data_type=data_type, data_count=data_count)


class SimPV(PV):
    def __init__(self, options: PVOptions):
        self.cm: Optional[SimConnectionManager] = None
        super().__init__(options)

    def read(self, *, wait=True, callback=None,
             timeout=None, data_type=None, data_count=None, notify=True):
        if timeout is not None or data_type is not None or data_count is not None:
            raise
        return self.cm.sim.read_channel(self.name)

    def write(self, data, *, wait=True, callback=None,
              timeout=None, notify=None, data_type=None, data_count=None) -> WriteResponse:
        if not isinstance(data, (int, float, str)):
            raise InvalidWriteError(f'Data {data} is not of valid type')
        # Check access
        if self.options.security != PVAccess.READWRITE:
            raise SecurityError(f'Write on PV ({self.name}) forbidden by access mask')
        # Propose a write - any issues will raise an Exception
        self.cm.acc.propose_writes([self.name], [data])
        # Perform write
        self.cm.sim.write_channel(self.name, data)
        return WriteResponse(ts=time.time(), data=None)



class ConnectionOptions(BaseModel):
    network: Literal['epics', 'dummy'] = 'dummy'
    pvs: list[PVOptions] = []


class ConnectionManager:
    def __init__(self, acc, options: ConnectionOptions):
        self.acc = acc
        self.pv_map: dict[str, PV] = {}
        self.circular_buffers_map: dict[str, collections.deque] = {}
        self.last_results_map: dict[str, Any] = {}
        self.callbacks_map: dict[str, list[Callable]] = {}
        self.subscribed_pv_names: list[str] = []
        self.logger = logging.getLogger(self.__class__.__name__)
        self.options = options

    def __getitem__(self, pv_names):
        return self.get_pvs(pv_names)

    def __contains__(self, item):
        assert isinstance(item, str)
        return item in self.pv_map

    @abstractmethod
    def add_pvs(self, pv_names: list[str], pvs_configs: dict[str, PVOptions]):
        pass

    @abstractmethod
    def get_pvs(self, pv_names: list[str]) -> list[PV]:
        pass

    def dump_model(self):
        opts = self.options


class SimConnectionManager(ConnectionManager):
    def __init__(self, acc, options, ctx: SimulationEngine) -> None:
        super().__init__(acc, options)
        self.logger.info('Creating dummy connection manager')
        assert ctx.is_running
        self.sim = ctx

    def add_pvs(self, pv_names: list[str], pvs_configs: dict[str, PVOptions]):
        self.logger.debug(f'Adding {len(pv_names)} PVs')
        assert all(isinstance(pv_name, str) for pv_name in pv_names)
        if pvs_configs is None:
            pvs_config_default = PVOptions()
        else:
            for pv_name in pv_names:
                assert pv_name in pvs_configs, f'Missing config for {pv_name}'
                assert isinstance(pvs_configs[pv_name], PVOptions)
            pvs_config_default = None

        for i in range(len(pv_names)):
            pv_name = pv_names[i]
            cfg = pvs_config_default or pvs_configs[pv_name]
            pv = PV(options=cfg)
            pv.cm = self
            self.circular_buffers_map[pv_name] = collections.deque(maxlen=50)
            self.callbacks_map[pv_name] = []
            self.pv_map[pv_name] = pv
            self.last_results_map[pv_name] = None
            if pv.options.monitor:
                self.subscribe_monitor(pv)
            self.options.pvs.append(pv.options)

    def add_pvs_objects(self, pvs: list[SimPV]):
        assert all(isinstance(pv, SimPV) for pv in pvs), f'Only SimPVs can be added'
        self.logger.debug(f'Adding {len(pvs)} PV objects')
        pv_names = [pv.name for pv in pvs]
        for i in range(len(pv_names)):
            pv_name = pv_names[i]
            pv = pvs[i]
            pv.cm = self
            self.circular_buffers_map[pv_name] = collections.deque(maxlen=50)
            self.callbacks_map[pv_name] = []
            self.pv_map[pv_name] = pv
            self.last_results_map[pv_name] = None
            if pv.options.monitor:
                self.subscribe_monitor(pv)
            self.options.pvs.append(pv.options)

    def get_pvs(self, pv_names: list[str]) -> list[PV]:
        for pv_name in pv_names:
            assert isinstance(pv_name, str), f'Expect string PV names, not {repr(pv_name)}'
            if pv_name not in self.pv_map:
                raise KeyError(f'PV ({pv_name}) not found, make sure to add first')
        return [self.pv_map[pv_name] for pv_name in pv_names]

    def subscribe_monitor(self, pv: PV):
        if len(self.callbacks_map[pv.name]) != 0:
            raise ValueError(f'PV {pv.name} already has existing subscriptions')

        def callback(sub, response: np.ndarray):
            if self.acc.TRACE:
                self.logger.debug(f'Monitor callback for PV ({sub.name}): ({response})')
            name = sub.name
            self.circular_buffers_map[name].append(response)
            self.last_results_map[name] = response

        cb = callback
        subscription = self.sim.subscribe_channel(pv.name)
        subscription.add_callback(cb)
        self.callbacks_map[pv.name].append(cb)
        self.subscribed_pv_names.append(pv.name)


class EPICSConnectionManager(ConnectionManager):
    def __init__(self, acc, options, ctx=None) -> None:
        super().__init__(acc)
        self.logger.info('Creating EPICS connection manager')
        if ctx is None:
            self.logger.info('Context not provided, creating new caproto context')
            from caproto.threading.client import Context
            ctx = Context()
        self.ctx = ctx

        # All maps are keyed on string due to better performance of the underlying hashmap
        self.pv_caproto_map = {}
        self.initial_pv_data_map = {}

    def __connection_state_callback(self, pv: caproto.threading.client.PV, state: str):
        self.logger.debug(f'Connection state of {pv.name} changed to {state}')
        if state == 'connected':
            if pv.name not in self.initial_pv_data_map:
                start = pv.read(data_type='control')
                self.initial_pv_data_map[pv.name] = start
                self.pv_map[pv.name].lower_ctrl_limit = start.metadata.lower_ctrl_limit
                self.pv_map[pv.name].upper_ctrl_limit = start.metadata.upper_ctrl_limit
        elif state == 'disconnected':
            pass
        else:
            self.logger.warning(f'Unrecognized state {state} for {pv.name}')

    def add_pvs_objects(self, pvs):
        self.logger.debug(f'Adding {len(pvs)} PV objects')
        assert all(isinstance(pv, EPICSPV) for pv in pvs), f'Only EPICSPVs can be added'
        pv_names = [pv.name for pv in pvs]
        pvs_caproto = self.ctx.get_pvs(*pv_names, priority=1)
        for i in range(len(pv_names)):
            pv_name = pv_names[i]
            pv = pvs[i]
            pv.cm = self
            self.pv_caproto_map[pv_name] = pvs_caproto[i]
            self.circular_buffers_map[pv_name] = collections.deque(maxlen=50)
            self.callbacks_map[pv_name] = []
            self.pv_map[pv_name] = pv
            self.last_results_map[pv_name] = None
            if pv.options.monitor:
                self.subscribe_monitor(pv)

    def add_pvs(self, pv_names: list[str], pvs_configs: dict[str, PVOptions]):
        self.logger.debug(f'Adding {len(pv_names)} PVs')
        assert all(isinstance(pv_name, str) for pv_name in pv_names)
        if pvs_configs is None:
            pvs_config_default = PVOptions()
        else:
            for pv_name in pv_names:
                assert pv_name in pvs_configs, f'Missing config for {pv_name}'
                assert isinstance(pvs_configs[pv_name], PVOptions)
            pvs_config_default = None

        pvs_caproto = self.ctx.get_pvs(*pv_names, priority=1)
        for i in range(len(pv_names)):
            pv_name = pv_names[i]
            pv = PV(options=pvs_configs[pv_name] if pvs_config_default is None else pvs_config_default)
            pv.cm = self
            self.pv_caproto_map[pv_name] = pvs_caproto[i]
            self.circular_buffers_map[pv_name] = collections.deque(maxlen=50)
            self.callbacks_map[pv_name] = []
            self.pv_map[pv_name] = pv
            if pv.options.monitor:
                self.subscribe_monitor(pv)

    def get_pvs(self, pv_names: list[str]) -> list[PV]:
        for pv_name in pv_names:
            assert isinstance(pv_name, str), f'Expect only string PV names, not {repr(pv_name)}'
            if pv_name not in self.pv_caproto_map:
                raise KeyError(f'PV ({pv_name}) was not found in known list, make sure to add first')
        return [self.pv_map[pv_name] for pv_name in pv_names]

    def subscribe_monitor(self, pv: PV):
        if len(self.callbacks_map[pv.name]) != 0:
            # TODO: allow custom ones
            raise ValueError(f'PV {pv.name} already has existing subscriptions')

        def callback(sub, response):
            name = sub.pv.name
            self.circular_buffers_map[name].append(response)
            self.last_results_map[name] = response

        cb = callback
        subscription = pv.caproto.subscribe(data_type='time')
        subscription.add_callback(cb)
        self.callbacks_map[pv.name].append(cb)
        self.subscribed_pv_names.append(pv.name)

    def _get_recent_buffer_data(self, name: str, start: float = None):
        buf = self.circular_buffers_map[name]
        responses = list(buf)
        idx = 0
        for r in responses[::-1]:
            if r.metadata.timestamp is None:
                raise Exception(f'Found measurement {r} without timestamp')
            if start is None or r.metadata.timestamp > start:
                idx += 1
            else:
                break

        if idx > 0:
            # print(f'PV {name}: buffer had {idx} readings past {start} ({[r.metadata.timestamp for r in responses[-idx:]]})')
            return responses[-idx:]
        else:
            # print(f'PV {name}: buffer had {idx} readings past {start} ({[]})')
            return []

    def start_epics_repeater(self):
        self.logger.info('Spawning repeater')
        from caproto.sync import repeater
        repeater.spawn_repeater()
