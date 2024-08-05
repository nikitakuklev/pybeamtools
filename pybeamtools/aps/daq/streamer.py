import collections
import datetime
import logging
import os
import socket
import threading
import time
import traceback
from abc import ABC, abstractmethod
from typing import Callable, Optional

import caproto
from caproto.threading.client import PV
import numba
import numpy as np

from pybeamtools.aps.daq.data import FakePvObject, PerformanceData
from pybeamtools.controls.ray import RayMixin
from pybeamtools.controlsdirect.clib import Accelerator
from pybeamtools.utils.logging import config_root_logging


def get_bpm_fields(c) -> list[str]:
    struct = c.getIntrospectionDict()
    found_fields = [x for x in struct.keys() if is_bpm_field(x)]
    return found_fields


def is_bpm_field(x):
    return x[0] == "s" and len(x) == 6


WINDOW = 2048 // 2
STEP = 1024 // 2
DAQ_DOWNSAMPLE_FACTOR = 32
TRACE = False


def get_bpm_channel_properties(c, devices, fields: list[str], time_field="time", extra_fields=None):
    if devices is None:
        bpms = get_bpm_fields(c)
    else:
        bpms = devices
    fl = []
    fp = {}
    for field in fields:
        fl.extend([f"{x}.{field}" for x in bpms])
        fp[field] = [(x, field) for x in bpms]
    if time_field is not None:
        fl.insert(0, "time")
    if extra_fields is not None:
        fl.extend(extra_fields)
    fstr = ", ".join(fl)
    return fp, f"field({fstr})"


def get_ps_channel_properties(c, fields: list[str], add_time=True):
    bpms = get_bpm_fields(c)
    fl = []
    fp = {}
    for field in fields:
        fl.extend([f"{x}.{field}" for x in bpms])
        fp[field] = [(x, field) for x in bpms]
    if add_time:
        fl.insert(0, "time")
    fstr = ", ".join(fields)
    return fp, f"field({fstr})"


# def post_process_daqtbt_object(data: dict,
#                                fields: list[str],
#                                ignore_errors=True,
#                                time_field='time',
#                                debug=False,
#                                expected_frame_len=None
#                                ):
#     arrays = {field: [] for field in fields}
#     bpms = []
#     time_array = None
#     datafields = list(data.keys())
#     if debug:
#         print(f'PVO processing | Have {len(datafields)} channels, will search for {fields=}')
#     for bpm in datafields:
#         if bpm == time_field:
#             time_array = data[time_field].copy()
#         elif is_bpm_field(bpm):
#             for field in fields:
#                 arr = data[bpm][field]
#                 if expected_frame_len is not None and len(arr) != EXPECTED_TBT_FRAME_LEN:
#                     print(f'Bad length {len(arr)}')
#                     if not ignore_errors:
#                         raise Exception(f'Bad length {len(arr)}, expected {EXPECTED_TBT_FRAME_LEN}')
#                 if len(arr) > 0:
#                     if debug:
#                         print(f'Found {field} {bpm}')
#                     arrays[field].append(arr)
#                     bpms.append(bpm)
#                 else:
#                     if not ignore_errors:
#                         print(f'Bad bpm {bpm}')
#         else:
#             if debug:
#                 print(f'Skipping field {bpm=}')
#             pass
#
#     if time_array is None:
#         raise Exception('Missing time field')
#
#     final_matrices = []
#     for field in fields:
#         if len(arrays[field]) == 0:
#             final_matrices.append(None)
#             continue
#
#         # convert to float due to possible overflow for int32
#         # float32 is also faster and has enough precision
#         # np.nextafter(59852530.0, 59852530.0+1) = 59852528.00000001
#         if (s := set([len(x) for x in arrays[field]])) != {len(arrays[field][0])}:
#             print(f'Have nonuniform lengths {s}')
#         mat = np.row_stack(arrays[field]).astype(np.float32).T  # this now has F order for column-wise mean
#         assert mat.flags['F_CONTIGUOUS']
#         # mat = np.column_stack(arrays).astype(np.float64)
#         # assert mat.flags['C_CONTIGUOUS']# and mat.flags['OWNDATA']
#
#         del arrays[field]
#         final_matrices.append(mat)
#
#     bpm_names = [SR_BPMS_DAQ_TO_NAME[x] for x in bpms]
#     assert time_array.flags['C_CONTIGUOUS'] and time_array.flags['OWNDATA']
#
#     return final_matrices, time_array, bpm_names


