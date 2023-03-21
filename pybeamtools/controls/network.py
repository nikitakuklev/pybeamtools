import collections
import logging
import traceback
from abc import abstractmethod
from typing import Any, Callable, Literal

import numpy as np
from pydantic import BaseModel

from .pv import EPICSPV, PV, PVOptions, SimPV

logger = logging.getLogger(__name__)

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
        # assert ctx.is_running
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
        pv_names = [pv.name for pv in pvs]
        self.logger.debug(f'Adding ({len(pvs)}) PV objects: {pv_names=}')
        for i in range(len(pv_names)):
            pv_name = pv_names[i]
            pv = pvs[i]
            pv.cm = self
            self.circular_buffers_map[pv_name] = collections.deque(maxlen=50)
            self.callbacks_map[pv_name] = []
            self.custom_callbacks_map[pv_name] = []
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

        def monitor_callback(sub, response: np.ndarray):
            if self.acc.TRACE:
                self.logger.debug(
                        f'ACC callback for PV ({sub.name}): ({response})')
            name = sub.name
            self.circular_buffers_map[name].append(response)
            self.last_results_map[name] = response

        cb = monitor_callback
        subscription = self.sim.subscribe_channel(pv.name)
        subscription.add_callback(cb)
        self.callbacks_map[pv.name].append(cb)
        self.subscribed_pv_names.append(pv.name)

    def subscribe_custom(self, pv: SimPV, callback: Callable):
        """ Add custom input_var_change_callback """
        subscription = self.sim.subscribe_channel(pv.name)
        subscription.add_callback(callback)
        self.custom_callbacks_map[pv.name].append(callback)

        # Force update
        self.logger.debug(f'Triggering full update of ({pv.name})')
        self.sim.push_full_update_to_device(self.sim.channel_to_device[pv.name])

    def is_connected(self, pvn: str):
        if pvn in self.sim.channels:
            dn = self.sim.channel_to_device_name[pvn]
            try:
                self.sim.check_enabled_state(dn)
                return True
            except:
                pass
        return False


class EPICSConnectionManager(ConnectionManager):
    def __init__(self, acc, options, ctx=None) -> None:
        from caproto.threading.client import Context
        import caproto.threading.client
        super().__init__(acc, options)
        self.logger.info('Creating EPICS connection manager')
        if ctx is None:
            self.logger.info('Context not provided, creating new one for each!!!')
            ctx = Context()
            self.ctx: caproto.threading.client.Context = ctx
        # self.def_ctx = ctx
        self.ctxs = {}

        # All maps are keyed on string due to better performance of the underlying hashmap
        self.pv_caproto_map: dict[str, caproto.threading.client.PV] = {}
        self.initial_pv_data_map = {}

    def __state_callback(self, pv, state: str):
        self.logger.debug(f'Connection state of PV ({pv.name}) changed to ({state})')
        if state == 'connected':
            #if pv.name not in self.initial_pv_data_map:
                #start = pv.read(data_type='control')
                #self.initial_pv_data_map[pv.name] = start
                #self.pv_map[pv.name].lower_ctrl_limit = start.metadata.lower_ctrl_limit
                #self.pv_map[pv.name].upper_ctrl_limit = start.metadata.upper_ctrl_limit
            pass
        elif state == 'disconnected':
            pass
        else:
            self.logger.warning(f'Unrecognized state {state} for {pv.name}')

    def add_pvs_objects(self, pvs: list[EPICSPV]):
        from caproto.threading.client import Context
        assert all(isinstance(pv, EPICSPV) for pv in pvs), f'Only EPICSPVs can be added'
        pv_names = [pv.name for pv in pvs]
        # No individual contexts
        #self.ctxs.update({pv.name: Context() for pv in pvs})
        self.ctxs.update({pv.name: self.ctx for pv in pvs})

        # pvs_caproto = self.ctx.get_pvs(*pv_names, priority=1)
        pvs_caproto = []
        for pv in pvs:
            pvca = self.ctxs[pv.name].get_pvs(pv.name,
                                              priority=0,
                                              connection_state_callback=self.__state_callback)[0]
            pvs_caproto.append(pvca)

        # time.sleep(1)
        # self.logger.debug(f'{self.ctx.pvs_needing_circuits=}')
        self.logger.debug(f'Adding ({len(pvs)}) PV objects: {pv_names=} {pvs_caproto=}')
        for i in range(len(pv_names)):
            # ctx = self.ctxs[pv_names[i]]
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
                self.logger.debug(f'Adding monitor for ({pv_name})')

    # def add_pvs(self, pv_names: list[str], pvs_configs: dict[str, PVOptions]):
    #     self.logger.debug(f'Adding {len(pv_names)} PVs')
    #     assert all(isinstance(pv_name, str) for pv_name in pv_names)
    #     if pvs_configs is None:
    #         o_default = PVOptions()
    #     else:
    #         for pv_name in pv_names:
    #             assert pv_name in pvs_configs, f'Missing config for {pv_name}'
    #             assert isinstance(pvs_configs[pv_name], PVOptions)
    #         o_default = None
    #
    #     pvs_caproto = self.ctx.get_pvs(*pv_names, priority=1)
    #     for i in range(len(pv_names)):
    #         pv_name = pv_names[i]
    #         pv = EPICSPV(
    #             options=pvs_configs[pv_name] if o_default is None else o_default)
    #         pv.cm = self
    #         self.pv_caproto_map[pv_name] = pvs_caproto[i]
    #         self.circular_buffers_map[pv_name] = collections.deque(maxlen=50)
    #         self.callbacks_map[pv_name] = []
    #         self.pv_map[pv_name] = pv
    #         if pv.options.monitor:
    #             self.subscribe_monitor(pv)

    def get_pvs(self, pv_names: list[str]) -> list[PV]:
        for pv_name in pv_names:
            assert isinstance(pv_name, str), f'Expect only string PV names, not {repr(pv_name)}'
            if pv_name not in self.pv_caproto_map:
                raise KeyError(
                        f'PV ({pv_name}) was not found in known list, make sure to add first')
        return [self.pv_map[pv_name] for pv_name in pv_names]

    def subscribe_monitor(self, pv: EPICSPV):
        # ctx = self.ctxs[pv.name]
        if len(self.callbacks_map[pv.name]) != 0:
            self.logger.warning(f'PV {pv.name} already has subscriptions')

        def callback(sub, response):
            #logger.warning(f'EPICS callback ({sub=} {response=})')
            try:
                name = sub.pv.name
                self.circular_buffers_map[name].append(response)
                self.last_results_map[name] = response
            except Exception as ex:
                self.logger.warning(f'EPICS callback ({sub=} {response=}) failed')
                self.logger.warning(f'{traceback.format_exc()}')

        cb = callback
        subscription = pv.caproto.subscribe(data_type='time')
        subscription.add_callback(cb)
        self.callbacks_map[pv.name].append(cb)
        self.subscribed_pv_names.append(pv.name)

    def subscribe_custom(self, pv: EPICSPV, callback: Callable):
        """ Add custom input_var_change_callback """
        subscription = pv.caproto.subscribe(data_type='time')
        subscription.add_callback(callback)
        self.custom_callbacks_map[pv.name].append(callback)

    def is_connected(self, pv_name: str) -> bool:
        return self.pv_caproto_map[pv_name].connected

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

    # def start_epics_repeater(self):
    #     self.logger.info('Spawning repeater')
    #     from caproto.sync import repeater
    #     repeater.spawn_repeater()
