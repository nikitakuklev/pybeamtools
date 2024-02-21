import logging
import time

import numpy as np
import pytest
from pybeamtools.sim.core import SignalEngineOptions, SignalEngine
from pybeamtools.sim.templates import MockSetupPairDevice

t = 0.0

logger = logging.getLogger(__name__)


def fixed_time():
    return t


@pytest.fixture
def sim_engine() -> SignalEngine:
    sim = SignalEngine(SignalEngineOptions(time_function=fixed_time))
    sim.TRACE = True
    sim.TIME_TRACE = True
    return sim


@pytest.fixture
def sim_engine_realtime() -> SignalEngine:
    sim = SignalEngine(SignalEngineOptions(time_function=time.time))
    sim.TRACE = True
    sim.TIME_TRACE = True
    return sim


def test_pair_mock(sim_engine):
    variables = ['X0', 'X1', 'X2']
    readbacks = ['XO_RB', 'X1_RB', 'X2_RB']
    objectives = ['OBJ0']

    mg = MockSetupPairDevice(variables=variables,
                             objectives=objectives,
                             readbacks=readbacks,
                             noise=0.01)

    sim = sim_engine
    mg.create(sim)

    sim.write_channel(variables[0], 3.0)
    assert sim.latest_data[variables[0]] == 3.0
    sim.process_events()
    obj0 = sim.latest_data[objectives[0]]
    assert obj0 == (np.linalg.norm(np.array([2.8, -0.2, -0.2])[None, :],
                                   axis=1, keepdims=True) ** 2)[0, 0]


def test_pair_mock_rate_1(sim_engine_realtime):
    sim = sim_engine_realtime
    variables = ['X0', 'X1', 'X2']
    readbacks = ['X0_RB', 'X1_RB', 'X2_RB']
    objectives = ['OBJ0']
    scan_period_rb = 1.0
    scan_period_obj = 1.5

    mg = MockSetupPairDevice(variables=variables,
                             objectives=objectives,
                             readbacks=readbacks,
                             noise=0.01,
                             variable_pmodel_kwargs=dict(readback_update_rate=1.0,
                                                        model='exponential',
                                                        pmodel_kwargs={'decay_constant': 0.5},
                                                        ),
                             scan_period_rb=scan_period_rb,
                             scan_period_obj=scan_period_obj,
                             realtime=True)

    mg.create(sim)

    exp_var = {variables[0]: 1, variables[1]: 1, variables[2]: 1}
    exp_rb = {readbacks[0]: 1, readbacks[1]: 1, readbacks[2]: 1}

    for var in variables:
        assert sim.history[var].size == exp_var[var]
    for rb in readbacks:
        assert sim.history[rb].size == exp_rb[rb]
    for obj in objectives:
        assert sim.history[obj].size == 1

    sim.write_channel(variables[0], 3.0)
    sim.process_events()
    assert sim.latest_data[variables[0]] == 3.0

    exp_var = {variables[0]: 2, variables[1]: 1, variables[2]: 1}
    exp_rb = {readbacks[0]: 2, readbacks[1]: 1, readbacks[2]: 1}

    for var in variables:
        assert sim.history[var].size == exp_var[var]
    for rb in readbacks:
        assert sim.history[rb].size == exp_rb[rb]
    for obj in objectives:
        assert sim.history[obj].size == 2

    time.sleep(2)

    sim.start_scan_thread()
    ts = 3.3
    time.sleep(ts)

    exp_var = {variables[0]: 2, variables[1]: 1, variables[2]: 1}
    exp_rb = {readbacks[0]: 2, readbacks[1]: 1, readbacks[2]: 1}

    for var in variables:
        assert sim.history[var].size == exp_var[var]
    for rb in readbacks:
        assert sim.history[rb].size == exp_rb[rb] + ts // scan_period_rb + 1
    for obj in objectives:
        ans = 2 + (ts // scan_period_obj) + (ts // scan_period_rb + 1)*len(variables) + 1
        assert sim.history[obj].size == ans

    time.sleep(1)

    for i in range(5):
        sim.write_channel(variables[0], i)
        time.sleep(2)

    for el in readbacks:
        h = sim.history[el]
        logger.info(h.times_to_numpy())
        logger.info(h.values_to_numpy())


def test_pair_mock_rate_2(sim_engine_realtime):
    sim = sim_engine_realtime
    variables = ['X0', 'X1', 'X2']
    readbacks = ['X0_RB', 'X1_RB', 'X2_RB']
    objectives = ['OBJ0']
    scan_period_rb = 1.0
    scan_period_obj = 1.5

    mg = MockSetupPairDevice(variables=variables,
                             objectives=objectives,
                             readbacks=readbacks,
                             noise=0.01,
                             variable_pmodel_kwargs=dict(readback_update_rate=2.0,
                                                        model='exponential',
                                                        pmodel_kwargs={'decay_constant': 0.5},
                                                        ),
                             scan_period_rb=scan_period_rb,
                             scan_period_obj=scan_period_obj,
                             realtime=True)

    mg.create(sim)

    exp_var = {variables[0]: 1, variables[1]: 1, variables[2]: 1}
    exp_rb = {readbacks[0]: 1, readbacks[1]: 1, readbacks[2]: 1}

    for var in variables:
        assert sim.history[var].size == exp_var[var]
    for rb in readbacks:
        assert sim.history[rb].size == exp_rb[rb]
    for obj in objectives:
        assert sim.history[obj].size == 1

    time.sleep(3)

    sim.start_scan_thread()
    ts = 6.3
    time.sleep(ts)

    exp_var = {variables[0]: 1, variables[1]: 1, variables[2]: 1}
    exp_rb = {readbacks[0]: 1, readbacks[1]: 1, readbacks[2]: 1}

    for var in variables:
        assert sim.history[var].size == exp_var[var]
    for rb in readbacks:
        assert sim.history[rb].size == exp_rb[rb] + ts // 2.0 + 1
    for obj in objectives:
        ans = 2 + (ts // scan_period_obj) + (ts // 2.0 + 1)*len(variables) + 1
        assert sim.history[obj].size == ans