def post_process_daq_object_via_paths(
        data: dict,
        field_paths: dict[str, list[str]],
        ignore_errors=True,
        time_field="time",
        tag_field="acqClkTimestamp",
        frame_len: int = None,
        debug=False,
        # tag_function: Optional[Callable] = None,
) -> tuple[list[np.ndarray], np.ndarray, list[str], tuple[int, int]]:
    """Process the data dictionary from the PV using the field paths to traverse the structure."""
    arrays = {field: [] for field in field_paths}
    channels = []
    datafields = list(data.keys())
    logger = logging.getLogger(__name__)
    if debug:
        logger.debug(f"PVO processing | analyzing {len(datafields)} channels")
        if TRACE:
            logger.debug(f"Have {datafields=}, will search for {field_paths=}")
    for field, path_list in field_paths.items():
        for fp in path_list:
            arr = data.get(fp[0], None)
            if arr is None:
                raise Exception(f"Bad device path {fp=}, have {data.keys()}")
            for p in fp[1:]:
                arr = arr.get(p, None)
                if arr is None:
                    raise Exception(f"Bad path {fp=} - no data")
            larr = len(arr)
            if frame_len is not None and larr != frame_len:
                if larr == 0:
                    pass
                else:
                    logger.error(f"Bad length {larr=} vs {frame_len=}")
                    if not ignore_errors:
                        raise Exception(f"Bad length {larr}, expected {frame_len}")
            if larr > 0:
                if TRACE:
                    logger.debug(f"Found path {fp=}")
                arrays[field].append(arr)
                channels.append(fp[0])
            else:
                if not ignore_errors:
                    raise ValueError(f"Bad channel {fp[0]=}")

    time_array = data[time_field].copy()
    time_tag = data[tag_field]
    tag = (time_tag["secondsPastEpoch"], (time_tag["nanoseconds"] // 10000000) * 10)

    final_matrices = []
    for field in field_paths:
        if len(arrays[field]) == 0:
            final_matrices.append(None)
            continue

        # convert to float due to possible overflow for int32
        # float32 is also faster and has enough precision
        # np.nextafter(59852530.0, 59852530.0+1) = 59852528.00000001
        if (s := set([len(x) for x in arrays[field]])) != {len(arrays[field][0])}:
            print(f"Have nonuniform lengths {s}")
        mat = np.row_stack(arrays[field]).astype(np.float32).T  # this now has F order for column-wise mean
        assert mat.flags["F_CONTIGUOUS"]
        # mat = np.column_stack(arrays).astype(np.float64)
        # assert mat.flags['C_CONTIGUOUS']# and mat.flags['OWNDATA']

        del arrays[field]
        final_matrices.append(mat)

    # bpm_names = [SR_BPMS_DAQ_TO_NAME[x] for x in bpms]
    assert time_array.flags["C_CONTIGUOUS"] and time_array.flags["OWNDATA"]

    return final_matrices, time_array, channels, tag


# Numba will hopefully hardcode the window and step values, ala C++ templates


def get_numba_rolling_mean_2d(frame_len, window, step):
    @numba.jit(
            [
                "int32[:,:](int32[::1,:])",
                "float32[:,:](float32[::1,:])",
                "float64[:,:](float64[::1,:])",
            ],
            nopython=True,
            nogil=True,
            fastmath=True,
    )  # parallel=True,
    def numpy_rolling_mean_2d(mat):
        N = (frame_len - window) // step + 1
        out = np.zeros((N, mat.shape[1]), dtype=mat.dtype)
        for i in range(N):
            out[i] = np.sum(mat[i * step: i * step + window, :], axis=0) / window
        return out

    return numpy_rolling_mean_2d


def get_numba_rolling_mean_1d(frame_len, window, step):
    @numba.jit("float64[:](float64[::1])", nopython=True, nogil=True, fastmath=True)
    def numpy_rolling_mean_1d(mat):
        N = (frame_len - window) // step + 1
        out = np.zeros(N, dtype=mat.dtype)
        for i in range(N):
            out[i] = np.sum(mat[i * step: i * step + window], axis=0) / window
        return out

    return numpy_rolling_mean_1d


def numpy_rolling_mean_cumsum(mat, tarr):
    n = 2001
    q = 501

    def ra_1d(a, n, q):
        assert n % 2 == 1
        cumsum_vec = np.cumsum(np.insert(a, 0, 0))
        rm = (cumsum_vec[n:] - cumsum_vec[:-n]) / n
        return rm[::q]

    def ra_2d(a, n, q):
        cumsum_vec = np.cumsum(np.insert(a, 0, 0, axis=0), axis=0)
        rm = (cumsum_vec[n:, :] - cumsum_vec[:-n, :]) / n
        return rm[::q, :]

    return [ra_2d(mat, n, q), tarr[::q]]


# def scipy_decimate(mat, tarr):
#     from scipy import signal
#     matnew = signal.decimate(mat, q=101, axis=0, ftype='fir')
#     return [matnew, tarr[::13]]

# def df_rolling_mean(self, mat, tarr, bpms):
#     df = pd.DataFrame(mat, columns=bpms)
#     rdf = df.rolling(window=2000, step=1000).mean().iloc[2:-2, :]
#     ts = pd.Series(tarr, name='time').rolling(window=2000, step=1000).mean().iloc[2:-2]
#     # rdf.index = ts
#     return [rdf.values, ts.values]
class GenericStreamer(ABC):
    def __init__(self, name: str, channel: str, buffer_size: int, debug=False):
        self.acc = Accelerator.get_singleton()
        self.name = name
        self.channel_name = channel

        self.logger = logging.getLogger(__name__)

        self.is_monitoring = False
        self.callback_received = False
        self.stop_requested = False
        self.event_last = None
        self.store_last_event = False
        self.n_channels = None
        self.buffer = collections.deque(maxlen=buffer_size)  # [None] * buffer_size
        self.buf_lock = threading.Lock()
        self.event_callback_lock = threading.Lock()
        self.cbs: dict[str, Callable] = {}
        self.cbs_kwargs: dict[str, dict] = {}
        self.monitor_limit = None
        self.monitor_thread = None
        self.time_start: Optional[float] = None
        self.connection_evt_timestamps = collections.deque(maxlen=buffer_size)

        self.event_cb_time_history = collections.deque(maxlen=buffer_size)
        self.event_cb_timestamps = collections.deque(maxlen=buffer_size)
        self.event_cb_time = 0
        self.event_cnt = 0
        self.event_cb_thread_id = None
        self.event_cb_process_id = None
        self.event_cb_avg_time = 0.0
        self.event_cb_max_time = 0.0
        self.event_fault_threshold = 0.11
        self.event_cb_fault_cnt = 0
        self.event_cb_result = None
        self.event_cb_result_buffer = collections.deque(maxlen=buffer_size)
        self.avg_load = 0.0
        self.debug = debug
        self.channel = None
        self.is_connected = False
        self.log_with_print = False
        self.finalizers = []

    def __str__(self):
        return f"{self.__class__.__name__} {self.channel_name}: {self.is_monitoring=}, {self.is_connected=}"

    def exec_fun(self, f):
        return f(self)

    def ldebug(self, msg):
        if self.debug:
            if self.log_with_print:
                # Useful with ray
                print(msg)
            else:
                self.logger.debug(msg)

    def lerror(self, msg):
        if self.log_with_print:
            # Useful with ray
            print(msg)
        else:
            self.logger.error(msg, stacklevel=2)

    @abstractmethod
    def connect(self):
        pass

    @property
    def load(self) -> float:
        if self.event_cnt == 0:
            return 0.0
        return np.mean(list(self.event_cb_time_history)) / 0.1

    @property
    def event_rate(self) -> float:
        if len(self.event_cb_timestamps) == 0:
            return 0.0
        times = list(self.event_cb_timestamps)
        return 1 / np.diff(times).mean() if len(times) > 2 else 0.0

    def _connection_cb(self, state: bool):
        if self.debug:
            now = datetime.datetime.now().isoformat(sep=" ", timespec="milliseconds")
            self.logger.info(f"Conn cb [{self.channel_name}]@[{now}] -> {state=}")
        self.connection_evt_timestamps.append((time.time(), state))
        self.is_connected = state

    @abstractmethod
    def process_monitor_event(self, x):
        pass

    def add_callback(self, name: str, f: Callable, f_kwargs: Optional[dict] = None):
        """Add a callback function to be called for each new frame.

        :param name: Name of the callback
        :param f:  A callable (can be a class instance)
        :param f_kwargs: Keyword arguments to pass to the function
        """
        # TODO: weakref
        f_kwargs = f_kwargs or {}
        with self.event_callback_lock:
            self.cbs[name] = f
            self.cbs_kwargs[name] = f_kwargs

    def remove_callback(self, name: str):
        with self.event_callback_lock:
            if name in self.cbs:
                del self.cbs[name]
                del self.cbs_kwargs[name]
            else:
                raise ValueError(f"No such callback {name}")

    def clear_callbacks(self):
        with self.event_callback_lock:
            self.cbs = {}

    def run_callbacks(self, pvo_dict):
        self.ldebug(f"ST [{self.name}] | Running [{len(self.cbs)}] callbacks")
        cb_results = {}
        for k, f in self.cbs.items():
            try:
                cb_results[k] = f(streamer=self, data=pvo_dict, **self.cbs_kwargs[k])
                self.ldebug(f"ST [{self.name}] | CB [{k}] returned [{cb_results[k]}]")
            except Exception as e:
                self.lerror(f"Error in callback [{k}]: {e} {traceback.format_exc()}")
        return cb_results

    def add_finalizer(self, f: Callable):
        self.finalizers.append(f)

    def run_finalizers(self):
        self.ldebug(f"ST [{self.name}] | Running [{len(self.finalizers)}] finalizers")
        for f in self.finalizers:
            f(self)

    def get_full_buffer(self):
        with self.buf_lock:
            return np.array([x[0] for x in self.buffer]), np.array([x[1] for x in self.buffer])



    def get_perf_stats2(self):
        return PerformanceData(
                cb_thread_id=self.event_cb_thread_id,
                cb_process_id=self.event_cb_process_id,
                event_rate=self.event_rate,
                event_cnt=self.event_cnt,
                cb_time_total=self.event_cb_time,
                cb_avg_time=self.event_cb_avg_time,
                avg_load=self.avg_load,
                connection_state_changes=list(self.connection_evt_timestamps),
                cb_timestamps=list(self.event_cb_timestamps),
                cb_time_history=list(self.event_cb_time_history),
        )


class EPICSStreamer(GenericStreamer):

    def process_monitor_event(self, x: caproto.EventAddResponse):
        try:
            self.event_cb_thread_id = threading.get_ident()
            self.event_cb_process_id = os.getpid()

            v = x.data
            t = x.metadata.timestamp
            tag = (int(t), int((t - int(t)) * 1e2) * 10)

            if self.debug:
                self.ldebug(f"ST [{self.name}] | Processed data {v=} {t=}")

            with self.buf_lock:
                self.buffer.append([v, t, tag])

            cb_results = self.run_callbacks(x)
            self.event_cb_result = {
                "success": True,
                "tag": tag,
                "cbs": cb_results,
                "evcnt": self.event_cnt,
            }
            self.event_cb_result_buffer.append(self.event_cb_result)

        except Exception as e:
            self.lerror(f"Error in event processing: {e} {traceback.format_exc()}")
            self.event_cb_result = {
                "success": False,
                "tag": None,
                "cbs": {},
                "evcnt": self.event_cnt,
            }
            self.event_cb_result_buffer.append(self.event_cb_result)

    def get_latest_buffers(self, n):
        if self.event_cnt < n:
            return None, None, None
        # release quickly
        with self.buf_lock:
            buffers = list(self.buffer)[-n:]
        data, times, tags = (
            [x[0][0] for x in buffers], #scalar
            [x[1] for x in buffers],
            [x[2] for x in buffers],
        )
        return np.array(data), np.array(times), tags

    def event_callback(self, sub: caproto.threading.client.Subscription, x: caproto.EventAddResponse):
        self.ldebug(f"ST [{self.name}] | monitor {x=}")
        try:
            self.callback_received = True
            t1 = time.time()
            if self.store_last_event:
                self.event_last = x
            with self.event_callback_lock:
                self.process_monitor_event(x)
            t2 = time.time()
            delta = t2 - t1
            self.event_cb_time += delta
            self.event_cnt += 1
            self.event_cb_last_timestamp = t1
            self.event_cb_time_history.append(delta)
            self.event_cb_timestamps.append(t1)
            self.event_cb_avg_time = self.event_cb_time / self.event_cnt
            if delta > self.event_cb_max_time:
                self.event_cb_max_time = delta
            if delta > self.event_fault_threshold:
                self.event_cb_fault_cnt += 1
            self.avg_load = self.event_cb_time / (t2 - self.time_start)

            self.ldebug(
                    f'ST {self.channel_name} | monitor {self.event_cb_result["tag"]} handled in'
                    f' {delta:.3f} at local times {t1} -> {t2}'
            )
            self.run_finalizers()
        except Exception as e:
            self.lerror(f"Error in monitor callback: {e} {traceback.format_exc()}")
        finally:
            if self.monitor_limit is not None:
                self.monitor_limit -= 1
                if self.monitor_limit <= 0:
                    self.logger.info(f"ST [{self.name}] | Monitor limit reached, stopping")
                    self.stop_monitor()

    def connect(self):
        self.channel: PV = self.acc.kv.get(self.channel_name)
        self.ldebug(f"Connecting to {self.channel_name} {self.channel=}")
        self.acc.ensure_connected(self.channel_name)
        if self.channel.connected:
            self._connection_cb(True)

        for i in range(500):
            if self.is_connected:
                break
            time.sleep(0.01)

        if not self.is_connected:
            raise Exception(f"Connection to {self.channel_name} failed")

        self.ldebug(f"Connected to {self.channel_name}")
        return True

    def start_monitor(self, limit=None):
        self.monitor_limit = limit
        if not self.is_connected:
            raise Exception("Not connected")
        if self.is_monitoring:
            raise Exception("Already running")

        self.time_start = time.time()
        self.acc.ensure_monitored(self.channel_name)
        self.acc.subscribe_custom(self.channel_name, self.event_callback)
        self.is_monitoring = True
        self.ldebug(f"ST [{self.name}] | started monitor")
        return self.is_monitoring

    def stop_monitor(self):
        if not self.is_monitoring:
            self.lerror("No monitor running")
            return
        self.stop_requested = True
        self.acc.unsubscribe_custom(self.channel_name, self.event_callback)
        self.is_monitoring = False
        self.stop_requested = False
        assert not self.stop_requested

    def get_callback_results(self) -> dict:
        return self.event_cb_result

    def get_callback_results_by_tag(self, tag) -> Optional[dict]:
        for r in self.event_cb_result_buffer:
            if r["tag"] == tag:
                return r
        return None


class DAQStreamer(ABC):
    def __init__(self, name: str, channel: str, buffer_size: int, debug=False):
        self.acc = Accelerator.get_singleton()
        self.name = name
        self.channel_name = channel

        self.logger = logging.getLogger(__name__)

        self.is_monitoring = False
        self.callback_received = False
        self.stop_requested = False
        self.event_last = None
        self.store_last_event = False
        self.n_channels = None
        self.buffer = collections.deque(maxlen=buffer_size)  # [None] * buffer_size
        self.buf_lock = threading.Lock()
        self.event_callback_lock = threading.Lock()
        self.field_spec = None
        self.fields_paths: dict[str, list[str]] = {}
        self.keys = None
        self.cbs: dict[str, Callable] = {}
        self.cbs_kwargs: dict[str, dict] = {}
        self.monitor_limit = None
        self.monitor_thread = None
        self.time_start: Optional[float] = None
        self.connection_evt_timestamps = collections.deque(maxlen=buffer_size)

        self.event_cb_time_history = collections.deque(maxlen=buffer_size)
        self.event_cb_timestamps = collections.deque(maxlen=buffer_size)
        self.event_cb_time = 0
        self.event_cnt = 0
        self.event_cb_thread_id = None
        self.event_cb_process_id = None
        self.event_cb_avg_time = 0.0
        self.event_cb_max_time = 0.0
        self.event_fault_threshold = 0.11
        self.event_cb_fault_cnt = 0
        self.event_cb_result = None
        self.event_cb_result_buffer = collections.deque(maxlen=buffer_size)

        self.avg_load = 0.0

        self.debug = debug

        self.channel = None
        self.is_connected = False

        self.log_with_print = True

        # if debug:
        #     print(f'Created streamer [{self.channel_name}]: have [{self.n_channels}] channels, {self.downsample=}')
        #     print(f'Field spec: {self.field_spec}')

    def __str__(self):
        return f"{self.__class__.__name__} {self.channel_name}: {self.is_monitoring=}, {self.is_connected=}"

    def exec_fun(self, f):
        return f(self)

    def ldebug(self, msg):
        if self.debug:
            if self.log_with_print:
                # Useful with ray
                print(msg)
            else:
                self.logger.debug(msg)

    def lerror(self, msg):
        if self.log_with_print:
            # Useful with ray
            print(msg)
        else:
            self.logger.error(msg, stacklevel=2)

    def connect(self):
        self.channel = self.acc.kvpva(self.channel_name)
        self.channel.setConnectionCallback(self._connection_cb)
        self.ldebug(f"Connecting to {self.channel_name} {self.channel=}")

        if self.channel.isConnected():
            self._connection_cb(True)

        for i in range(500):
            if self.is_connected:
                break
            time.sleep(0.01)

        if not self.is_connected:
            raise Exception(f"Connection to {self.channel_name} failed - pvapy reports {self.channel.isConnected()=}")

        fstr, fields_paths = self.get_channel_settings(self.channel)
        self.fields_paths = fields_paths
        self.field_spec = fstr
        self.n_channels = len(self.fields_paths)
        self.ldebug(f"Connected to {self.channel_name} with {self.n_channels} paths")
        return True

    @abstractmethod
    def get_channel_settings(self, channel) -> tuple[str, dict[str, list[tuple[str]]]]:
        """Return a list of paths in the struct to the data"""
        pass

    @property
    def load(self) -> float:
        if self.event_cnt == 0:
            return 0.0
        return np.mean(list(self.event_cb_time_history)) / 0.1

    @property
    def event_rate(self) -> float:
        if len(self.event_cb_timestamps) == 0:
            return 0.0
        times = list(self.event_cb_timestamps)
        return 1 / np.diff(times).mean() if len(times) > 2 else 0.0

    def _connection_cb(self, state: bool):
        if self.debug:
            now = datetime.datetime.now().isoformat(sep=" ", timespec="milliseconds")
            self.logger.info(f"Conn cb [{self.channel_name}]@[{now}] -> {state=}")
        self.connection_evt_timestamps.append((time.time(), state))
        self.is_connected = state

    def process_monitor_event(self, x):
        """Should override"""
        try:
            self.event_cb_thread_id = threading.get_ident()
            self.event_cb_process_id = os.getpid()
            cb_results = self.run_callbacks(x)
            self.event_cb_result = {"success": True, "cbs": cb_results}
            self.event_cb_result_buffer.append(self.event_cb_result)
        except Exception as e:
            self.lerror(f"Error in event processing: {e} {traceback.format_exc()}")
            self.event_cb_result = {"success": False, "cbs": {}}
            self.event_cb_result_buffer.append(self.event_cb_result)

    # gets pvaccess.pvaccess.PvObject
    def __cbinternal(self, x):
        if "acqClkTimestamp" not in x:
            raise Exception(f"No acqClkTimestamp in monitor for {self.channel_name} - have {x.keys()=}")
        time_tuple = (
            x["acqClkTimestamp"]["secondsPastEpoch"],
            x["acqClkTimestamp"]["nanoseconds"],
        )
        self.ldebug(f"ST [{self.name}] | monitor tag [{time_tuple}] callback with {x.keys()=}")
        try:
            self.callback_received = True
            t1 = time.time()
            if self.store_last_event:
                self.event_last = x.copy()
            with self.event_callback_lock:
                self.process_monitor_event(x)
            t2 = time.time()
            delta = t2 - t1
            # if delta > 0.08:
            #     print(f'Callback time {delta:.3f} IS TOO DAMN LONG')
            self.event_cb_time += delta
            self.event_cnt += 1
            self.event_cb_last_timestamp = t1
            self.event_cb_time_history.append(delta)
            self.event_cb_timestamps.append(t1)
            self.event_cb_avg_time = self.event_cb_time / self.event_cnt
            if delta > self.event_cb_max_time:
                self.event_cb_max_time = delta
            if delta > self.event_fault_threshold:
                self.event_cb_fault_cnt += 1
            self.avg_load = self.event_cb_time / (t2 - self.time_start)

            self.ldebug(
                    f'ST {self.channel_name} | monitor {self.event_cb_result["tag"]} handled in'
                    f' {delta:.3f} at local times {t1} -> {t2}'
            )

            if self.stop_requested:
                self.channel.stopMonitor()
                self.stop_requested = False
                self.is_monitoring = False
        except Exception as e:
            self.lerror(f"Error in monitor callback: {e} {traceback.format_exc()}")
        finally:
            if self.monitor_limit is not None:
                self.monitor_limit -= 1
                if self.monitor_limit <= 0:
                    self.logger.info(f"ST [{self.name}] | Monitor limit reached, stopping")
                    self.channel.stopMonitor()
                    self.is_monitoring = False

    def start_monitor(self, limit=None):
        self.monitor_limit = limit
        if not self.is_connected:
            raise Exception("Not connected")
        if self.is_monitoring:
            raise Exception("Already running")

        self.time_start = time.time()
        self.channel.monitor(self.__cbinternal, self.field_spec)
        self.is_monitoring = True
        # monitor_thread_started.set()

        # self.monitor_thread = threading.Thread(target=runnable, name=f'streamer_{self.channel_name}', daemon=True)
        # self.monitor_thread.start()
        # try:
        #    monitor_thread_started.wait(1.0)
        # except Exception as e:
        #    self.lerror(f'Error starting monitor thread: {e} {traceback.format_exc()}')
        #    self.is_monitoring = False
        # self.ldebug(f'ST {self.channel_name} | started monitor thread {self.monitor_thread.name}')
        self.ldebug(f"ST [{self.name}] | started monitor")
        return self.is_monitoring

    def start_monitor_triggered(self, trigger, limit=None):
        self.acc.ensure_monitored(trigger)
        self.acc.await_next_event(trigger)
        self.start_monitor(limit)

    def stop_monitor(self):
        if not self.is_monitoring:
            self.lerror("No monitor running")
            return
        self.stop_requested = True
        for i in range(200):
            if not self.is_monitoring:
                break
            time.sleep(0.01)
        if self.is_monitoring:
            raise Exception("Monitor thread did not stop")
        assert not self.stop_requested

    def add_callback(self, name: str, f: Callable, f_kwargs: Optional[dict] = None):
        """Add a callback function to be called for each new frame.

        :param name: Name of the callback
        :param f:  A callable (can be a class instance)
        :param f_kwargs: Keyword arguments to pass to the function
        """
        # TODO: weakref
        f_kwargs = f_kwargs or {}
        with self.event_callback_lock:
            self.cbs[name] = f
            self.cbs_kwargs[name] = f_kwargs

    def remove_callback(self, name: str):
        """Remove a callback"""
        with self.event_callback_lock:
            if name in self.cbs:
                del self.cbs[name]
                del self.cbs_kwargs[name]
            else:
                raise ValueError(f"No such callback {name}")

    def clear_callbacks(self):
        with self.event_callback_lock:
            self.cbs = {}

    def run_callbacks(self, pvo_dict: dict):
        self.ldebug(f"ST [{self.name}] | Running [{len(self.cbs)}] callbacks")
        cb_results = {}
        for k, f in self.cbs.items():
            try:
                cb_results[k] = f(streamer=self, data=pvo_dict, **self.cbs_kwargs[k])
                self.ldebug(f"ST [{self.name}] | CB [{k}] returned [{cb_results[k]}]")
            except Exception as e:
                self.lerror(f"Error in callback [{k}]: {e} {traceback.format_exc()}")
        return cb_results

    def get_full_buffer(self):
        with self.buf_lock:
            return np.vstack([x[0] for x in self.buffer]), np.hstack([x[1] for x in self.buffer])

    def get_latest_buffers(self, n, mode="ds"):
        if self.event_cnt < n:
            return None, None
        # release quickly
        with self.buf_lock:
            buffers = list(self.buffer)[-n:]
        matrices, times, tags = (
            [x[0] for x in buffers],
            [x[1] for x in buffers],
            [x[2] for x in buffers],
        )
        return np.vstack(matrices), np.hstack(times), tags

    def get_perf_stats(self):
        """Build all perf stats into a dict"""
        return {
            "event_cb_thread_id": self.event_cb_thread_id,
            "event_cb_process_id": self.event_cb_process_id,
            "event_rate": self.event_rate,
            "event_cb_time": self.event_cb_time,
            "event_cb_avg_time": self.event_cb_avg_time,
            "load": self.avg_load,
            "event_cnt": self.event_cnt,
            "connection_evt_timestamps": list(self.connection_evt_timestamps),
            "event_cb_timestamps": list(self.event_cb_timestamps),
            "event_cb_time_history": list(self.event_cb_time_history),
        }

    def get_perf_stats2(self):
        return PerformanceData(
                cb_thread_id=self.event_cb_thread_id,
                cb_process_id=self.event_cb_process_id,
                event_rate=self.event_rate,
                event_cnt=self.event_cnt,
                cb_time_total=self.event_cb_time,
                cb_avg_time=self.event_cb_avg_time,
                avg_load=self.avg_load,
                connection_state_changes=list(self.connection_evt_timestamps),
                cb_timestamps=list(self.event_cb_timestamps),
                cb_time_history=list(self.event_cb_time_history),
        )


class ArrayStreamer(DAQStreamer, RayMixin, ABC):
    TIME_FIELD = "time"
    TAG_FIELD = "acqClkTimestamp"

    def __init__(
            self,
            name,
            channel,
            devices,
            buffer_size,
            frame_len,
            fields=None,
            downsample=True,
            debug=False,
            ds_window=WINDOW,
            ds_step=STEP,
    ):
        self.fields: list[str] = fields
        self.devices = devices
        self.frame_len = frame_len
        self.buffer_idx = 0
        self.downsample = downsample
        self.ds_window = ds_window
        self.ds_step = ds_step
        self.rmmean1d = get_numba_rolling_mean_1d(frame_len, ds_window, ds_step)
        self.rmmean2d = get_numba_rolling_mean_2d(frame_len, ds_window, ds_step)
        self.downsampled_buffer = collections.deque(maxlen=buffer_size)  # [None] * buffer_size
        super().__init__(name, channel, buffer_size, debug)

    def get_latest_buffers(self, n, mode="ds") -> tuple[np.ndarray, np.ndarray, list[str]]:
        """Get the latest n buffers of particular kind"""
        if self.event_cnt < n:
            return None, None, []
        # release quickly
        if mode == "full":
            with self.buf_lock:
                buffers = list(self.buffer)[-n:]
            matrices, times, tags = (
                [x[0] for x in buffers],
                [x[1] for x in buffers],
                [x[2] for x in buffers],
            )
            return np.vstack(matrices), np.hstack(times), tags
        elif mode == "ds":
            # with self.buf_lock:
            #     matrices = [self.downsampled_buffer[i] for i in range(-n, 0)]
            # return np.vstack(matrices), np.hstack([x.index for x in matrices])
            with self.buf_lock:
                buffers = list(self.downsampled_buffer)[-n:]
            matrices, times, tags = (
                [x[0] for x in buffers],
                [x[1] for x in buffers],
                [x[2] for x in buffers],
            )
            return np.vstack(matrices), np.hstack(times), tags

    @abstractmethod
    def process_daq_object(
            self, x, ignore_errors=True
    ) -> tuple[list[np.ndarray], np.ndarray, list[str], tuple[int, int]]:
        pass

    def process_monitor_event(self, x):
        # print(self.buffer_idx, threading.current_thread().name, self.event_cnt)
        try:
            self.event_cb_thread_id = threading.get_ident()
            self.event_cb_process_id = os.getpid()

            mat_list, tarr, channels, tag = self.process_daq_object(x)
            for field, mat in zip(self.fields, mat_list):
                if mat is None:
                    self.ldebug(f"No data in PV object for {field=} {self.field_spec=} {x.keys()=}")

            if tarr is None:
                self.channel.stopMonitor()
                self.lerror(f"Missing time! {self.field_spec=} {x.keys()}")
                raise Exception(f"Missing time! {self.field_spec=} {x.keys()=}")
            # if len(bpm_names) <= self.n_channels, (f'Wrong channel count {len(bpm_names)=} {self.n_channels=}'
            #                                       f' {bpm_names=}')
            if self.keys is None:
                self.keys = channels
            else:
                if self.keys != channels:
                    self.channel.stopMonitor()
                    self.lerror(f"Names changed {self.keys=} {channels=}")
                    raise Exception("Names changed")

            if self.debug:
                mat_shapes = [m.shape if m is not None else None for m in mat_list]
                self.ldebug(f"ST [{self.name}] | Processed data {mat_shapes=} {tarr.shape=}")
                if TRACE:
                    self.ldebug(f"Got {channels=}")

            with self.buf_lock:
                # self.buffer[self.idx] = [mat, tarr]
                self.buffer.append(mat_list + [tarr] + [tag])
                if self.downsample:
                    # self.downsampled_buffer[self.idx] = self.df_rolling_mean(mat, tarr, bpm_names)
                    # self.downsampled_buffer.append(self.scipy_decimate(mat, tarr, bpm_names))
                    dmat_list = []
                    for mat in mat_list:
                        if mat is None:
                            dmat_list.append(None)
                            continue
                        dmat = self.rmmean2d(mat)
                        dtarr = self.rmmean1d(tarr)
                        dmat_list.append(dmat)
                    self.downsampled_buffer.append(dmat_list + [dtarr] + [tag])
                self.buffer_idx += 1

            if self.buffer_idx == len(self.buffer):
                self.buffer_idx = 0

            cb_results = self.run_callbacks(x)
            self.event_cb_result = {
                "success": True,
                "tag": tag,
                "cbs": cb_results,
                "evcnt": self.event_cnt,
            }
            self.event_cb_result_buffer.append(self.event_cb_result)
        except Exception as e:
            self.lerror(f"Error in event processing: {e} {traceback.format_exc()}")
            self.event_cb_result = {
                "success": False,
                "tag": None,
                "cbs": {},
                "evcnt": self.event_cnt,
            }
            self.event_cb_result_buffer.append(self.event_cb_result)
            # raise e

    def get_callback_results(self) -> dict:
        return self.event_cb_result

    def get_callback_results_by_tag(self, tag) -> Optional[dict]:
        for r in self.event_cb_result_buffer:
            if r["tag"] == tag:
                return r
        return None

    def get_available_tags(self) -> list:
        return [x["tag"] for x in self.event_cb_result_buffer]


class TBTStreamer(ArrayStreamer, RayMixin):
    DAQ_TYPE = "tbt"
    EXPECTED_TBT_FS = 352055e3 / 1296
    EXPECTED_TBT_FRAME_LEN = 27120

    def __init__(
            self,
            name,
            sector,
            channel,
            devices=None,
            buffer_size=100,
            fields=None,
            downsample=True,
            debug=False,
            daq_dec_factor=1,
            ds_window=WINDOW,
            ds_step=STEP,
    ):
        fields = fields or ["sum"]
        self.sector = sector
        super().__init__(
                name,
                channel,
                devices,
                buffer_size,
                fields=fields,
                downsample=downsample,
                debug=debug,
                frame_len=self.EXPECTED_TBT_FRAME_LEN // daq_dec_factor,
                ds_window=ds_window // daq_dec_factor,
                ds_step=ds_step // daq_dec_factor,
        )

    def get_channel_settings(self, channel) -> tuple[str, dict[str, list[tuple[str, ...]]]]:
        fields_paths, fstr = get_bpm_channel_properties(
                channel,
                self.devices,
                self.fields,
                time_field=self.TIME_FIELD,
                extra_fields=[self.TAG_FIELD],
        )
        return fstr, fields_paths

    def process_daq_object(self, x, ignore_errors=True):
        """Process the data dictionary from the PV"""
        data = x.toDict()
        return post_process_daq_object_via_paths(
                data,
                self.fields_paths,
                debug=self.debug,
                ignore_errors=ignore_errors,
                time_field=self.TIME_FIELD,
                frame_len=self.frame_len,
        )


class LifetimeTBTStreamer(TBTStreamer):
    def reset_counters(self):
        self.ldebug(f"ST [{self.name}] | Resetting lifetime counters")
        lt_cb: LifetimeCallback = self.cbs["lifetime"]
        lt_cb.reset_counters()
        return True


class FakeTBTStreamer(TBTStreamer):
    def __init__(self, *args, daemon=True, event_period=0.1, **kwargs):
        self.fake_source_stop = False
        self.event_period = event_period
        self.daemon = daemon
        super().__init__(*args, **kwargs)

    def connect(self):
        self.channel = f"SECTOR_{self.sector:02d}_TBT"
        self._connection_cb(True)
        fstr, fields_paths = self.get_channel_settings(self.channel)
        self.fields_paths = fields_paths
        self.field_spec = fstr
        self.n_channels = len(self.fields_paths)
        self.ldebug(f"FAKE | Connected to {self.channel_name} with paths {self.fields_paths}")
        return threading.get_ident(), os.getpid(), socket.gethostname()

    def get_channel_settings(self, channel) -> tuple[str, dict[str, list[tuple[str, ...]]]]:
        if self.sector == 1:
            fields_paths, fstr = (
                {"sum": [("bpm011", "sum"), ("bpm012", "sum")]},
                "field(bpm011.sum,bpm012.sum)",
            )
        elif self.sector == 3:
            fields_paths, fstr = (
                {"sum": [("bpm031", "sum"), ("bpm032", "sum")]},
                "field(bpm031.sum,bpm032.sum)",
            )
        else:
            raise Exception(f"Unknown channel {channel}")
        return fstr, fields_paths

    def start_monitor(self, limit=None):
        self.monitor_limit = limit
        self.fake_source_stop = False
        self.stop_requested = False
        if not self.is_connected:
            raise Exception("Not connected")
        if self.is_monitoring:
            raise Exception("Already running")

        def __cbinternal(x):
            self.ldebug(f"ST {self.channel_name} | monitor with {x.keys()=}")
            try:
                self.callback_received = True
                t1 = time.time()
                if self.store_last_event:
                    self.event_last = x.copy()
                with self.event_callback_lock:
                    self.process_monitor_event(x)
                t2 = time.time()
                delta = t2 - t1
                # if delta > 0.08:
                #     print(f'Callback time {delta:.3f} IS TOO DAMN LONG')
                self.event_cb_time += delta
                self.event_cnt += 1
                self.event_cb_last_timestamp = t1
                self.event_cb_time_history.append(delta)
                self.event_cb_timestamps.append(t1)
                self.event_cb_avg_time = self.event_cb_time / self.event_cnt
                if delta > self.event_cb_max_time:
                    self.event_cb_max_time = delta
                if delta > self.event_fault_threshold:
                    self.event_cb_fault_cnt += 1
                self.avg_load = self.event_cb_time / (t2 - self.time_start)

                self.ldebug(
                        f'ST {self.channel_name} | monitor {self.event_cb_result["tag"]} handled in'
                        f' {delta:.3f} at local times {t1} -> {t2}'
                )

                if self.stop_requested:
                    # self.channel.stopMonitor()
                    self.fake_source_stop = True
                    self.stop_requested = False
                    self.is_monitoring = False
            except Exception as e:
                self.lerror(f"Error in monitor callback: {e} {traceback.format_exc()}")
            finally:
                if self.monitor_limit is not None:
                    self.monitor_limit -= 1
                    if self.monitor_limit <= 0:
                        self.logger.info(f"ST {self.channel_name} | Monitor limit reached, stopping")
                        # self.channel.stopMonitor()
                        self.fake_source_stop = True
                        # self.is_monitoring = False

        monitor_thread_started = threading.Event()

        def fake_event_source(cb):
            try:
                self.logger.info("Fake event source started")
                N0 = 50000
                fake_cnt = 0
                self.is_monitoring = True
                monitor_thread_started.set()
                while not self.fake_source_stop:
                    t = time.time()
                    tarr = np.linspace(t - self.event_period, t, 27120)
                    toffsetarr = tarr - tarr[0]
                    # rand_slope = np.random.rand(1) * 0.01
                    # N = np.exp(-(1/3600)*(fake_cnt*0.1))*N0
                    N2 = np.exp(-(1 / 1800) * (fake_cnt * self.event_period + toffsetarr)) * N0
                    base_signal = N2.astype(np.float32)
                    base_x = np.random.rand(27120) * 0.01
                    # base_y = np.random.rand(27120) * 0.01
                    if self.sector == 1:
                        name1, name2 = "bpm011", "bpm012"
                    elif self.sector == 3:
                        name1, name2 = "bpm031", "bpm032"
                    else:
                        raise Exception(f"Unknown sector {self.sector}")
                    x = {
                        name1: {
                            "x": base_x.copy(),
                            "sum": np.random.rand(27120).astype(np.float32) * 1e0 + base_signal,
                        },
                        name2: {
                            "x": base_x.copy(),
                            "sum": np.random.rand(27120).astype(np.float32) * 1e0 + base_signal,
                        },
                        "time": tarr,
                        "acqClkTimestamp": {
                            "secondsPastEpoch": int(t),
                            "nanoseconds": int((t - int(t)) * 1e9),
                        },
                    }
                    pvo = FakePvObject(x)
                    fake_cnt += 1
                    # if self.debug:
                    #    logger.debug(f'Fake event emit {x=}')
                    t1 = time.time()
                    cb(pvo)
                    t2 = time.time()
                    time.sleep(max(0.0, self.event_period - (t2 - t1)))
            finally:
                self.logger.info("Fake event source stopped")
                self.is_monitoring = False

        try:
            self.time_start = time.time()
            fake_thread = threading.Thread(target=fake_event_source, args=(__cbinternal,), daemon=self.daemon)
            fake_thread.start()
        except Exception as e:
            self.lerror(f"Error starting monitor thread: {e} {traceback.format_exc()}")

        monitor_thread_started.wait()
        self.ldebug(f"ST {self.channel_name} | started monitor")
        return self.is_monitoring

    def stop_monitor(self):
        if not self.is_monitoring:
            self.lerror("No monitor running")
            return
        self.fake_source_stop = True
        self.stop_requested = True
        for i in range(200):
            if not self.is_monitoring:
                break
            time.sleep(0.01)
        if self.is_monitoring:
            raise Exception("Monitor thread did not stop")


class RayStreamerWrapper:
    PASSTHROUGH_METHODS = [
        "connect",
        "start_monitor",
        "get_callback_results_by_tag",
        "get_callback_results",
        "stop_monitor",
        "get_available_tags",
        "clear_callbacks",
        "add_callback",
        "reset_counters",
    ]
    SYNC_METHODS = ["get_perf_stats", "get_perf_stats2"]

    def __init__(self, ray_class, *args, reset_logging=True, **kwargs):
        import ray

        @ray.remote
        class WRAPPED_STREAMER_CLASS(ray_class):
            pass

        if reset_logging:
            config_root_logging(reset_handlers=True)

        self.ray_class = ray_class
        self.wrapped_class = WRAPPED_STREAMER_CLASS

        self.args = args
        self.kwargs = kwargs
        self.obj = WRAPPED_STREAMER_CLASS.remote(*args, **kwargs)

    def __getattr__(self, item):
        if item in RayStreamerWrapper.PASSTHROUGH_METHODS:
            return getattr(self.obj, item)
        elif item in RayStreamerWrapper.SYNC_METHODS:

            def f(*args, **kwargs):
                return self.__sync_call(item, *args, **kwargs)

            return f
        return object.__getattribute__(self, item)

    def remote(self, method, *args, **kwargs):
        return getattr(self.obj, method).remote(*args, **kwargs)

    def __sync_call(self, method, *args, **kwargs):
        import ray

        m = getattr(self.obj, method)
        return ray.get(m.remote(*args, **kwargs))

    def call_remotely(self, f):
        import ray

        return ray.get(self.obj.exec_fun.remote(f))


class LifetimeCallback:
    def __init__(self, lifetime_processors, debug=False):
        self.results = {}
        for k, v in lifetime_processors.items():
            self.results[k] = collections.deque(maxlen=100)
        self.counter = 0
        self.lifetime_processors = lifetime_processors
        self.result_last = {}
        self.result_combined = {k: {} for k in self.lifetime_processors.keys()}
        self.debug = debug
        self.logger = logging.getLogger(__name__)
        self.log_with_print = False

    def ldebug(self, msg):
        if self.debug:
            self.logger.debug(msg)

    def reset_counters(self):
        self.counter = 0

    def __call__(self, streamer: ArrayStreamer, data, st_name: str):
        from pybeamtools.physics.lifetime import compute_lifetime_exponential_v2

        cnt = self.counter
        updates = {}

        # if self.debug:
        #    print(f"Processing S{sector} {cnt=} from {streamer=}")
        for metric, metric_config in self.lifetime_processors.items():
            trigcnt, avgcnt = metric_config
            if cnt > 0 and cnt % trigcnt == 0:
                mat, times, tags = streamer.get_latest_buffers(avgcnt)
                if mat is not None:
                    lts = compute_lifetime_exponential_v2(times, mat)
                    # df = pd.DataFrame(lts[None, :], columns=streamer.keys, index=[time.time()])
                    # self.results[k][sector].append(df)
                    individual = {streamer.keys[i]: lts[i] for i in range(len(streamer.keys))}
                    # median_lt = np.median(lts)
                    updates[metric] = {
                        "timestamp": time.time(),
                        "raw": individual,
                        "msum": {streamer.keys[i]: np.mean(mat, axis=0)[i] for i in range(len(streamer.keys))}
                    }
                    self.result_combined[metric].update(updates[metric])
                    self.ldebug(
                            f"LTCB trig [{st_name=}] [{metric=}]: {mat.shape=} @ " f"{updates[metric]['timestamp']}"
                    )
                else:
                    self.ldebug(f"LTCB trig [{st_name=}] [{metric=}]: NO DATA")
        self.result_last = updates

        self.counter += 1
        self.ldebug(f"LTCB {cnt=} result [{st_name=}] = {self.result_last}")
        # return self.result_combined
        return self.result_last


class ScalarLifetimeCallback(LifetimeCallback):
    def __call__(self, streamer: ArrayStreamer, data, st_name: str):
        from pybeamtools.physics.lifetime import compute_lifetime_exponential_v2

        cnt = self.counter
        updates = {}

        for metric, metric_config in self.lifetime_processors.items():
            trigcnt, avgcnt = metric_config
            if cnt > 0 and cnt % trigcnt == 0:
                values, times, tags = streamer.get_latest_buffers(avgcnt)
                if values is not None:
                    if values.ndim != 1:
                        raise ValueError(f'Expected 1D array, got {values=}')
                    values = values.clip(1e-6, None)
                    values = values[:, None]
                    lts = compute_lifetime_exponential_v2(times, values)
                    assert len(lts) == 1, f'BAD LIFETIME {lts=} {values.shape=} {times.shape=} {tags=}'
                    individual = lts[0]
                    if not np.isfinite(individual):
                        individual = 0.0
                    updates[metric] = {
                        "timestamp": time.time(),
                        "raw": individual,
                    }
                    self.result_combined[metric].update(updates[metric])
                    self.ldebug(
                            f"LTCB trig [{st_name=}] [{metric=}]: {values.shape=} @ " f"{updates[metric]['timestamp']}"
                    )
                else:
                    self.ldebug(f"LTCB trig [{st_name=}] [{metric=}]: NO DATA")
        self.result_last = updates

        self.counter += 1
        self.ldebug(f"LTCB {cnt=} result [{st_name=}] = {self.result_last}")
        return self.result_last
