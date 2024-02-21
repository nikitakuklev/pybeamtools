import logging
import multiprocessing
import os
import time

import numpy as np
import pytest

from pybeamtools.controls import EPICSPV
from pybeamtools.controls import ConnectionOptions, PVAccess, \
    PVOptions
from pybeamtools.controls.errors import InterlockWriteError, SecurityError
from pybeamtools.controls.interlocks import LimitInterlock, LimitInterlockOptions
from pybeamtools.sim.core import SignalEngineOptions, SignalEngine
from pybeamtools.sim.softioc import EchoIOC, SimpleIOC
from pybeamtools.sim.templates import MockSetupPairDevice
import pybeamtools.controls as pc
import pytest
from pybeamtools.controls import Accelerator, AcceleratorOptions, ConnectionOptions, PVAccess, \
    PVOptions
from pybeamtools.controls.errors import SecurityError
from pybeamtools.sim.core import SignalEngineOptions, SignalEngine
from pybeamtools.sim.errors import DeviceWriteError
from pybeamtools.sim.pddevices import DS, EPICSDevice, EPICSDeviceOptions, EchoDevice, \
    EchoDeviceOptions, ProxyDevice, ProxyDeviceOptions, TRIG
from pybeamtools.sim.templates import MockSetupPairDevice

logger = logging.getLogger(__name__)

variables = ['X0', 'X1', 'X2']
variables_pv = [x + 'PV' for x in variables]
readbacks = ['X0_RB', 'X1_RB', 'X2_RB']
readbacks_pv = [x + 'PV' for x in readbacks]
objectives = ['OBJ0']
objectives_pv = [x + 'PV' for x in objectives]

ED = EPICSDevice
EDO = EPICSDeviceOptions

# @pytest.fixture
# def sim_engine() -> SimulationEngine:
#     sim = SimulationEngine(SignalEngineOptions(time_function=time.time(),
#                                                update_thread_name='simaccupd'))
#     sim.TRACE = True
#     sim.TIME_TRACE = True
#     sim.txid = 50000
#     return sim
os.environ['EPICS_CA_AUTO_ADDR_LIST'] = 'no'
os.environ['EPICS_CA_ADDR_LIST'] = '127.0.0.1'


