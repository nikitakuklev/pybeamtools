import asyncio
import logging
import time
from threading import Thread

import numpy as np
import pytest
import os

from pybeamtools.controls.errors import ControlLibException, SecurityError, InvalidWriteError, InterlockWriteError
from pybeamtools.sim.core import SimulationEngine
import pybeamtools.controls as pc
from pybeamtools.controls.control_lib import ConnectionOptions
from pybeamtools.controls.network import SimPV, PVOptions, PVAccess, EPICSPV
from pybeamtools.controls.interlocks import LimitInterlock, LimitInterlockOptions
from pybeamtools.sim.softioc import EchoIOC
from sim.devices import UNIXTimer

logger = logging.getLogger(__name__)


class TestEPICSPV:
    @pytest.fixture(autouse=False)
    def soft_ioc(self, sim_engine):
        os.environ['EPICS_CA_AUTO_ADDR_LIST'] = 'no'
        os.environ['EPICS_CA_ADDR_LIST'] = '127.0.0.1'

        from caproto.sync import repeater
        repeater.spawn_repeater()
        time.sleep(0.1)

        channels = ['TEST:CHANNEL:A', 'TEST:CHANNEL:B', 'TEST:CHANNEL:C', 'TEST:CHANNEL:T']
        sioc = EchoIOC(channels=channels, sim_engine=sim_engine)
        sioc.setup()
        sioc.run_in_background()
        logger.debug(f'Soft IOC started')
        for ch in channels:
            def callback(sub, response: np.ndarray):
                name = sub.name
                logger.debug(f'Soft IOC put callback for PV ({sub.name}): ({response})')
                # logger.debug(f'{type(name)=} {type(response[0])=}')
                # logger.debug(f'{sioc=} {sioc.__dict__=}')
                # sioc.bl.pvdb[name].write(response[0], verify_value=False)
                # sioc.ping()
                sioc.send_updates(name, response)

            cb = callback
            subscription = sim_engine.subscribe_channel(ch)
            subscription.add_callback(cb)

        time.sleep(0.1)
        return sioc

    @pytest.fixture(autouse=False)
    def soft_ioc_low(self, sim_engine_low):
        sim_engine = sim_engine_low
        os.environ['EPICS_CA_AUTO_ADDR_LIST'] = 'no'
        os.environ['EPICS_CA_ADDR_LIST'] = '127.0.0.1'

        from caproto.sync import repeater
        repeater.spawn_repeater()
        time.sleep(0.1)

        channels = ['TEST:CHANNEL:A', 'TEST:CHANNEL:B']
        sioc = EchoIOC(channels=channels, sim_engine=sim_engine)
        sioc.setup()
        sioc.run_in_background()
        logger.debug(f'Soft IOC started')
        for ch in channels:
            def callback(sub, response: np.ndarray):
                name = sub.name
                logger.debug(f'Soft IOC put callback for PV ({sub.name}): ({response})')
                # logger.debug(f'{type(name)=} {type(response[0])=}')
                # logger.debug(f'{sioc=} {sioc.__dict__=}')
                # sioc.bl.pvdb[name].write(response[0], verify_value=False)
                # sioc.ping()
                sioc.send_updates(name, response)

            cb = callback
            subscription = sim_engine.subscribe_channel(ch)
            subscription.add_callback(cb)

        time.sleep(0.1)
        return sioc

    @pytest.fixture
    def sim_engine(self) -> SimulationEngine:
        from pybeamtools.sim.core import SimulationEngine, ChannelMap, ChannelMapSet
        from pybeamtools.sim.devices import RealisticMagnet

        sim = SimulationEngine()
        mag = RealisticMagnet(name='TEST:DEVICE:A', value=0.5)
        sim.add_device(mag, period=5.0)
        mag2 = RealisticMagnet(name='TEST:DEVICE:B', value=1.5)
        sim.add_device(mag2, period=5.0)
        mag3 = RealisticMagnet(name='TEST:DEVICE:C', value=2.5)
        sim.add_device(mag3, period=5.0)
        unix = UNIXTimer(name='TEST:DEVICE:T')
        sim.add_device(unix, period=2.0)

        def get(device, output):
            return device.read()

        def set(device, output, value):
            return device.write(value)

        m = ChannelMap(device=mag, channels='TEST:CHANNEL:A', read_fun=get, write_fun=set)
        m2 = ChannelMap(device=mag2, channels='TEST:CHANNEL:B', read_fun=get, write_fun=set)
        m3 = ChannelMap(device=mag3, channels='TEST:CHANNEL:C', read_fun=get, write_fun=set)
        t = ChannelMap(device=unix, channels='TEST:CHANNEL:T', read_fun=get, write_fun=None)
        chm = ChannelMapSet(maps=[m, m2, m3, t])
        sim.add_mapper(chm)
        sim.start_update_thread()
        sim.read_channel('TEST:CHANNEL:A')
        sim.read_channel('TEST:CHANNEL:B')
        sim.read_channel('TEST:CHANNEL:C')
        sim.read_channel('TEST:CHANNEL:T')
        time.sleep(0)
        return sim

    @pytest.fixture
    def sim_engine_low(self) -> SimulationEngine:
        from pybeamtools.sim.core import SimulationEngine, ChannelMap, ChannelMapSet
        from pybeamtools.sim.devices import RealisticMagnet

        sim = SimulationEngine()
        mag = RealisticMagnet(name='TEST:DEVICE:A', value=0.5)
        sim.add_device(mag, period=5.0)
        mag2 = RealisticMagnet(name='TEST:DEVICE:B', value=1.5)
        sim.add_device(mag2, period=1.0)

        def get(device, output):
            return device.read()

        def set(device, output, value):
            return device.write(value)

        m = ChannelMap(device=mag, channels='TEST:CHANNEL:A', read_fun=get, write_fun=set)
        m2 = ChannelMap(device=mag2, channels='TEST:CHANNEL:B', read_fun=get, write_fun=set)
        chm = ChannelMapSet(maps=[m, m2])
        sim.add_mapper(chm)
        sim.start_update_thread()
        time.sleep(0)
        return sim

    @pytest.fixture
    def sim_engine_with_pvs(self, sim_engine):
        ao = pc.AcceleratorOptions(connection_settings=ConnectionOptions(network='epics'))
        acc = pc.Accelerator(options=ao)
        pv_settings = PVOptions(name='TEST:CHANNEL:A', low=0.0, high=5.0,
                                security=PVAccess.READWRITE)
        pv = EPICSPV(pv_settings)
        pv_settings = PVOptions(name='TEST:CHANNEL:B', low=0.0, high=5.0,
                                security=PVAccess.READWRITE)
        pv2 = EPICSPV(pv_settings)
        pv_settings = PVOptions(name='TEST:CHANNEL:C', low=0.0, high=5.0,
                                security=PVAccess.READONLY)
        pv3 = EPICSPV(pv_settings)
        pv_settings = PVOptions(name='TEST:CHANNEL:T', security=PVAccess.READONLY)
        pv4 = EPICSPV(pv_settings)
        acc.add_pv_object([pv, pv2, pv3, pv4])
        return sim_engine, acc, pv, pv2, pv3, pv4

    @pytest.fixture
    def sim_engine_with_pvs_low(self, sim_engine_low):
        ao = pc.AcceleratorOptions(connection_settings=ConnectionOptions(network='epics'))
        acc = pc.Accelerator(options=ao)
        pv_settings = PVOptions(name='TEST:CHANNEL:A', low=0.0, high=5.0,
                                security=PVAccess.READWRITE)
        pv = EPICSPV(pv_settings)
        acc.add_pv_object([pv])
        return sim_engine_low, acc, pv

    def test_pytest(self, sim_engine):
        sim_engine.TRACE = True
        assert os.environ['EPICS_CA_AUTO_ADDR_LIST'] == 'no'
        time.sleep(10)

    def test_pv_simple(self, sim_engine_with_pvs_low, soft_ioc_low):
        sim_engine, acc, pv = sim_engine_with_pvs_low
        sim_engine.TRACE = True
        time.sleep(10)
        logger.info(f'{acc.cm.last_results_map=}')
        for k, v in acc.cm.circular_buffers_map.items():
            # assert len(v) > 2
            logger.info(f'{k}:{len(v)}')

    def test_pv_simple2(self, sim_engine_with_pvs):
        sim_engine, acc, pv, pv2, pv3, pv4 = sim_engine_with_pvs
        time.sleep(2)
        logger.info(f'{acc.cm.last_results_map=}')
        t1 = pv4.read()
        r = pv.read()
        assert r.data == 0.5, r
        time.sleep(2)
        t2 = pv4.read()
        assert t2.data > t1.data
        logger.info(f'{acc.cm.last_results_map=}')
        for k, v in acc.cm.circular_buffers_map.items():
            assert len(v) > 2
            logger.info(f'{k}:{len(v)}')

    def test_pv_softioc(self, sim_engine_with_pvs, soft_ioc):
        sim_engine, acc, pv, pv2, pv3 = sim_engine_with_pvs
        interlock_limits = {'TEST:CHANNEL:A': (-1.0, 1.0),
                            'TEST:CHANNEL:B': (-1.0, None),
                            'TEST:CHANNEL:C': (-1.0, 1.0)}
        pv_list = ['TEST:CHANNEL:A', 'TEST:CHANNEL:B', 'TEST:CHANNEL:C']
        lopt = LimitInterlockOptions(pv_list=pv_list,
                                     read_events=[],
                                     write_events=pv_list,
                                     limits=interlock_limits)
        ilock = LimitInterlock(options=lopt)
        acc.add_interlock(ilock)

        with pytest.raises(SecurityError):
            pv3.write(2.6)

        assert acc.cm.last_results_map['TEST:CHANNEL:B'] is None, acc.cm.last_results_map
        time.sleep(0.51)
        assert acc.cm.last_results_map['TEST:CHANNEL:B'] is not None, acc.cm.last_results_map
        assert acc.cm.last_results_map['TEST:CHANNEL:C'] is not None, acc.cm.last_results_map

        with pytest.raises(InterlockWriteError):
            pv.write(1.4)

        with pytest.raises(InterlockWriteError):
            pv2.write(-1.4)

        assert soft_ioc.pvdb['TEST:CHANNEL:A'].value == 0.0
        assert soft_ioc.pvdb['TEST:CHANNEL:B'].value == 0.0
        assert soft_ioc.pvdb['TEST:CHANNEL:C'].value == 0.0

        print(ilock.__dict__)
        pv2.write(1.4)

        assert sim_engine.read_channel('TEST:CHANNEL:B') == 1.4
        assert soft_ioc.pvdb['TEST:CHANNEL:B'].value == 1.4

        acc.pm.stop_interlock(ilock)


