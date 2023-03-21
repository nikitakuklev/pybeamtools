import logging
import time

import pybeamtools.controls as pc
import pytest
from pybeamtools.controls import PVAccess
from pybeamtools.controls.control_lib import ConnectionOptions
from pybeamtools.controls.errors import ControlLibException, InterlockWriteError, InvalidWriteError, \
    SecurityError
from pybeamtools.controls.network import PVOptions, SimPV
from pybeamtools.sim.core import SignalEngineOptions, SimulationEngine
from pybeamtools.sim.pddevices import EchoDevice, EchoDeviceOptions, ModelPairDevice, \
    ModelPairDeviceOptions, SignalContext
from sim.devices import RealisticModel, RealisticModelOptions
from pybeamtools.controls.interlocks import LimitInterlock, LimitInterlockOptions
logger = logging.getLogger(__name__)

t = 0.0


def fixed_time():
    return t


class TestSimPV:
    @pytest.fixture
    def sim_engine(self) -> SimulationEngine:
        sim = SimulationEngine(SignalEngineOptions(time_function=fixed_time))
        sim.TRACE = True
        sim.TIME_TRACE = True
        return sim

    @pytest.fixture
    def sim_engine_with_models(self, sim_engine: SimulationEngine) -> SimulationEngine:
        ctx = SignalContext(se=sim_engine)
        echo1 = EchoDevice(EchoDeviceOptions(name='echo1', data={'ECHO:1': 5.0}))
        mag1model = RealisticModel(RealisticModelOptions(name='mag1model', value=0.5), t)
        mag1 = ModelPairDevice(ModelPairDeviceOptions(name='DEVICE:A',
                                                      readback_name='DEVICE:A_RB',
                                                      device=mag1model))
        mag2model = RealisticModel(RealisticModelOptions(name='mag2model', value=1.5), t)
        mag2 = ModelPairDevice(ModelPairDeviceOptions(name='DEVICE:B',
                                                      readback_name='DEVICE:B_RB',
                                                      device=mag2model))
        mag3model = RealisticModel(RealisticModelOptions(name='mag3model', value=2.5), t)
        mag3 = ModelPairDevice(ModelPairDeviceOptions(name='DEVICE:C',
                                                      readback_name='DEVICE:C_RB',
                                                      device=mag3model))
        ctx.add_device(echo1)
        ctx.add_device(mag1)
        ctx.add_device(mag2)
        ctx.add_device(mag3)

        sim_engine.enable_device(echo1)
        sim_engine.enable_device(mag1)
        sim_engine.enable_device(mag2)
        sim_engine.enable_device(mag3)
        return sim_engine

    # @pytest.fixture
    # def sim_engine_with_pvs(self, sim_engine):
    #     ao = pc.AcceleratorOptions(connection_settings=ConnectionOptions(network='dummy'))
    #     acc = pc.Accelerator(options=ao, ctx=sim_engine)
    #     pv_settings = PVOptions(name='DEVICE:A', low=0.0, high=5.0,
    #                             security=PVAccess.READWRITE)
    #     pv = SimPV(pv_settings)
    #     pv_settings = PVOptions(name='DEVICE:B', low=0.0, high=5.0,
    #                             security=PVAccess.READWRITE)
    #     pv2 = SimPV(pv_settings)
    #     pv_settings = PVOptions(name='DEVICE:C', low=0.0, high=5.0,
    #                             security=PVAccess.READONLY)
    #     pv3 = SimPV(pv_settings)
    #     acc.add_pv_object([pv, pv2, pv3])
    #     return sim_engine, acc, pv, pv2, pv3

    def test_pv_sim(self, sim_engine_with_models: SimulationEngine):
        ao = pc.AcceleratorOptions(connection_settings=ConnectionOptions(network='dummy'))
        acc = pc.Accelerator(options=ao, ctx=sim_engine_with_models)
        acc.TRACE = True
        pv_settings = PVOptions(name='DEVICE:A', low=0.0, high=5.0,
                                security=PVAccess.RW)
        pv = SimPV(pv_settings)
        pv_settings = PVOptions(name='DEVICE:B', low=0.0, high=5.0,
                                security=PVAccess.RW)
        pv2 = SimPV(pv_settings)

        acc.add_pv_object([pv])
        assert acc.pv_names == ['DEVICE:A']
        acc.add_pv_object([pv2])
        assert acc.pv_names == ['DEVICE:A', 'DEVICE:B']
        assert acc.cm.subscribed_pv_names == ['DEVICE:A', 'DEVICE:B']

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

        pv_settings = PVOptions(name='DEVICE:C', low=0.0, high=5.0,
                                security=PVAccess.RO, monitor=False)
        pv3 = SimPV(pv_settings)
        acc.add_pv_object([pv3])

        r = pv3.read()
        assert r == 2.5

        with pytest.raises(SecurityError):
            pv3.write(2.6)

        for ch in ['DEVICE:A']:
            assert acc.cm.last_results_map[ch] is not None

        for ch in ['DEVICE:B', 'DEVICE:C']:
            assert acc.cm.last_results_map[ch] is None

        dB = sim_engine_with_models.devices_map['DEVICE:B']
        sim_engine_with_models.push_full_update_to_device(dB)

        dC = sim_engine_with_models.devices_map['DEVICE:C']
        sim_engine_with_models.push_full_update_to_device(dC)

        for ch in ['DEVICE:B']:
            assert acc.cm.last_results_map[ch] is not None

        for ch in ['DEVICE:C']:
            assert acc.cm.last_results_map[ch] is None

    @pytest.fixture
    def sim_engine_with_dummy_pvs(self, sim_engine_with_models):
        ao = pc.AcceleratorOptions(connection_settings=ConnectionOptions(network='dummy'))
        acc = pc.Accelerator(options=ao, ctx=sim_engine_with_models)
        pv_dict = {}

        for pvn in ['DEVICE:A', 'DEVICE:B']:
            pv_settings = PVOptions(name=pvn, low=0.0, high=5.0,
                                    security=PVAccess.RW)
            pv = SimPV(pv_settings)
            acc.add_pv_object([pv])
            pv_dict[pvn] = pv

            dev = sim_engine_with_models.devices_map[pvn]
            sim_engine_with_models.push_full_update_to_device(dev)

        for pvn in ['DEVICE:C']:
            pv_settings = PVOptions(name=pvn, low=0.0, high=5.0,
                                    security=PVAccess.RO)
            pv = SimPV(pv_settings)
            acc.add_pv_object([pv])
            pv_dict[pvn] = pv

            dev = sim_engine_with_models.devices_map[pvn]
            sim_engine_with_models.push_full_update_to_device(dev)

        return sim_engine_with_models, acc, pv_dict

    def test_interlock_simple(self, sim_engine_with_dummy_pvs):
        sim_engine, acc, pv_dict = sim_engine_with_dummy_pvs

        interlock_limits = {'DEVICE:A': (-1.0, 1.0),
                            'DEVICE:B': (-1.0, None),
                            'DEVICE:C': (-1.0, 1.0)
                            }
        pv_list = ['DEVICE:A', 'DEVICE:B', 'DEVICE:C']
        pv1, pv2, pv3 = [pv_dict[x] for x in pv_list]
        lopt = LimitInterlockOptions(pv_list=pv_list,
                                     read_events=[],
                                     write_events=pv_list,
                                     limits=interlock_limits)
        ilock = LimitInterlock(options=lopt)
        acc.add_interlock(ilock)

        with pytest.raises(SecurityError):
            pv3.write(2.6)

        assert acc.cm.last_results_map['DEVICE:B'] is not None
        assert acc.cm.last_results_map['DEVICE:C'] is not None, acc.cm.last_results_map

        with pytest.raises(InterlockWriteError):
            pv1.write(1.4)

        with pytest.raises(InterlockWriteError):
            pv2.write(-1.4)

        #print(ilock.__dict__)
        pv2.write(1.4)

        assert sim_engine.read_channel('DEVICE:B') == 1.4

        acc.pm.stop_interlock(ilock)
        time.sleep(0.1)
        pid = acc.pm.id_map[ilock.uuid]
        p, queue_out, queue_in, interlock = acc.pm.queue_map[pid]
        assert p.exitcode == -15

    @pytest.fixture
    def sim_engine_with_dummy_pvs_rb(self, sim_engine_with_models):
        ao = pc.AcceleratorOptions(connection_settings=ConnectionOptions(network='dummy'))
        acc = pc.Accelerator(options=ao, ctx=sim_engine_with_models)
        pv_dict = {}

        for pvn in ['DEVICE:A', 'DEVICE:B']:
            pv_settings = PVOptions(name=pvn, low=0.0, high=5.0,
                                    security=PVAccess.RW)
            pv = SimPV(pv_settings)
            acc.add_pv_object([pv])
            pv_dict[pvn] = pv

        for pvn in ['DEVICE:A_RB', 'DEVICE:B_RB']:
            pv_settings = PVOptions(name=pvn, security=PVAccess.RO)
            pv = SimPV(pv_settings)
            acc.add_pv_object([pv])
            pv_dict[pvn] = pv

        for pvn in ['DEVICE:A', 'DEVICE:B']:
            dev = sim_engine_with_models.devices_map[pvn]
            sim_engine_with_models.push_full_update_to_device(dev)

        for pvn in ['DEVICE:C']:
            pv_settings = PVOptions(name=pvn, security=PVAccess.RO)
            pv = SimPV(pv_settings)
            acc.add_pv_object([pv])
            pv_dict[pvn] = pv

            dev = sim_engine_with_models.devices_map[pvn]
            sim_engine_with_models.push_full_update_to_device(dev)

        return sim_engine_with_models, acc, pv_dict

    def test_acc_rb(self, sim_engine_with_dummy_pvs_rb):
        sim_engine, acc, pv_dict = sim_engine_with_dummy_pvs_rb
        pv_list = ['DEVICE:A', 'DEVICE:A_RB', 'DEVICE:B', 'DEVICE:B_RB', 'DEVICE:C']
        pv1, pv1rb, pv2, pv2rb, pv3 = [pv_dict[x] for x in pv_list]

        for pv in pv_list:
            assert acc.cm.last_results_map[pv] is not None

        assert set(acc.pv_names) == set(pv_list)
        assert set(acc.cm.subscribed_pv_names) == set(pv_list)

        r = pv1.read()
        assert r == 0.5
        assert pv1rb.read() == 0.5

        r = pv1.write(1.3)
        assert r is not None
        r = pv1.read()
        assert r == 1.3
        assert pv1rb.read() == 1.3

        with pytest.raises(ControlLibException):
            # too high
            pv1.write(6.0)
        assert pv1.read() == 1.3
        assert pv1rb.read() == 1.3

    def test_acc_time(self, sim_engine_with_dummy_pvs_rb):
        sim_engine, acc, pv_dict = sim_engine_with_dummy_pvs_rb
        pv_list = ['DEVICE:A', 'DEVICE:A_RB', 'DEVICE:B', 'DEVICE:B_RB', 'DEVICE:C']
        pv1, pv1rb, pv2, pv2rb, pv3 = [pv_dict[x] for x in pv_list]




