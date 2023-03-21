import numpy as np
import pytest
from sim.devices import RealisticModel, RealisticModelOptions


def test_realistic():
    opt = RealisticModelOptions(name='test1', value=0.5, model='instant')
    t = 0.0
    model = RealisticModel(opt, t)

    assert model.setpoint == model.raw_value == 0.5

    model.write(5.5, t)
    model.update(t)
    assert model.setpoint == model.raw_value == 5.5

    t += 10
    model.update(t)
    assert model._time_last_call == model.last_known_t == 10.0
    assert model.time_last_write == 0.0


def test_realistic_models():
    opt = RealisticModelOptions(name='test1', value=0.5, model='exponential',
                                readback_update_rate=1.0)
    t = 0.0
    model = RealisticModel(opt, t)

    t += 1.0
    model.update(t)
    model.write(5.0, t)
    assert model._time_last_call == model.time_last_write == model.last_known_t == 1.0
    assert model.setpoint == 5.0
    model.update(t)
    assert model.setpoint == 5.0
    assert model.raw_value == model.value == 0.5
    assert model.time_last_update == 1.0

    t += 1.0
    model.update(t)
    assert 0.5 < model.read(t) < 5.0
    assert model.read(t) == 5.0 + -4.5 * np.exp(-2.0 * 1.0)

    t += 2.0
    model.update(t)
    assert 0.5 < model.read(t) < 5.0
    assert model.read(t) == 5.0 + -4.5 * np.exp(-2.0 * 3.0)


def test_realistic_models_ud():
    opt = RealisticModelOptions(name='test1', value=0.5, model='underdamped',
                                readback_update_rate=1.0)
    t = 0.0
    model = RealisticModel(opt, t)

    t += 1.0
    model.update(t)
    model.write(5.0, t)
    assert model._time_last_call == model.time_last_write == model.last_known_t == 1.0
    assert model.setpoint == 5.0
    model.update(t)
    assert model.setpoint == 5.0
    assert model.raw_value == model.value == 0.5
    assert model.time_last_update == 1.0

    for i in range(30):
        t += 0.1
        model.update(t)
        assert 0.5 < model.read(t) < 9.5
        print(t, model.read(t))


def test_realistic_time():
    opt = RealisticModelOptions(name='test1', value=0.5, model='instant',
                                readback_update_rate=1.0)
    t = 0.0
    model = RealisticModel(opt, t)
    model.update(0.5)
    model.write(5.5, 0.5)
    assert model._time_last_call == model.time_last_write == model.last_known_t == 0.5

    with pytest.raises(ValueError):
        model.write(5.4, 0.4)
    assert model.setpoint == 5.5


def test_realistic_readback():
    opt = RealisticModelOptions(name='test1', value=0.5, model='instant',
                                readback_update_rate=1.0)
    t = 0.0
    model = RealisticModel(opt, t)

    t += 1.0
    events = model.advance_time(t)
    assert len(events) == 1
    assert events == [(1.0, 0.5)]

    t += 2.0
    events = model.advance_time(t)
    assert len(events) == 2
    assert events == [(2.0, 0.5), (3.0, 0.5)]

    ##
    opt = RealisticModelOptions(name='test1', value=0.5, model='instant')
    t = 0.0
    model = RealisticModel(opt, t)
    t += 2.0
    events = model.advance_time(t)
    assert len(events) == 0

    ##
    opt = RealisticModelOptions(name='test1', value=0.5, model='instant',
                                readback_update_rate=1.0)
    t = 0.0
    model = RealisticModel(opt, t)
    t += 2.0
    events = model.advance_time(t)
    assert len(events) == 2
    assert events == [(1.0, 0.5), (2.0, 0.5)]
    model.write(5.5, t)

    t += 2.0
    events = model.advance_time(t)
    assert len(events) == 2
    assert events == [(3.0, 5.5), (4.0, 5.5)]
