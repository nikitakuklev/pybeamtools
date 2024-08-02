import asyncio
import functools
import logging
import multiprocessing
import os
import signal
import time
from asyncio import AbstractEventLoop
from threading import Thread
from typing import Any, Optional

import caproto
import nest_asyncio
import numpy as np
from caproto import ChannelNumeric, ChannelType, SkipWrite
from caproto._data import _read_only_property
from caproto.asyncio.server import AsyncioAsyncLayer, Context, run
from caproto.server import SubGroup, pvproperty, PvpropertyDouble, PVSpec
from caproto.server.typing import AsyncLibraryLayer, T_contra

from pybeamtools.sim.core import SignalEngine
from .models import RealisticMagnet, StaticInputDevice
from ..controls.test_problems import Quadratic
from ..controls.virtual_tools import (
    AdaptivePVGroup,
    EchoFactory,
)

logger = logging.getLogger(__name__)


class SimController:
    def __init__(self, inputs, outputs, eval_fn=None) -> None:
        self.inputs = inputs
        self.outputs = outputs
        self.eval_fn = eval_fn

    def read(self, name):
        assert name in self.outputs
        return self.eval_fn(name)


class AsyncioQueue:
    def __init__(
            self,
            loop,
            maxsize=0,
    ):
        self._queue = asyncio.Queue(maxsize)
        self._loop = loop

    async def async_get(self):
        #logger.debug(f"Getting from queue {self=}")
        r = await self._queue.get()
        #logger.debug(f"Got {r} from queue {self=}")
        return r

    async def async_put(self, value):
        return await self._queue.put(value)

    def get(self):
        future = asyncio.run_coroutine_threadsafe(self._queue.get(), self._loop)
        return future.result()

    def put(self, value):
        #logger.debug(f"Putting {value} to queue {self=}")
        future = asyncio.run_coroutine_threadsafe(self._queue.put(value), self._loop)
        #logger.debug(f"Put {future} to queue {self=}")
        return future.result()
        # return self._loop.call_soon_threadsafe(self._queue.put_nowait, value)


class SoftIOC:
    def __init__(self, interfaces=None, debug=False):
        self.pvdb = None
        self.stop_requested = False
        self.thread_started = False
        self.ctx = None
        self.port = None
        self.background_thread = None
        self.thread_data = None
        self.loop = None
        self.extra_coro_queue = None
        interfaces = interfaces or ["127.0.0.1"]
        self.interfaces = interfaces

    def ping(self):
        logger.info("Pong")
        return "pong"

    def run(self):
        nest_asyncio.apply()
        logger.info("Starting loop")
        run(self.pvdb, log_pv_names=True, interfaces=self.interfaces)

    def run_in_current_loop(self):
        logger.info("Starting in current loop")
        run(self.pvdb, log_pv_names=True, interfaces=self.interfaces)

    def run_in_background(self, daemon=True):
        async def task_starter(async_lib):
            logger.debug(f"Starting extra coro task loop")
            while True:
                coro = await self.extra_coro_queue.async_get()
                logger.debug(f"Starting extra coro [{coro}]")
                await asyncio.create_task(coro(async_lib))

        async def startup_hook(async_lib):
            logger.debug("SoftIOC: starting startup hook for stop monitoring")
            self.port = self.ctx.port
            await asyncio.create_task(task_starter(async_lib))
            while True:
                # coro = await self.extra_coro_queue.async_get()
                # logger.info(f"Starting extra coro [{coro}]")
                # await asyncio.create_task(coro(async_lib))

                if self.stop_requested:
                    logger.warning("SoftIOC: hook detected stop request, exiting")
                    raise asyncio.CancelledError
                await async_lib.library.sleep(0.01)

        def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
            self.thread_started = True
            self.loop = loop = asyncio.new_event_loop()
            #async_lib = AsyncioAsyncLayer()
            loop.set_debug(True)
            asyncio.set_event_loop(loop)
            logger.info(f"Starting soft ioc in loop [{loop}]")

            async def start_server(pvdb, *, interfaces=None, log_pv_names=False,
                                   startup_hook=None
                                   ):
                """Start an asyncio server with a given PV database"""
                self.ctx = ctx = Context(pvdb, interfaces)
                self.thread_data = ctx
                self.extra_coro_queue = AsyncioQueue(loop)
                #asyncio.create_task(task_starter())
                logger.debug(f'Entering context run loop')
                return await ctx.run(log_pv_names=log_pv_names, startup_hook=startup_hook)

            coro = start_server(
                            self.pvdb,
                            interfaces=self.interfaces,
                            log_pv_names=True,
                            startup_hook=startup_hook,
                    )
            #asyncio.ensure_future(coro, loop=loop)
            #loop.create_task(coro)
            loop.run_until_complete(coro)
            logger.info(f"Server run method exited")
            self.thread_started = self.stop_requested = False

        t = Thread(daemon=daemon, target=start_background_loop, args=(None,))
        logger.info(f"Starting SoftIOC in thread [{t}]")
        self.background_thread = t
        t.start()
        return t

    def stop(self):
        logger.info(f"SoftIOC: stop requested")
        self.stop_requested = True
        for i in range(100):
            if not self.thread_started:
                logger.info(f"SoftIOC: thread stop OK")
                return
            time.sleep(0.01)
        raise Exception(f"SoftIOC: thread stop failed")

    def join(self):
        if self.background_thread is not None:
            self.background_thread.join()
        else:
            raise Exception("No thread to join")

    def process_task(self, loop: asyncio.AbstractEventLoop) -> None:
        loop = asyncio.new_event_loop()
        loop.set_debug(True)
        asyncio.set_event_loop(loop)
        logger.info(f"Starting loop {loop=}")
        run(self.pvdb, log_pv_names=True, interfaces=self.interfaces)

    def run_in_process(self):
        process = multiprocessing.Process(target=self.process_task)
        process.daemon = True
        logger.info(f"Starting process {process=}")
        process.start()
        logger.info(f"Started process {process=}")


