import concurrent
import logging
import queue
import sys
import threading
import time
import traceback
from collections import deque
from concurrent.futures import Future
from typing import Annotated, Callable, Optional

import numpy as np
from pydantic import Field, NonNegativeFloat, PositiveInt

from .errors import DeviceDependencyError, DeviceDisabledError, DeviceError, DeviceEventTimeout, \
    MissingDependencyError, \
    ReadTimeoutError, SimulationError, WriteTimeoutError
from .pddevices import AllOptionsT, DS, DataT, EngineDevice, Event, OP, Result, SignalContext, TRIG
from ..utils.logging import config_root_logging
from ..utils.pydantic import SerializableBaseModel

logger = logging.getLogger(__name__)


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

    def remove_callback(self, cb: Callable):
        assert isinstance(cb, Callable)
        with self.lock:
            self.callbacks.remove(cb)

    def process_update(self, value):
        with self.lock:
            if self.engine.TRACE:
                self.logger.debug(
                        f'Running ({len(self.callbacks)}) callbacks for CH ({self.name})')
            for i, cb in enumerate(self.callbacks):
                try:
                    if self.engine.TRACE:
                        self.logger.debug(f'Callback ({i}): ({cb})')
                    cb(self, value)
                except Exception as ex:
                    self.logger.error(
                            f'Callback {i=} {cb} on channel {self.name} resulted in exception {ex}',
                            exc_info=sys.exc_info())


class EventQueue(queue.PriorityQueue):
    def join_with_timeout(self, timeout=None):
        # if timeout and timeout < 0:
        #     raise ValueError("'timeout' must be a non-negative number")
        # with self.all_tasks_done:
        #     while self.unfinished_tasks:
        #         self.all_tasks_done.wait(timeout)
        self.all_tasks_done.acquire()
        try:
            if timeout is None:
                while self.unfinished_tasks:
                    self.all_tasks_done.wait()
            elif timeout < 0:
                raise ValueError("'timeout' must be a positive number")
            else:
                endtime = time.time() + timeout
                while self.unfinished_tasks:
                    remaining = endtime - time.time()
                    if remaining <= 0.0:
                        raise Exception
                    self.all_tasks_done.wait(remaining)
        finally:
            self.all_tasks_done.release()


# class Measurement:
#     def __init__(self, data: np.ndarray, timestamp: float):
#         self.metadata = Metadata()
#         self.metadata.timestamp = timestamp
#         self.data = data
#
#     data_count = property(lambda self: len(self.data))

class Measurement:
    def __init__(self, t=None, value=None, **kwargs) -> None:
        self.value = value
        self.time = t
        self.metadata = kwargs


class TimedHistory:
    def __init__(self, se, channel_name: str):
        self.name = channel_name
        self.q: deque[tuple[int, Measurement]] = deque(maxlen=se.options.history_length)
        self.mid = 0

    def __len__(self):
        return len(self.q)

    def __repr__(self):
        return f'TimedHistory of ({self.name}) at <{hex(id(self))}>: {len(self)} measurements '

    @property
    def size(self):
        return len(self.q)

    def next_mid(self):
        mid = self.mid
        self.mid += 1
        return mid

    def append(self, m: Measurement):
        assert isinstance(m, Measurement)
        # logger.debug(f'HIST ({self.name}) {len(self.q)=}: append')
        self.q.append((self.next_mid(), m))

    def to_list(self) -> list[tuple[int, Measurement]]:
        return list(self.q)

    def to_numpy(self, include_missing: bool = False) -> np.ndarray:
        return np.vstack(self.times_to_numpy(include_missing),
                         self.values_to_numpy(include_missing))

    def values_to_numpy(self, include_missing: bool = False) -> np.ndarray:
        if include_missing:
            return np.array([x[1].value for x in self.q], dtype=float)
        else:
            return np.array([x[1].value for x in self.q if x[1].value is not None],
                            dtype=float)

    def times_to_numpy(self, include_missing: bool = False) -> np.ndarray:
        if include_missing:
            return np.array([x[1].time for x in self.q], dtype=float)
        else:
            return np.array([x[1].time for x in self.q if x[1].value is not None],
                            dtype=float)

    def ts(self, t_start=None, t_end=None, mid_start=None) -> list[Measurement]:
        m_list: list[tuple[int, Measurement]] = self.to_list()
        m_subset = []
        for (mid, m) in m_list:
            if t_start is not None and m.time < t_start:
                continue
            if t_end is not None and m.time > t_end:
                continue
            if mid_start is not None and mid < mid_start:
                continue
            m_subset.append(m)
        return m_subset


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

    def to_numpy(self):
        return np.array(list(self.q))

    # data_count = property(lambda self: len(self.q))


class SignalEngineOptions(SerializableBaseModel):
    history_length: PositiveInt = 1000
    time_function: Callable

    devices: list[Annotated[AllOptionsT, Field(discriminator='device_type')]] = []
    # devices: list[DeviceOptions] = []
    periods: dict[str, float] = {}

    # timeouts
    readback_delay_min: NonNegativeFloat = 0.0
    readback_delay_max: Optional[NonNegativeFloat] = None

    # util
    update_thread_name: str = 'simupd'


