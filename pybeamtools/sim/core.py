import logging
import queue
import sys
import threading
import time
from collections import deque
from enum import Enum
from typing import Annotated, Any, Callable, Optional, Union

import numpy as np
from pydantic import Field

from .errors import MissingDependencyError, SimulationError
from .pddevices import ALL_DEVICE_OPTIONS_CLASS_TYPE, EngineDevice, TRIGSPEC
from ..utils.pydantic import SerializableBaseModel

TRACE = False
TIME_TRACE = False


# class DeviceSubscription:
#     def __init__(self, device: VirtualDevice, engine):
#         self.device = device
#         self.name = self.device.name
#         self.engine = engine
#         self.callbacks: list[Callable] = []
#         self.logger = logging.getLogger(self.__class__.__qualname__)
#         self.lock = threading.Lock()
#
#     def add_callback(self, cb: Callable):
#         assert isinstance(cb, Callable)
#         with self.lock:
#             self.callbacks.append(cb)
#
#     def process_update(self, value):
#         with self.lock:
#             if self.engine.TRACE:
#                 self.logger.debug(f'Running ({len(self.callbacks)}) callbacks for device ({self.name})')
#             for i, cb in enumerate(self.callbacks):
#                 try:
#                     cb(self, value)
#                 except Exception as ex:
#                     self.logger.error(f'Callback {i=} {cb} on device {self.name} resulted in exception {ex}',
#                                       exc_info=sys.exc_info())


class ChannelSubscription:
    def __init__(self, channel: str, engine):
        self.channel = channel
        self.name = channel
        self.engine = engine
        self.callbacks = []
        self.logger = logging.getLogger(self.__class__.__qualname__)
        self.lock = threading.Lock()

    def add_callback(self, cb: Callable):
        assert isinstance(cb, Callable)
        with self.lock:
            self.callbacks.append(cb)

    def process_update(self, value):
        with self.lock:
            if self.engine.TRACE:
                self.logger.debug(
                        f'Running ({len(self.callbacks)}) callbacks for channel ({self.name})')
            for i, cb in enumerate(self.callbacks):
                try:
                    cb(self, value)
                except Exception as ex:
                    self.logger.error(
                            f'Callback {i=} {cb} on channel {self.name} resulted in exception {ex}',
                            exc_info=sys.exc_info())


# class Measurement:
#     def __init__(self, data: np.ndarray, timestamp: float):
#         self.metadata = Metadata()
#         self.metadata.timestamp = timestamp
#         self.data = data
#
#     data_count = property(lambda self: len(self.data))


class History:
    def __init__(self, se, channel_name: str):
        self.name = channel_name
        self.q = deque(maxlen=se.options.history_length)

    def __len__(self):
        return len(self.q)

    def append(self, v):
        self.q.append(v)

    def to_list(self):
        return list(self.q)

    # data_count = property(lambda self: len(self.q))


class DEVICE_STATE(Enum):
    INITIALIZED = 0
    RUNNING = 1
    PAUSED = 2
    ERROR_DEPENDENCIES = 3
    ERROR_UPDATE = 4


class SignalEngineOptions(SerializableBaseModel):
    history_length: int = 1000
    time_function: Callable

    devices: list[Annotated[ALL_DEVICE_OPTIONS_CLASS_TYPE, Field(discriminator='device_type')]] = []
    # devices: list[DeviceOptions] = []
    periods: dict[str, float] = {}


TYPE_DATA = Union[float, str, int, None]


class Event:
    def __init__(self, op, txid: int, t_event: float, data: dict[str, TYPE_DATA]):
        self.op = op
        self.txid = txid
        self.t_event = t_event
        self.data = data


