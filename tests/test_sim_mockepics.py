import logging
import random
import time

import pybeamtools.controls as pc
import pytest
from pybeamtools.controls import Accelerator, AcceleratorOptions, ConnectionOptions, PVAccess, \
    PVOptions
from pybeamtools.controls.errors import SecurityError
from pybeamtools.sim.core import SignalEngineOptions, SimulationEngine
from pybeamtools.sim.errors import DeviceWriteError
from pybeamtools.sim.pddevices import DS, EPICSDevice, EPICSDeviceOptions, EchoDevice, \
    EchoDeviceOptions, ProxyDevice, ProxyDeviceOptions, TRIG
from pybeamtools.sim.templates import MockSetupPairDevice

logger = logging.getLogger(__name__)

t = 0.0


def fixed_time():
    return t


ED = EPICSDevice
EDO = EPICSDeviceOptions


@pytest.fixture
def f_acc_and_sim():
    sim = SimulationEngine(SignalEngineOptions(time_function=time.time,
                                               update_thread_name='simaccupd'))
    sim.TRACE = True
    sim.TIME_TRACE = True
    sim.txid = 50000

    variables = ['X0PV', 'X1PV', 'X2PV']
    readbacks = ['X0_RBPV', 'X1_RBPV', 'X2_RBPV']
    objectives = ['OBJ0PV']

    mg = MockSetupPairDevice(variables=variables, objectives=objectives, readbacks=readbacks,
                             constants=[],
                             extra_vars=[],
                             evaluation_functions=None,
                             evaluation_variables=None,
                             noise=0.01)

    mg.create(sim)

    ao = AcceleratorOptions(connection_settings=ConnectionOptions(network='dummy'))
    acc = Accelerator(options=ao, ctx=sim)
    acc.TRACE = True
    return acc, sim


@pytest.fixture
def acc_and_sim_rt_noscan():
    sim = SimulationEngine(SignalEngineOptions(time_function=time.time,
                                               update_thread_name='simaccupd'))
    sim.TRACE = True
    sim.TIME_TRACE = True
    sim.txid = 50000

    variables = ['X0PV', 'X1PV', 'X2PV']
    readbacks = ['X0_RBPV', 'X1_RBPV', 'X2_RBPV']
    objectives = ['OBJ0PV']

    mg = MockSetupPairDevice(variables=variables, objectives=objectives, readbacks=readbacks,
                             constants=[], extra_vars=[],
                             evaluation_functions=None,
                             evaluation_variables=None,
                             noise=0.01,
                             variable_pmodel_kwargs=dict(readback_update_rate=1.0,
                                                        model='exponential',
                                                        pmodel_kwargs={'decay_constant': 0.5},
                                                        ),
                             scan_period_rb=0.0,
                             realtime=True)

    mg.create(sim)

    # echo1 = EchoDevice(EchoDeviceOptions(name='echo1', data={'XECHOPV': 2.0}))
    # sim.add_device(echo1)
    # sim.enable_device(echo1)

    ao = AcceleratorOptions(connection_settings=ConnectionOptions(network='dummy'))
    acc = Accelerator(options=ao, ctx=sim)
    acc.TRACE = True
    return acc, sim


@pytest.fixture
def acc_and_sim_rt_scan():
    sim = SimulationEngine(SignalEngineOptions(time_function=time.time,
                                               update_thread_name='simaccupd'))
    sim.TRACE = True
    sim.TIME_TRACE = True
    sim.txid = 50000

    variables = ['X0PV', 'X1PV', 'X2PV']
    readbacks = ['X0_RBPV', 'X1_RBPV', 'X2_RBPV']
    objectives = ['OBJ0PV']

    mg = MockSetupPairDevice(variables=variables, objectives=objectives, readbacks=readbacks,
                             constants=[], extra_vars=[],
                             evaluation_functions=None,
                             evaluation_variables=None,
                             noise=0.01,
                             variable_pmodel_kwargs=dict(readback_update_rate=1.0,
                                                        model='exponential',
                                                        pmodel_kwargs={'decay_constant': 0.5},
                                                        ),
                             scan_period_rb=2.0,
                             realtime=True)

    mg.create(sim)

    ao = AcceleratorOptions(connection_settings=ConnectionOptions(network='dummy'))
    acc = Accelerator(options=ao, ctx=sim)
    acc.TRACE = True
    return acc, sim


@pytest.fixture
def acc_and_sim_rt_scan_simple():
    def fixed_time():
        return time.time()

    simacc = SimulationEngine(SignalEngineOptions(time_function=fixed_time))
    simacc.TRACE = True
    simacc.TIME_TRACE = True

    echo1 = EchoDevice(EchoDeviceOptions(name='echo1', data={'X0PV': 2.0}, scan_period=1.0))
    simacc.add_device(echo1)
    simacc.enable_device(echo1)

    ao = pc.AcceleratorOptions(connection_settings=ConnectionOptions(network='dummy'))
    acc = pc.Accelerator(options=ao, ctx=simacc)
    acc.TRACE = True
    return acc, simacc


