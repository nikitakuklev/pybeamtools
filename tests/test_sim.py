import logging
import queue
import threading
import time

import numpy as np
import pytest

from pybeamtools.sim.core import SignalEngineOptions, SimulationEngine
from pybeamtools.sim.devices import RealisticModel, RealisticModelOptions
from pybeamtools.sim.errors import DeviceDependencyError, DeviceError, ReadTimeoutError, \
    SimulationError, \
    WriteTimeoutError
from pybeamtools.sim.pddevices import CounterDevice, CounterDeviceOptions, DS, EchoDevice, \
    EchoDeviceOptions, ModelDevice, ModelDeviceOptions, ModelPairDevice, ModelPairDeviceOptions, \
    ProxyDevice, ProxyDeviceOptions, SignalContext, TRIG

ED = EchoDevice
EDO = EchoDeviceOptions
PD = ProxyDevice
PDO = ProxyDeviceOptions


def sd(d):
    status_dict = {'disable': 0, 'enable': 0, 'read': 0, 'read_now': 0, 'scan': 0, 'update': 0,
                   'write': 0
                   }
    status_dict.update(d)
    return status_dict


class SimTest:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name


t = 0.0


def fixed_time():
    return t


@pytest.fixture
def sim_engine() -> SimulationEngine:
    sim = SimulationEngine(SignalEngineOptions(time_function=fixed_time))
    sim.TRACE = True
    sim.TIME_TRACE = True
    return sim


@pytest.fixture
def sim_engine_realtime() -> SimulationEngine:
    sim = SimulationEngine(SignalEngineOptions(time_function=time.time))
    sim.TRACE = True
    sim.TIME_TRACE = True
    return sim


@pytest.fixture
def sim_engine_with_devices(sim_engine) -> SimulationEngine:
    echo1 = ED(EDO(name='echo1', data={'TEST:ECHO:1': 5}))
    echo2 = ED(EDO(name='echo2', data={'TEST:ECHO:2': 15}))
    echo3 = ED(EDO(name='echo3', data={'TEST:ECHO:3': 25}))
    echo4 = ED(EDO(name='echo4', data={'TEST:ECHO:4': 35}))

    proxy1 = PD(PDO(name='proxy1', channel_map={
        'TEST:PROXY:1': {'TEST:ECHO:1': TRIG.PROPAGATE}
    }))
    proxy2 = PD(PDO(name='proxy2', channel_map={
        'TEST:PROXY:2': {'TEST:ECHO:2': TRIG.IGNORE}
    }))
    proxy3 = PD(PDO(name='proxy3', channel_map={
        'TEST:PROXY:3': {'TEST:PROXY:1': TRIG.PROPAGATE}
    }))
    proxy4 = PD(PDO(name='proxy4', channel_map={
        'TEST:PROXY:4': {'TEST:PROXY:1': TRIG.PROPAGATE}
    }))
    for dev in [echo1, echo2, echo3, echo4, proxy1, proxy2, proxy3, proxy4]:
        sim_engine.add_device(dev)

    return sim_engine


def test_device_add(sim_engine):
    ctx = SignalContext(se=sim_engine)
    echo1 = ED(EDO(name='echo1', data={'TEST:ECHO:1': 5.0}))
    echo1dup = ED(EDO(name='echo1', data={'TEST:ECHO:1': 5.0}))
    echo2 = ED(EDO(name='echo2', data={'TEST:ECHO:2': 15.0}))

    ctx.add_device(echo1)
    ctx.add_device(echo2)
    with pytest.raises(SimulationError):
        ctx.add_device(echo1dup)
    with pytest.raises(SimulationError):
        ctx.add_device(echo2)

    assert sim_engine.devices_list == [echo1, echo2]
    assert sim_engine.devices_map['echo1'] is echo1
    assert echo1.state == echo2.state == DS.CREATED

    with pytest.raises(DeviceError):
        sim_engine.read_channel('TEST:ECHO:1')


def test_device_read(sim_engine: SimulationEngine):
    ctx = SignalContext(se=sim_engine)
    echo1 = ED(EDO(name='echo1', data={'TEST:ECHO:1': 5.0}))
    echo2 = ED(EDO(name='echo2', data={'TEST:ECHO:2': 15.0}))

    ctx.add_device(echo1)
    ctx.add_device(echo2)

    with pytest.raises(DeviceError):
        sim_engine.read_channel('TEST:ECHO:1')
    assert sim_engine.latest_data['TEST:ECHO:1'] is None
    sim_engine.enable_device(echo1)
    assert echo1.state == DS.ENABLED
    assert echo1.stats == sd({'update': 1, 'enable': 1})
    assert sim_engine.latest_data['TEST:ECHO:1'] == 5.0
    assert sim_engine.read_channel('TEST:ECHO:1') == 5.0
    assert echo1.stats == sd({'update': 1, 'read': 1, 'enable': 1})


def test_device_read_now(sim_engine: SimulationEngine):
    echo1 = ED(EDO(name='echo1', data={'TEST:ECHO:1': 5.0}))
    echo2 = ED(EDO(name='echo2', data={'TEST:ECHO:2': 15.0}))
    sim_engine.add_device(echo1)
    sim_engine.add_device(echo2)

    with pytest.raises(DeviceError):
        sim_engine.read_channel_now('TEST:ECHO:1')
    assert sim_engine.latest_data['TEST:ECHO:1'] is None
    sim_engine.enable_device(echo1)
    assert echo1.state == DS.ENABLED
    assert echo1.stats == sd({'update': 1, 'enable': 1})
    assert sim_engine.latest_data['TEST:ECHO:1'] == 5.0
    assert sim_engine.read_channel_now('TEST:ECHO:1') == 5.0
    assert echo1.stats == sd({'update': 1, 'enable': 1, 'read_now': 1})