class SimpleTuningIOC:
    def __init__(
            self,
            variables: list[str],
            objectives: list[str],
            test_variables=None,
            # prefix: str = 'AI:',
            noise=None,
    ):
        # self.prefix = prefix
        self.variables = variables
        self.objectives = objectives
        self.test_variables = test_variables
        self.device_dir = {}
        # self.pvprops_dict = {}
        self.obj_idx_map = {o: i for i, o in enumerate(objectives)}
        self.pvdb = None
        self.noise = noise

    def setup(self):
        controller = SimController(self.variables, self.objectives)

        async def var_put_handler(instance: T_contra, value: Any, *args):
            logger.debug(f"ai_writer {instance=} {value=}")
            if len(args) > 0:
                raise
            dev = self.device_dir[instance.name]
            logger.debug(f"Writing device {dev} -> {value}")
            dev.write(value)
            for obj in self.objectives:
                val = get_objectives(obj)
                logger.debug(f"Writing {obj} -> {val}")
                dev = self.device_dir[obj]
                dev.write(val)
                # logger.debug(f"Propagating {obj} to PV")
                # await self.pvprops_dict[obj].write(val)
                await self.pvdb[obj].write(val, verify_value=False)

        # async def obj_put_handler(instance: T_contra, value: Any, *args):
        #     logger.debug(f'objective writer {instance=} {value=}')
        #     dev = self.device_dir[instance.name]
        #     logger.debug(f'writing {dev=} -> {value=}')
        #     dev.write(value)

        async def get_handler(instance: T_contra, *args):
            logger.debug(f"ai_getter {instance=}")
            if len(args) > 0:
                raise
            value = self.device_dir[instance.name].read()
            logger.debug(f"Read {value} from PV {instance.name}")
            return value

        async def get_setp_handler(instance: T_contra, *args):
            logger.debug(f"ai_setp_getter {instance=}")
            if len(args) > 0:
                raise
            value = self.device_dir[instance.name].setpoint
            logger.debug(f"Read {value} from PV {instance.name}")
            return value

        async def startup_handler(
                instance: T_contra, async_lib: AsyncLibraryLayer, *args
        ):
            logger.info(f"Startup for {instance.name=}")
            dev = self.device_dir[instance.name]
            try:
                while True:
                    await async_lib.sleep(2)
                    value = dev.read()
                    logger.info(f"Update for {instance.name=} = {value}")
                    await instance.write(value, verify_value=False)  #
            except Exception as ex:
                logger.error(f"{instance.name=} exception {ex}")
            finally:
                logger.warning(f"{instance.name=} is exiting")

        all_specs = []
        self.input_names = []
        for i, el in enumerate(self.variables):
            mag = RealisticMagnet(
                    name=el,
                    value=0.0,
                    low=-5.0,
                    high=5.0,
                    noise=self.noise,
                    resolution=None,
                    model="exponential",
                    pmodel_kwargs={"decay_constant": 0.03},
            )
            pv_ai = pvproperty(
                    name=el,
                    value=mag.setpoint,
                    record="ai",
                    get=get_setp_handler,
                    put=var_put_handler,
                    upper_ctrl_limit=5.0,
                    lower_ctrl_limit=-5.0,
                    dtype=PvpropertyDouble,
            )
            pv_ao = pvproperty(
                    name=el + "_RB",
                    value=mag.value,
                    record="ao",
                    get=get_handler,
                    startup=startup_handler,
                    read_only=True,
                    dtype=PvpropertyDouble,
            )
            all_specs.append(pv_ai)
            all_specs.append(pv_ao)
            self.device_dir[el] = mag
            self.device_dir[el + "_RB"] = mag
            # self.pvprops_dict[el+':AI'] = pv_ai
            # self.pvprops_dict[el + ':AO'] = pv_ao
            self.input_names.append(el)

        for i, el in enumerate(self.objectives):
            output = StaticInputDevice(name=el, value=1.0)
            pv_out = pvproperty(
                    name=el,
                    value=output.value,
                    record="ao",
                    get=get_handler,
                    read_only=True,
                    startup=startup_handler,
                    dtype=PvpropertyDouble,
            )
            all_specs.append(pv_out)
            self.device_dir[el] = output
            # self.pvprops_dict[el] = pv_out

        pvdb = {
            pvspec.pvspec.name: pvspec.pvspec.create(group=None) for pvspec in all_specs
        }
        self.pvdb = pvdb

        logger.info("Soft IOC config:")
        logger.info(f"Vars: {self.variables}")
        logger.info(f"Objectives: {self.objectives}")
        logger.info(f"Test vars: {self.test_variables}")
        logger.info(f"PVDB: {pvdb}")
        for pvp in all_specs:
            logger.info(f"{pvp=}")

        problem = Quadratic(n_var=len(self.variables))

        last_inputs: Optional[np.ndarray] = None
        last_results: Optional[np.ndarray] = None

        def get_objectives(obj):
            nonlocal last_results, last_inputs
            assert obj in self.objectives
            # gather inputs
            inputs = np.array([self.device_dir[var].read() for var in self.input_names])
            inputs = inputs[None, :]
            assert inputs.shape == (1, len(self.variables))
            if last_inputs is not None and np.array_equal(inputs, last_inputs):
                results = last_results.copy()
            else:
                results = problem._evaluate(inputs)
                # print(results)
                assert results.shape == (1, len(self.objectives))
                last_inputs = inputs.copy()
                last_results = results
            val = results[0, self.obj_idx_map[obj]]
            # logger.debug(f'Inputs {self.input_names} = {inputs}
            # {[self.device_dir[var] for var in self.input_names]}')
            logger.info(f"Value of {obj} for {inputs} = {val}")
            return val

        controller.eval_fn = get_objectives
        self.controller = controller

    def run(self):
        nest_asyncio.apply()
        logger.info("Starting loop")
        run(
                self.pvdb,
                log_pv_names=True,
                # interfaces=['0.0.0.0']
                interfaces=["127.0.0.1"],
        )

    def run_in_background(self, daemon=True):
        def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
            asyncio.set_event_loop(loop)
            logger.info("Starting loop in separate thread")
            run(
                    self.pvdb,
                    log_pv_names=True,
                    interfaces=["0.0.0.0"],
                    # interfaces=['127.0.0.1']
            )

        loop = asyncio.new_event_loop()
        t = Thread(daemon=daemon, target=start_background_loop, args=(loop,))
        t.start()


