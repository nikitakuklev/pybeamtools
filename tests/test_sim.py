import collections
import logging
import time

import numpy as np
import pytest
from pybeamtools.sim.core import SimulationEngine, ChannelMap, ChannelMapper, SimException
from pybeamtools.sim.devices import RealisticMagnet


class SimTest:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name


@pytest.fixture
def sim_engine() -> SimulationEngine:
    sim = SimulationEngine()

    # mag = RealisticMagnet(name='magneto', value=0, low=-2, high=2, noise=0.1, resolution=None, model='instant')
    # sim.add_device(mag, period=5.0)
    #
    # def eval_mag(device, output):
    #     return device.read()
    #
    # m = ChannelMap(device=mag, output='TEST:CHANNEL', f=eval_mag)
    # chm = ChannelMapper(maps=[m])
    # sim.add_mapper(chm)

    return sim


def test_device_add_dup(sim_engine):
    mag = RealisticMagnet(name='mag1', value=0, low=-2, high=2, noise=0.1, resolution=None, model='instant')
    sim_engine.add_device(mag, period=5.0)
    mag2 = RealisticMagnet(name='mag1', value=0, low=-2, high=2, noise=0.1, resolution=None, model='instant')
    with pytest.raises(SimException):
        sim_engine.add_device(mag2, period=5.0)


def test_device_add(sim_engine):
    mag = RealisticMagnet(name='mag1', value=0)
    sim_engine.add_device(mag, period=5.0)
    mag2 = RealisticMagnet(name='mag2', value=0)
    sim_engine.add_device(mag2, period=5.0)
    assert list(sim_engine.devices) == ['mag1', 'mag2']
    assert sim_engine.devices['mag1'] == mag

    def eval_mag(device, output):
        return device.read()

    mag3 = RealisticMagnet(name='mag3', value=0)
    m = ChannelMap(device=mag3, output='MAG3:CHANNEL', read_fun=eval_mag)
    chm = ChannelMapper(maps=[m])
    with pytest.raises(AssertionError):
        sim_engine.add_mapper(chm)

    m = ChannelMap(device=mag2, output='MAG2:CHANNEL', read_fun=eval_mag)
    chm = ChannelMapper(maps=[m])
    sim_engine.add_mapper(chm)

    assert sim_engine.channels == ['MAG2:CHANNEL']


def test_device_set(sim_engine: SimulationEngine):
    mag = RealisticMagnet(name='mag1', value=0.5)
    sim_engine.add_device(mag, period=5.0)
    mag2 = RealisticMagnet(name='mag2', value=0.5)
    sim_engine.add_device(mag2, period=5.0)
    assert list(sim_engine.devices) == ['mag1', 'mag2']
    assert sim_engine.devices['mag1'] == mag
    logger = logging.getLogger(__name__)

    def read_fun(device, output):
        return device.read()

    def write_fun(device, output, value):
        logger.debug(f'write_fun: {device=} {output=} {value=}')
        return device.write(value)

    m = ChannelMap(device=mag2, output='MAG2:CHANNEL',
                   read_fun=read_fun, write_fun=write_fun)
    chm = ChannelMapper(maps=[m])
    sim_engine.add_mapper(chm)

    assert sim_engine.device_channels == {'mag2': ['MAG2:CHANNEL']}

    with pytest.raises(AssertionError):
        sim_engine.write_channel('MAG2:CHANNELBAD', 4.5)
    sim_engine.write_channel('MAG2:CHANNEL', 2.0)
    assert mag2.setpoint == 2.0
    assert sim_engine.read_channel('MAG2:CHANNEL') == 2.0
    assert mag2.value == 2.0
    assert mag2.raw_value == 2.0


def test_running_logic(sim_engine: SimulationEngine):
    mag = RealisticMagnet(name='mag1', value=0.5)
    sim_engine.add_device(mag, period=0.05)
    mag2 = RealisticMagnet(name='mag2', value=1.5)
    sim_engine.add_device(mag2, period=0.05)

    def read_fun(device, output):
        return device.read()

    def write_fun(device, output, value):
        return device.write(value)

    m = ChannelMap(device=mag, output='MAG1:CHANNEL',
                   read_fun=read_fun, write_fun=write_fun)
    m2 = ChannelMap(device=mag2, output='MAG2:CHANNEL',
                   read_fun=read_fun, write_fun=write_fun)
    chm = ChannelMapper(maps=[m, m2])
    sim_engine.add_mapper(chm)

    t1 = time.time()
    sim_engine.start_update_thread()
    delta = time.time() - t1
    assert delta < 0.1
    assert sim_engine.poll_thread.is_alive()
    assert mag2.raw_value == mag2.value == 1.5

    with pytest.raises(SimException):
        sim_engine.start_update_thread()

    time.sleep(0.1)

    # Check callbacks
    last_results_map = {}
    circular_buffers_map = {}
    circular_buffers_map['MAG1:CHANNEL'] = collections.deque(maxlen=50)
    def callback(sub, response: np.ndarray):
        name = sub.name
        circular_buffers_map[name].append(response)
        last_results_map[name] = response

    cb1 = callback
    subscription1 = sim_engine.subscribe_channel('MAG1:CHANNEL')
    subscription1.add_callback(cb1)
    assert subscription1.callbacks == [cb1]
    time.sleep(0.06)

    assert last_results_map['MAG1:CHANNEL'] == 0.5
    time.sleep(2.6)
    assert len(circular_buffers_map['MAG1:CHANNEL']) == 50

    sim_engine.write_channel('MAG1:CHANNEL', 2.3)
    time.sleep(0.06)
    assert last_results_map['MAG1:CHANNEL'] == 2.3

    t1 = time.time()
    sim_engine.stop_update_thread()
    delta = time.time() - t1
    assert delta < 0.1

    with pytest.raises(SimException):
        sim_engine.stop_update_thread()