def test_device_write(sim_engine: SimulationEngine):
    ctx = SignalContext(se=sim_engine)
    echo1 = ED(EDO(name='echo1', data={'TEST:ECHO:1': 5.0}))
    ctx.add_device(echo1)

    with pytest.raises(DeviceError):
        sim_engine.write_channel('TEST:ECHO:1', 0.0)
    assert sim_engine.latest_data['TEST:ECHO:1'] is None

    sim_engine.enable_device(echo1)
    sim_engine.write_channel('TEST:ECHO:1', 4.0)
    assert echo1.stats == sd({'update': 1, 'write': 1, 'enable': 1})
    assert sim_engine.latest_data['TEST:ECHO:1'] == 4.0
    assert sim_engine.read_channel('TEST:ECHO:1') == 4.0
    assert echo1.stats == sd({'update': 1, 'read': 1, 'write': 1, 'enable': 1})


def test_device_scan(sim_engine: SimulationEngine):
    t_local = 0.0

    def local_time():
        return t_local

    sim_engine.time_fun = local_time
    ctx = SignalContext(se=sim_engine)
    echo1 = ED(EDO(name='echo1', data={'TEST:ECHO:1': 5.0},
                   scan_period=2.0))
    ctx.add_device(echo1)
    assert sim_engine.latest_data['TEST:ECHO:1'] is None
    assert echo1.stats == sd({})
    print(sim_engine.next_scan_time)
    assert sim_engine.next_scan_time['echo1'] == 2.0

    t_local = 5.5
    sim_engine.scan_until(5.5)
    assert echo1.stats == sd({})

    sim_engine.enable_device(echo1)
    assert sim_engine.latest_data['TEST:ECHO:1'] == 5.0
    assert echo1.stats == sd({'update': 1, 'enable': 1})

    t_local = 8.5
    sim_engine.scan_until(8.5)
    assert echo1.stats == sd({'update': 1, 'enable': 1, 'scan': 1})

    t_local = 12
    sim_engine.scan_until(t_local)
    assert echo1.stats == sd({'update': 1, 'enable': 1, 'scan': 3})

    sim_engine.write_channel('TEST:ECHO:1', 4.0)
    assert echo1.stats == sd({'update': 1, 'enable': 1, 'write': 1, 'scan': 3})
    assert sim_engine.latest_data['TEST:ECHO:1'] == 4.0
    assert sim_engine.read_channel('TEST:ECHO:1') == 4.0


# TODO: scan with no return

def test_ordering(sim_engine: SimulationEngine):
    echo1 = ED(EDO(name='echo1', data={'TEST:ECHO:1': 5.0}))
    sim_engine.add_device(echo1)
    sim_engine.enable_device(echo1)
    assert sim_engine.read_channel('TEST:ECHO:1') == 5.0
    for i in range(10):
        sim_engine.write_channel('TEST:ECHO:1', i)
        assert sim_engine.read_channel('TEST:ECHO:1') == i


def test_adv_read(sim_engine: SimulationEngine):
    t_local = 0.0

    def local_time():
        return t_local

    sim_engine.time_fun = local_time
    ctx = SignalContext(se=sim_engine)
    echo1 = CounterDevice(CounterDeviceOptions(name='echo1', data={'TEST:ECHO:1': 5.0},
                                               scan_period=2.0))
    ctx.add_device(echo1)
    sim_engine.enable_device(echo1)

    def time_thread():
        nonlocal t_local
        for i in range(10):
            t_local += 1
            sim_engine.scan_until(t_local)

    th = threading.Thread(target=time_thread, name='time_thread')
    th.daemon = True
    th.start()
    th.join()

    logger = logging.getLogger(__name__)
    logger.info(f"{sim_engine.history['TEST:ECHO:1']=}")

    h = sim_engine.history['TEST:ECHO:1']
    assert h.size == 6
    assert np.array_equal(h.values_to_numpy(), np.array([5.0, 5.0, 6.0, 7.0, 8.0, 9.0]))
    assert np.array_equal(h.times_to_numpy(), np.array([0.0, 2.0, 4.0, 6.0, 8.0, 10.0]))

    assert [x.time for x in h.ts(4.0, 8.0)] == [4.0, 6.0, 8.0]
    assert [x.time for x in h.ts(4.0, 8.0, mid_start=3)] == [6.0, 8.0]

    channels = ['TEST:ECHO:1']
    data = sim_engine.read_fresh(channels, now=5.0, reduce=None, max_readings=100)
    assert len(data) == 1
    assert list(data[channels[0]]) == [7.0, 8.0, 9.0]

    data = sim_engine.read_fresh(channels, now=5.0, reduce=None, max_readings=2)
    assert list(data[channels[0]]) == [8.0, 9.0]

    data = sim_engine.read_fresh(channels, now=5.0, reduce=None)
    assert list(data[channels[0]]) == [9.0]

    with pytest.raises(ReadTimeoutError):
        data = sim_engine.read_fresh(channels, now=10.1, reduce=None)

    with pytest.raises(ReadTimeoutError):
        data = sim_engine.read_fresh(channels, now=5.0, reduce=None, use_buffer=False)

    with pytest.raises(ReadTimeoutError):
        data = sim_engine.read_fresh(channels, now=10.1, reduce=None)

    def time_thread():
        nonlocal t_local
        for i in range(5):
            t_local += 1
            sim_engine.scan_until(t_local)

    th = threading.Thread(target=time_thread, name='time_thread')
    th.daemon = True
    th.start()

    data = sim_engine.read_fresh(channels, now=5.0, reduce=None, use_buffer=False,
                                 min_readings=2, max_readings=100)
    th.join()
    assert list(data[channels[0]]) == [10.0, 11.0]