class TestIOC:
    def __init__(
            self,
            variables: list[str],
            objectives: list[str],
            test_variables=None,
            prefix: str = "AI:",
    ):
        self.prefix = prefix
        self.variables = variables
        self.objectives = objectives
        self.test_variables = test_variables
        self.device_dir = {}
        self.obj_idx_map = {o: i for i, o in enumerate(objectives)}

    def setup(self):
        controller = SimController(self.variables, self.objectives)

        def eval_fn(name):
            return controller.read(name)

        async def put_handler(instance: T_contra, value: Any, *args):
            logger.info(f"ai_writer {instance=} {value=}")
            # logger.info(f'{args=}')
            dev = self.device_dir[instance.name]
            dev.write(value)

        async def get_handler(instance: T_contra, *args):
            logger.info(f"ai_getter {instance=}")
            # logger.info(f'{args=}')
            value = self.device_dir[instance.pvname].value
            logger.info(f"Read {value} from {instance.pvname}.")
            return value

        async def bad_put_handler(instance: T_contra, value: Any, *args):
            logger.info(f"ai_writer {instance=} {value=}")
            raise ValueError(instance.name)

        async def weird_get_handler(instance: T_contra, *args):
            logger.info(f"weird_get_handler {instance=} {instance.alarm=}")
            await instance.alarm.write(
                    status=caproto.AlarmStatus.READ,
                    severity=caproto.AlarmSeverity.MAJOR_ALARM,
                    alarm_string="alarm string",
            )
            # instance.write
            return None

        alarm = caproto.ChannelAlarm(
                status=caproto.AlarmStatus.READ,
                severity=caproto.AlarmSeverity.MINOR_ALARM,
                alarm_string="alarm string",
        )

        all_specs = []
        for i, el in enumerate(self.variables):
            mag = RealisticMagnet(
                    name=f"{i}",
                    value=0.0,
                    low=-2.0,
                    high=2.0,
                    noise=None,
                    resolution=None,
                    model="instant",
            )
            pv_ai = pvproperty(
                    name=self.prefix + f"variable_{i}:AI",
                    value=mag.value,
                    record="ai",
                    get=get_handler,
                    put=put_handler,
                    upper_ctrl_limit=2.0,
                    lower_ctrl_limit=-2.0,
                    dtype=PvpropertyDouble,
            )
            pv_ao = pvproperty(
                    name=self.prefix + f"variable_{i}:AO",
                    value=mag.value,
                    record="ao",
                    get=get_handler,
                    read_only=True,
                    dtype=PvpropertyDouble,
            )
            all_specs.append(pv_ai)
            all_specs.append(pv_ao)
            self.device_dir[self.prefix + f"variable_{i}:AI"] = mag
            self.device_dir[self.prefix + f"variable_{i}:AO"] = mag

        for i, el in enumerate(self.variables):
            mag = RealisticMagnet(
                    name=f"{i}F",
                    value=0.0,
                    low=-2.0,
                    high=2.0,
                    noise=None,
                    resolution=None,
                    model="instant",
            )
            pv_ai = pvproperty(
                    name=self.prefix + f"variable_{i}:AIF",
                    value=mag.value,
                    record="ai",
                    get=get_handler,
                    put=bad_put_handler,
                    upper_ctrl_limit=2.0,
                    lower_ctrl_limit=-2.0,
                    dtype=PvpropertyDouble,
            )
            pv_ao = pvproperty(
                    name=self.prefix + f"variable_{i}:AOF",
                    value=mag.value,
                    record="ao",
                    get=weird_get_handler,
                    read_only=True,
                    dtype=PvpropertyDouble,
            )
            all_specs.append(pv_ai)
            all_specs.append(pv_ao)
            self.device_dir[self.prefix + f"variable_{i}:AIF"] = mag
            self.device_dir[self.prefix + f"variable_{i}:AOF"] = mag

        for i, el_name in enumerate(self.objectives):
            output = StaticInputDevice(name=f"objective_{i}", value=1.0)
            pv_out = pvproperty(
                    name=self.prefix + f"objective_{i}",
                    value=output.value,
                    record="ao",
                    get=get_handler,
                    read_only=True,
                    dtype=PvpropertyDouble,
            )
            all_specs.append(pv_out)
            self.device_dir[self.prefix + f"objective_{i}"] = output

        pvdb = {
            pvspec.pvspec.name: pvspec.pvspec.create(group=None) for pvspec in all_specs
        }
        self.pvdb = pvdb

        logger.info("Soft IOC config:")
        logger.info(f"Vars: {self.variables}")
        logger.info(f"Objectives: {self.objectives}")
        logger.info(f"Test vars: {self.test_variables}")
        logger.info(f"PVDB: {pvdb}")
        for pvp in all_specs:
            logger.info(f"{pvp=}")

        problem = Quadratic(n_var=len(self.variables))

        last_inputs: Optional[np.ndarray] = None
        last_results: Optional[np.ndarray] = None

        def get_objectives(obj):
            # print('getobj1')
            nonlocal last_results, last_inputs
            assert obj in self.objectives
            # gather inputs
            inputs = np.array([self.pvdb[var].value for var in self.variables])
            inputs = inputs[None, :]
            assert inputs.shape == (1, len(self.variables))
            if last_inputs is not None and np.array_equal(inputs, last_inputs):
                results = last_results.copy()
            else:
                results = problem._evaluate(inputs)
                # print(results)
                assert results.shape == (1, len(self.objectives))
                last_inputs = inputs.copy()
                last_results = results
            val = results[0, self.obj_idx_map[obj]]
            logger.info(f"Requested value of {obj} @ {inputs} = {val}")
            return val

        controller.eval_fn = get_objectives

        self.controller = controller

    def run(self):
        # logger.info('Starting repeater')
        # repeater.spawn_repeater()
        nest_asyncio.apply()
        logger.info("Starting loop")
        run(self.pvdb, log_pv_names=True, interfaces=["0.0.0.0"])

    def run_in_background(self, daemon=True):
        def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
            asyncio.set_event_loop(loop)
            logger.info("Starting loop in separate thread")
            run(self.pvdb, log_pv_names=True, interfaces=["0.0.0.0"])
            # loop.run_forever()

        # logger.info('Starting repeater')
        # repeater.spawn_repeater()
        loop = asyncio.new_event_loop()
        t = Thread(daemon=daemon, target=start_background_loop, args=(loop,))
        t.start()