@pytest.fixture
def mock_sim_engine_with_pvs(acc_and_sim_rt_noscan) -> tuple[
    SimulationEngine, Accelerator, SimulationEngine]:
    sim = SimulationEngine(SignalEngineOptions(time_function=time.time))
    sim.TRACE = True
    sim.TIME_TRACE = True

    acc, simacc = acc_and_sim_rt_noscan

    x0rb = ED(EDO(name='epicsX0_RB', pv_to_ch_map={'X0_RBPV': 'X0_RB'}, connection='dummy',
                  pv_config=PVOptions(name='X0_RBPV', low=0.0, high=7.0,
                                      security=PVAccess.RW, monitor=True)),
              ctx=None, acc_context=acc)

    x0 = ED(EDO(name='epicsX0', pv_to_ch_map={'X0PV': 'X0'}, connection='dummy',
                pv_config=PVOptions(name='X0PV', low=0.0, high=7.0,
                                    security=PVAccess.RW, monitor=True)),
            ctx=None, acc_context=acc)

    obj0 = ED(EDO(name='epicsOBJ0', pv_to_ch_map={'OBJ0PV': 'OBJ0'}, connection='dummy',
                  pv_config=PVOptions(name='OBJ0PV',
                                      security=PVAccess.RO, monitor=True)),
              ctx=None, acc_context=acc)

    for dev in [x0rb, x0, obj0]:
        sim.add_device(dev)

    for dev in [x0rb, x0, obj0]:
        sim.enable_device(dev)

    for dev in [x0rb, x0, obj0]:
        assert dev.is_connected()

    return sim, acc, simacc


@pytest.fixture
def mock_sim_engine_with_pvs_simple(acc_and_sim_rt_scan_simple) -> tuple[
    SimulationEngine, Accelerator, SimulationEngine]:
    sim = SimulationEngine(SignalEngineOptions(time_function=time.time))
    sim.TRACE = True
    sim.TIME_TRACE = True

    acc, simacc = acc_and_sim_rt_scan_simple

    x0 = ED(EDO(name='epicsX0', pv_to_ch_map={'X0PV': 'X0'}, connection='dummy',
                pv_config=PVOptions(name='X0PV', security=PVAccess.RW, monitor=True)),
            ctx=None, acc_context=acc)

    for dev in [x0]:
        sim.add_device(dev)
        sim.enable_device(dev)
        assert dev.is_connected()

    return sim, acc, simacc


def test_scan_rt(mock_sim_engine_with_pvs_simple):
    sim, acc, simacc = mock_sim_engine_with_pvs_simple

    logger.debug(f'{sim.channels=}')
    logger.debug(f'{sim.summarize()=}')
    logger.debug(f'{simacc.channels=}')
    logger.debug(f'{simacc.summarize()=}')

    h = sim.history["X0"]
    len_h = len(h)
    logger.debug(f'{sim.history["X0"]=}')

    simacc.start_scan_thread()

    time.sleep(5)
    assert len(h) == len_h + 5

    sim.write_channel('X0', 1.5)
    sim.process_events()
    time.sleep(0.1)

    assert sim.read_channel('X0') == 1.5

    t_start = time.perf_counter()
    r = sim.read_fresh(['X0'], timeout=1.1)
    dt = time.perf_counter() - t_start
    assert r == {'X0': 1.5}
    assert dt <= 1.0