def test_adv_write(sim_engine: SimulationEngine):
    t_local = 0.0

    def local_time():
        return t_local

    sim_engine.time_fun = local_time
    ctx = SignalContext(se=sim_engine)
    echo1 = ED(EDO(name='echo1',
                   data={'TEST:ECHO:1': 5.0},
                   scan_period=2.0))
    mag1model = RealisticModel(RealisticModelOptions(name='mag1model',
                                                     value=0.5,
                                                     readback_update_rate=0.0), t_local)
    mag1 = ModelPairDevice(ModelPairDeviceOptions(name='MAG1',
                                                  variable_name='MAG1',
                                                  scan_period=2.0,
                                                  readback_name='MAG1RB',
                                                  device=mag1model))
    ctx.add_device(mag1)
    ctx.add_device(echo1)
    sim_engine.enable_device(mag1)
    sim_engine.enable_device(echo1)

    def start_time_scan() -> threading.Thread:
        def time_thread():
            nonlocal t_local
            for i in range(10):
                t_local += 1
                sim_engine.scan_until(t_local)
                time.sleep(0.1)

        th = threading.Thread(target=time_thread, name='time_thread')
        th.daemon = True
        th.start()
        return th

    start_time_scan().join()

    h = sim_engine.history['TEST:ECHO:1']
    assert h.size == 6
    assert np.array_equal(h.values_to_numpy(), np.array([5.0, 5.0, 5.0, 5.0, 5.0, 5.0]))
    assert np.array_equal(h.times_to_numpy(), np.array([0.0, 2.0, 4.0, 6.0, 8.0, 10.0]))

    h = sim_engine.history['MAG1']
    assert h.size == 1
    assert np.array_equal(h.values_to_numpy(), np.array([0.5]))
    assert np.array_equal(h.times_to_numpy(), np.array([0.0]))

    h = sim_engine.history['MAG1RB']
    assert h.size == 6
    assert np.array_equal(h.values_to_numpy(), np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5]))
    assert np.array_equal(h.times_to_numpy(), np.array([0.0, 2.0, 4.0, 6.0, 8.0, 10.0]))

    rb_dict = {'MAG1': 'MAG1RB', 'MAG2': 'MAG2RB'}
    atol_map = {}
    rtol_map = {}
    wav = sim_engine.write_and_verify

    assert sim_engine.read_fresh(['MAG1RB'], timeout=0.0, now=sim_engine.time()) == {'MAG1RB': 0.5}
    w, rb = wav({'MAG1': 0.5}, rb_dict, 5.0, atol_map=atol_map,
                rtol_map=rtol_map,
                readback_timeout=1.0)
    assert w == {'MAG1': None}
    assert rb == {'MAG1': 0.5}

    w, rb = wav({'MAG1': 3.5}, rb_dict, 5.0, atol_map=atol_map,
                rtol_map=rtol_map,
                readback_timeout=1.0)
    assert rb == {'MAG1': 3.5}

    mag2model = RealisticModel(RealisticModelOptions(name='mag2model',
                                                     value=5.5,
                                                     model='exponential',
                                                     readback_update_rate=0.0), t_local)
    mag2 = ModelPairDevice(ModelPairDeviceOptions(name='MAG2',
                                                  variable_name='MAG2',
                                                  scan_period=2.0,
                                                  readback_name='MAG2RB',
                                                  device=mag2model))
    ctx.add_device(mag2)
    sim_engine.enable_device(mag2)
    timeout = 5.0

    logging.debug('======================== 0')
    w, rb = wav({'MAG2': 5.5}, rb_dict, timeout, atol_map=atol_map,
                rtol_map=rtol_map)
    assert rb == {'MAG2': 5.5}

    logging.debug('======================== 1')
    with pytest.raises(WriteTimeoutError):
        w, rb = wav({'MAG2': 8.5}, rb_dict, timeout)

    logging.debug('======================== 2')
    start_time_scan()
    with pytest.raises(WriteTimeoutError):
        w, rb = wav({'MAG2': 8.5}, rb_dict, timeout)

    logging.debug('======================== 3')
    start_time_scan()
    with pytest.raises(WriteTimeoutError):
        w, rb = wav({'MAG2': 5.5}, rb_dict, 1.0)

    logging.debug('======================== 4')
    start_time_scan()
    w, rb = wav({'MAG2': 11.5}, rb_dict, timeout,
                atol_map={'MAG2': 0.001}, rtol_map=rtol_map)
    assert np.isclose(rb['MAG2'], 11.5, atol=0.001)

    logging.debug('======================== 5')
    start_time_scan()
    w, rb = wav({'MAG1': 13.5, 'MAG2': 13.5}, rb_dict, timeout,
                atol_map={'MAG2': 0.001}, rtol_map=rtol_map)
    assert w == {'MAG1': None, 'MAG2': None}
    assert np.isclose(rb['MAG2'], 13.5, atol=0.001)
    assert np.isclose(rb['MAG1'], 13.5, atol=0.001)

    logging.debug('======================== 6')
    start_time_scan()
    with pytest.raises(WriteTimeoutError):
        w, rb = wav({'MAG1': 9.5, 'MAG2': 9.5}, rb_dict, timeout,
                    atol_map={'MAG1': 0.001}, rtol_map=rtol_map)

    logging.debug('======================== 7')
    start_time_scan()
    w, rb = wav({'MAG1': 13.5, 'MAG2': 13.5}, rb_dict, timeout,
                atol_map={'MAG2': 0.000001}, )
    assert w == {'MAG1': None, 'MAG2': None}
    assert rb['MAG1'] == 13.5
    assert np.isclose(rb['MAG2'], 13.5, atol=0.001)

    logging.debug('======================== 8')
    start_time_scan()
    with pytest.raises(WriteTimeoutError):
        w, rb = wav({'MAG1': 9.5, 'MAG2': 9.5}, rb_dict, timeout=0.0,
                    atol_map={'MAG1': 0.001})
        assert np.isclose(mag2model.value, 9.5, atol=0.001)

    # partial readbacks
    logging.debug('======================== 9')
    start_time_scan()
    w, rb = wav({'MAG1': 11.5, 'MAG2': 11.5})
    assert w == {'MAG1': None, 'MAG2': None}
    assert rb['MAG1'] is None
    assert rb['MAG2'] is None

    logging.debug('======================== 10')
    rb_dict_partial = {'MAG2': 'MAG2RB'}
    start_time_scan()
    atol_map = {'MAG2': 0.001}
    w, rb = wav({'MAG1': 13.5, 'MAG2': 13.5}, rb_dict_partial, timeout,
                atol_map=atol_map, rtol_map=rtol_map)
    assert w == {'MAG1': None, 'MAG2': None}
    assert np.isclose(rb['MAG2'], 13.5, atol=0.001)
    assert rb['MAG1'] is None