class EchoIOC(SoftIOC):
    """Soft IOC that mirror SE values"""

    def __init__(self, channels: list[str], sim_engine: SignalEngine):
        super().__init__()
        self.se = sim_engine
        self.channels = channels
        self.pvspecs: list[PVSpec] = []
        self.loop: AbstractEventLoop = None
        for ch in channels:
            assert ch in self.se.channels

    def setup(self):
        logger.info(f"Setting up echo IOC with channels {self.channels}")

        class VirtualBeamline(AdaptivePVGroup):
            pass

        async def ai_getter(group, instance, channel):
            # value = group.device.read()
            value = self.se.read_channel(channel)
            logger.info(f"ai_getter {instance.pvname=}: {value=} {channel=} {group=} ")
            return value

        async def ai_putter(group, instance, value, channel):
            # value = group.device.read()
            logger.info(f"ai_writer {instance.pvname=}: {value=} {channel=} {group=} ")
            try:
                self.se.write_channel(channel, value)
                # skip official write since callback will do it
                # return SkipWrite
            except Exception:
                # TODO: add more logging
                # raise SkipWrite
                raise
            return None
            # return value

        async def async_updater(group, instance, async_lib, channel, q):
            logger.debug(f"SoftIOC updater for {channel=} starting")
            try:
                while True:
                    async_q = AsyncioQueue(asyncio.get_running_loop())
                    q.queues[channel] = async_q
                    # logger.info(f'SoftIOC updater for {channel=} starting 2')
                    data = await async_q.async_get()
                    logger.debug(f"SoftIOC updater for {channel=} received {data=}")
                    await instance.write(data, verify_value=False)
            except Exception as ex:
                logger.error(f"SoftIOC {channel=} exception {ex}")
            finally:
                logger.warning(f"Updater for {channel=} is exiting")

        self.bl = bl = VirtualBeamline(prefix="")
        self.queues = {}
        for i, channel in enumerate(self.channels):
            ch = channel
            j = 0
            props = {}
            # self.queues[channel] = async_q = AsyncioQueue(self.loop)
            updater = functools.partial(async_updater, channel=ch, q=self)
            value = self.se.read_channel(channel)
            assert isinstance(value, float)
            props[f"property_{j}"] = pvproperty(
                    record="ai",
                    doc=f"echo_{i}",
                    name=ch,
                    value=value,
                    dtype=PvpropertyDouble,
                    get=functools.partial(ai_getter, channel=ch),
                    put=functools.partial(ai_putter, channel=ch),
                    startup=updater,
            )
            # props[f'property_{j}'].scan(5.0)
            echo_cls = EchoFactory.make(channels=props)
            # logger.debug(f'Echo class {echo_cls} {echo_cls.__dict__=}')
            mag_grp = SubGroup(
                    echo_cls,
                    channel=ch,
                    # read_fun=eval_fn,
                    prefix="",
            )
            setattr(bl, f"channel_{i}", mag_grp)
            # logger.info(f'{mag_grp.group_dict=}')
            # logger.info(f'{mag_grp.__dict__=}')

        # bl._create_pvdb()
        # logger.info(f'BL dict 0: {bl.__dict__}')
        # logger.info(f'BL base dict 0: {bl.__class__.__bases__[0].__dict__}')
        bl.update_pvs()
        # logger.info(f'BL dict 1: {bl.__dict__}')
        # logger.info(f'BL base dict 1: {bl.__class__.__bases__[0].__dict__}')
        # logger.info(f'BL pvdb {bl.pvdb=}')
        # logger.info(f'{bl.channel_0.__dict__=}')
        # logger.info(f'{bl.channel_0.group_cls.__dict__=}')
        # logger.info(f'{bl.channel_1.__dict__=}')
        # logger.info(f'{bl.channel_1.group_cls.__dict__=}')
        bl._create_pvdb()
        # logger.info(f'Soft IOC config:')
        # logger.info(f'Channels: {self.channels}')
        # logger.info(f'BL dict 2: {bl.__dict__}')
        # logger.info(f'PVDB: {bl.pvdb}')
        self.pvdb = bl.pvdb

    def send_updates(self, channel, data):
        # logger.info(f'Pong')
        assert channel in self.channels
        logger.info(f"EchoIOC sending {data=} to echo channel {channel=}")
        q = self.queues[channel]
        q.put(data)
        # self.loop.call_soon_threadsafe(q._queue.put_nowait, data)
        # result = future.result()
        # logger.info(f'Got result {q._queue.qsize()}')

    def set_failure_status(self, channel, status):
        assert channel in self.channels
        assert isinstance(status, bool)
        logger.info(f"Channel {channel} set failure to {status}")
        q = self.queues[channel]
        q.put({"op": "status", "data": status})