class SimulationEngine:
    def __init__(self, options: SignalEngineOptions):
        self.options = self.o = options
        self.logger = logging.getLogger(self.__class__.__qualname__)
        self.TRACE = False
        self.TIME_TRACE = False
        #
        self.devices_list: list[EngineDevice] = []
        self.devices_name_list: list[str] = []
        self.devices_map: dict[str, EngineDevice] = {}
        self.devices_dependencies_map: dict[str, list[str]] = {}
        self.devices_channels_map: dict[str, list[str]] = {}
        self.devices_state: dict[str, DEVICE_STATE] = {}
        # self.device_subs: dict[str, DeviceSubscription] = {}
        #
        self.channels_map_chain: dict[str, list[str]] = {}
        self.channels_dep_chain: dict[str, list[str]] = {}
        self.channels: list[str] = []
        self.channel_to_device: dict[str, EngineDevice] = {}
        self.channel_subs: dict[str, ChannelSubscription] = {}
        #
        # self.periods: dict[str, float] = {}
        self.times = []
        self.next_periodic_read_time: dict[str, float] = {}

        self.latest_data: dict[str, TYPE_DATA] = {}
        self.latest_data_timestamp: dict[str, Optional[float]] = {}
        self.history_data: dict[str, History] = {}
        self.history_data_timestamp: dict[str, History] = {}
        #
        self.is_running: bool = False
        self.cmdq = None
        self.poll_thread: Optional[threading.Thread] = None
        self.settings_lock = threading.Lock()
        self.fatal_error = False

        #
        self.update_queue = queue.Queue()
        self.update_command_queue = queue.Queue()
        self.update_thread = None
        self.update_thread_running = False

        time_fun = options.time_function
        if time_fun is None:
            self.time_fun = time.time
        else:
            self.time_fun = time_fun
        self.last_sim_time: float = self.time()

        self.txid = 0
        self.start_update_thread()

    # def serialize(self):
    # @property
    # def devices_list(self):
    #     return self.options.devices

    @property
    def periods(self):
        return self.options.periods

    def time(self):
        try:
            t = self.time_fun()
            return t
        except Exception as ex:
            self.logger.error(f'Time function failed', exc_info=sys.exc_info())
            raise ex

    def add_device(self, device: EngineDevice, period: float = None):
        with self.settings_lock:
            if device.name in self.devices_map:
                raise SimulationError(f'Device ({device.name}) is already added')
            deps_list = []
            for output, dependencies in device.channel_map.items():
                if output in self.channels_map_chain:
                    raise SimulationError(f'Channel ({output}) already exists')
                for dep, trig in dependencies.items():
                    assert isinstance(dep, str)
                    assert isinstance(trig, TRIGSPEC), f'Trigger {trig} is not valid'
                    # if dep not in self.channels_map_chain:
                    #    raise SimulationError(f'Dependency ({dep}) of channel ({output}) unknown')
                    deps_list.append(dep)
            deps_list = list(set(deps_list))
            self.options.devices.append(device.options)
            self.devices_list.append(device)
            self.devices_name_list.append(device.name)
            self.devices_map[device.name] = device
            self.devices_channels_map[device.name] = list(device.channel_map.keys())
            self.devices_dependencies_map[device.name] = deps_list

            for output, dependencies in device.channel_map.items():
                self.channels_map_chain[output] = dependencies
                for dep, trig in dependencies.items():
                    if dep not in self.channels_dep_chain:
                        self.channels_dep_chain[dep] = []
                    if trig.value == TRIGSPEC.PROPAGATE.value:
                        self.channels_dep_chain[dep].append(output)
                self.channels.append(output)
                self.channel_to_device[output] = device
                self.history_data[output] = History(self, channel_name=output)
                self.history_data_timestamp[output] = History(self, channel_name=output)
                self.latest_data[output] = None
                self.latest_data_timestamp[output] = None

            if period is None:
                period = 0.0
            self.periods[device.name] = period

            self.devices_state[device.name] = DEVICE_STATE.PAUSED

            self.logger.debug(f'Added device ({device.name}) ({device.channel_map=})')

    def schedule_update(self, device_name: str = None):
        now = self.time()
        if device_name is None:
            for dn in self.devices_name_list:
                self.next_periodic_read_time[dn] = now
        else:
            assert device_name in self.devices_name_list
            self.next_periodic_read_time[device_name] = now

    def subscribe_channel(self, channel_name: str) -> ChannelSubscription:
        with self.settings_lock:
            if channel_name not in self.channels:
                raise SimulationError(f'Channel ({channel_name}) not found')
            if channel_name not in self.channel_subs:
                self.logger.debug(f'Created subscription for channel ({channel_name})')
                self.channel_subs[channel_name] = ChannelSubscription(channel=channel_name,
                                                                      engine=self)
        return self.channel_subs[channel_name]

    def _poll_thread(self, command_queue: queue.Queue):
        t = self.time()
        self.logger.debug(f'Hello from sim thread (id {threading.get_ident()}) at {t=}')
        i = 0
        while True:
            i += 1
            # if self.TRACE:
            #    self.logger.debug(f'Update loop {i=} at {self.time()}')
            threshold_time = self.time()
            t1 = time.perf_counter()
            self._time_step(threshold_time)
            t2 = time.perf_counter()

            # Check shutdown
            try:
                cmd = command_queue.get(timeout=0.1)
                if cmd is None:
                    self.logger.debug(f'Goodbye from simulation poll thread')
                    break
            except queue.Empty:
                pass

    def _time_step(self, threshold_time: float):
        self.last_sim_time = threshold_time
        if self.TIME_TRACE:
            self.logger.debug(f'Advancing sim to ({threshold_time})')
        # Other devices can be added from main thread but wont be polled this cycle
        device_names = self.devices_name_list.copy()
        i = 0
        while True:
            triggered_devices = []
            for dn in device_names:
                if self.periods[dn] > 0 and self.next_periodic_read_time[dn] <= threshold_time:
                    triggered_devices.append([self.next_periodic_read_time[dn], dn])
            sorted_triggered_devices = sorted(triggered_devices, key=lambda x: x[0])

            if len(sorted_triggered_devices) == 0:
                if self.TIME_TRACE:
                    self.logger.debug(f'Time step done ({i} cycles)')
                break
            else:
                if self.TRACE:
                    self.logger.debug(f'Devices to process: {sorted_triggered_devices}')
            t_scheduled, dn = sorted_triggered_devices[0]
            try:
                self.settings_lock.acquire()
                t_run = self.time()
                t1 = time.perf_counter()
                self._recursive_update(t_scheduled, t_run, dn)
                self.next_periodic_read_time[dn] += self.periods[dn]
                t4 = time.perf_counter()

                if t4 - t1 > 0.5 * self.periods[dn]:
                    logging.warning(
                            f'Device {dn} took ({t4 - t1:.4f})s, over half of period')
            except SimulationError as ex:
                self.logger.error(f'Exception for {dn=}', exc_info=sys.exc_info())
            finally:
                self.settings_lock.release()
            i += 1

    def _recursive_update(self, t_scheduled: float, t_run: float, dn: str, depth=0):
        if dn not in self.devices_name_list:
            return
        device = self.devices_map[dn]
        prefix = '>' * depth

        # Verify dependencies
        deps = self.devices_dependencies_map[dn]
        for dep in deps:
            if dep not in self.channels:
                self.devices_state[dn] = DEVICE_STATE.ERROR_DEPENDENCIES
            if dep not in self.latest_data or self.latest_data[dep] is None:
                raise Exception(f'{prefix}UP ({dn}): value of ({dep}) is missing')

        # Direct channels
        try:
            updated_channels = device.update(t_scheduled, t_run, self.latest_data)
            if updated_channels is None:
                updated_channels = {}
            for k, v in updated_channels.items():
                # TODO: Filter only those of device
                if k not in self.channels:
                    continue
                self.latest_data[k] = v
                self.latest_data_timestamp[k] = t_run
                self.history_data[k].append(v)
                self.history_data_timestamp[k].append(v)
        except Exception as ex:
            self.logger.error(f'Error reading ({dn=})', exc_info=sys.exc_info())
            return

        if self.TRACE:
            self.logger.debug(f'{prefix}UP ({dn}): result ({updated_channels})')

        # Trigger channel subscriptions
        for channel, value in updated_channels.items():
            if channel not in self.channel_subs:
                continue
            try:
                # channel_value = device.read(t_scheduled, t_run, channel)
                if self.TRACE:
                    self.logger.debug(
                            f'{prefix}UP ({dn}): subs for ({channel})=({value})')
                self.channel_subs[channel].process_update(value)
            except Exception as ex:
                self.logger.error(f'Channel ({channel}) callback fail',
                                  exc_info=sys.exc_info())

        # Begin propagating updates
        dn_list = []
        for channel in updated_channels:
            if channel not in self.channels_dep_chain:
                continue
            channel_deps = self.channels_dep_chain[channel]
            for dep in channel_deps:
                dn_list.append(self.channel_to_device[dep].name)
        dn_list = list(set(dn_list))
        if TRACE:
            self.logger.debug(f'{prefix}UP ({dn}): propagating to ({dn_list})')
        for device_name in dn_list:
            self._recursive_update(t_scheduled, t_run, device_name, depth=depth + 1)
        # updated_channels = self.devices_map[dn].update(t_scheduled, t_run, self.latest_data)

    def read_channel(self, channel_name: str):
        """ Read from channel """
        with self.settings_lock:
            if channel_name not in self.channels:
                raise SimulationError(f'Channel ({channel_name}) not available')
            self.logger.debug(f'Reading channel ({channel_name})')
            deps = self.channels_map_chain[channel_name]
            for dep in deps:
                if dep not in self.latest_data:
                    raise Exception(f'Missing dep ({dep})for channel ({channel_name})')
                if self.latest_data[dep] is None:
                    raise Exception(f'Last value of ({dep}) for channel ({channel_name}) is None')
            device = self.channel_to_device[channel_name]
            now = self.time()
            value = device.read(t_sched=None, t_run=now, channel_name=channel_name)
            return value

    # def write_channel(self, channel_name: str, value: Any):
    #     """ Write to a channel """
    #     with self.settings_lock:
    #         assert channel_name in self.channels
    #         self.logger.debug(f'Writing ({value}) to channel ({channel_name})')
    #         values_dict = {channel_name: value}
    #         self.channel_to_device[channel_name].write(None, self.time(), values_dict)

    def write_channel(self, channel_name: str, value: Any):
        """ Write to a channel """
        with self.settings_lock:
            assert channel_name in self.channels
            self.logger.debug(f'Generating write event {channel_name}={value}')
            ev = Event(op='write', txid=self._get_next_txid(), t_event=self.time(),
                       data={channel_name: value})
            self.update_queue.put(ev)

    def get_deps_tree(self, channel_name: str):
        """ Get deps tree """
        assert channel_name in self.channels
        deps = self.channels_map_chain[channel_name]
        deps_dict = {}
        for dep in deps:
            if dep not in self.channels_map_chain:
                deps_dict[dep] = False
            else:
                deps_dict[dep] = self.get_deps_tree(dep)
        tree = {channel_name: deps_dict}
        return tree

    def get_deps_list(self, channel_name: str):
        """ Get full flattened list of deps"""
        assert channel_name in self.channels
        deps = self.channels_map_chain[channel_name]
        deps_list = []
        for dep in deps:
            if dep not in self.channels_map_chain:
                raise MissingDependencyError(f'Channel ({dep}) not available')
            deps_list.extend(self.get_deps_list(dep))
        return list(set(deps_list))

    def _get_next_txid(self):
        txid = self.txid
        txid += 1
        return txid

    def notify_update_available(self, device: EngineDevice, update_data: dict[str, TYPE_DATA]):
        """ Notify engine that a new value is available """
        assert device.name in self.devices_name_list
        for channel_name, data in update_data.items():
            assert channel_name in self.channels, f'Channel {channel_name} missing?'
            assert channel_name in self.devices_channels_map, f' Channel {channel_name} ' \
                                                              f'registered to another device'

        ev = Event(op='update', txid=self._get_next_txid(), t_event=self.time(),
                   data=update_data.copy())
        self.update_queue.put(ev)

    def start_update_poll_thread(self, reset_update_time: bool = True):
        if self.is_running:
            raise SimulationError(f'Polling thread is already running')
        if reset_update_time:
            self.schedule_update()
        self.cmdq = queue.Queue()
        self.logger.debug(f'Starting poll thread')
        th = threading.Thread(target=self._poll_thread,
                              name='sim_engine_poll',
                              args=(self.cmdq,))
        th.daemon = True
        th.start()
        self.is_running = True
        self.poll_thread = th

    def stop_update_poll_thread(self):
        if not self.is_running:
            raise SimulationError(f'No thread to stop')
        self.cmdq.put(None)
        self.poll_thread.join(timeout=1.0)

        self.is_running = False
        self.cmdq = None
        self.poll_thread = None

    def _update_thread(self, update_q: queue.Queue, command_q: queue.Queue):
        self.logger.debug(f'Update thread (id {threading.get_ident()}) on')
        while True:
            try:
                event = update_q.get()
                with self.settings_lock:
                    for k, v in event.data:
                        if k not in self.channels:
                            self.logger.error('Channel %s missing, fatal', k)
                            raise Exception
                        device = self.channel_to_device[k]
                        dn = device.name
                        t_run = self.time()
                        if event.op == 'update':
                            if self.TRACE:
                                self.logger.debug(f'{event.txid} | Update ({k}={v}) at ({t_run})')
                            self._recursive_update(None, t_run, dn)
                        elif event.op == 'write':
                            if self.TRACE:
                                self.logger.debug(f'{event.txid} | Write ({k}={v}) at ({t_run})')
                            device.write(None, t_run, event.data)
            except queue.Empty:
                # Check shutdown
                try:
                    cmd = command_q.get(timeout=0.01)
                    if cmd is None:
                        self.logger.debug(f'Goodbye from update thread')
                        break
                except queue.Empty:
                    pass

    def start_update_thread(self):
        if self.update_thread_running:
            raise SimulationError(f'Update thread is already running')
        self.logger.debug(f'Starting update thread')
        th = threading.Thread(target=self._update_thread,
                              name='update_thread',
                              args=(self.update_queue, self.update_command_queue))
        th.daemon = True
        th.start()
        self.update_thread = th
        self.update_thread_running = True

    def stop_update_thread(self):
        if not self.update_thread_running:
            raise SimulationError(f'No thread to stop')
        self.update_command_queue.put(None)
        self.poll_thread.join(timeout=1.0)
        self.update_thread = None
        self.update_thread_running = False

    ### Periodic updates

    def get_channel_update_period(self, channel_name: str) -> float:
        assert channel_name in self.channels
        dev = self.channel_to_device[channel_name]
        return self.periods[dev.name]

    # def read_device(self, device_name: str):
    #     assert device_name in self.devices_list
    #     with self.settings_lock:
    #         self.logger.debug(f'Reading device ({device_name})')
    #         value = self.devices_list[device_name].read(t=self.time())
    #         return value

    # def write_device(self, device_name: str, value: Any):
    #     with self.settings_lock:
    #         self.devices_list[device_name].write(value, t=self.time())

# class ChannelMapSet:
#     def __init__(self, maps: list[ChannelMap]):
#         self.channel_maps = maps
#         self.output_to_map = {}
#         for m in maps:
#             if m.outputs in self.output_to_map:
#                 raise ValueError(f'Output ({m.outputs}) already exists in this mapper')
#             self.output_to_map[m.outputs] = m
#
#     def required_devices(self):
#         return list(set([c.device.name for c in self.channel_maps]))
#
#     def available_channels(self):
#         return list(set([c.outputs for c in self.channel_maps]))
#
#     def devices_to_channels(self) -> dict[str, list[str]]:
#         data = {}
#         for c in self.channel_maps:
#             if c.device.name not in data:
#                 data[c.device.name] = []
#             data[c.device.name] += [c.outputs]
#         for k, v in data.items():
#             data[k] = list(set(v))
#         # print(f'{data=}')
#         return data
#
#     def process_read(self, output_name: str) -> Union[str, int, float]:
#         return self.output_to_map[output_name].process_read()
#
#     def process_write(self, output_name: str, value) -> Union[str, int, float]:
#         return self.output_to_map[output_name].process_write(value)