def test_startup(mock_sim_engine_with_pvs):
    sim, acc, simacc = mock_sim_engine_with_pvs
    logger.debug(f'{sim.channels=}')
    logger.debug(f'{sim.summarize()=}')
    logger.debug(f'{simacc.channels=}')
    logger.debug(f'{simacc.summarize()=}')
    # with pytest.raises(DeviceEventTimeout):
    # assert sim.read_channel('X0') is None
    assert sim.read_channel('X0') == 0
    assert -0.2 < sim.read_channel('X0_RB') < 0.2
    assert -0.2 < sim.read_channel('OBJ0') < 0.2
    assert sim.channel_to_device['X0_RB'].state == DS.ENABLED
    assert sim.channel_to_device['OBJ0'].state == DS.ENABLED

    logger.debug(f'------------------------------------------0')
    simacc.write_channel('XECHOPV', 2.5)
    simacc.process_events()
    time.sleep(0.1)
    assert sim.channel_to_device['X0_RB'].state == DS.ENABLED
    assert sim.channel_to_device['OBJ0'].state == DS.ENABLED

    logger.debug(f'------------------------------------------1')
    simacc.write_channel('X0PV', 3.5)
    simacc.process_events()
    time.sleep(0.1)
    assert sim.channel_to_device['X0_RB'].state == DS.ENABLED
    assert sim.channel_to_device['OBJ0'].state == DS.ENABLED

    logger.debug(f'------------------------------------------2')
    sim.write_channel('X0', 1.5)
    sim.process_events()
    time.sleep(0.1)
    assert sim.channel_to_device['X0_RB'].state == DS.ENABLED
    assert sim.channel_to_device['OBJ0'].state == DS.ENABLED

    logger.debug(f'------------------------------------------3')
    with pytest.raises(DeviceWriteError):
        sim.write_channel('X0_RB', random.random())
    sim.process_events()
    assert simacc.channel_to_device['X0_RBPV'].state == DS.ERROR_WRITE
    assert sim.channel_to_device['X0_RB'].state == DS.ERROR_WRITE
    assert simacc.channel_to_device['OBJ0PV'].state == DS.ENABLED
    simacc.channel_to_device['X0_RBPV'].state = DS.ENABLED
    sim.channel_to_device['X0_RB'].state = DS.ENABLED
    assert sim.channel_to_device['X0_RB'].state == DS.ENABLED
    assert sim.channel_to_device['OBJ0'].state == DS.ENABLED
    time.sleep(0.1)

    logger.debug(f'------------------------------------------4')
    with pytest.raises(SecurityError):
        sim.write_channel('OBJ0', random.random())
    sim.process_events()
    time.sleep(0.1)
    assert simacc.channel_to_device['X0_RBPV'].state == DS.ENABLED
    assert simacc.channel_to_device['OBJ0PV'].state == DS.ENABLED
    assert sim.channel_to_device['X0_RB'].state == DS.ENABLED
    assert sim.channel_to_device['OBJ0'].state == DS.ERROR_WRITE
    sim.channel_to_device['OBJ0'].state = DS.ENABLED

    logger.debug(f'------------------------------------------5')
    sim.write_channel('X0', 2.5)
    sim.process_events()
    time.sleep(0.1)
    assert simacc.channel_to_device['X0_RBPV'].state == DS.ENABLED
    assert simacc.channel_to_device['OBJ0PV'].state == DS.ENABLED
    assert sim.channel_to_device['X0_RB'].state == DS.ENABLED
    assert sim.channel_to_device['OBJ0'].state == DS.ENABLED

    logger.debug(f'------------------------------------------6')
    sim.write_channel('X0', 4)
    logger.debug(f"{sim.read_channel('OBJ0')=}")
    assert sim.read_channel('OBJ0') > 0


def test_epics_simulated(f_acc_and_sim):
    acc, simacc = f_acc_and_sim
    t = 0.0

    def fixed_time():
        return t

    sim = SimulationEngine(SignalEngineOptions(time_function=fixed_time))
    sim.TRACE = True
    sim.TIME_TRACE = True

    pvo = PVOptions(name='X0PV', security=PVAccess.RW, low=-2.0, high=5.0, monitor=False)
    epics1 = ED(EDO(name='epics1', pv_to_ch_map={'X0PV': 'X0'}, connection='dummy',
                    pv_config=pvo),
                ctx=None, acc_context=acc)

    sim.add_device(epics1)
    sim.enable_device(epics1)
    epics1.is_connected()

    assert sim.latest_data == {'X0': 0.0}

    simacc.write_channel('X0PV', 2.5)
    time.sleep(0.1)
    assert sim.read_channel('X0') == 2.5
    assert sim.latest_data == {'X0': 2.5}

    proxy1 = ProxyDevice(
            ProxyDeviceOptions(name='proxy1',
                               channel_map={'TEST:PROXY:1': {'X0': TRIG.PROPAGATE}}))
    sim.add_device(proxy1)
    sim.enable_device(proxy1)

    assert sim.read_channel('TEST:PROXY:1') == 2.5
    assert sim.latest_data == {'X0': 2.5, 'TEST:PROXY:1': 2.5}

    proxy2 = ProxyDevice(
            ProxyDeviceOptions(name='proxy2',
                               channel_map={'TEST:PROXY:2': {'TEST:PROXY:1': TRIG.PROPAGATE}}))
    sim.add_device(proxy2)
    sim.enable_device(proxy2)
    assert sim.latest_data == {'X0': 2.5, 'TEST:PROXY:1': 2.5, 'TEST:PROXY:2': 2.5}

    proxy1.state = DS.ERROR_INTERNAL
    simacc.write_channel('X0PV', 3.5)
    time.sleep(0.1)
    assert sim.latest_data == {'X0': 3.5, 'TEST:PROXY:1': 2.5, 'TEST:PROXY:2': 2.5}

    assert proxy2.state == DS.ENABLED
    assert epics1.state == DS.ENABLED


def test_channels_ext_sioc(mock_sim_engine_with_pvs):
    sim, acc, simacc = mock_sim_engine_with_pvs
    logger.debug(f"{sim.devices_map=}")

    logger.debug(f"Connected: {[d.is_connected() for d in sim.devices_map.values()]}")
    logger.debug(f"{acc.cm.custom_callbacks_map=}")
    sim.write_channel('X0', 0)
    time.sleep(3)
    assert sim.read_channel('X0') == 0
    assert -0.2 < sim.read_channel('X0_RB') < 0.2

    sim.write_channel('X0', 4)

    logger.debug(f"{sim.read_channel('OBJ0')=}")
    assert sim.read_channel('OBJ0') > 0