class EchoIOCV2(SoftIOC):
    """Soft IOC that mirror SE values"""

    def __init__(self, channels: list[str], se: SignalEngine):
        super().__init__()
        logger.info(f"Setting up echo IOC with channels {channels}")
        self.se = se
        self.channels = []
        self.pvspecs: list[PVSpec] = []
        self.queues = {}
        self.getter = self.putter = self.push_updater = None
        self.pvdb = {}
        self.getter, self.putter, self.push_updater = self.get_funcs()

        for i, channel in enumerate(channels):
            self.add_channel(channel)

    def get_funcs(self):
        async def ai_getter(instance, *args, channel):
            value = self.se.read_channel(channel)
            logger.info(
                    f"ai_getter {instance.pvname=}: {value=} {channel=} {instance=}"
            )
            # Does not work since does not update data without triggering subs
            # instance.write(value, verify_value=False)
            # Trick caproto to directly modify ChannelData, it will be returned by _read
            instance._data["value"] = value
            # Return none to avoid putter call
            return None

        async def ai_putter(instance, value, *args, channel):
            logger.info(
                    f"ai_writer {instance.pvname=}: {value=} {channel=} {instance=}"
            )
            try:
                self.se.write_channel(channel, value)
                # skip official write since callback will do it
                # return SkipWrite
            except Exception as ex:
                logger.error(f"Error writing {channel=} {ex} (rejecting)")
                raise SkipWrite
                # raise
            return None

        async def async_updater(instance: PvpropertyDouble,
                                async_lib: AsyncLibraryLayer,
                                *args,
                                channel: str, q
                                ):
            logger.info(f"SoftIOC updater for {channel=} starting")
            try:
                async_q = AsyncioQueue(asyncio.get_running_loop())
                q.queues[channel] = async_q
                while True:
                    # async_q = AsyncioQueue(asyncio.get_running_loop())
                    # q.queues[channel] = async_q
                    # logger.info(f'SoftIOC updater for {channel=} starting 2')
                    data = await async_q.async_get()
                    logger.debug(f"SoftIOC updater for {channel=} received {data=}")
                    await instance.write(data, verify_value=False)
            except Exception as ex:
                logger.error(f"SoftIOC {channel=} exception {ex}")
            finally:
                logger.warning(f"Updater for {channel=} is exiting")

        return ai_getter, ai_putter, async_updater

    def send_updates(self, channel: str, data: float):
        assert isinstance(data, float)
        # assert len(data) > 0
        assert channel in self.channels
        logger.info(f"EchoIOC sending {data=} to {channel=}")
        q = self.queues[channel]
        q.put(data)

    def set_failure_status(self, channel, status):
        assert channel in self.channels
        assert isinstance(status, bool)
        logger.info(f"Channel {channel} set failure to {status}")
        q = self.queues[channel]
        q.put({"op": "status", "data": status})

    def add_channel(self, channel: str):
        assert channel in self.se.channels
        if channel in self.pvdb:
            raise ValueError(f"Channel {channel} already exists")

        value = self.se.read_channel(channel)
        assert isinstance(
                value, float
        ), f"Invalid value {value} for {channel}"

        prop = pvproperty(
                record="ai",
                doc=f"echo_{channel}",
                name=channel,
                value=value,
                dtype=PvpropertyDouble,
                get=functools.partial(self.getter, channel=channel),
                put=functools.partial(self.putter, channel=channel),
                startup=functools.partial(self.push_updater, channel=channel, q=self),
        )
        self.pvdb[prop.pvspec.name] = prop.pvspec.create(group=None)
        self.channels.append(channel)
        logger.debug(f"Added channel {channel} to EchoIOC")

        # async def var_put_handler(instance: T_contra, value: Any, *args):
        #     logger.debug(f'ai_writer {instance=} {value=}')
        #     if len(args) > 0:
        #         raise
        #     dev = self.device_dir[instance.name]
        #     logger.debug(f"Writing device {dev} -> {value}")
        #     dev.write(value)
        #     for obj in self.objectives:
        #         val = get_objectives(obj)
        #         logger.debug(f"Writing {obj} -> {val}")
        #         dev = self.device_dir[obj]
        #         dev.write(val)
        #         # logger.debug(f"Propagating {obj} to PV")
        #         # await self.pvprops_dict[obj].write(val)
        #         await self.pvdb[obj].write(val, verify_value=False)
        #
        # # async def obj_put_handler(instance: T_contra, value: Any, *args):
        # #     logger.debug(f'objective writer {instance=} {value=}')
        # #     dev = self.device_dir[instance.name]
        # #     logger.debug(f'writing {dev=} -> {value=}')
        # #     dev.write(value)
        #
        # async def get_handler(instance: T_contra, *args):
        #     logger.debug(f'ai_getter {instance=}')
        #     if len(args) > 0:
        #         raise
        #     value = self.device_dir[instance.name].read()
        #     logger.debug(f"Read {value} from PV {instance.name}")
        #     return value
        #
        # async def get_setp_handler(instance: T_contra, *args):
        #     logger.debug(f'ai_setp_getter {instance=}')
        #     if len(args) > 0:
        #         raise
        #     value = self.device_dir[instance.name].setpoint
        #     logger.debug(f"Read {value} from PV {instance.name}")
        #     return value
        #
        # async def startup_handler(instance: T_contra, async_lib: AsyncLibraryLayer, *args):
        #     logger.info(f'Startup for {instance.name=}')
        #     dev = self.device_dir[instance.name]
        #     try:
        #         while True:
        #             await async_lib.sleep(2)
        #             value = dev.read()
        #             logger.info(f'Update for {instance.name=} = {value}')
        #             await instance.write(value, verify_value=False)  #
        #     except Exception as ex:
        #         logger.error(f'{instance.name=} exception {ex}')
        #     finally:
        #         logger.warning(f'{instance.name=} is exiting')


