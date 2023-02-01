import collections
import logging
from abc import abstractmethod
from typing import Any, Callable, Literal

import caproto.threading.client
import numpy as np
from .pv import EPICSPV, PV, PVOptions, SimPV
from pydantic import BaseModel




class ConnectionOptions(BaseModel):
    network: Literal['epics', 'dummy'] = 'dummy'
    pvs: list[PVOptions] = []
    timeout: float = 5.0


class ConnectionManager:
    def __init__(self, acc, options: ConnectionOptions):
        self.acc = acc
        self.pv_map: dict[str, PV] = {}
        self.circular_buffers_map: dict[str, collections.deque] = {}
        self.last_results_map: dict[str, Any] = {}
        self.callbacks_map: dict[str, list[Callable]] = {}
        self.custom_callbacks_map: dict[str, list[Callable]] = {}
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
    def __init__(self, acc, options, ctx) -> None:
        from ..sim.core import SimulationEngine
        super().__init__(acc, options)
        self.logger.info('Creating dummy connection manager')
        assert ctx.is_running
        self.sim: SimulationEngine = ctx

        if len(options.pvs) > 0:
            names = [x.name for x in self.options.pvs]
            opts = {x.name: x for x in self.options.pvs}
            self.add_pvs(names, opts)

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
        super().__init__(acc, options)
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
            self.custom_callbacks_map[pv_name] = []
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

    def subscribe_monitor(self, pv: EPICSPV):
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

    def subscribe_custom(self, pv: EPICSPV, callback: Callable):
        """ Add custom callback """
        subscription = pv.caproto.subscribe(data_type='time')
        subscription.add_callback(callback)
        self.custom_callbacks_map[pv.name].append(callback)

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
