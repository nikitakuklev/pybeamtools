import random
import time

import pytest
from controls import Accelerator, AcceleratorOptions, ConnectionOptions, PVAccess, PVOptions
from sim.core import SignalEngineOptions, SimulationEngine
from pybeamtools.sim.softioc import SimpleIOC
from sim.pddevices import EPICSDevice, EPICSDeviceOptions, EchoDevice, EchoDeviceOptions, \
    ProxyDevice, \
    ProxyDeviceOptions, \
    SignalContext, TRIGSPEC


@pytest.fixture(scope='session', autouse=True)
def softioc():
    variables = ['X0', 'X1']
    objectives = ['OBJ0']
    test_variables = []
    sioc = SimpleIOC(variables, objectives, test_variables, noise=0.01)
    sioc.run_in_background()
    return sioc


@pytest.fixture
def accelerator():
    ao = AcceleratorOptions(connection_settings=ConnectionOptions(network='epics'))
    acc = Accelerator(options=ao)
    return acc


@pytest.fixture
def sim_engine(accelerator):
    acc = accelerator
    sim = SimulationEngine(SignalEngineOptions(time_function=time.time))
    ctx = SignalContext(se=sim)
    echo = EchoDevice(ctx, options=EchoDeviceOptions(name='echo', data={'TEST:ECHO:1': 5}))
    echo2 = EchoDevice(ctx, options=EchoDeviceOptions(name='echo2', data={'TEST:ECHO:2': 15}))
    echo3 = EchoDevice(ctx, options=EchoDeviceOptions(name='echo3', data={'TEST:ECHO:3': 25}))
    echo4 = EchoDevice(ctx, options=EchoDeviceOptions(name='echo4', data={'TEST:ECHO:4': 35}))

    var = 'TEST:GEN1'

    proxy1 = ProxyDevice(ctx, options=ProxyDeviceOptions(name='proxy1', channel_map={
        'TEST:PROXY:1': {var: TRIGSPEC.PROPAGATE}
    }))
    proxy2 = ProxyDevice(ctx, options=ProxyDeviceOptions(name='proxy2', channel_map={
        'TEST:PROXY:2': {'TEST:ECHO:2': TRIGSPEC.IGNORE}
    }))
    proxy3 = ProxyDevice(ctx, options=ProxyDeviceOptions(name='proxy3', channel_map={
        'TEST:PROXY:3': {'TEST:PROXY:1': TRIGSPEC.PROPAGATE}
    }))
    proxy4 = ProxyDevice(ctx, options=ProxyDeviceOptions(name='proxy4', channel_map={
        'TEST:PROXY:4': {'TEST:PROXY:1': TRIGSPEC.PROPAGATE}
    }))

    epics_x0ao = EPICSDevice(ctx, options=EPICSDeviceOptions(name='VARX0AO',
                                                             pv_config=PVOptions(name='X0:AO',
                                                                                 security=PVAccess.READONLY)),
                             acc_context=acc)
    epics_x0ai = EPICSDevice(ctx, options=EPICSDeviceOptions(name='VARX0AI',
                                                             pv_config=PVOptions(name='X0:AI',
                                                                                 security=PVAccess.READWRITE)),
                             acc_context=acc)
    epics_obj = EPICSDevice(ctx, options=EPICSDeviceOptions(name='OBJECTIVE',
                                                            pv_config=PVOptions(name='OBJ0',
                                                                                security=PVAccess.READONLY)),
                            acc_context=acc)


def test_startup(sim_engine):
    sim = sim_engine
    sim.write_channel('VARX0AI', random.random())
