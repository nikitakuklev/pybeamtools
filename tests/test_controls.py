import asyncio
import time
from threading import Thread

import pytest
import os

from pybeamtools.controls.errors import ControlLibException, SecurityError, InvalidWriteError, InterlockWriteError
from pybeamtools.sim.core import SimulationEngine
import pybeamtools.controls as pc
from pybeamtools.controls.control_lib import ConnectionOptions
from pybeamtools.controls.network import SimPV, PVOptions, PVAccess


class TestEPICSPV:
    @pytest.fixture(scope='class', autouse=True)
    def setup_epics(self):
        os.environ['EPICS_CA_AUTO_ADDR_LIST'] = 'no'
        os.environ['EPICS_CA_ADDR_LIST'] = '127.0.0.1'

        from caproto.sync import repeater
        repeater.spawn_repeater()
        time.sleep(0.1)

        from caproto.server import PVGroup, ioc_arg_parser, pvproperty, run

        class SimpleIOC(PVGroup):
            B = pvproperty(
                value=2.0,
                doc='A float'
            )

        ioc_options = {'prefix': 'TEST:', 'macros': {}}
        run_options = {'module_name': 'caproto.asyncio.server',
                       'log_pv_names': True,
                       'interfaces': ['127.0.0.1']}
        ioc = SimpleIOC(**ioc_options)

        def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
            asyncio.set_event_loop(loop)
            run(ioc.pvdb, **run_options)

        loop = asyncio.new_event_loop()
        t = Thread(daemon=True, target=start_background_loop, args=(loop,))
        t.start()
        time.sleep(0.1)

    @pytest.fixture
    def sim_engine(self) -> SimulationEngine:
        from pybeamtools.sim.core import SimulationEngine, ChannelMap, ChannelMapper
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

        m = ChannelMap(device=mag, output='TEST:CHANNEL:A', read_fun=get, write_fun=set)
        m2 = ChannelMap(device=mag2, output='TEST:CHANNEL:B', read_fun=get, write_fun=set)
        m3 = ChannelMap(device=mag3, output='TEST:CHANNEL:C', read_fun=get, write_fun=set)
        chm = ChannelMapper(maps=[m, m2, m3])
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

    def test_write(self):
        assert os.environ['EPICS_CA_AUTO_ADDR_LIST'] == 'no'


class TestSimPV:
    @pytest.fixture
    def sim_engine(self) -> SimulationEngine:
        from pybeamtools.sim.core import SimulationEngine, ChannelMap, ChannelMapper
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

        m = ChannelMap(device=mag, output='TEST:CHANNEL:A', read_fun=get, write_fun=set)
        m2 = ChannelMap(device=mag2, output='TEST:CHANNEL:B', read_fun=get, write_fun=set)
        m3 = ChannelMap(device=mag3, output='TEST:CHANNEL:C', read_fun=get, write_fun=set)
        chm = ChannelMapper(maps=[m, m2, m3])
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
            pv.write(None)
        with pytest.raises(InvalidWriteError):
            pv.write('bla'.encode())
        with pytest.raises(ControlLibException):
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