def test_adv_write_rt(sim_engine_realtime: SimulationEngine):
    t_start = time.time()
    sim_engine = sim_engine_realtime
    ctx = SignalContext(se=sim_engine)

    def local_time():
        return time.time()

    mag2model = RealisticModel(RealisticModelOptions(name='mag2model', value=5.5,
                                                     model='exponential',
                                                     model_kwargs={'decay_constant': 0.5},
                                                     readback_update_rate=0.0), local_time())
    mag2 = ModelPairDevice(ModelPairDeviceOptions(name='MAG2',
                                                  variable_name='MAG2',
                                                  scan_period=1.0,
                                                  readback_name='MAG2RB',
                                                  device=mag2model))
    ctx.add_device(mag2)
    sim_engine.enable_device(mag2)

    q = queue.Queue()

    def start_time_scan() -> threading.Thread:
        def time_thread():
            while True:
                try:
                    q.get_nowait()
                    break
                except queue.Empty:
                    sim_engine.scan_until(local_time())
                    time.sleep(0.1)

        th = threading.Thread(target=time_thread, name='time_thread')
        th.daemon = True
        th.start()
        return th

    th = start_time_scan()

    timeout = 5.0
    rb_dict = {'MAG2': 'MAG2RB'}
    atol_map = {}
    rtol_map = {}
    wav = sim_engine.write_and_verify

    w, rb = wav({'MAG2': 5.5}, rb_dict, timeout, atol_map=atol_map,
                rtol_map=rtol_map)
    assert rb == {'MAG2': 5.5}

    with pytest.raises(WriteTimeoutError):
        w, rb = wav({'MAG2': 8.5}, rb_dict, timeout, atol_map=atol_map,
                    rtol_map=rtol_map)

    with pytest.raises(WriteTimeoutError):
        w, rb = wav({'MAG2': 11.5}, rb_dict, timeout, atol_map=atol_map,
                    rtol_map=rtol_map)

    atol_map = {'MAG2': 0.001}

    with pytest.raises(WriteTimeoutError):
        w, rb = wav({'MAG2': 8.5}, rb_dict, timeout=0.1, atol_map=atol_map,
                    rtol_map=rtol_map)

    w, rb = wav({'MAG2': 11.5}, rb_dict, timeout, atol_map=atol_map,
                rtol_map=rtol_map)
    assert np.isclose(rb['MAG2'], 11.5, atol=0.01)

    with pytest.raises(WriteTimeoutError):
        w, rb = wav({'MAG2': 8.5}, rb_dict, timeout=2.5, atol_map=atol_map,
                    rtol_map=rtol_map)

    w, rb = wav({'MAG2': 8.5}, rb_dict, timeout, atol_map=atol_map,
                rtol_map=rtol_map)
    assert np.isclose(rb['MAG2'], 8.5, atol=0.01)

    q.put(None)
    th.join()


