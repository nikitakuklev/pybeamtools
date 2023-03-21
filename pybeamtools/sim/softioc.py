import asyncio
import functools
import logging
import multiprocessing
from asyncio import AbstractEventLoop
from threading import Thread
from typing import Any, Optional

import caproto
import nest_asyncio
import numpy as np
from caproto import SkipWrite
from caproto.asyncio.server import run
from caproto.server import PVGroup, SubGroup, pvproperty, PvpropertyDouble, PVSpec
from caproto.server.typing import AsyncLibraryLayer, T_contra

from .core import SimulationEngine
from .devices import RealisticMagnet, StaticInputDevice
from ..controls.test_problems import Quadratic
from ..controls.virtual_tools import EPICSVirtualInput, AdaptivePVGroup, EPICSVirtualIOC, \
    EPICSEchoGroup, EchoFactory

logger = logging.getLogger(__name__)


class SimController:
    def __init__(self, inputs, outputs, eval_fn=None) -> None:
        self.inputs = inputs
        self.outputs = outputs
        self.eval_fn = eval_fn

    def read(self, name):
        assert name in self.outputs
        return self.eval_fn(name)


class SoftIOC:
    def __init__(self):
        self.pvdb = None

    def ping(self):
        logger.info(f'Pong')
        return 'pong'

    def run(self):
        nest_asyncio.apply()
        logger.info('Starting loop')
        run(self.pvdb, log_pv_names=True, interfaces=['127.0.0.1'])

    def run_in_current_loop(self):
        logger.info('Starting in current loop')
        run(self.pvdb, log_pv_names=True, interfaces=['127.0.0.1'])

    def run_in_background(self, daemon=True):
        def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
            self.loop = loop = asyncio.new_event_loop()
            loop.set_debug(True)
            asyncio.set_event_loop(loop)
            logger.info(f'Starting loop {loop=}')
            run(self.pvdb, log_pv_names=True,
                interfaces=['127.0.0.1'])

        t = Thread(daemon=daemon, target=start_background_loop, args=(None,))
        logger.info(f'Starting thread {t=}')
        t.start()
        return t

    def process_task(self, loop: asyncio.AbstractEventLoop) -> None:
        loop = asyncio.new_event_loop()
        loop.set_debug(True)
        asyncio.set_event_loop(loop)
        logger.info(f'Starting loop {loop=}')
        run(self.pvdb, log_pv_names=True,
            interfaces=['127.0.0.1'])

    def run_in_process(self):
        process = multiprocessing.Process(target=self.process_task)
        process.daemon = True
        logger.info(f'Starting process {process=}')
        process.start()
        logger.info(f'Started process {process=}')


