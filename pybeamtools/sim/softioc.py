import asyncio
import functools
import logging
from asyncio import AbstractEventLoop
from threading import Thread
from typing import Optional

import caproto
import nest_asyncio
import numpy as np
from caproto import SkipWrite
from caproto.asyncio.server import run
from caproto.server import SubGroup, pvproperty, PvpropertyDouble

from .core import SimulationEngine
from .devices import RealisticMagnet, StaticInputDevice
from ..controls.test_problems import Quadratic
from ..controls.virtual_tools import EPICSVirtualInput, AdaptivePVGroup, EPICSVirtualIOC, EPICSEchoGroup, EchoFactory

logger = logging.getLogger(__name__)


class SimController:
    def __init__(self, inputs, outputs, eval_fn=None) -> None:
        self.inputs = inputs
        self.outputs = outputs
        self.eval_fn = eval_fn

    def read(self, name):
        # print(f'SimCtr: request for {name}')
        assert name in self.outputs
        return self.eval_fn(name)


class SimpleBeamlineSoftIOC:
    def __init__(self, variables, objectives, test_variables=None, prefix='AI:'):
        self.prefix = prefix
        self.variables = variables
        self.objectives = objectives
        self.test_variables = test_variables
        self.obj_idx_map = {o: i for i, o in enumerate(objectives)}

    def setup(self):
        controller = SimController(self.variables, self.objectives)

        def eval_fn(name):
            return controller.read(name)

        class VirtualBeamline(AdaptivePVGroup):
            pass
            # def __new__(cls, *args, **kwargs):
            #    super().__new__(cls, *args, **kwargs)

        bl = VirtualBeamline(prefix=self.prefix)

        for i, el in enumerate(self.variables):
            mag = RealisticMagnet(value=0, low=-2, high=2, noise=None, resolution=None, model='instant')
            mag_grp = SubGroup(EPICSVirtualIOC, device=mag, input_name=el + ':AI', output_name=el + ':AO', prefix=el)
            setattr(bl, f'variable_{i}', mag_grp)

        for i, el_name in enumerate(self.objectives):
            output = StaticInputDevice(value=1.0)
            obj_grp = SubGroup(EPICSVirtualInput, device=output, input_name=el_name, prefix=el_name)
            setattr(bl, f'objective_{i}', obj_grp)

        # for i, (el1, el2) in enumerate(self.test_variables):
        #     el = StaticInputDevice(value=1.0)
        #     el_grp = SubGroup(EPICSVirtualIOC, device=el, input_name=el2, output_name=el1)
        #     setattr(bl, f'testvariable_{i}', el_grp)

        bl.update_pvs()
        bl._create_pvdb()
        logger.info(f'Soft IOC config:')
        logger.info(f'Vars: {self.variables}')
        logger.info(f'Objectives: {self.objectives}')
        logger.info(f'Test vars: {self.test_variables}')
        logger.info(f'PVDict: {bl.__dict__}')
        logger.info(f'PVDB: {bl.pvdb}')

        problem = Quadratic(n_var=len(self.variables))

        last_inputs: Optional[np.ndarray] = None
        last_results: Optional[np.ndarray] = None

        def get_objectives(obj):
            # print('getobj1')
            nonlocal last_results, last_inputs
            assert obj in self.objectives
            # gather inputs
            inputs = np.array([bl.pvdb[var].value for var in self.variables])
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
            logger.info(f'Requested value of {obj} @ {inputs} = {val}')
            return val

        controller.eval_fn = get_objectives

        self.bl = bl
        self.controller = controller

    def run(self):
        logger.info('Starting repeater')
        # repeater.spawn_repeater()
        nest_asyncio.apply()
        logger.info('Starting loop')
        run(self.bl.pvdb, log_pv_names=True, interfaces=['0.0.0.0'])

    def run_in_background(self, daemon=True):
        def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
            asyncio.set_event_loop(loop)
            logger.info('Starting loop in separate thread')
            run(self.bl.pvdb, log_pv_names=True, interfaces=['127.0.0.1'])  #
            # loop.run_forever()

        logger.info('Starting repeater')
        # repeater.spawn_repeater()
        loop = asyncio.new_event_loop()
        t = Thread(daemon=daemon, target=start_background_loop, args=(loop,))
        t.start()