def test_realtime(sim_engine_realtime: SimulationEngine):
    t_start = time.time()
    sim_engine = sim_engine_realtime
    # ctx = SignalContext(se=sim_engine)
    echo1 = ED(EDO(name='echo1', data={'TEST:ECHO:1': 5.0},
                   scan_period=2.0))
    sim_engine.add_device(echo1)
    sim_engine.enable_device(echo1)

    q = queue.Queue()

    def start_time_scan():
        def time_thread():
            while True:
                try:
                    q.get_nowait()
                    break
                except queue.Empty:
                    sim_engine.scan_until(time.time())
                    time.sleep(0.1)

        th = threading.Thread(target=time_thread, name='time_thread')
        th.daemon = True
        th.start()
        return th

    th = start_time_scan()
    time.sleep(10.1)
    q.put(None)
    th.join()

    t_end = time.time()

    h = sim_engine.history['TEST:ECHO:1']
    assert h.size == 6
    assert all([t_start < x[1].time < t_end for x in h.to_list()])


def test_modeldevice(sim_engine: SimulationEngine):
    ctx = SignalContext(se=sim_engine)
    echo1 = ED(EDO(name='echo1', data={'TEST:ECHO:1': 5.0}))
    t = sim_engine.time()
    mag1model = RealisticModel(RealisticModelOptions(name='mag1model', value=0.5), t)
    mag1 = ModelDevice(ModelDeviceOptions(name='mag1', device=mag1model))
    ctx.add_device(echo1)
    ctx.add_device(mag1)

    sim_engine.enable_device(echo1)
    sim_engine.enable_device(mag1)

    assert sim_engine.read_channel('mag1') == 0.5
    sim_engine.write_channel('mag1', 1.5)
    assert sim_engine.latest_data['mag1'] == 1.5
    assert sim_engine.read_channel('mag1') == 1.5


def test_modelpairdevice(sim_engine: SimulationEngine):
    ctx = SignalContext(se=sim_engine)
    echo1 = ED(EDO(name='echo1', data={'TEST:ECHO:1': 5.0}))
    t = 0.0
    mag1model = RealisticModel(RealisticModelOptions(name='mag1model', value=0.5), t)
    mag1 = ModelPairDevice(ModelPairDeviceOptions(name='mag1',
                                                  variable_name='mag1',
                                                  readback_name='mag1rb',
                                                  device=mag1model))
    ctx.add_device(echo1)
    ctx.add_device(mag1)

    sim_engine.enable_device(echo1)
    sim_engine.enable_device(mag1)

    assert sim_engine.read_channel('mag1') == 0.5
    assert sim_engine.read_channel('mag1rb') == 0.5
    sim_engine.write_channel('mag1', 1.5)
    assert sim_engine.latest_data['mag1'] == 1.5
    assert sim_engine.read_channel('mag1') == 1.5
    assert sim_engine.latest_data['mag1rb'] == 1.5
    assert sim_engine.read_channel('mag1rb') == 1.5


def test_modelpair_scan(sim_engine: SimulationEngine):
    t_local = 0.0

    def local_time():
        return t_local

    sim_engine.time_fun = local_time
    ctx = SignalContext(se=sim_engine)
    echo1 = ED(EDO(name='echo1',
                   data={'TEST:ECHO:1': 5.0},
                   scan_period=0.5))
    mag1model = RealisticModel(RealisticModelOptions(name='mag1model',
                                                     value=0.5,
                                                     readback_update_rate=2.5), t_local)
    mag1 = ModelPairDevice(ModelPairDeviceOptions(name='MAG1',
                                                  variable_name='MAG1',
                                                  scan_period=0.5,
                                                  readback_name='MAG1RB',
                                                  device=mag1model))
    ctx.add_device(echo1)
    ctx.add_device(mag1)

    sim_engine.enable_device(echo1)
    sim_engine.enable_device(mag1)
    assert len(sim_engine.history_data['MAG1RB']) == 1

    t_local = 5.0
    sim_engine.scan_until(t_local)
    assert mag1.stats == {'disable': 0,'enable': 1,'update': 1, 'read': 0, 'read_now': 0,'write': 0, 'scan': 10}
    assert echo1.stats == {'disable': 0,'enable': 1,'update': 1, 'read': 0, 'read_now': 0,'write': 0, 'scan': 10}
    h = sim_engine.history_data['TEST:ECHO:1']
    assert len(h) == 1 + 10
    assert len(sim_engine.history_data['MAG1RB']) == 1 + 2

    assert sim_engine.read_channel('MAG1') == 0.5
    assert sim_engine.read_channel('MAG1RB') == 0.5
    sim_engine.write_channel('MAG1', 1.5)
    assert sim_engine.latest_data['MAG1'] == 1.5
    assert sim_engine.read_channel('MAG1') == 1.5
    assert sim_engine.latest_data['MAG1RB'] == 1.5
    assert sim_engine.read_channel('MAG1RB') == 1.5
    assert mag1.stats == {'disable': 0,'enable': 1,'update': 1, 'read': 4, 'read_now': 0,'write': 1, 'scan': 10}
    assert echo1.stats == {'disable': 0,'enable': 1,'update': 1, 'read': 0, 'read_now': 0,'write': 0, 'scan': 10}

    t_local = 15.0
    sim_engine.scan_until(t_local)
    assert mag1.stats == {'disable': 0,'enable': 1,'update': 1, 'read': 4, 'read_now': 0,'write': 1, 'scan': 30}

    h = sim_engine.history_data['MAG1RB']
    assert len(h) == 1 + 7


