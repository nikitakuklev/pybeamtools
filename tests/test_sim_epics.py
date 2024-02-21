import logging
import os
import random
import time

import pytest
from pybeamtools.controls.errors import SecurityError
from pybeamtools.controls import Accelerator, AcceleratorOptions, ConnectionOptions, PVAccess, \
    PVOptions
from pybeamtools.sim.softioc import SimpleIOC
from pybeamtools.sim.core import SignalEngineOptions, SignalEngine
from pybeamtools.sim.pddevices import DS, EPICSDevice, EPICSDeviceOptions, EchoDevice, \
    EchoDeviceOptions, \
    ProxyDevice, \
    ProxyDeviceOptions, SignalContext, TRIG
from pybeamtools.sim.templates import MockSetupPairDevice
from pybeamtools.sim.errors import DeviceEventTimeout

logger = logging.getLogger(__name__)


# @pytest.fixture(scope='session', autouse=False)
# def softioc():
#     variables = ['X0', 'X1']
#     objectives = ['OBJ0']
#     test_variables = []
#     sioc = SimpleIOC(variables, objectives, test_variables, noise=0.01)
#     sioc.run_in_background()
#     return sioc


@pytest.fixture
def accelerator():
    ao = AcceleratorOptions(connection_settings=ConnectionOptions(network='epics'))
    acc = Accelerator(options=ao)
    return acc


@pytest.fixture
def sim_engine_realtime() -> SignalEngine:
    sim = SignalEngine(SignalEngineOptions(time_function=time.time))
    sim.TRACE = True
    sim.TIME_TRACE = True
    return sim


# @pytest.fixture
# def sim_engine(accelerator, sim_engine_realtime):
#     acc = accelerator
#     sim = sim_engine_realtime
#     ctx = SignalContext(se=sim)
#     echo = EchoDevice(ctx, options=EchoDeviceOptions(name='echo', data={'TEST:ECHO:1': 5}))
#     echo2 = EchoDevice(ctx, options=EchoDeviceOptions(name='echo2', data={'TEST:ECHO:2': 15}))
#     echo3 = EchoDevice(ctx, options=EchoDeviceOptions(name='echo3', data={'TEST:ECHO:3': 25}))
#     echo4 = EchoDevice(ctx, options=EchoDeviceOptions(name='echo4', data={'TEST:ECHO:4': 35}))
#
#     def test_pair_mock_rate(sim_engine_realtime):
#     sim_engine = sim_engine_realtime
#     variables = ['X0', 'X1', 'X2']
#     readbacks = ['X0_RB', 'X1_RB', 'X2_RB']
#     objectives = ['OBJ0']
#
#     mg = MockSetupPairDevice(variables=variables, objectives=objectives, readbacks=readbacks,
#                              constants=[],
#                              extra_vars=[],
#                              evaluation_functions=None,
#                              evaluation_variables=None, noise=0.01,
#                              variable_pmodel_kwargs=dict(readback_update_rate=1.0,
#                                                         model='exponential',
#                                                         pmodel_kwargs={'decay_constant': 0.5},
#                                                         ),
#                              realtime=True)
#
#     sim = sim_engine
#     mg.create(sim)
#
#     sim.write_channel(variables[0], 3.0)
#     assert sim.latest_data[variables[0]] == 3.0
#     time.sleep(3)
#     sim.scan_until(time.time())
#
#     th = mg.make_scan_thread(sim)
#     th.start()
#
#     var = 'TEST:GEN1'
#
#     proxy1 = ProxyDevice(ctx, options=ProxyDeviceOptions(name='proxy1', channel_map={
#         'TEST:PROXY:1': {var: TRIGSPEC.PROPAGATE}
#     }))
#     proxy2 = ProxyDevice(ctx, options=ProxyDeviceOptions(name='proxy2', channel_map={
#         'TEST:PROXY:2': {'TEST:ECHO:2': TRIGSPEC.IGNORE}
#     }))
#     proxy3 = ProxyDevice(ctx, options=ProxyDeviceOptions(name='proxy3', channel_map={
#         'TEST:PROXY:3': {'TEST:PROXY:1': TRIGSPEC.PROPAGATE}
#     }))
#     proxy4 = ProxyDevice(ctx, options=ProxyDeviceOptions(name='proxy4', channel_map={
#         'TEST:PROXY:4': {'TEST:PROXY:1': TRIGSPEC.PROPAGATE}
#     }))
#
#     epics_x0ao = EPICSDevice(ctx, options=EPICSDeviceOptions(name='VARX0AO',
#                                                              pv_config=PVOptions(name='X0:AO',
#                                                                                  security=PVAccess.RO)),
#                              acc_context=acc)
#     epics_x0ai = EPICSDevice(ctx, options=EPICSDeviceOptions(name='VARX0AI',
#                                                              pv_config=PVOptions(name='X0:AI',
#                                                                                  security=PVAccess.RW)),
#                              acc_context=acc)
#     epics_obj = EPICSDevice(ctx, options=EPICSDeviceOptions(name='OBJECTIVE',
#                                                             pv_config=PVOptions(name='OBJ0',
#                                                                                 security=PVAccess.RO)),
#                             acc_context=acc)