class TestSimPV:
    @pytest.fixture
    def sim_engine(self) -> SimulationEngine:
        from pybeamtools.sim.core import SimulationEngine, ChannelMap, ChannelMapSet
        from pybeamtools.sim.devices import RealisticMagnet

        sim = SimulationEngine()
        mag = RealisticMagnet(name='TEST:DEVICE:A', value=0.5)
        sim.add_device(mag, period=0.05)
        mag2 = RealisticMagnet(name='TEST:DEVICE:B', value=1.5)
        sim.add_device(mag2, period=0.05)
        mag3 = RealisticMagnet(name='TEST:DEVICE:C', value=2.5)
        sim.add_device(mag3, period=0.05)

        def get(device, output):
            return device.read()

        def set(device, output, value):
            return device.write(value)

        m = ChannelMap(device=mag, channels='TEST:CHANNEL:A', read_fun=get, write_fun=set)
        m2 = ChannelMap(device=mag2, channels='TEST:CHANNEL:B', read_fun=get, write_fun=set)
        m3 = ChannelMap(device=mag3, channels='TEST:CHANNEL:C', read_fun=get, write_fun=set)
        chm = ChannelMapSet(maps=[m, m2, m3])
        sim.add_mapper(chm)
        sim.start_update_thread()
        sim.read_channel('TEST:CHANNEL:A')
        sim.read_channel('TEST:CHANNEL:B')
        sim.read_channel('TEST:CHANNEL:C')
        time.sleep(0)
        return sim

    @pytest.fixture
    def sim_engine_with_pvs(self, sim_engine):
        ao = pc.AcceleratorOptions(connection_settings=ConnectionOptions(network='dummy'))
        acc = pc.Accelerator(options=ao, ctx=sim_engine)
        pv_settings = PVOptions(name='TEST:CHANNEL:A', low=0.0, high=5.0,
                                security=PVAccess.READWRITE)
        pv = SimPV(pv_settings)
        pv_settings = PVOptions(name='TEST:CHANNEL:B', low=0.0, high=5.0,
                                security=PVAccess.READWRITE)
        pv2 = SimPV(pv_settings)
        pv_settings = PVOptions(name='TEST:CHANNEL:C', low=0.0, high=5.0,
                                security=PVAccess.READONLY)
        pv3 = SimPV(pv_settings)
        acc.add_pv_object([pv, pv2, pv3])
        return sim_engine, acc, pv, pv2, pv3

    def test_pv_sim(self, sim_engine: SimulationEngine):
        ao = pc.AcceleratorOptions(connection_settings=ConnectionOptions(network='dummy'))
        acc = pc.Accelerator(options=ao, ctx=sim_engine)
        pv_settings = PVOptions(name='TEST:CHANNEL:A', low=0.0, high=5.0,
                                security=PVAccess.READWRITE)
        pv = SimPV(pv_settings)
        pv_settings = PVOptions(name='TEST:CHANNEL:B', low=0.0, high=5.0,
                                security=PVAccess.READWRITE)
        pv2 = SimPV(pv_settings)

        acc.add_pv_object([pv])
        assert acc.pv_names == ['TEST:CHANNEL:A']
        acc.add_pv_object([pv2])
        assert acc.pv_names == ['TEST:CHANNEL:A', 'TEST:CHANNEL:B']
        assert acc.cm.subscribed_pv_names == ['TEST:CHANNEL:A', 'TEST:CHANNEL:B']

        r = pv.read()
        assert r == 0.5

        r = pv.write(1.3)
        assert r is not None
        r = pv.read()
        assert r == 1.3

        with pytest.raises(InvalidWriteError):
            # None not valid
            pv.write(None)
        with pytest.raises(InvalidWriteError):
            # bytes not valid
            pv.write('bla'.encode())
        with pytest.raises(ControlLibException):
            # too high
            pv.write(6.0)

        pv_settings = PVOptions(name='TEST:CHANNEL:C', low=0.0, high=5.0,
                                security=PVAccess.READONLY, monitor=False)
        pv3 = SimPV(pv_settings)
        acc.add_pv_object([pv3])

        r = pv3.read()
        assert r == 2.5

        with pytest.raises(SecurityError):
            pv3.write(2.6)

        time.sleep(0.1)
        for ch in ['TEST:CHANNEL:A', 'TEST:CHANNEL:B']:
            assert acc.cm.last_results_map[ch] is not None, ch

        assert acc.cm.last_results_map['TEST:CHANNEL:C'] is None

    def test_interlock_simple(self, sim_engine_with_pvs):
        sim_engine, acc, pv, pv2, pv3 = sim_engine_with_pvs

        from pybeamtools.controls.interlocks import LimitInterlock, LimitInterlockOptions
        interlock_limits = {'TEST:CHANNEL:A': (-1.0, 1.0),
                            'TEST:CHANNEL:B': (-1.0, None),
                            'TEST:CHANNEL:C': (-1.0, 1.0)}
        pv_list = ['TEST:CHANNEL:A', 'TEST:CHANNEL:B', 'TEST:CHANNEL:C']
        lopt = LimitInterlockOptions(pv_list=pv_list,
                                     read_events=[],
                                     write_events=pv_list,
                                     limits=interlock_limits)
        ilock = LimitInterlock(options=lopt)
        acc.add_interlock(ilock)

        with pytest.raises(SecurityError):
            pv3.write(2.6)

        assert acc.cm.last_results_map['TEST:CHANNEL:B'] is None
        time.sleep(0.51)
        assert acc.cm.last_results_map['TEST:CHANNEL:B'] is not None
        assert acc.cm.last_results_map['TEST:CHANNEL:C'] is not None, acc.cm.last_results_map

        with pytest.raises(InterlockWriteError):
            pv.write(1.4)

        with pytest.raises(InterlockWriteError):
            pv2.write(-1.4)

        print(ilock.__dict__)
        pv2.write(1.4)

        assert sim_engine.read_channel('TEST:CHANNEL:B') == 1.4

        acc.pm.stop_interlock(ilock)