def test_modelpair_scan_rt(sim_engine: SimulationEngine):
    def local_time():
        return time.time()

    t_start = local_time()
    logging.debug(f'Start at {t_start}')
    sim_engine.time_fun = local_time
    ctx = SignalContext(se=sim_engine)
    echo1 = ED(EDO(name='echo1',
                   data={'TEST:ECHO:1': 5.0},
                   scan_period=1.0))
    mag1model = RealisticModel(RealisticModelOptions(name='mag1model',
                                                     value=0.7,
                                                     readback_update_rate=0.0), local_time())
    mag1 = ModelPairDevice(ModelPairDeviceOptions(name='MAG1',
                                                  variable_name='MAG1',
                                                  scan_period=1.0,
                                                  readback_name='MAG1RB',
                                                  device=mag1model))
    ctx.add_device(echo1)
    ctx.add_device(mag1)

    sim_engine.enable_device(echo1)
    sim_engine.enable_device(mag1)
    assert len(sim_engine.history_data['MAG1RB']) == 1

    time.sleep(2.0)
    sim_engine.scan_now(t_start + 2.0)
    assert mag1.stats == {'update': 1, 'read': 0, 'write': 0, 'scan': 1}
    assert echo1.stats == {'update': 1, 'read': 0, 'write': 0, 'scan': 1}
    assert len(sim_engine.history_data['TEST:ECHO:1']) == 1 + 1
    assert len(sim_engine.history_data['MAG1RB']) == 1 + 1

    assert sim_engine.read_channel('MAG1') == 0.7
    assert sim_engine.read_channel('MAG1RB') == 0.7
    sim_engine.write_channel('MAG1', 1.5)
    assert sim_engine.latest_data['MAG1'] == 1.5
    assert sim_engine.read_channel('MAG1') == 1.5
    assert sim_engine.latest_data['MAG1RB'] == 1.5
    assert sim_engine.read_channel('MAG1RB') == 1.5
    assert mag1.stats == {'update': 1, 'read': 4, 'write': 1, 'scan': 1}
    assert echo1.stats == {'update': 1, 'read': 0, 'write': 0, 'scan': 1}
    assert len(sim_engine.history_data['MAG1RB']) == 1 + 2

    # Not enough time passed, no scan
    sim_engine.scan_now(local_time())
    assert mag1.stats == {'update': 1, 'read': 4, 'write': 1, 'scan': 1}

    sim_engine.start_scan_thread()
    time.sleep(5.1)
    sim_engine.stop_update_thread()
    assert mag1.stats == {'update': 1, 'read': 4, 'write': 1, 'scan': 1 + 6}
    assert echo1.stats == {'update': 1, 'read': 0, 'write': 0, 'scan': 1 + 6}
    assert len(sim_engine.history_data['MAG1RB']) == 1 + 2 + 6
    assert len(sim_engine.history_data['TEST:ECHO:1']) == 1 + 1 + 6


def test_device_deps(sim_engine: SimulationEngine):
    ctx = SignalContext(se=sim_engine)
    echo1 = ED(EDO(name='echo1', data={'TEST:ECHO:1': 5.0}))
    proxy1 = PD(PDO(name='proxy1', channel_map={
        'TEST:PROXY:1': {'TEST:ECHO:1': TRIG.PROPAGATE}
    }))
    proxy2 = PD(PDO(name='proxy2', channel_map={
        'TEST:PROXY:2': {'TEST:PROXY:1': TRIG.PROPAGATE}
    }))
    ctx.add_device(proxy2)
    ctx.add_device(proxy1)
    ctx.add_device(echo1)

    sim_engine.enable_device(echo1)
    sim_engine.process_events()
    assert echo1.stats == {'disable': 0, 'enable': 1, 'update': 1, 'read': 0, 'read_now': 0,
                           'write': 0, 'scan': 0
                           }
    assert proxy1.stats == {'disable': 0, 'update': 0, 'read': 0, 'write': 0, 'scan': 0}
    assert proxy2.stats == {'disable': 0, 'update': 0, 'read': 0, 'write': 0, 'scan': 0}
    assert echo1.aux_data == {}
    assert echo1.state == DS.ENABLED
    assert proxy1.state == DS.CREATED

    sim_engine.write_channel('TEST:ECHO:1', 4.0)
    sim_engine.process_events()
    assert echo1.stats == {'disable': 0, 'enable': 1, 'update': 1, 'read': 0, 'read_now': 0,
                           'write': 1, 'scan': 0
                           }
    assert proxy1.stats == {'disable': 0, 'enable': 1, 'update': 0, 'read': 0, 'read_now': 0,
                            'write': 0, 'scan': 0
                            }
    assert proxy2.stats == {'disable': 0, 'enable': 1, 'update': 0, 'read': 0, 'read_now': 0,
                            'write': 0, 'scan': 0
                            }
    assert sim_engine.latest_data['TEST:ECHO:1'] == 4.0
    assert sim_engine.latest_data['TEST:PROXY:1'] is None
    assert sim_engine.latest_data['TEST:PROXY:2'] is None

    sim_engine.enable_device(proxy1)
    assert proxy1.stats == {'disable': 0, 'enable': 1, 'update': 1, 'read': 0, 'read_now': 0,
                            'write': 0, 'scan': 0
                            }
    assert sim_engine.latest_data['TEST:PROXY:1'] == 4.0
    sim_engine.write_channel('TEST:ECHO:1', 3.0)
    sim_engine.process_events()
    assert echo1.stats == {'disable': 0, 'enable': 1, 'update': 1, 'read': 0, 'write': 2, 'scan': 0}
    assert proxy1.stats == {'disable': 0, 'enable': 1, 'update': 2, 'read': 0, 'write': 0,
                            'scan': 0
                            }
    assert proxy2.stats == {'disable': 0, 'enable': 1, 'update': 0, 'read': 0, 'write': 0,
                            'scan': 0
                            }
    assert sim_engine.latest_data['TEST:ECHO:1'] == 3.0
    assert sim_engine.latest_data['TEST:PROXY:1'] == 3.0
    assert sim_engine.latest_data['TEST:PROXY:2'] is None
    assert proxy1.aux_data == {'TEST:ECHO:1': 3.0}

    sim_engine.enable_device(proxy2)
    assert proxy2.stats == {'update': 1, 'read': 0, 'write': 0, 'scan': 0}
    assert sim_engine.latest_data['TEST:PROXY:2'] == 3.0
    sim_engine.write_channel('TEST:ECHO:1', 2.0)
    sim_engine.process_events()
    assert echo1.stats == {'update': 1, 'read': 0, 'write': 3, 'scan': 0}
    assert proxy1.stats == {'update': 3, 'read': 0, 'write': 0, 'scan': 0}
    assert proxy2.stats == {'update': 2, 'read': 0, 'write': 0, 'scan': 0}
    assert sim_engine.latest_data['TEST:ECHO:1'] == 2.0
    assert sim_engine.latest_data['TEST:PROXY:1'] == 2.0
    assert sim_engine.latest_data['TEST:PROXY:2'] == 2.0
    assert proxy1.aux_data == {'TEST:ECHO:1': 2.0}
    assert proxy2.aux_data == {'TEST:PROXY:1': 2.0}