def test_mock_startup(accelerator, sim_engine_realtime):
    acc = accelerator
    sim = sim_engine_realtime
    ctx = SignalContext(se=sim)

    variables = ['X0', 'X1', 'X2']
    readbacks = ['X0_RB', 'X1_RB', 'X2_RB']
    objectives = ['OBJ0']

    pmodel_kwargs = dict(readback_update_rate=1.0,
                        model='exponential',
                        pmodel_kwargs={'decay_constant': 0.5},
                        )
    mg = MockSetupPairDevice(variables=variables,
                             objectives=objectives,
                             readbacks=readbacks,
                             noise=0.01,
                             variable_pmodel_kwargs=pmodel_kwargs,
                             realtime=True)
    mg.create(sim)

    sim.write_channel(variables[0], 3.0)

    var = 'TEST:GEN1'


@pytest.fixture(autouse=False, scope='class')
def simple_soft_ioc():
    os.environ['EPICS_CA_AUTO_ADDR_LIST'] = 'no'
    os.environ['EPICS_CA_ADDR_LIST'] = '127.0.0.1'

    variables = ['X0', 'X1']
    objectives = ['OBJ0']
    test_variables = []

    from caproto.sync import repeater
    repeater.spawn_repeater()
    time.sleep(0.5)

    sioc = SimpleIOC(variables, objectives, test_variables, noise=0.05)
    sioc.setup()
    sioc.run_in_background()
    logger.debug(f'Soft IOC started')
    time.sleep(1.0)
    return sioc


@pytest.fixture(autouse=False)
def sim_engine_with_pvs(sim_engine_realtime) -> tuple[SignalEngine, Accelerator]:
    sim = sim_engine_realtime
    ao = AcceleratorOptions(connection_settings=ConnectionOptions(network='epics'))
    acc = Accelerator(options=ao, ctx=None)

    x0rb = EPICSDevice(EPICSDeviceOptions(name='X0_RB',
                                          pv_config=PVOptions(name='X0_RB', low=0.0, high=7.0,
                                                              security=PVAccess.RW, monitor=True)),
                       ctx=None, acc_context=acc)
    # time.sleep(2)
    # assert x0rb.is_connected()

    x0 = EPICSDevice(EPICSDeviceOptions(name='X0',
                                        pv_config=PVOptions(name='X0', low=0.0, high=7.0,
                                                            security=PVAccess.RW, monitor=True)),
                     ctx=None, acc_context=acc)

    # time.sleep(2)
    # assert x0.is_connected()

    obj0 = EPICSDevice(EPICSDeviceOptions(name='OBJ0',
                                          pv_config=PVOptions(name='OBJ0',
                                                              security=PVAccess.RO, monitor=True)),
                       ctx=None, acc_context=acc)

    time.sleep(4)
    # assert x0.is_connected()

    for dev in [x0rb, x0, obj0]:
        assert dev.is_connected()
    for dev in [x0rb, x0, obj0]:
        sim.add_device(dev)
    for dev in [x0rb, x0, obj0]:
        sim.enable_device(dev)
    time.sleep(1)
    return sim, acc