class SimpleIOC:
    def __init__(self,
                 variables: list[str],
                 objectives: list[str],
                 test_variables=None,
                 # prefix: str = 'AI:',
                 noise=None
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
            logger.debug(f'ai_writer {instance=} {value=}')
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
            logger.debug(f'ai_getter {instance=}')
            if len(args) > 0:
                raise
            value = self.device_dir[instance.name].read()
            logger.debug(f"Read {value} from PV {instance.name}")
            return value

        async def get_setp_handler(instance: T_contra, *args):
            logger.debug(f'ai_setp_getter {instance=}')
            if len(args) > 0:
                raise
            value = self.device_dir[instance.name].setpoint
            logger.debug(f"Read {value} from PV {instance.name}")
            return value

        async def startup_handler(instance: T_contra, async_lib: AsyncLibraryLayer, *args):
            logger.info(f'Startup for {instance.name=}')
            dev = self.device_dir[instance.name]
            try:
                while True:
                    await async_lib.sleep(2)
                    value = dev.read()
                    logger.info(f'Update for {instance.name=} = {value}')
                    await instance.write(value, verify_value=False)  #
            except Exception as ex:
                logger.error(f'{instance.name=} exception {ex}')
            finally:
                logger.warning(f'{instance.name=} is exiting')

        all_specs = []
        self.input_names = []
        for i, el in enumerate(self.variables):
            mag = RealisticMagnet(name=el, value=0.0, low=-5.0, high=5.0, noise=self.noise,
                                  resolution=None, model='exponential', model_kwargs={
                    'decay_constant': 0.03
                })
            pv_ai = pvproperty(name=el, value=mag.setpoint,
                               record='ai', get=get_setp_handler, put=var_put_handler,
                               upper_ctrl_limit=5.0, lower_ctrl_limit=-5.0,
                               dtype=PvpropertyDouble)
            pv_ao = pvproperty(name=el + '_RB', value=mag.value,
                               record='ao', get=get_handler,
                               startup=startup_handler, read_only=True,
                               dtype=PvpropertyDouble)
            all_specs.append(pv_ai)
            all_specs.append(pv_ao)
            self.device_dir[el] = mag
            self.device_dir[el + '_RB'] = mag
            # self.pvprops_dict[el+':AI'] = pv_ai
            # self.pvprops_dict[el + ':AO'] = pv_ao
            self.input_names.append(el)

        for i, el in enumerate(self.objectives):
            output = StaticInputDevice(name=el, value=1.0)
            pv_out = pvproperty(name=el, value=output.value,
                                record='ao',
                                get=get_handler,
                                read_only=True,
                                startup=startup_handler,
                                dtype=PvpropertyDouble)
            all_specs.append(pv_out)
            self.device_dir[el] = output
            # self.pvprops_dict[el] = pv_out

        pvdb = {pvspec.pvspec.name: pvspec.pvspec.create(group=None) for pvspec in all_specs}
        self.pvdb = pvdb

        logger.info(f'Soft IOC config:')
        logger.info(f'Vars: {self.variables}')
        logger.info(f'Objectives: {self.objectives}')
        logger.info(f'Test vars: {self.test_variables}')
        logger.info(f'PVDB: {pvdb}')
        for pvp in all_specs:
            logger.info(f'{pvp=}')

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
            logger.info(f'Value of {obj} for {inputs} = {val}')
            return val

        controller.eval_fn = get_objectives
        self.controller = controller

    def run(self):
        nest_asyncio.apply()
        logger.info('Starting loop')
        run(self.pvdb, log_pv_names=True,
            # interfaces=['0.0.0.0']
            interfaces=['127.0.0.1']
            )

    def run_in_background(self, daemon=True):
        def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
            asyncio.set_event_loop(loop)
            logger.info('Starting loop in separate thread')
            run(self.pvdb, log_pv_names=True,
                interfaces=['0.0.0.0']
                # interfaces=['127.0.0.1']
                )

        loop = asyncio.new_event_loop()
        t = Thread(daemon=daemon, target=start_background_loop, args=(loop,))
        t.start()


class TestIOC:
    def __init__(self,
                 variables: list[str],
                 objectives: list[str],
                 test_variables=None,
                 prefix: str = 'AI:'
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
            logger.info(f'ai_writer {instance=} {value=}')
            # logger.info(f'{args=}')
            dev = self.device_dir[instance.name]
            dev.write(value)

        async def get_handler(instance: T_contra, *args):
            logger.info(f'ai_getter {instance=}')
            # logger.info(f'{args=}')
            value = self.device_dir[instance.pvname].value
            logger.info(f"Read {value} from {instance.pvname}.")
            return value

        async def bad_put_handler(instance: T_contra, value: Any, *args):
            logger.info(f'ai_writer {instance=} {value=}')
            raise ValueError(instance.name)

        async def weird_get_handler(instance: T_contra, *args):
            logger.info(f'weird_get_handler {instance=} {instance.alarm=}')
            await instance.alarm.write(status=caproto.AlarmStatus.READ,
                                       severity=caproto.AlarmSeverity.MAJOR_ALARM,
                                       alarm_string="alarm string")
            # instance.write
            return None

        alarm = caproto.ChannelAlarm(
                status=caproto.AlarmStatus.READ,
                severity=caproto.AlarmSeverity.MINOR_ALARM,
                alarm_string="alarm string",
        )

        all_specs = []
        for i, el in enumerate(self.variables):
            mag = RealisticMagnet(name=f'{i}', value=0.0, low=-2.0, high=2.0, noise=None,
                                  resolution=None, model='instant')
            pv_ai = pvproperty(name=self.prefix + f'variable_{i}:AI', value=mag.value,
                               record='ai', get=get_handler, put=put_handler,
                               upper_ctrl_limit=2.0, lower_ctrl_limit=-2.0,
                               dtype=PvpropertyDouble)
            pv_ao = pvproperty(name=self.prefix + f'variable_{i}:AO', value=mag.value,
                               record='ao', get=get_handler, read_only=True, dtype=PvpropertyDouble)
            all_specs.append(pv_ai)
            all_specs.append(pv_ao)
            self.device_dir[self.prefix + f'variable_{i}:AI'] = mag
            self.device_dir[self.prefix + f'variable_{i}:AO'] = mag

        for i, el in enumerate(self.variables):
            mag = RealisticMagnet(name=f'{i}F', value=0.0, low=-2.0, high=2.0, noise=None,
                                  resolution=None, model='instant')
            pv_ai = pvproperty(name=self.prefix + f'variable_{i}:AIF', value=mag.value,
                               record='ai', get=get_handler, put=bad_put_handler,
                               upper_ctrl_limit=2.0, lower_ctrl_limit=-2.0,
                               dtype=PvpropertyDouble)
            pv_ao = pvproperty(name=self.prefix + f'variable_{i}:AOF', value=mag.value,
                               record='ao', get=weird_get_handler, read_only=True,
                               dtype=PvpropertyDouble)
            all_specs.append(pv_ai)
            all_specs.append(pv_ao)
            self.device_dir[self.prefix + f'variable_{i}:AIF'] = mag
            self.device_dir[self.prefix + f'variable_{i}:AOF'] = mag

        for i, el_name in enumerate(self.objectives):
            output = StaticInputDevice(name=f'objective_{i}', value=1.0)
            pv_out = pvproperty(name=self.prefix + f'objective_{i}', value=output.value,
                                record='ao', get=get_handler, read_only=True,
                                dtype=PvpropertyDouble)
            all_specs.append(pv_out)
            self.device_dir[self.prefix + f'objective_{i}'] = output

        pvdb = {pvspec.pvspec.name: pvspec.pvspec.create(group=None) for pvspec in all_specs}
        self.pvdb = pvdb

        logger.info(f'Soft IOC config:')
        logger.info(f'Vars: {self.variables}')
        logger.info(f'Objectives: {self.objectives}')
        logger.info(f'Test vars: {self.test_variables}')
        logger.info(f'PVDB: {pvdb}')
        for pvp in all_specs:
            logger.info(f'{pvp=}')

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
            logger.info(f'Requested value of {obj} @ {inputs} = {val}')
            return val

        controller.eval_fn = get_objectives

        self.controller = controller

    def run(self):
        # logger.info('Starting repeater')
        # repeater.spawn_repeater()
        nest_asyncio.apply()
        logger.info('Starting loop')
        run(self.pvdb, log_pv_names=True, interfaces=['0.0.0.0'])

    def run_in_background(self, daemon=True):
        def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
            asyncio.set_event_loop(loop)
            logger.info('Starting loop in separate thread')
            run(self.pvdb, log_pv_names=True, interfaces=['0.0.0.0'])
            # loop.run_forever()

        # logger.info('Starting repeater')
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


class EchoIOC(SoftIOC):
    """ Soft IOC that mirror SE values """

    def __init__(self, channels: list[str], sim_engine: SimulationEngine):
        super().__init__()
        self.se = sim_engine
        self.channels = channels
        self.pvspecs: list[PVSpec] = []
        self.loop: AbstractEventLoop = None
        for ch in channels:
            assert ch in self.se.channels

    def setup(self):
        logger.info(f'Setting up echo IOC with channels {self.channels}')

        class VirtualBeamline(AdaptivePVGroup):
            pass

        async def ai_getter(group, instance, channel):
            # value = group.device.read()
            value = self.se.read_channel(channel)
            logger.info(f'ai_getter {instance.pvname=}: {value=} {channel=} {group=} ')
            return value

        async def ai_putter(group, instance, value, channel):
            # value = group.device.read()
            logger.info(f'ai_writer {instance.pvname=}: {value=} {channel=} {group=} ')
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
            logger.info(f'SoftIOC updater for {channel=} starting')
            try:
                while True:
                    async_q = AsyncioQueue(asyncio.get_running_loop())
                    q.queues[channel] = async_q
                    # logger.info(f'SoftIOC updater for {channel=} starting 2')
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
            # self.queues[channel] = async_q = AsyncioQueue(self.loop)
            updater = functools.partial(async_updater, channel=ch, q=self)
            value = self.se.read_channel(channel)
            assert isinstance(value, float)
            props[f'property_{j}'] = pvproperty(record='ai',
                                                doc=f'echo_{i}',
                                                name=ch,
                                                value=value,
                                                dtype=PvpropertyDouble,
                                                get=functools.partial(ai_getter, channel=ch),
                                                put=functools.partial(ai_putter, channel=ch),
                                                startup=updater)
            # props[f'property_{j}'].scan(5.0)
            echo_cls = EchoFactory.make(channels=props)
            # logger.debug(f'Echo class {echo_cls} {echo_cls.__dict__=}')
            mag_grp = SubGroup(echo_cls,
                               channel=ch,
                               # read_fun=eval_fn,
                               prefix='')
            setattr(bl, f'channel_{i}', mag_grp)
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
        logger.info(f'EchoIOC sending {data=} to echo channel {channel=}')
        q = self.queues[channel]
        q.put(data)
        # self.loop.call_soon_threadsafe(q._queue.put_nowait, data)
        # result = future.result()
        # logger.info(f'Got result {q._queue.qsize()}')

    def set_failure_status(self, channel, status):
        assert channel in self.channels
        assert isinstance(status, bool)
        logger.info(f'Channel {channel} set failure to {status}')
        q = self.queues[channel]
        q.put({'op': 'status', 'data': status})


class EchoIOCV2(SoftIOC):
    """ Soft IOC that mirror SE values """

    def __init__(self, channels: list[str], sim_engine: SimulationEngine):
        super().__init__()
        self.se = sim_engine
        self.channels = channels
        self.pvspecs: list[PVSpec] = []
        self.queues = {}
        for ch in channels:
            assert ch in self.se.channels

    def setup(self):
        logger.info(f'Setting up echo IOC with channels {self.channels}')

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

        async def ai_getter(instance, *args, channel):
            value = self.se.read_channel(channel)
            logger.info(f'ai_getter {instance.pvname=}: {value=} {channel=} {instance=}')
            # Does not work since does not update data without triggering subs
            #instance.write(value, verify_value=False)
            # Trick caproto to directly modify ChannelData, it will be returned by _read
            instance._data['value'] = value
            # Return none to avoid putter call
            return None

        async def ai_putter(instance, value, *args, channel):
            logger.info(f'ai_writer {instance.pvname=}: {value=} {channel=} {instance=}')
            try:
                self.se.write_channel(channel, value)
                # skip official write since callback will do it
                # return SkipWrite
            except Exception:
                # TODO: add more logging
                raise SkipWrite
                #raise
            return None

        async def async_updater(instance, async_lib, *args, channel, q):
            logger.info(f'SoftIOC updater for {channel=} starting')
            try:
                async_q = AsyncioQueue(asyncio.get_running_loop())
                q.queues[channel] = async_q
                while True:
                    # async_q = AsyncioQueue(asyncio.get_running_loop())
                    # q.queues[channel] = async_q
                    # logger.info(f'SoftIOC updater for {channel=} starting 2')
                    data = await async_q.async_get()
                    logger.debug(f'SoftIOC updater for {channel=} received {data=}')
                    await instance.write(data, verify_value=False)
            except Exception as ex:
                logger.error(f'SoftIOC {channel=} exception {ex}')
            finally:
                logger.warning(f'Updater for {channel=} is exiting')

        props = []
        for i, channel in enumerate(self.channels):
            value = self.se.read_channel(channel)
            assert isinstance(value, float), f'Invalid value {value} for channel {channel}'
            props.append(pvproperty(record='ai',
                                    doc=f'echo_{i}',
                                    name=channel,
                                    value=value,
                                    dtype=PvpropertyDouble,
                                    get=functools.partial(ai_getter, channel=channel),
                                    put=functools.partial(ai_putter, channel=channel),
                                    startup=functools.partial(async_updater, channel=channel, q=self)))

        pvdb = {pvspec.pvspec.name: pvspec.pvspec.create(group=None) for pvspec in props}
        self.pvdb = pvdb

    def send_updates(self, channel: str, data: float):
        assert isinstance(data, float)
        #assert len(data) > 0
        assert channel in self.channels
        logger.info(f'EchoIOC sending {data=} to {channel=}')
        q = self.queues[channel]
        q.put(data)

    def set_failure_status(self, channel, status):
        assert channel in self.channels
        assert isinstance(status, bool)
        logger.info(f'Channel {channel} set failure to {status}')
        q = self.queues[channel]
        q.put({'op': 'status', 'data': status})