def test_device_deps_prop(sim_engine: SimulationEngine):
    ctx = SignalContext(se=sim_engine)
    echo1 = ED(EDO(name='echo1', data={'TEST:ECHO:1': 5.0}))
    proxy1 = PD(PDO(name='proxy1', channel_map={
        'TEST:PROXY:1': {'TEST:ECHO:1': TRIG.IGNORE}
    }))
    proxy2 = PD(PDO(name='proxy2', channel_map={
        'TEST:PROXY:2': {'TEST:PROXY:1': TRIG.PROPAGATE}
    }))
    ctx.add_device(echo1)
    ctx.add_device(proxy1)
    ctx.add_device(proxy2)

    sim_engine.enable_device(echo1)
    sim_engine.enable_device(proxy1)
    sim_engine.enable_device(proxy2)

    sim_engine.check_deps_satisfied('TEST:ECHO:1')
    sim_engine.check_deps_satisfied('TEST:PROXY:1')
    with pytest.raises(DeviceDependencyError):
        sim_engine.check_deps_satisfied('TEST:PROXY:2')

    assert echo1.stats == {'update': 1, 'read': 0, 'write': 0, 'scan': 0}
    assert proxy1.stats == {'update': 1, 'read': 0, 'write': 0, 'scan': 0}
    assert proxy2.stats == {'update': 1, 'read': 0, 'write': 0, 'scan': 0}


def test_device_deps_err(sim_engine: SimulationEngine):
    ctx = SignalContext(se=sim_engine)
    echo1 = ED(EDO(name='echo1', data={'TEST:ECHO:1': 5.0}))
    proxy1 = PD(PDO(name='proxy1', channel_map={'TEST:PROXY:1': {'TEST:ECHO:1': TRIG.PROPAGATE}}))
    proxy2 = PD(PDO(name='proxy2', channel_map={
        'TEST:PROXY:2': {'TEST:PROXY:1': TRIG.PROPAGATE}
    }))
    ctx.add_device(proxy2)
    ctx.add_device(proxy1)
    ctx.add_device(echo1)

    sim_engine.enable_device(echo1)
    sim_engine.enable_device(proxy1)
    sim_engine.enable_device(proxy2)

    assert echo1.stats == {'update': 1, 'read': 0, 'write': 0, 'scan': 0}
    assert proxy1.stats == {'update': 1, 'read': 0, 'write': 0, 'scan': 0}
    assert proxy2.stats == {'update': 1, 'read': 0, 'write': 0, 'scan': 0}

    proxy1.state = DS.ERROR_INTERNAL
    sim_engine.write_channel('TEST:ECHO:1', 3.0)
    assert echo1.stats == {'update': 1, 'read': 0, 'write': 1, 'scan': 0}
    assert proxy1.stats == {'update': 1, 'read': 0, 'write': 0, 'scan': 0}
    assert proxy2.stats == {'update': 1, 'read': 0, 'write': 0, 'scan': 0}
    assert proxy1.aux_data == {'TEST:ECHO:1': 5.0}
    assert proxy2.aux_data == {'TEST:PROXY:1': 5.0}