def test_epics_direct():
    os.environ['EPICS_CA_AUTO_ADDR_LIST'] = 'no'
    os.environ['EPICS_CA_ADDR_LIST'] = '127.0.0.1'

    from caproto.threading.client import Context
    ctx = Context()
    x0 = ctx.get_pvs('X0')[0]
    x0_rb = ctx.get_pvs('X0_RB')[0]
    time.sleep(1)
    readx0 = x0.read()
    logger.info(f'{readx0=}')
    assert readx0.data[0] == 0
    x0rb = x0_rb.read()
    assert -0.2 < x0rb.data[0] < 0.2
    logger.info(f'OK')


def test_bad_startup(sim_engine_with_pvs):
    sim = sim_engine_with_pvs
    # with pytest.raises(DeviceEventTimeout):
    assert sim.read_channel('X0') is None

    with pytest.raises(DeviceEventTimeout):
        sim.write_channel('X0', random.random())

    with pytest.raises(SecurityError):
        sim.write_channel('X0_RB', random.random())


def test_channels_ext_sioc(sim_engine_with_pvs):
    sim, acc = sim_engine_with_pvs
    logger.debug(f"{sim.devices_map=}")

    logger.debug(f"Connected: {[d.is_connected() for d in sim.devices_map.values()]}")
    logger.debug(f"{acc.cm.custom_callbacks_map=}")
    sim.write_channel('X0', 0)
    time.sleep(3)
    assert sim.read_channel('X0') == 0
    assert -0.2 < sim.read_channel('X0_RB') < 0.2

    sim.write_channel('X0', 4)

    # sim.write_channel('X0', 6)

    logger.debug(f"{sim.read_channel('OBJ0')=}")
    assert sim.read_channel('OBJ0') > 0


def test_channels(simple_soft_ioc, sim_engine_with_pvs):
    sim = sim_engine_with_pvs

    time.sleep(10)

    assert sim.read_channel('X0') == 0

# def test_connect():
#     x0 = EPICSDevice(EPICSDeviceOptions(name='X0', pv_config=PVOptions(name='X0',
#                                                                        security=PVAccess.RO)),
#                      ctx=ctx, acc_context=acc)
#
#     proxy1 = ProxyDevice(ctx, options=ProxyDeviceOptions(name='proxy1', channel_map={
#         'TEST:PROXY:1': {var: TRIGSPEC.PROPAGATE}
#     }))
#     proxy2 = ProxyDevice(ctx, options=ProxyDeviceOptions(name='proxy2', channel_map={
#         'TEST:PROXY:2': {'TEST:ECHO:2': TRIGSPEC.IGNORE}
#     }))
#     proxy3 = ProxyDevice(ctx, options=ProxyDeviceOptions(name='proxy3', channel_map={
#         'TEST:PROXY:3': {'TEST:PROXY:1': TRIGSPEC.PROPAGATE}
#     }))
#     proxy4 = ProxyDevice(ctx, options=ProxyDeviceOptions(name='proxy4', channel_map={
#         'TEST:PROXY:4': {'TEST:PROXY:1': TRIGSPEC.PROPAGATE}
#     }))
#
#     epics_x0ai = EPICSDevice(ctx, options=EPICSDeviceOptions(name='VARX0AI',
#                                                              pv_config=PVOptions(name='X0:AI',
#                                                                                  security=PVAccess.RW)),
#                              acc_context=acc)
#     epics_obj = EPICSDevice(ctx, options=EPICSDeviceOptions(name='OBJECTIVE',
#                                                             pv_config=PVOptions(name='OBJ0',
#                                                                                 security=PVAccess.RO)),
#                             acc_context=acc)