class DynamicIOC(SoftIOC):
    """ Soft IOC that just serves whatever is in the dictionary """

    def __init__(self, data: dict[str, float], **kwargs):
        super().__init__(**kwargs)
        self.data = data
        channels = list(data.keys())
        logger.info(f"Setting up dynamic IOC with channels {channels}")
        self.pvspecs: list[PVSpec] = []
        self.queues = {}
        # self.getter = self.putter = self.push_updater = None
        self.pvdb = {}
        self.getter, self.putter, self.push_updater = self.get_funcs()

        for i, (k, v) in enumerate(data.items()):
            self.add_channel(k, v)

        self.push_timestamps = {}

    @property
    def channels(self):
        return list(self.data.keys())

    def get_funcs(self):
        async def ai_getter(instance, *args, channel):
            value = self.data.get(channel)
            logger.info(
                    f"ai_getter {instance.pvname=}: {value=} {channel=} {instance=}"
            )
            # Does not work since does not update data without triggering subs
            # instance.write(value, verify_value=False)
            # Trick caproto to directly modify ChannelData, it will be returned by _read
            instance._data["value"] = value
            # Return none to avoid putter call
            return None

        async def ai_putter(instance, value, *args, channel):
            logger.info(
                    f"ai_writer {instance.pvname=}: {value=} {channel=} {instance=}"
            )
            try:
                self.data[channel] = value
                # skip official write since callback will do it
                # return SkipWrite
            except Exception as ex:
                logger.error(f"Error writing {channel=} {ex} (rejecting)")
                raise SkipWrite
                # raise
            return None

        async def push_updater(instance: PvpropertyDouble,
                               async_lib: AsyncLibraryLayer,
                               *args,
                               channel: str, q
                               ):
            logger.info(f"SoftIOC updater for {channel=} starting")
            try:
                async_q = AsyncioQueue(asyncio.get_running_loop())
                q.queues[channel] = async_q
                while True:
                    # async_q = AsyncioQueue(asyncio.get_running_loop())
                    # q.queues[channel] = async_q
                    # logger.info(f'SoftIOC updater for {channel=} starting 2')
                    data = await async_q.async_get()
                    logger.debug(f"SoftIOC updater for {channel=} received {data=}")
                    self.data[channel] = data
                    await instance.write(data, verify_value=False)
            except Exception as ex:
                logger.error(f"SoftIOC {channel=} exception {ex}")
            finally:
                logger.warning(f"Updater for {channel=} is exiting")

        return ai_getter, ai_putter, push_updater

    def send_updates(self, channel: str, data: float):
        assert isinstance(data, float)
        assert channel in self.channels
        logger.info(f"Sending [{channel=}] = [{data=}]")
        q = self.queues[channel]
        q.put(data)
        self.push_timestamps[channel] = time.time()

    def set_failure_status(self, channel: str, status: bool):
        assert channel in self.channels
        assert isinstance(status, bool)
        logger.info(f"Channel [{channel}] set failure to [{status}]")
        q = self.queues[channel]
        q.put({"op": "status", "data": status})

    def add_channel(self, channel: str, value: float):
        if channel in self.pvdb:
            raise ValueError(f"Channel {channel} already exists")

        assert isinstance(value, float), f"Invalid value {value} for {channel}"
        self.data[channel] = value
        startup_fun = functools.partial(self.push_updater, channel=channel, q=self)
        prop = pvproperty(
                record="ai",
                doc=f"echo_{channel}",
                name=channel,
                value=value,
                dtype=PvpropertyDouble,
                get=functools.partial(self.getter, channel=channel),
                put=functools.partial(self.putter, channel=channel),
                startup=startup_fun,
                precision=6
        )
        self.pvdb[prop.pvspec.name] = spec = prop.pvspec.create(group=None)
        self.channels.append(channel)

        # MEGA HACK TO ADD NEW STARTUP METHOD TO RUNNING TASKS
        if self.background_thread is not None:
            logger.debug(f"Adding channel {channel} to coro startup requests as late addition")
            assert self.extra_coro_queue is not None
            self.extra_coro_queue.put(spec.server_startup)
        # while channel not in self.queues:
        #    time.sleep(0.5)
        #import faulthandler, signal
        #faulthandler.enable()
        #signal.raise_signal(signal.SIGABRT)
        logger.debug(f"Added channel {channel}")


def DynamicPVDB():
    def __init__(self):
        self.handlers = {}

    def __getitem__(self, key):
        return self.handlers[key]

    def __setitem__(self, key, value):
        self.handlers[key] = value


class ChannelCustomDouble(ChannelNumeric):
    data_type = ChannelType.DOUBLE

    def __init__(self, *, precision=0, **kwargs):
        super().__init__(**kwargs)

        self._data['precision'] = precision

    precision = _read_only_property('precision')

    def __getnewargs_ex__(self):
        args, kwargs = super().__getnewargs_ex__()
        kwargs['precision'] = self.precision
        return (args, kwargs)