def test_device_deps_blank_init(sim_engine: SimulationEngine):
    ctx = SignalContext(se=sim_engine)
    echo1 = ED(EDO(name='echo1', data={'TEST:ECHO:1': 5.0}))
    proxy1 = PD(PDO(name='proxy1', channel_map={
        'TEST:PROXY:1': {'TEST:ECHO:1': TRIG.PROPAGATE}
    }))
    proxy2 = PD(PDO(name='proxy2', channel_map={
        'TEST:PROXY:2': {'TEST:PROXY:1': TRIG.PROPAGATE}
    }))
    ctx.add_device(proxy2)
    ctx.add_device(proxy1)
    ctx.add_device(echo1)

    sim_engine.enable_device(proxy2)
    assert proxy2.aux_data == {'TEST:PROXY:1': None}
    assert proxy2.state == DS.ENABLED

    sim_engine.enable_device(proxy1)
    assert proxy1.aux_data == {'TEST:ECHO:1': None}
    assert proxy2.aux_data == {'TEST:PROXY:1': None}
    assert proxy1.state == DS.ENABLED

    sim_engine.enable_device(echo1)
    sim_engine.process_events()
    assert proxy1.aux_data == {'TEST:ECHO:1': 5.0}
    assert proxy2.aux_data == {'TEST:PROXY:1': 5.0}

    assert echo1.stats == {'update': 1, 'read': 0, 'write': 0, 'scan': 0}
    assert proxy1.stats == {'update': 2, 'read': 0, 'write': 0, 'scan': 0}
    assert proxy2.stats == {'update': 3, 'read': 0, 'write': 0, 'scan': 0}

    proxy1.state = DS.ERROR_INTERNAL
    sim_engine.write_channel('TEST:ECHO:1', 3.0)
    assert echo1.stats == {'update': 1, 'read': 0, 'write': 1, 'scan': 0}
    assert proxy1.stats == {'update': 2, 'read': 0, 'write': 0, 'scan': 0}
    assert proxy2.stats == {'update': 3, 'read': 0, 'write': 0, 'scan': 0}
    assert proxy1.aux_data == {'TEST:ECHO:1': 5.0}
    assert proxy2.aux_data == {'TEST:PROXY:1': 5.0}


def test_device_set(sim_engine: SimulationEngine):
    ctx = SignalContext(se=sim_engine)
    echo1 = ED(EDO(name='echo1', data={'TEST:ECHO:1': 5}))
    echo2 = ED(EDO(name='echo2', data={'TEST:ECHO:2': 15}))
    ctx.add_device(echo1)
    ctx.add_device(echo2)
    sim_engine.enable_device(echo1)
    sim_engine.enable_device(echo2)

    assert sim_engine.read_channel('TEST:ECHO:1') == 5
    sim_engine.write_channel('TEST:ECHO:1', 10)
    assert sim_engine.read_channel('TEST:ECHO:1') == 10

    for i in range(10):
        sim_engine.write_channel('TEST:ECHO:1', 10 + i)
        sim_engine.write_channel('TEST:ECHO:2', 20 + i)
        assert sim_engine.read_channel('TEST:ECHO:1') == 10 + i


def test_device_propagate(sim_engine_with_devices: SimulationEngine):
    sim = sim_engine_with_devices
    for dev in sim.devices_list:
        assert dev.state == DS.CREATED

# def test_running_logic(sim_engine: SimulationEngine):
#     mag = RealisticMagnet(name='mag1', value=0.5)
#     sim_engine.add_device(mag, period=0.05)
#     mag2 = RealisticMagnet(name='mag2', value=1.5)
#     sim_engine.add_device(mag2, period=0.05)
#
#     def read_fun(device, output):
#         return device.read()
#
#     def write_fun(device, output, value):
#         return device.write(value)
#
#     m = ChannelMap(device=mag, channels='MAG1:CHANNEL',
#                    read_fun=read_fun, write_fun=write_fun)
#     m2 = ChannelMap(device=mag2, channels='MAG2:CHANNEL',
#                     read_fun=read_fun, write_fun=write_fun)
#     chm = ChannelMapSet(maps=[m, m2])
#     sim_engine.add_mapper(chm)
#
#     t1 = time.time()
#     sim_engine.start_update_thread()
#     delta = time.time() - t1
#     assert delta < 0.1
#     assert sim_engine.poll_thread.is_alive()
#     assert mag2.raw_value == mag2.value == 1.5
#
#     with pytest.raises(SimulationError):
#         sim_engine.start_update_thread()
#
#     time.sleep(0.1)
#
#     # Check callbacks
#     last_results_map = {}
#     circular_buffers_map = {}
#     circular_buffers_map['MAG1:CHANNEL'] = collections.deque(maxlen=50)
#     def callback(sub, response: np.ndarray):
#         name = sub.name
#         circular_buffers_map[name].append(response)
#         last_results_map[name] = response
#
#     cb1 = callback
#     subscription1 = sim_engine.subscribe_channel('MAG1:CHANNEL')
#     subscription1.add_callback(cb1)
#     assert subscription1.callbacks == [cb1]
#     time.sleep(0.06)
#
#     assert last_results_map['MAG1:CHANNEL'] == 0.5
#     time.sleep(2.6)
#     assert len(circular_buffers_map['MAG1:CHANNEL']) == 50
#
#     sim_engine.write_channel('MAG1:CHANNEL', 2.3)
#     time.sleep(0.06)
#     assert last_results_map['MAG1:CHANNEL'] == 2.3
#
#     t1 = time.time()
#     sim_engine.stop_update_thread()
#     delta = time.time() - t1
#     assert delta < 0.1
#
#     with pytest.raises(SimulationError):
#         sim_engine.stop_update_thread()