class SimulationEngine:
    def __init__(self, options: SignalEngineOptions):
        config_root_logging()
        self.options = self.o = options
        self.logger = logging.getLogger(self.__class__.__qualname__)
        self.TRACE = False
        self.TIME_TRACE = False
        #
        self.devices_list: list[EngineDevice] = []
        self.devices_name_list: list[str] = []
        self.devices_map: dict[str, EngineDevice] = {}
        self.dev_deps_map: dict[str, list[str]] = {}
        self.dev_channels_map: dict[str, list[str]] = {}
        self.devices_state: dict[str, DS] = {}
        # self.device_subs: dict[str, DeviceSubscription] = {}
        #
        self.channels_map_chain: dict[str, list[str]] = {}
        self.channels_dep_chain: dict[str, list[str]] = {}
        self.channels: list[str] = []
        self.channel_to_device: dict[str, EngineDevice] = {}
        self.channel_to_device_name: dict[str, str] = {}
        self.channel_subs: dict[str, ChannelSubscription] = {}
        #
        # self.periods: dict[str, float] = {}
        self.times = []
        self.next_scan_time: dict[str, float] = {}
        #
        self.latest_data: dict[str, DataT] = {}
        self.latest_data_timestamp: dict[str, Optional[float]] = {}
        self.history_data: dict[str, History] = {}
        self.history_data_timestamp: dict[str, History] = {}
        self.history: dict[str, TimedHistory] = {}
        #
        self.is_running: bool = False
        self.cmdq = None
        self.poll_thread: Optional[threading.Thread] = None
        self.settings_lock = threading.RLock()
        self.fatal_error = False
        #
        self.event_q = EventQueue()
        self.event_command_q = queue.Queue()
        self.event_q_prio = queue.Queue()
        self.update_thread = None
        self.update_thread_running = False
        self.set_seen_txids = set()
        self.txid_map = {}

        time_fun = options.time_function
        if time_fun is None:
            self.time_fun = time.time
        else:
            self.time_fun = time_fun
        self.t_start = self.time()
        self.last_scan_threshold: float = self.time()
        self.scan_periods: dict[str, float] = {}

        self.ctx = SignalContext(self)

        self.txid = 0
        self.start_update_thread()

        #
        self.event_count = 0
        self.event_wall_time = 0.0
        self.time_created = time.perf_counter()

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

    def summarize(self):
        s = ''
        for dev in self.devices_map.values():
            s += f'Device ({dev.name}): ({dev.state}) | ({dev.channel_map}) '
        return s

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
                    assert isinstance(trig, TRIG), f'Trigger {trig} is not valid'
                    # if dep not in self.channels_map_chain:
                    #    raise SimulationError(f'Dependency ({dep}) of channel ({output}) unknown')
                    deps_list.append(dep)
            deps_list = list(set(deps_list))
            self.options.devices.append(device.options)
            self.devices_list.append(device)
            self.devices_name_list.append(device.name)
            self.devices_map[device.name] = device
            self.dev_channels_map[device.name] = list(device.channel_map.keys())
            self.dev_deps_map[device.name] = deps_list

            for output, dependencies in device.channel_map.items():
                self.channels_map_chain[output] = dependencies
                for dep, trig in dependencies.items():
                    if dep not in self.channels_dep_chain:
                        self.channels_dep_chain[dep] = []
                    if trig.value == TRIG.PROPAGATE.value:
                        self.channels_dep_chain[dep].append(output)
                self.channels.append(output)
                self.channel_to_device[output] = device
                self.channel_to_device_name[output] = device.name
                self.history_data[output] = History(self, channel_name=output)
                self.history_data_timestamp[output] = History(self, channel_name=output)
                self.history[output] = TimedHistory(self, channel_name=output)
                self.latest_data[output] = None
                self.latest_data_timestamp[output] = None

            if period is None:
                period = 0.0
            self.periods[device.name] = period

            sp = device.options.scan_period
            self.scan_periods[device.name] = sp
            self.next_scan_time[device.name] = self.time() + sp
            # else:
            #     self.next_scan_time[device.name] = None

            self.devices_state[device.name] = DS.PAUSED
            device.ctx = self.ctx
            self.logger.debug(f'Added device ({device.name}) ({device.channel_map=})')

    def enable_device(self, dev: EngineDevice, timeout=1.0):
        """ Enable device after creation or pausing """
        if dev.state == DS.CREATED:
            with self.settings_lock:
                assert dev in self.devices_list
                assert dev.ctx == self.ctx
                ev = Event(op=OP.ENABLE, dn=dev.name, txid=self.next_txid(), t_event=self.time())
                f = self.get_future_for_event(ev)
            result = self.await_future(f, timeout=timeout)
            if isinstance(result.data, Exception):
                raise result.data
            self.logger.debug(f'Device ({dev.name}) enabled')
            return result
        elif dev.state == DS.PAUSED:
            raise SimulationError(f'Device ({dev.name}) paused')
        else:
            raise SimulationError(f'Device ({dev.name}) wrong state ({dev.state})')

    def subscribe_channel(self, channel_name: str) -> ChannelSubscription:
        """ Get subscription for a channel """
        with self.settings_lock:
            if channel_name not in self.channels:
                raise SimulationError(f'Channel ({channel_name}) not found')
            if channel_name not in self.channel_subs:
                self.logger.debug(f'Created subscription for channel ({channel_name})')
                self.channel_subs[channel_name] = ChannelSubscription(channel=channel_name,
                                                                      engine=self)
        return self.channel_subs[channel_name]

    def process_events(self, timeout=5.0, root: int = None):
        # GRRRRR no timeout on queue.join()
        q = self.event_q
        self.logger.debug(f'Blocking to process ({q.unfinished_tasks}) events')
        # q.join_with_timeout(timeout)
        q.all_tasks_done.acquire()
        try:
            endtime = time.time() + timeout
            while q.unfinished_tasks:
                remaining = endtime - time.time()
                if remaining <= 0.0:
                    raise SimulationError('Timed out waiting for event processing')
                q.all_tasks_done.wait(remaining)
                self.logger.debug(f'Wait wake up at {time.time()}')
        finally:
            q.all_tasks_done.release()

    # def _time_step(self, threshold_time: float):
    #     self.last_sim_time = threshold_time
    #     if self.TIME_TRACE:
    #         self.logger.debug(f'Advancing sim to ({threshold_time})')
    #     # Other devices can be added from main thread but wont be polled this cycle
    #     device_names = self.devices_name_list.copy()
    #     i = 0
    #     while True:
    #         triggered_devices = []
    #         for dn in device_names:
    #             if self.periods[dn] > 0 and self.next_periodic_read_time[dn] <= threshold_time:
    #                 triggered_devices.append([self.next_periodic_read_time[dn], dn])
    #         sorted_triggered_devices = sorted(triggered_devices, key=lambda x: x[0])
    #
    #         if len(sorted_triggered_devices) == 0:
    #             if self.TIME_TRACE:
    #                 self.logger.debug(f'Time step done ({i} cycles)')
    #             break
    #         else:
    #             if self.TRACE:
    #                 self.logger.debug(f'Devices to process: {sorted_triggered_devices}')
    #         t_scheduled, dn = sorted_triggered_devices[0]
    #         try:
    #             self.settings_lock.acquire()
    #             t_run = self.time()
    #             t1 = time.perf_counter()
    #             self._recursive_update(t_scheduled, t_run, dn)
    #             self.next_periodic_read_time[dn] += self.periods[dn]
    #             t4 = time.perf_counter()
    #
    #             if t4 - t1 > 0.5 * self.periods[dn]:
    #                 logging.warning(
    #                         f'Device {dn} took ({t4 - t1:.4f})s, over half of period')
    #         except SimulationError as ex:
    #             self.logger.error(f'Exception for {dn=}', exc_info=sys.exc_info())
    #         finally:
    #             self.settings_lock.release()
    #         i += 1
    #
    # def _recursive_update(self, t_scheduled: float, t_run: float, dn: str, depth=0):
    #     """ This method is lock-shielded """
    #     assert self.settings_lock.locked()
    #     device = self.devices_map[dn]
    #     prefix = '>' * depth
    #
    #     # Verify dependencies
    #     deps = self.dev_deps_map[dn]
    #     for dep in deps:
    #         if dep not in self.channels:
    #             self.devices_state[dn] = DS.ERROR_DEPENDENCIES
    #         if dep not in self.latest_data or self.latest_data[dep] is None:
    #             raise Exception(f'{prefix}UP ({dn}): value of ({dep}) is missing')
    #
    #     # Direct channels
    #     try:
    #         updated_channels = device.update(t_run, self.latest_data)
    #         if updated_channels is None:
    #             updated_channels = {}
    #         for k, v in updated_channels.items():
    #             # TODO: Filter only those of device
    #             if k not in self.channels:
    #                 continue
    #             self.latest_data[k] = v
    #             self.latest_data_timestamp[k] = t_run
    #             self.history_data[k].append(v)
    #             self.history_data_timestamp[k].append(v)
    #     except Exception as ex:
    #         self.logger.error(f'Error reading ({dn=})', exc_info=sys.exc_info())
    #         return
    #
    #     if self.TRACE:
    #         self.logger.debug(f'{prefix}UP ({dn}): result ({updated_channels})')
    #
    #     # Trigger channel subscriptions
    #     for channel, value in updated_channels.items():
    #         if channel not in self.channel_subs:
    #             continue
    #         try:
    #             # channel_value = device.read(t_scheduled, t_run, channel)
    #             if self.TRACE:
    #                 self.logger.debug(
    #                         f'{prefix}UP ({dn}): subs for ({channel})=({value})')
    #             self.channel_subs[channel].process_update(value)
    #         except Exception as ex:
    #             self.logger.error(f'Channel ({channel}) input_var_change_callback fail',
    #                               exc_info=sys.exc_info())
    #
    #     # Begin propagating updates
    #     dn_list = []
    #     for channel in updated_channels:
    #         if channel not in self.channels_dep_chain:
    #             continue
    #         channel_deps = self.channels_dep_chain[channel]
    #         for dep in channel_deps:
    #             dn_list.append(self.channel_to_device[dep].name)
    #     dn_list = list(set(dn_list))
    #     if TRACE:
    #         self.logger.debug(f'{prefix}UP ({dn}): propagating to ({dn_list})')
    #     for device_name in dn_list:
    #         self._recursive_update(t_scheduled, t_run, device_name, depth=depth + 1)
    #     # updated_channels = self.devices_map[dn].update(t_scheduled, t_run, self.latest_data)

    def ensure_channel_exists(self, channel_name: str):
        if channel_name not in self.channels:
            raise SimulationError(f'Channel ({channel_name}) not known')

    def check_deps_satisfied(self, channel_name: str, data_required: bool = True):
        """ Verify if channel dependencies are present and have data """
        deps = self.channels_map_chain[channel_name]
        for dep in deps:
            if dep not in self.channels:
                raise SimulationError(f'Unknown dependency ({dep}) for channel ({channel_name})')
            if dep not in self.latest_data:
                raise DeviceDependencyError(f'Missing dep ({dep}) for channel ({channel_name})')
            if data_required and self.latest_data[dep] is None:
                raise DeviceDependencyError(
                        f'Last value of ({dep}) for channel ({channel_name}) is None')

    def check_enabled_state(self, dn: str):
        dev = self.devices_map[dn]
        if dev.state not in [DS.ENABLED, DS.ENABLED_AND_SCANNING]:
            # self.logger.warning(f'Device ({dn}) non-functional state ({dev.state})')
            raise DeviceDisabledError(f'Device ({dn}) in non-functional state ({dev.state})')

    def read_channel(self, cn: str, timeout=5.0) -> DataT:
        """ Read from channel """
        with self.settings_lock:
            self.ensure_channel_exists(cn)
            dn = self.channel_to_device_name[cn]
            # self.check_enabled_state(dn)
            # self.check_deps_satisfied(cn)
            ev = Event(op=OP.READ, dn=dn, txid=self.next_txid(), t_event=self.time(),
                       data={cn: None})
            f = self.get_future_for_event(ev)
            if self.TRACE:
                self.logger.debug(f'Read request event for C({cn}) added')
        try:
            result = self.await_future(f, timeout=timeout)
        except DeviceEventTimeout as ex:
            self.logger.debug(f'Read event ({ev.data=}) timeout')
            raise ex
        self.logger.debug(f'Read event ({result=})')
        if isinstance(result.data, Exception):
            raise result.data
        return result.data[cn]

    def read_channel_now(self, cn: str, timeout=5.0) -> DataT:
        """ Read from channel immediately """
        with self.settings_lock:
            self.ensure_channel_exists(cn)
            dn = self.channel_to_device_name[cn]
            ev = Event(op=OP.READ_NOW, dn=dn, txid=self.next_txid(), t_event=self.time(),
                       data={cn: None})
            f = self.get_future_for_event(ev)
            self.logger.debug(f'Read now request event for C({cn}) added')
        try:
            result = self.await_future(f, timeout=timeout)
        except DeviceEventTimeout as ex:
            self.logger.debug(f'Read now event ({ev.data=}) timeout')
            raise ex
        self.logger.debug(f'Read now event ({result=})')
        if isinstance(result.data, Exception):
            raise result.data
        return result.data[cn]

    def read(self, channels: list[str], include_timestamps=False):
        data = {}
        for i, cn in enumerate(channels):
            data[cn] = self.read_channel(cn)
        return data

    def read_fresh(self, channels: list[str], timeout: float = 1.0, now: float = None,
                   min_readings: int = 1, max_readings: int = None,
                   reduce='mean', use_buffer=True
                   ) -> dict:
        if now is None:
            now = self.time()
        t_start = time.perf_counter()
        assert min_readings is not None and min_readings >= 1
        assert max_readings is None or max_readings >= min_readings
        assert reduce is None or reduce in ['mean', 'median']
        if max_readings is None:
            max_readings = min_readings
        if self.TRACE:
            self.logger.debug(f'FR of ({channels}): ({min_readings})-({max_readings}) '
                              f'reads in max ({timeout})s, reducer ({reduce})')
        max_observed_responses = {}
        completed_channels = []
        starting_mids = {}
        for cn in channels:
            assert cn in self.channels, f'Channel ({cn}) unknown'
            if use_buffer:
                starting_mids[cn] = None
            else:
                starting_mids[cn] = self.history[cn].mid
        # self.logger.debug(f'RF: {starting_mids=}')
        while True:
            if len(completed_channels) == len(channels):
                break
            for i, cn in enumerate(channels):
                if cn in completed_channels:
                    continue
                history = self.history[cn]
                responses = history.ts(t_start=now, t_end=None, mid_start=starting_mids[cn])
                max_observed_responses[cn] = len(responses)
                if len(responses) >= min_readings:
                    completed_channels.append(cn)
                    continue
                if time.perf_counter() - t_start > timeout:
                    still_need = set(channels) - set(completed_channels)
                    raise ReadTimeoutError(
                            f'RF: timeout, still need ({still_need}) | '
                            f'({min_readings=}) | ({max_observed_responses})')
                time.sleep(0.05)

        # All data is available - proceed
        r_dict = {}
        for i, cn in enumerate(channels):
            history = self.history[cn]
            responses = history.ts(t_start=now, t_end=None, mid_start=starting_mids[cn])
            if len(responses) > max_readings:
                responses = responses[-max_readings:]
            r_dict[cn] = responses

        value_dict = {}
        for cn, responses in r_dict.items():
            data = np.array([m.value for m in responses])
            if reduce == 'mean':
                value = np.mean(data, axis=0)
            elif reduce == 'median':
                value = np.median(data, axis=0)
            else:
                value = data
            value_dict[cn] = value

        if self.TRACE:
            self.logger.debug(f'FR result: ({value_dict})')
        return value_dict

    def write_channel(self, channel_name: str, value: DataT, timeout: float = 10.0):
        """ Write to a channel """
        t1 = time.perf_counter()
        with self.settings_lock:
            self.ensure_channel_exists(channel_name)
            dn = self.channel_to_device_name[channel_name]
            ev = Event(op=OP.WRITE, dn=dn, txid=self.next_txid(), t_event=self.time(),
                       data={channel_name: value})
            f = self.get_future_for_event(ev)
            t2 = time.perf_counter()
        try:
            result = self.await_future(f, timeout=timeout)
            t3 = time.perf_counter()
        except DeviceEventTimeout as ex:
            self.logger.debug(f'Write event ({ev.data=}) timeout')
            raise ex
        # self.process_events()
        dt2 = t2 - t1
        dt3 = t3 - t2
        self.logger.debug(f'Write event ({ev.data=}) -> ({result=}) in ({dt2:.3f})|({dt3:.3f})')
        if isinstance(result.data, Exception):
            raise result.data

    def write_and_verify(self,
                         data_dict: dict[str, DataT],
                         readback_map: dict[str, str] = None,
                         timeout: float = 1.0,
                         readback_kwargs: dict = None,
                         atol_map: dict[str, float] = None,
                         rtol_map: dict[str, float] = None,
                         delay_after_write: float = None,
                         readback_timeout: float = None,
                         delay_after_readback: float = None,
                         total_cycle_min_time: float = 0.0,
                         try_read_now_after: float = 2.0,
                         ):
        self.logger.debug(f'WAV: start {data_dict=}')
        readback_map = readback_map or {}
        delay_after_write = delay_after_write or self.options.readback_delay_min
        readback_timeout = readback_timeout or self.options.readback_delay_max
        readback_kwargs = readback_kwargs or dict(min_readings=1)
        atol_map = atol_map or {}
        rtol_map = rtol_map or {}
        last_read_now_map = {cn: 0.0 for cn in readback_map}

        for k in data_dict:
            assert k in self.channels, f'Channel ({k}) unknown'
            # assert readback_map[k] in self.channels
            if k not in atol_map:
                atol_map[k] = 0.0
            if k not in rtol_map:
                rtol_map[k] = 0.0

        t_start = time.perf_counter()
        write_results = {}
        for (cn, setp) in data_dict.items():
            dev = self.channel_to_device[cn]
            if not dev.is_ready_to_write():
                raise DeviceError(f'Channel {cn} device {dev} not ready to write')
        for (cn, setp) in data_dict.items():
            write_results[cn] = self.write_channel(cn, setp)
        self.logger.debug(f'WAV: after-write sleep for ({delay_after_write})')
        time.sleep(delay_after_write)

        t_start_rb = time.perf_counter()
        now = self.time()
        rb_results = {}
        last_read = {}
        all_reads = {cn: [] for cn in data_dict}
        while len(rb_results) < len(data_dict):
            # self.logger.debug(f'RB: loop {last_read=}')
            for (cn, setp) in data_dict.items():
                if cn in rb_results:
                    continue
                if cn not in readback_map or readback_map[cn] is None:
                    rb_results[cn] = last_read[cn] = None
                    continue
                cn_rb = readback_map[cn]
                # Check buffer for latest value
                try:
                    if time.perf_counter() - t_start > try_read_now_after:
                        if time.perf_counter() - last_read_now_map[cn] > 2.0:
                            self.read_channel_now(cn_rb)
                            last_read_now_map[cn] = time.perf_counter()
                    d = self.read_fresh([cn_rb], timeout=0.0, now=now, **readback_kwargs)
                    assert len(d) == 1 and cn_rb in d
                    val = d[cn_rb]
                    last_read[cn] = val
                    all_reads[cn].append(val)
                except ReadTimeoutError:
                    last_read[cn] = None
                    continue

                if np.all(np.isclose(val, setp, atol=atol_map[cn], rtol=rtol_map[cn])):
                    rb_results[cn] = val
                    self.logger.debug(f'WAV: {cn}={val:+.5f} ({setp=:+.5f}) finished')
                else:
                    margin = (rtol_map[cn] * abs(setp)) + atol_map[cn]
                    if self.TRACE:
                        self.logger.debug(f'WAV: ({cn})=({val:+.5f}) ({setp=:+.5f}) ({margin=})')
            if len(rb_results) == len(data_dict):
                break
            dt = time.perf_counter() - t_start
            dt_rb = time.perf_counter() - t_start_rb
            if (timeout is not None and dt > timeout) or (readback_timeout is not None and dt_rb >
                                                          readback_timeout):
                bads = {}
                bads_read = {}
                for k, v in data_dict.items():
                    if k in rb_results:
                        continue
                    bads[k] = v
                    bads_read[k] = last_read[k]
                    logger.debug(f'WAV timeout: {k=} -> {data_dict[k]=} vs {last_read[k]=}')
                raise WriteTimeoutError(f'WAV: readback timeout {bads=} vs {bads_read=}')
            time.sleep(0.1)

        if delay_after_readback is not None:
            self.logger.debug(f'WAV: after-readback sleep for ({delay_after_write})')
        t_spent = time.perf_counter() - t_start
        if total_cycle_min_time is not None:
            t_sleep = max(0.0, total_cycle_min_time - t_spent)
            if t_sleep > 0:
                self.logger.debug(f'WAV: min cycle time sleep for ({t_sleep})')
                time.sleep(t_sleep)
        self.logger.debug(f'WAV: done in {t_spent:.3f}s')
        # resort dict
        rb_temp = {}
        for k in data_dict:
            if k in rb_results:
                rb_temp[k] = rb_results[k]
        return write_results, rb_temp

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

    def next_txid(self, ev=None) -> int:
        if ev is not None:
            txid = self.txid_map[ev.root]
            self.txid_map[ev.root] += 1
            return txid
        else:
            txid = self.txid
            self.txid_map[txid] = txid + 1
            self.txid += 1000
            return txid

    def push_update(self, dev: EngineDevice, data: dict[str, DataT], txid: int = None,
                    timeout: float = 0.0
                    ):
        """ Notify engine that a new value is available """
        # self.logger.debug(f'Pushing dev ({dev.name}) update ({data})')
        dn = dev.name
        assert isinstance(data, dict)
        txid = txid if txid is not None else self.next_txid()
        # assert dev.name in self.devices_name_list
        # for k, v in data.items():
        #     assert k in self.channels, f'Channel ({k}) missing?'
        #     assert k in self.dev_channels_map[dn], \
        #         f'Channel ({k}) not registered to ({dev.name})'
        t_run = self.time()
        ev = Event(op=OP.UPDATE_PUSH, dn=dn, txid=txid, t_event=t_run,
                   data=data.copy())
        f = self.get_future_for_event(ev)
        if timeout > 0.0:
            result = self.await_future(f, timeout=timeout)
            if isinstance(result.data, Exception):
                raise result.data
        # self._propagate_update_event(t_run, dn, ev)
        # with self.settings_lock:
        #     self.logger.debug(f'Pushing dev ({dev.name}) update ({data})')
        #     dn = dev.name
        #     assert isinstance(data, dict)
        #     txid = txid if txid is not None else self.next_txid()
        #     assert dev.name in self.devices_name_list
        #     for k, v in data.items():
        #         assert k in self.channels, f'Channel ({k}) missing?'
        #         assert k in self.dev_channels_map[dn], \
        #             f'Channel ({k}) not registered to ({dev.name})'
        #     t_run = self.time()
        #     ev = Event(op=OP.UPDATE_PROP, dn=dn, txid=txid, t_event=t_run,
        #                data=data.copy())
        #     self._propagate_update_event(t_run, dn, ev)

    def push_full_update_to_device(self, dev: EngineDevice,
                                   ignore_state: bool = False
                                   ):
        self.logger.debug(f'Sending full update to ({dev.name})')
        dn = dev.name
        if not ignore_state:
            self.check_enabled_state(dn)
        with self.settings_lock:
            for channel_name in dev.channels:
                self.check_deps_satisfied(channel_name)
            data = {k: self.latest_data[k] for k in self.dev_deps_map[dev.name]}
            ev = Event(op=OP.UPDATE, dn=dn, txid=self.next_txid(), t_event=self.time(),
                       data=data.copy())
            f = self.get_future_for_event(ev)
        # release lock
        self.logger.debug(f'{ev.uuid} | waiting for futures')
        result = self.await_future(f)
        self.logger.debug(f'{ev.uuid} | {result=}')
        return result

    def get_future_for_event(self, ev: Event) -> Future:
        f = Future()

        def cb(r):
            if self.TRACE:
                self.logger.debug(f'{ev.uuid} | Future callback with ({r=})')
            f.set_result(r)

        ev.set_cb(cb)
        self.event_q.put(ev)
        if self.TRACE:
            self.logger.debug(f'{ev.uuid} | Event ({ev.op=}) for ({ev.dn=}) submitted')

        # try:
        #     success = read_done_event.wait(1.5)
        #     self.logger.debug(f'Future done, ({results=} ({success=})')
        # except BaseException as e:
        #     f.set_exception(e)
        # else:
        #     f.set_result(results[0])

        return f

    def await_future(self, f: Future, timeout=0.5):
        # Use RLock for now
        # if self.settings_lock.locked():
        #    raise SimulationError(f'Lock held when attempting to wait on event - internal error')
        done, not_done = concurrent.futures.wait([f], timeout=timeout)
        if not f.done():
            raise DeviceEventTimeout(f'Future {f} timeout after ({timeout})s')
        ex = f.exception()
        if ex is not None:
            raise ex
        else:
            return f.result()

    def scan_until(self, threshold_time: float):
        """ Simulation only method - scan time forward until newer time """
        t_scan = self.time()
        assert t_scan >= threshold_time
        self.last_scan_threshold = threshold_time
        if self.TIME_TRACE:
            self.logger.debug(f'Advancing sim to ({threshold_time})')
        # Other devices can be added from main thread but wont be polled this cycle
        device_names = self.devices_name_list.copy()
        i = 0
        with self.settings_lock:
            while True:
                triggered_devices = []
                for dn in device_names:
                    if self.scan_periods[dn] > 0 and self.next_scan_time[dn] <= threshold_time:
                        triggered_devices.append((self.next_scan_time[dn], dn))
                sorted_triggered_devices = sorted(triggered_devices, key=lambda x: x[0])

                if len(sorted_triggered_devices) == 0:
                    if self.TIME_TRACE and i > 0:
                        self.logger.debug(f'Time step done ({i} cycles)')
                    break
                else:
                    if self.TIME_TRACE:
                        self.logger.debug(f'Devices to process: {sorted_triggered_devices}')

                t_scheduled, dn = sorted_triggered_devices[0]
                try:
                    ev = Event(op=OP.SCAN, dn=dn, txid=self.next_txid(), t_event=t_scheduled)
                    dev = self.devices_map[dn]
                    try:
                        if self.TRACE:
                            self.logger.debug(
                                    f'{ev.uuid} | Scan ({dn}) at scheduled time ({t_scheduled})')
                        self.check_enabled_state(dn)
                        r = dev.scan(ev)
                        if self.TRACE:
                            self.logger.debug(f'{ev.uuid} | Scan result ({r})')
                        evx = Event(op=OP.UPDATE_PROP, dn=dn, txid=self.next_txid(ev),
                                    t_event=t_scheduled, data=r, root=ev.root, source=ev.txid)
                        self._propagate_update_event(t_scheduled, dn, evx)
                        ev.cb(True)
                    except DeviceDisabledError as ex:
                        self.logger.debug(f'{ev.uuid} | Scan of disabled device ({dn})')
                        ev.cb(ex)
                finally:
                    self.next_scan_time[dn] += self.scan_periods[dn]
                i += 1

    def scan_now(self, threshold_time: float, add_execution_time: bool = False):
        """ Real-time method to invoke any needed scans """
        t_scan_start = self.time()
        assert t_scan_start >= threshold_time
        if self.TIME_TRACE:
            self.logger.debug(f'Advancing sim to ({threshold_time})')

        i = 0
        with self.settings_lock:
            while True:
                triggered_devices = []
                for dn in self.scan_periods:
                    if self.scan_periods[dn] > 0 and self.next_scan_time[dn] <= threshold_time:
                        triggered_devices.append((self.next_scan_time[dn], dn))
                sorted_triggered_devices = sorted(triggered_devices, key=lambda x: x[0])

                if len(sorted_triggered_devices) == 0:
                    if self.TIME_TRACE and i > 0:
                        self.logger.debug(f'Time step done ({i} cycles)')
                    break
                else:
                    if self.TIME_TRACE:
                        self.logger.debug(f'Devices to process: {sorted_triggered_devices}')

                t_scheduled, dn = sorted_triggered_devices[0]
                try:
                    t_run = self.time()
                    t_start_walltime = time.perf_counter()
                    ev = Event(op=OP.SCAN, dn=dn, txid=self.next_txid(), t_event=t_run)
                    if self.TRACE:
                        self.logger.debug(f'{ev.uuid} | {ev.op=} {ev.dn=} {ev.data=} {ev.t_event=}')
                    dev = self.devices_map[dn]
                    try:
                        # if self.TRACE:
                        #     self.logger.debug(f'{ev.uuid} | Scan ({dn}) at time ({t_run})')
                        self.check_enabled_state(dn)
                        r = dev.scan(ev)
                        if self.TRACE:
                            self.logger.debug(f'{ev.uuid} | Scan ({dn}) at ({t_run:.4f}): result '
                                              f'({r})')
                        if len(r) > 0:
                            assert (isinstance(v, float) for v in r.values())
                            assert all(k in self.channels for k in r)
                            evx = Event(op=OP.UPDATE_PROP, dn=dn, txid=self.next_txid(ev),
                                        t_event=t_run, data=r, root=ev.root, source=ev.txid)
                            self._propagate_update_event(t_run, dn, evx)
                        else:
                            if self.TRACE:
                                self.logger.debug(f'{ev.uuid} | No scan data, skipping propagation')
                        ev.cb(Result(t_run, r, True))
                    except DeviceDisabledError as ex:
                        self.logger.debug(f'{ev.uuid} | Scan of disabled device ({dn})')
                        ev.cb(Result(t_run, ex, False))
                    except Exception as ex:
                        self.logger.debug(f'{ev.uuid} | Scan error ({ex})')
                        self.logger.debug(f'{ev.uuid} | {traceback.format_exc()}')
                        ev.cb(Result(t_run, ex, False))
                finally:
                    # Reset to current time
                    if add_execution_time:
                        self.next_scan_time[dn] = self.time() + self.scan_periods[dn]
                        # self.next_scan_time[dn] += (time.perf_counter() - t_start_walltime)
                    else:
                        self.next_scan_time[dn] = t_run + self.scan_periods[dn]

                    # # Catch-up method
                    # self.next_scan_time[dn] += self.scan_periods[dn]
                    # if add_execution_time:
                    #     self.next_scan_time[dn] += (time.perf_counter() - t_start_walltime)
                i += 1
        self.last_scan_threshold = threshold_time

    def _scan_thread(self, command_queue: queue.Queue):
        t = self.time()
        self.logger.debug(f'Hello from scan thread (id {threading.get_ident()}) at ({t=})')
        i = 0
        while True:
            i += 1
            threshold_time = self.time()
            skip = True
            for dn in self.scan_periods:
                if self.scan_periods[dn] > 0 and self.next_scan_time[dn] <= threshold_time:
                    skip = False
                    break
            if not skip:
                if self.TRACE:
                    self.logger.debug(f'Scan loop ({i=}) at ({threshold_time=})')
                self.scan_now(threshold_time)
            time.sleep(0)
            try:
                cmd = command_queue.get(timeout=0.02)
                if cmd is None:
                    self.logger.debug(f'Goodbye from scan thread')
                    break
            except queue.Empty:
                time.sleep(0)

    def start_scan_thread(self, reset_update_time: bool = True):
        if self.is_running:
            raise SimulationError(f'Scan thread is already running')
        if reset_update_time:
            now = self.time()
            for dn in self.scan_periods:
                self.next_scan_time[dn] = now
        self.cmdq = queue.Queue()
        self.logger.debug(f'Starting scan thread')
        th = threading.Thread(target=self._scan_thread,
                              name='sim_engine_scan',
                              args=(self.cmdq,))
        th.daemon = True
        th.start()
        self.is_running = True
        self.poll_thread = th

    def stop_scan_thread(self):
        if not self.is_running:
            raise SimulationError(f'No thread to stop')
        self.cmdq.put(None)
        self.poll_thread.join(timeout=1.0)

        self.is_running = False
        self.cmdq = None
        self.poll_thread = None

    def _update_thread(self, update_q: queue.Queue, command_q: queue.Queue):
        self.update_thread_running = True
        self.logger.debug(f'Update thread (id {threading.get_ident()}) on')
        while True:
            try:
                # try:
                #     ev = self.event_q_prio.get_nowait()
                # except queue.Empty:
                #     ev = update_q.get(block=True, timeout=0.5)
                ev = update_q.get(block=True, timeout=0.5)
                dn = ev.dn
                # uuid = f'E{ev.txid}:{ev.source}:{ev.root}'
                with self.settings_lock:
                    t_process = self.time()
                    t1 = time.perf_counter()
                    if self.TRACE:
                        self.logger.debug(f'{ev.uuid} | {ev.op=} {ev.dn=} {ev.data=} {ev.t_event=}')
                    if ev.txid in self.set_seen_txids:
                        raise SimulationError(f'Event {ev.txid} already seen')
                    else:
                        self.set_seen_txids.add(ev.txid)

                    if ev.op == OP.ENABLE:
                        self._process_enable_event(ev)
                    elif ev.op == OP.UPDATE_PUSH:
                        try:
                            dev = self.devices_map[ev.dn]
                            self.check_enabled_state(dn)
                            for cn, v in ev.data.items():
                                self.ensure_channel_exists(cn)
                                assert cn in self.dev_channels_map[dn], f'Channel ({cn}) not ' \
                                                                        f'registered to ({dev.name})'
                            evx = Event(op=OP.UPDATE_PROP, dn=dn, txid=self.next_txid(ev),
                                        t_event=t_process, data=ev.data, root=ev.root,
                                        source=ev.txid)
                            self._propagate_update_event(ev.t_event, dn, evx)
                            ev.cb(Result(t_process, ev.data, True))
                        except Exception as ex:
                            dev.state = DS.ERROR_UPDATE
                            self.logger.debug(f'{ev.uuid} | Push error ({ex})')
                            self.logger.debug(f'{ev.uuid} | {traceback.format_exc()}')
                            ev.cb(Result(t_process, ex, False))
                        if self.TRACE:
                            self.logger.debug(f'{ev.uuid} | === Push done ===')
                    elif ev.op == OP.UPDATE_PROP:
                        if self.TRACE:
                            self.logger.debug(f'{ev.uuid} | Propagate ({ev.data}) at '
                                              f'({t_process})')
                        self._propagate_callbacks(t_process, dn, ev)
                        if self.TRACE:
                            self.logger.debug(f'{ev.uuid} | === Propagate done ===')
                    elif ev.op == OP.UPDATE:
                        # Request new channel values for updated deps
                        dev = self.devices_map[ev.dn]
                        try:
                            self.check_enabled_state(dn)
                            if any(x not in self.dev_deps_map[dn] for x in ev.data):
                                raise DeviceError(f'Invalid data ({ev.data}) for update of ({dn})')
                            for cn, v in ev.data.items():
                                self.ensure_channel_exists(cn)
                                self.check_deps_satisfied(cn, data_required=False)
                            if self.TRACE:
                                self.logger.debug(
                                        f'{ev.uuid} | Update ({ev.data}) at ({t_process})')
                            r = dev.update(ev, aux_dict=ev.data)
                            if self.TRACE:
                                self.logger.debug(f'{ev.uuid} | Update result ({r})')
                            evx = Event(op=OP.UPDATE_PROP, dn=dn, txid=self.next_txid(),
                                        t_event=t_process,
                                        data=r, root=ev.root, source=ev.txid)
                            self._propagate_update_event(t_process, dn, evx)
                            ev.cb(Result(t_process, r, True))
                        except DeviceDisabledError as ex:
                            self.logger.warning(f'{ev.uuid} | Update of disabled device ({dn})')
                            ev.cb(Result(t_process, ex, False))
                        except DeviceDependencyError as ex:
                            dev.state = DS.ERROR_DEPENDENCIES
                            self.logger.debug(f'{ev.uuid} | Cannot update ({dn}) due to missing '
                                              f'deps')
                            ev.cb(Result(t_process, ex, False))
                        except Exception as ex:
                            dev.state = DS.ERROR_UPDATE
                            self.logger.debug(f'{ev.uuid} | Update error ({ex})')
                            self.logger.debug(f'{ev.uuid} | {traceback.format_exc()}')
                            ev.cb(Result(t_process, ex, False))
                        if self.TRACE:
                            self.logger.debug(f'{ev.uuid} | === Update done ===')
                    elif ev.op == OP.WRITE:
                        dev = self.devices_map[ev.dn]
                        try:
                            self.check_enabled_state(dn)
                            aux_dict = {k: self.latest_data[k] for k in self.dev_deps_map[dn]}
                            for cn, v in ev.data.items():
                                self.ensure_channel_exists(cn)
                                self.check_deps_satisfied(cn)
                            if self.TRACE:
                                self.logger.debug(f'{ev.uuid} | Write ({ev.data}) at ({t_process})')
                            r = dev.write(ev, ev.data, aux_dict)

                            if self.TRACE:
                                self.logger.debug(f'{ev.uuid} | Write result ({r})')
                            if r is None or len(r) == 0:
                                self.logger.warning(f'{ev.uuid} | No write update data?')
                            else:
                                evx = Event(op=OP.UPDATE_PROP, dn=dn, txid=self.next_txid(ev),
                                            t_event=t_process, data=r, root=ev.root, source=ev.txid)
                                # self.event_q_prio.put(evx)
                                self._propagate_data(t_process, dn, evx)
                                update_q.put(evx)
                                # self._propagate_update_event(t_process, dn, evx)
                            ev.cb(Result(t_process, r, True))
                        except DeviceDisabledError as ex:
                            self.logger.debug(f'{ev.uuid} | Write device disabled error ({ex})')
                            self.logger.debug(f'{ev.uuid} | {traceback.format_exc()}')
                            ev.cb(Result(t_process, ex, False))
                        except Exception as ex:
                            dev.state = DS.ERROR_WRITE
                            self.logger.debug(f'{ev.uuid} | Write error ({ex})')
                            self.logger.debug(f'{ev.uuid} | {traceback.format_exc()}')
                            ev.cb(Result(t_process, ex, False))
                        if self.TRACE:
                            self.logger.debug(f'{ev.uuid} | === Write done ===')
                    elif ev.op == OP.READ:
                        dev = self.devices_map[ev.dn]
                        try:
                            self.check_enabled_state(dn)
                            assert len(ev.data) == 1
                            cn = next(iter(ev.data))
                            self.ensure_channel_exists(cn)
                            self.check_deps_satisfied(cn, data_required=False)
                            value = dev.read(ev, cn)
                            if self.TRACE:
                                self.logger.debug(
                                        f'{ev.uuid} | Read ({cn})=({value}) at ({t_process})')
                            ev.cb(Result(t_process, {cn: value}, True))
                        except DeviceDisabledError as ex:
                            self.logger.debug(f'{ev.uuid} | Read of disabled device attempted')
                            ev.cb(Result(t_process, ex, False))
                        except Exception as ex:
                            dev.state = DS.ERROR_READ
                            self.logger.debug(f'{ev.uuid} | Read error ({ex})')
                            self.logger.debug(f'{ev.uuid} | {traceback.format_exc()}')
                            ev.cb(Result(t_process, ex, False))
                        if self.TRACE:
                            self.logger.debug(f'{ev.uuid} | === Read done ===')
                    elif ev.op == OP.READ_NOW:
                        dev = self.devices_map[ev.dn]
                        try:
                            self.check_enabled_state(dn)
                            assert len(ev.data) == 1
                            cn = next(iter(ev.data))
                            self.ensure_channel_exists(cn)
                            self.check_deps_satisfied(cn, data_required=False)
                            value = dev.read_now(ev, cn)
                            if self.TRACE:
                                self.logger.debug(
                                        f'{ev.uuid} | Read now ({cn})=({value}) at ({t_process})')
                            # New data, actually propagate it
                            evx = Event(op=OP.UPDATE_PROP, dn=dn, txid=self.next_txid(ev),
                                        t_event=t_process,
                                        data={cn: value}, root=ev.root, source=ev.txid)
                            self._propagate_update_event(t_process, dn, evx)
                            ev.cb(Result(t_process, {cn: value}, True))
                        except DeviceDisabledError as ex:
                            self.logger.debug(f'{ev.uuid} | Read now of disabled device attempted')
                            ev.cb(Result(t_process, ex, False))
                        except Exception as ex:
                            dev.state = DS.ERROR_READ
                            self.logger.debug(f'{ev.uuid} | Read now error ({ex})')
                            self.logger.debug(f'{ev.uuid} | {traceback.format_exc()}')
                            ev.cb(Result(t_process, ex, False))
                        if self.TRACE:
                            self.logger.debug(f'{ev.uuid} | === Read now done ===')
                update_q.task_done()
                dt = time.perf_counter() - t1
                self.event_count += 1
                self.event_wall_time += dt
            except queue.Empty:
                # Check shutdown
                try:
                    cmd = command_q.get(timeout=0.01)
                    if cmd is None:
                        self.logger.debug(f'Goodbye from update thread')
                        break
                except queue.Empty:
                    pass
            except Exception as ex:
                update_q.task_done()
                self.update_thread_running = False
                self.logger.error(f'Fatal error in update thread: {traceback.format_exc()}')
        self.logger.debug(f'Update thread (id {threading.get_ident()}) exiting')
        self.update_thread_running = False

    def _process_enable_event(self, ev: Event):
        t_run = self.time()
        dn = ev.dn
        dev = self.devices_map[dn]
        try:
            dev.state = DS.STARTING_UP
            if self.TRACE:
                self.logger.debug(f'{ev.uuid} | Enable ({dn=}) at ({t_run})')

            for cn in self.dev_channels_map[dn]:
                self.ensure_channel_exists(cn)
                self.check_deps_satisfied(cn, data_required=False)
            deps_data = {k: self.latest_data[k] for k in self.dev_deps_map[dn]}
            dev.enable(ev)
            r = dev.update(ev, aux_dict=deps_data)
            dev.state = DS.ENABLED
            self.next_scan_time[dn] = t_run + self.scan_periods[dn]
            if self.TRACE:
                self.logger.debug(f'{ev.uuid} | Enable result ({r})')
            evx = Event(op=OP.UPDATE_PROP, dn=dn, txid=self.next_txid(ev), t_event=t_run,
                        data=r, root=ev.root, source=ev.txid)
            self._propagate_update_event(t_run, dn, evx)
            ev.cb(Result(t_run, r, success=True))
            if self.TRACE:
                self.logger.debug(f'{ev.uuid} | Enable done')
        except DeviceDependencyError as ex:
            dev.state = DS.ERROR_DEPENDENCIES
            self.logger.debug(f'{ev.uuid} | Enable deps error ({ex})')
            self.logger.debug(f'{traceback.format_exc()}')
            ev.cb(Result(t_run, ex, success=False))
        except Exception as ex:
            dev.state = DS.ERROR_ENABLE
            self.logger.debug(f'{ev.uuid} | Enable error ({ex})')
            self.logger.debug(f'{traceback.format_exc()}')
            ev.cb(Result(t_run, ex, success=False))

    def _propagate_data(self, t_run: float, dn: str, ev: Event):
        assert ev.op == OP.UPDATE_PROP

        for cn in ev.data:
            assert cn in self.dev_channels_map[dn]

        for cn, v in ev.data.items():
            self.latest_data[cn] = v
            self.latest_data_timestamp[cn] = t_run
            self.history_data[cn].append(v)
            self.history_data_timestamp[cn].append(t_run)
            self.history[cn].append(Measurement(t=ev.t_event, value=v, event=ev))

    def _propagate_callbacks(self, t_run: float, dn: str, ev: Event):
        assert ev.op == OP.UPDATE_PROP

        for cn, v in ev.data.items():
            if cn not in self.channel_subs:
                continue
            if self.TRACE:
                self.logger.debug(f'{ev.uuid} | Invoking subs for ({cn})=({v})')
            self.channel_subs[cn].process_update(v)

        dn_list = []
        for cn in ev.data:
            if cn not in self.channels_dep_chain:
                continue
            channel_deps = self.channels_dep_chain[cn]
            for dep in channel_deps:
                dn_list.append(self.channel_to_device_name[dep])
        dn_list = list(set(dn_list))
        if self.TRACE:
            if dn_list:
                self.logger.debug(f'{ev.uuid} | Propagating to ({dn_list})')

        for dn in dn_list:
            assert dn in self.devices_name_list
            related_data = {k: v for k, v in ev.data.items() if k in self.dev_deps_map[dn]}
            self._validate_update_data(dn, related_data)
            txid = self.txid_map[ev.root]
            self.txid_map[ev.root] += 1
            ev = Event(op=OP.UPDATE, dn=dn, txid=txid, t_event=t_run,
                       data=related_data, root=ev.root, source=ev.source)
            self.event_q.put(ev)

    def _propagate_update_event(self, t_run: float, dn: str, ev: Event):
        assert ev.op == OP.UPDATE_PROP

        for cn in ev.data:
            assert cn in self.dev_channels_map[dn]

        for cn, v in ev.data.items():
            self.latest_data[cn] = v
            self.latest_data_timestamp[cn] = t_run
            self.history_data[cn].append(v)
            self.history_data_timestamp[cn].append(t_run)
            self.history[cn].append(Measurement(t=t_run, value=v, event=ev))

        for cn, v in ev.data.items():
            if cn not in self.channel_subs:
                continue
            if self.TRACE:
                self.logger.debug(f'{ev.uuid} | Invoking subs for ({cn})=({v})')
            self.channel_subs[cn].process_update(v)

        dn_list = []
        for cn in ev.data:
            if cn not in self.channels_dep_chain:
                continue
            channel_deps = self.channels_dep_chain[cn]
            for dep in channel_deps:
                dn_list.append(self.channel_to_device_name[dep])
        dn_list = list(set(dn_list))
        if self.TRACE:
            if dn_list:
                self.logger.debug(f'{ev.uuid} | Propagating to ({dn_list})')

        for dn in dn_list:
            assert dn in self.devices_name_list
            related_data = {k: v for k, v in ev.data.items() if k in self.dev_deps_map[dn]}
            self._validate_update_data(dn, related_data)
            txid = self.txid_map[ev.root]
            self.txid_map[ev.root] += 1
            ev = Event(op=OP.UPDATE, dn=dn, txid=txid, t_event=t_run,
                       data=related_data, root=ev.root, source=ev.source)
            self.event_q.put(ev)

    # def _process_update_event(self, t_run: float, dn: str, event: Event):
    #     self.logger.debug(f'{event.uuid} | process_update_event')
    #     for cn in event.data:
    #         assert cn in self.dev_channels_map[dn]
    #
    #     # Verify dependencies
    #     deps = self.dev_deps_map[dn]
    #     for dep in deps:
    #         if dep not in self.channels:
    #             self.devices_state[dn] = DS.ERROR_DEPENDENCIES
    #         if dep not in self.latest_data or self.latest_data[dep] is None:
    #             raise Exception(f'{event.uuid} | value of ({dep}) is missing')
    #
    #     # Direct channels
    #     updated_channels = event.data
    #     for dev, data in updated_channels.items():
    #         self.latest_data[dev] = data
    #         self.latest_data_timestamp[dev] = t_run
    #         self.history_data[dev].append(data)
    #         self.history_data_timestamp[dev].append(t_run)
    #
    #     # Trigger channel subscriptions
    #     for channel, value in updated_channels.items():
    #         if channel not in self.channel_subs:
    #             continue
    #         try:
    #             if self.TRACE:
    #                 self.logger.debug(
    #                         f'{event.uuid} | subs for ({channel})=({value})')
    #             self.channel_subs[channel].process_update(value)
    #         except Exception as ex:
    #             self.logger.error(f'Channel ({channel}) input_var_change_callback fail',
    #                               exc_info=sys.exc_info())
    #
    #     # Begin propagating updates
    #     dn_list = []
    #     for channel in updated_channels:
    #         if channel not in self.channels_dep_chain:
    #             continue
    #         channel_deps = self.channels_dep_chain[channel]
    #         for dep in channel_deps:
    #             dn_list.append(self.channel_to_device[dep].name)
    #     dn_list = list(set(dn_list))
    #     if self.TRACE:
    #         self.logger.debug(f'{event.uuid} | Propagating to ({dn_list})')
    #
    #     # responses = {}
    #     for dn in dn_list:
    #         # device = self.devices_map[dn]
    #         assert dn in self.devices_name_list
    #         related_channels = [c for c in updated_channels if c in
    #                             self.dev_deps_map[dn]]
    #         related_data = {k: v for k, v in event.data.items() if k in related_channels}
    #         self._validate_update_data(dn, related_data)
    #         txid = self.txid_map[event.source]
    #         self.txid_map[event.source] += 1
    #         ev = Event(op=OP.UPDATE, dn=dn, txid=txid, t_event=t_run,
    #                    data=related_data, root=event.root, source=event.source)
    #         self.event_q.put(ev)
    #         # response = device.update(t_run, related_data)
    #         # if response is not None:
    #         #    responses[device] = response

    def _validate_update_data(self, dn, data):
        for channel_name, value in data.items():
            if channel_name not in self.channels:
                raise SimulationError(f'Channel ({channel_name}) is not known')
            if channel_name not in self.dev_deps_map[dn]:
                raise SimulationError(f'Channel ({channel_name}) not registered to ({dn})')

    def start_update_thread(self):
        if self.update_thread_running:
            raise SimulationError(f'Update thread is already running')
        if self.TRACE:
            self.logger.debug(f'Starting update thread')
        th = threading.Thread(target=self._update_thread,
                              name=self.options.update_thread_name,
                              args=(self.event_q, self.event_command_q))
        th.daemon = True
        th.start()
        self.update_thread = th
        # self.update_thread_running = True

    def stop_update_thread(self):
        if not self.update_thread_running:
            raise SimulationError(f'No thread to stop')
        self.event_command_q.put(None)
        self.poll_thread.join(timeout=1.0)
        self.update_thread = None
        # self.update_thread_running = False

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