class TestEPICSPV:
    # variables = ['X0PV', 'X1PV', 'X2PV']
    # readbacks = ['X0_RBPV', 'X1_RBPV', 'X2_RBPV']
    # objectives = ['OBJ0PV']

    @pytest.fixture(autouse=True)
    def set_env(self):
        os.environ['EPICS_CA_AUTO_ADDR_LIST'] = 'no'
        os.environ['EPICS_CA_ADDR_LIST'] = '127.0.0.1'

    def run_repeater(self):
        from caproto.sync import repeater
        repeater.run(host='127.0.0.1')
        # time.sleep(1.0)

    def run_repeater_process(self):
        p = multiprocessing.Process(target=self.run_repeater)
        p.daemon = True
        p.start()
        logger.info(f'Repeater started {p=}')

    # @pytest.fixture
    # def soft_ioc(self, sim_engine):
    #     os.environ['EPICS_CA_AUTO_ADDR_LIST'] = 'no'
    #     os.environ['EPICS_CA_ADDR_LIST'] = '127.0.0.1'
    #
    #     from caproto.sync import repeater
    #     repeater.spawn_repeater()
    #     time.sleep(0.1)
    #
    #     channels = ['TEST:CHANNEL:A', 'TEST:CHANNEL:B', 'TEST:CHANNEL:C', 'TEST:CHANNEL:T']
    #     sioc = EchoIOC(channels=channels, sim_engine=sim_engine)
    #     sioc.setup()
    #     sioc.run_in_background()
    #     logger.debug(f'Soft IOC started')
    #     for ch in channels:
    #         def callback(sub, response: np.ndarray):
    #             name = sub.name
    #             logger.debug(f'Soft IOC put callback for PV ({sub.name}): ({response})')
    #             # logger.debug(f'{type(name)=} {type(response[0])=}')
    #             # logger.debug(f'{sioc=} {sioc.__dict__=}')
    #             # sioc.bl.pvdb[name].write(response[0], verify_value=False)
    #             # sioc.ping()
    #             sioc.send_updates(name, response)
    #
    #         cb = callback
    #         subscription = sim_engine.subscribe_channel(ch)
    #         subscription.add_callback(cb)
    #
    #     time.sleep(0.1)
    #     return sioc

    # @pytest.fixture
    # def f_sim_with_pvs_low(self, sim_engine_low):
    #     ao = pc.AcceleratorOptions(connection_settings=ConnectionOptions(network='epics'))
    #     acc = pc.Accelerator(options=ao)
    #     pv_settings = PVOptions(name='TEST:CHANNEL:A', low=0.0, high=5.0,
    #                             security=PVAccess.RW)
    #     pv = EPICSPV(pv_settings)
    #     acc.add_pv_object([pv])
    #     return sim_engine_low, acc, pv

    # @pytest.fixture(autouse=False)
    # def f_soft_ioc_low(self, sim_engine_low):
    #     sim_engine = sim_engine_low
    #     os.environ['EPICS_CA_AUTO_ADDR_LIST'] = 'no'
    #     os.environ['EPICS_CA_ADDR_LIST'] = '127.0.0.1'
    #
    #     from caproto.sync import repeater
    #     repeater.spawn_repeater()
    #     time.sleep(0.1)
    #
    #     channels = ['TEST:CHANNEL:A', 'TEST:CHANNEL:B']
    #     sioc = EchoIOC(channels=channels, sim_engine=sim_engine)
    #     sioc.setup()
    #     sioc.run_in_background()
    #     logger.debug(f'Soft IOC started')
    #     for ch in channels:
    #         def callback(sub, response: np.ndarray):
    #             name = sub.name
    #             logger.debug(
    #                 f'Soft IOC put input_var_change_callback for PV ({sub.name}): ({response})')
    #             # logger.debug(f'{type(name)=} {type(response[0])=}')
    #             # logger.debug(f'{sioc=} {sioc.__dict__=}')
    #             # sioc.bl.pvdb[name].write(response[0], verify_value=False)
    #             # sioc.ping()
    #             sioc.send_updates(name, response)
    #
    #         cb = callback
    #         subscription = sim_engine.subscribe_channel(ch)
    #         subscription.add_callback(cb)
    #
    #     time.sleep(0.1)
    #     return sioc

    # @pytest.fixture(autouse=False)
    # def f_simple_soft_ioc(self, sim_engine):
    #     os.environ['EPICS_CA_AUTO_ADDR_LIST'] = 'no'
    #     os.environ['EPICS_CA_ADDR_LIST'] = '127.0.0.1'
    #
    #     variables = ['X0', 'X1']
    #     objectives = ['OBJ0']
    #     test_variables = []
    #
    #     from caproto.sync import repeater
    #     repeater.spawn_repeater()
    #     time.sleep(0.1)
    #
    #     sioc = SimpleIOC(variables, objectives, test_variables, noise=0.05)
    #     sioc.setup()
    #     sioc.run_in_background()
    #     logger.debug(f'Soft IOC started')
    #     time.sleep(0.1)
    #     return sioc

    # @pytest.fixture
    # def f_sim_with_pvs(self, sim_engine):
    #     ao = pc.AcceleratorOptions(connection_settings=ConnectionOptions(network='epics'))
    #     acc = pc.Accelerator(options=ao)
    #     pv_settings = PVOptions(name='TEST:CHANNEL:A', low=0.0, high=5.0,
    #                             security=PVAccess.RW)
    #     pv = EPICSPV(pv_settings)
    #     pv_settings = PVOptions(name='TEST:CHANNEL:B', low=0.0, high=5.0,
    #                             security=PVAccess.RW)
    #     pv2 = EPICSPV(pv_settings)
    #     pv_settings = PVOptions(name='TEST:CHANNEL:C', low=0.0, high=5.0,
    #                             security=PVAccess.RO)
    #     pv3 = EPICSPV(pv_settings)
    #     pv_settings = PVOptions(name='TEST:CHANNEL:T', security=PVAccess.RO)
    #     pv4 = EPICSPV(pv_settings)
    #     acc.add_pv_object([pv, pv2, pv3, pv4])
    #     return sim_engine, acc, pv, pv2, pv3, pv4

    @pytest.fixture
    def f_sim_rt_noscan(self):
        sim = SignalEngine(SignalEngineOptions(time_function=time.time,
                                               update_thread_name='simaccupd'))
        sim.TRACE = True
        sim.TIME_TRACE = True
        sim.txid = 50000
        pmodel_kwargs = dict(readback_update_rate=1.0,
                            model='exponential',
                            pmodel_kwargs={'decay_constant': 0.5},
                            )
        mg = MockSetupPairDevice(variables=variables_pv,
                                 objectives=objectives_pv,
                                 readbacks=readbacks_pv,
                                 noise=0.01,
                                 variable_pmodel_kwargs=pmodel_kwargs,
                                 scan_period_rb=0.0,
                                 realtime=True)
        mg.create(sim)
        return sim

    @pytest.fixture
    def f_acc_and_sim_with_pvs(self) -> tuple[Accelerator, SignalEngine]:
        ao = AcceleratorOptions(connection_settings=ConnectionOptions(network='epics'))
        acc = Accelerator(options=ao)
        acc.TRACE = True

        sim = SignalEngine(SignalEngineOptions(time_function=time.time))
        sim.TRACE = True
        sim.TIME_TRACE = True

        devs = []
        for var in variables:
            dev = ED(EDO(name=f'epics_{var}',
                         pv_to_ch_map={f'{var}PV': f'{var}'}, connection='epics',
                         pv_config=PVOptions(name=f'{var}PV',
                                             security=PVAccess.RW,
                                             monitor=True)),
                     ctx=None, acc_context=acc)
            sim.add_device(dev)
            # sim.enable_device(dev)
            devs.append(dev)

        for el in readbacks+objectives:
            dev = ED(EDO(name=f'epics_{el}',
                         pv_to_ch_map={f'{el}PV': f'{el}'}, connection='epics',
                         pv_config=PVOptions(name=f'{el}PV',
                                             security=PVAccess.RO,
                                             monitor=True)),
                     ctx=None, acc_context=acc)
            sim.add_device(dev)
            # sim.enable_device(dev)
            devs.append(dev)

        return acc, sim

    @pytest.fixture
    def f_soft_ioc(self, f_sim_rt_noscan):
        sim = f_sim_rt_noscan

        self.run_repeater_process()
        time.sleep(3.0)

        channels = variables_pv + readbacks_pv + objectives_pv
        sioc = EchoIOC(channels=channels, sim_engine=sim)
        sioc.setup()
        sioc.run_in_background()
        logger.debug(f'Soft IOC started')
        for ch in readbacks_pv + objectives_pv:
            def callback(sub, response):
                name = sub.name
                logger.debug(f'Soft IOC put callback for PV ({sub.name}): ({response})')
                # logger.debug(f'{type(name)=} {type(response[0])=}')
                # logger.debug(f'{sioc=} {sioc.__dict__=}')
                # sioc.bl.pvdb[name].write(response[0], verify_value=False)
                # sioc.ping()
                sioc.send_updates(name, response)

            cb = callback
            subscription = sim.subscribe_channel(ch)
            subscription.add_callback(cb)

        time.sleep(0.1)
        return sioc

    @pytest.fixture
    def f_soft_ioc_process(self):
        self.run_repeater_process()
        time.sleep(3.0)

        process = multiprocessing.Process(target=self.soft_ioc_process)
        process.daemon = True
        logger.info(f'Starting process {process=}')
        process.start()
        logger.info(f'Started process {process=}')
        return process

    def soft_ioc_process(self):
        os.environ['EPICS_CA_AUTO_ADDR_LIST'] = 'NO'
        os.environ['EPICS_CA_ADDR_LIST'] = '127.0.0.1'

        sim = SignalEngine(SignalEngineOptions(time_function=time.time,
                                               update_thread_name='simaccupd'))
        sim.TRACE = True
        sim.TIME_TRACE = True
        sim.txid = 50000
        pmodel_kwargs = dict(readback_update_rate=1.0,
                            model='exponential',
                            pmodel_kwargs={'decay_constant': 0.5},
                            )
        mg = MockSetupPairDevice(variables=variables_pv,
                                 objectives=objectives_pv,
                                 readbacks=readbacks_pv,
                                 noise=0.01,
                                 variable_pmodel_kwargs=pmodel_kwargs,
                                 scan_period_rb=0.0,
                                 realtime=True)
        mg.create(sim)

        channels = variables_pv + readbacks_pv + objectives_pv
        sioc = EchoIOC(channels=channels, sim_engine=sim)
        sioc.setup()

        # Only do callbacks on non-vars
        for ch in readbacks_pv + objectives_pv:
            def callback(sub, response: np.ndarray):
                name = sub.name
                logger.debug(f'Soft IOC put callback for PV ({sub.name}): ({response})')
                sioc.send_updates(name, response)

            cb = callback
            subscription = sim.subscribe_channel(ch)
            subscription.add_callback(cb)

        logger.debug(f'Soft IOC starting')
        sioc.run_in_current_loop()

    def test_pytest(self, f_sim_rt_noscan):
        assert os.environ['EPICS_CA_AUTO_ADDR_LIST'] == 'no'
        time.sleep(10)

    def test_sioc_init(self, f_sim_rt_noscan, f_soft_ioc):
        time.sleep(3)
        f_sim_rt_noscan.write_channel(variables_pv[1], 5.0)
        time.sleep(1.0)
        assert f_sim_rt_noscan.read_channel(variables_pv[1]) == 5.0

    def test_sioc_process_init(self, f_soft_ioc_process):
        time.sleep(3)
        assert f_soft_ioc_process.exitcode is None

    def test_full_init(self, f_sim_rt_noscan, f_soft_ioc, f_acc_and_sim_with_pvs):
        acc, sim = f_acc_and_sim_with_pvs
        logger.info('========================')
        time.sleep(3.0)
        for dev in sim.devices_list:
            assert isinstance(dev, ED)
            with pytest.raises(KeyError):
                assert not dev.is_connected()
        logger.info('========================')
        for dev in sim.devices_list:
            assert isinstance(dev, ED)
            sim.enable_device(dev)
            assert not dev.is_connected()
        time.sleep(3.0)
        for dev in sim.devices_list:
            assert isinstance(dev, ED)
            assert dev.is_connected(), dev.name
        # f_sim_rt_noscan.write_channel(variables_pv[1], 5.0)
        f_soft_ioc.send_updates(variables_pv[1], 5.0)
        time.sleep(3.0)
        assert sim.read_channel(variables[1]) == 5.0

    def test_pv_simple(self, f_sim_rt_noscan, f_soft_ioc, f_acc_and_sim_with_pvs):
        acc, sim = f_acc_and_sim_with_pvs
        for dev in sim.devices_list:
            sim.enable_device(dev)
        time.sleep(3)
        logger.info(f'{acc.cm.last_results_map=}')
        for k, v in acc.cm.circular_buffers_map.items():
            # assert len(v) > 2
            logger.info(f'{k}:{len(v)}')

    # def test_pv_simple(self, sim_engine_with_pvs_low, soft_ioc_low):
    #     sim_engine, acc, pv = sim_engine_with_pvs_low
    #     sim_engine.TRACE = True
    #     time.sleep(10)
    #     logger.info(f'{acc.cm.last_results_map=}')
    #     for k, v in acc.cm.circular_buffers_map.items():
    #         # assert len(v) > 2
    #         logger.info(f'{k}:{len(v)}')

    # def test_pv_simple2(self, sim_engine_with_pvs):
    #     sim_engine, acc, pv, pv2, pv3, pv4 = sim_engine_with_pvs
    #     time.sleep(2)
    #     logger.info(f'{acc.cm.last_results_map=}')
    #     t1 = pv4.read()
    #     r = pv.read()
    #     assert r.data == 0.5, r
    #     time.sleep(2)
    #     t2 = pv4.read()
    #     assert t2.data > t1.data
    #     logger.info(f'{acc.cm.last_results_map=}')
    #     for k, v in acc.cm.circular_buffers_map.items():
    #         assert len(v) > 2
    #         logger.info(f'{k}:{len(v)}')

    def test_pv_softioc(self, f_sim_rt_noscan, f_soft_ioc, f_acc_and_sim_with_pvs):
        acc, sim = f_acc_and_sim_with_pvs
        sioc = f_soft_ioc
        for dev in sim.devices_list:
            sim.enable_device(dev)

        time.sleep(3)

        for dev in sim.devices_list:
            assert dev.is_connected()

        logger.info(f'{sim.channels=}')

        with pytest.raises(SecurityError):
            sim.channel_to_device[readbacks[0]].pv.write(2.6)

        for ch in sim.channels:
            assert sim.latest_data[ch] is not None

        for ch in acc.cm.pv_map:
            assert acc.cm.last_results_map[ch] is not None

        for ch in variables_pv:
            assert sioc.pvdb[ch].value == 0.0

        acc.cm.pv_map[variables_pv[0]].write(1.5)
        assert sim.read_channel(variables[0]) == 1.5
        assert sioc.pvdb[variables_pv[0]].value == 1.5

    # def test_pv_softioc(self, sim_engine_with_pvs, soft_ioc):
    #     sim_engine, acc, pv, pv2, pv3 = sim_engine_with_pvs
    #     interlock_limits = {'TEST:CHANNEL:A': (-1.0, 1.0),
    #                         'TEST:CHANNEL:B': (-1.0, None),
    #                         'TEST:CHANNEL:C': (-1.0, 1.0)
    #                         }
    #     pv_list = ['TEST:CHANNEL:A', 'TEST:CHANNEL:B', 'TEST:CHANNEL:C']
    #     lopt = LimitInterlockOptions(pv_list=pv_list,
    #                                  read_events=[],
    #                                  write_events=pv_list,
    #                                  limits=interlock_limits)
    #     ilock = LimitInterlock(options=lopt)
    #     acc.add_interlock(ilock)
    #
    #     with pytest.raises(SecurityError):
    #         pv3.write(2.6)
    #
    #     assert acc.cm.last_results_map['TEST:CHANNEL:B'] is None, acc.cm.last_results_map
    #     time.sleep(0.51)
    #     assert acc.cm.last_results_map['TEST:CHANNEL:B'] is not None, acc.cm.last_results_map
    #     assert acc.cm.last_results_map['TEST:CHANNEL:C'] is not None, acc.cm.last_results_map
    #
    #     with pytest.raises(InterlockWriteError):
    #         pv.write(1.4)
    #
    #     with pytest.raises(InterlockWriteError):
    #         pv2.write(-1.4)
    #
    #     assert soft_ioc.pvdb['TEST:CHANNEL:A'].value == 0.0
    #     assert soft_ioc.pvdb['TEST:CHANNEL:B'].value == 0.0
    #     assert soft_ioc.pvdb['TEST:CHANNEL:C'].value == 0.0
    #
    #     print(ilock.__dict__)
    #     pv2.write(1.4)
    #
    #     assert sim_engine.read_channel('TEST:CHANNEL:B') == 1.4
    #     assert soft_ioc.pvdb['TEST:CHANNEL:B'].value == 1.4
    #
    #     acc.pm.stop_interlock(ilock)