class AsyncioQueue:
    def __init__(self, loop, maxsize=0, ):
        self._queue = asyncio.Queue(maxsize)
        self._loop = loop

    async def async_get(self):
        return await self._queue.get()

    async def async_put(self, value):
        return await self._queue.put(value)

    def get(self):
        future = asyncio.run_coroutine_threadsafe(
            self._queue.get(), self._loop)

        return future.result()

    def put(self, value):
        asyncio.run_coroutine_threadsafe(
            self._queue.put(value), self._loop)

class EchoIOC:
    def __init__(self, channels: list[str], sim_engine: SimulationEngine):
        self.sim_engine = sim_engine
        self.channels = channels
        self.bl: Optional[AdaptivePVGroup] = None
        self.loop: AbstractEventLoop = None
        for ch in channels:
            assert ch in self.sim_engine.channels

    def setup(self):
        logger.info(f'Setting up echo IOC with channels {self.channels}')

        class VirtualBeamline(AdaptivePVGroup):
            pass

        async def ai_getter(group, instance, channel):
            # value = group.device.read()
            value = self.sim_engine.read_channel(channel)
            logger.info(f'ai_getter {group=} {instance.pvname=}: {value=} {channel=}')
            return None

        async def ai_putter(group, instance, value, channel):
            # value = group.device.read()
            logger.info(f'ai_writer {group=} {instance.pvname=}: {value=} {channel=}')
            try:
                self.sim_engine.write_channel(channel, value)
            except Exception:
                # TODO: add more logging
                #raise SkipWrite
                raise
            return None
            # return value

        async def async_updater(group, instance, async_lib, channel, q):
            logger.info(f'SoftIOC updater for {channel=} starting')
            try:
                while True:
                    async_q = AsyncioQueue(asyncio.get_running_loop())
                    q.queues[channel] = async_q
                    #logger.info(f'SoftIOC updater for {channel=} starting 2')
                    data = await async_q.async_get()
                    logger.debug(f'SoftIOC updater for {channel=} received {data=}')
                    await instance.write(data, verify_value=False)
            except Exception as ex:
                logger.error(f'SoftIOC {channel=} exception {ex}')
            finally:
                logger.warning(f'Updater for {channel=} is exiting')

        self.bl = bl = VirtualBeamline(prefix='')
        self.queues = {}
        for i, channel in enumerate(self.channels):
            ch = channel
            j = 0
            props = {}
            #self.queues[channel] = async_q = AsyncioQueue(self.loop)
            updater = functools.partial(async_updater, channel=ch, q=self)
            props[f'property_{j}'] = pvproperty(record='ai',
                                                doc=f'echo_{i}',
                                                name=ch,
                                                value=0.0,
                                                dtype=PvpropertyDouble,
                                                get=functools.partial(ai_getter, channel=ch),
                                                put=functools.partial(ai_putter, channel=ch),
                                                startup=updater)
            #props[f'property_{j}'].scan(5.0)
            echo_cls = EchoFactory.make(channels=props)
            #logger.debug(f'Echo class {echo_cls} {echo_cls.__dict__=}')
            mag_grp = SubGroup(echo_cls,
                               channel=ch,
                               # read_fun=eval_fn,
                               prefix='')
            setattr(bl, f'channel_{i}', mag_grp)
            #logger.info(f'{mag_grp.group_dict=}')
            #logger.info(f'{mag_grp.__dict__=}')

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

    def send_updates(self, channel, data):
        # logger.info(f'Pong')
        assert channel in self.channels
        logger.info(f'Sending {data=} to echo channel {channel=}')
        q = self.queues[channel]
        q.put(data)
        #self.loop.call_soon_threadsafe(q._queue.put_nowait, data)
        #result = future.result()
        #logger.info(f'Got result {q._queue.qsize()}')

    def ping(self):
        logger.info(f'Pong')
        return 'pong'

    def run(self):
        nest_asyncio.apply()
        logger.info('Starting loop')
        run(self.bl.pvdb, log_pv_names=True, interfaces=['0.0.0.0'])

    def run_in_background(self, daemon=True):
        def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
            self.loop = loop = asyncio.new_event_loop()
            loop.set_debug(True)
            asyncio.set_event_loop(loop)
            logger.info(f'Starting loop {loop=}')
            run(self.bl.pvdb, log_pv_names=True, interfaces=['127.0.0.1'])  #
            # loop.run_forever()

        t = Thread(daemon=daemon, target=start_background_loop, args=(None,))
        logger.info(f'Starting thread {t=}')
        t.start()
