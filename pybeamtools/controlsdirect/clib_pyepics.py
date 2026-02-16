import asyncio
import functools
import logging
import time
from typing import Callable, Literal, Optional, TYPE_CHECKING

import numpy as np
import pandas as pd
import collections
from epics import PV, camonitor, caput_many, caget_many

logger = logging.getLogger(__name__)


class CB:
    acc = None

    @staticmethod
    def process(sub, response):
        # t1 = time.perf_counter()
        name = sub.pv.name
        acc = CB.acc
        c = acc.cnts.get(name, 0)
        acc.cnts[name] = c + 1
        b = acc.cbuf.get(name, None)
        if b is None:
            acc.cbuf[name] = []
        acc.cbuf[name].append((time.time(), response))
        # acc.cbuf[name].append((None, response))
        # acc.busytime += time.perf_counter()-t1


class RingBuffer:
    """ Not as fast as deque to append, but faster list conversion """

    def __init__(self, size):
        self.size = size
        self.buf = [None] * 100
        self.idx = 0
        self.len = 0

    def append(self, el):
        self.buf[self.idx] = el
        self.len = min(self.len + 1, self.size)
        self.idx = (self.idx + 1) % self.size

    def to_list(self):
        return self.buf[:self.len]


class AcceleratorPE:
    DELAY_AFTER_WRITE = 0.1  # s, mandatory sleep time after setting inputs
    READBACK_OK_TIMEOUT = 60  # s, error if readback doesn't match after this long
    DELAY_AFTER_RB = 0.1  # s, minimum time to wait after readback confirmed
    READBACK_TOTAL_SET_TIME_MIN = (
        2  # s, minimum overall cycle time (to keep pacing roughly same)
    )
    CBUF_SIZE = 64
    TRACE = False

    __slots__ = "cbuf", "df", "ctx", "__dict__", "kv"

    class KV:
        def __init__(self, acc) -> None:
            self.acc = acc
            self.channels: dict[str, PV] = {}
            pass

        def __getitem__(self, name: list[str]) -> list[PV]:
            return self.get(name)

        def get_one(self, name: str, monitor: bool = None) -> PV:
            return self.get([name], monitor)[0]

        def get(self, name: list[str], monitor: bool = None) -> list[PV]:
            monitor = monitor or self.acc.default_monitor
            assert isinstance(name, str) or isinstance(name, list)
            pvs = [None] * len(name)
            new_idxs = []
            for i, n in enumerate(name):
                pv = self.channels.get(n, None)
                if pv is None:
                    new_idxs.append(i)
                else:
                    pvs[i] = pv
            if len(new_idxs) > 0:
                # pvs = self.ctx.get_pvs(*name, priority=52)
                pvs = []
                for n in name:
                    pvs.append(PV(n))
                    time.sleep(0.02)
                for pv, idx in zip(pvs, new_idxs):
                    self.channels[name[idx]] = pv
                    self.acc.cnts[name[idx]] = 0
                    self.acc.cbuf[name[idx]] = collections.deque(maxlen=self.acc.CBUF_SIZE)
                    pvs[idx] = pv
                    if monitor and pv.name not in self.acc.kv_pvs:
                        self.acc.subscribe(pv)
                        self.acc.kv_pvs.append(pv.name)
            return pvs

    @staticmethod
    def get_singleton(ctx=None, default_monitor=True):
        if not hasattr(AcceleratorPE, "SINGLETON"):
            AcceleratorPE.SINGLETON = AcceleratorPE(ctx, default_monitor)
        return AcceleratorPE.SINGLETON

    def __init__(self, ctx=None, default_monitor=True) -> None:
        self.kv = self.KV(self)
        self.pvakv = None
        self.kv_pvs: list[str] = []
        self.knobs = {}
        self.io_map = {}
        self.oi_map = {}
        self.pv_io_map = {}
        self.iprops = {"low": {}, "high": {}, "atol": {}, "rtol": {}}
        self.df = None
        self.cbuf = {}
        self.cnts = {}
        self.callbacks = {}
        self.subs_custom = {}
        self.cbobj = CB
        CB.acc = self
        self.busytime = 0.0
        self.pvacache = {}
        self.default_monitor = default_monitor

    def subscribe(self, pv: PV):
        pvname = pv.pvname
        if pvname not in self.cbuf:
            self.cbuf[pvname] = collections.deque(maxlen=AcceleratorPE.CBUF_SIZE)
            self.cnts[pvname] = 0

        if pvname not in self.callbacks:
            self.callbacks[pvname] = []
        assert len(self.callbacks[pvname]) == 0

        cbf = self.cbobj.process
        sub_idx = pv.add_callback(cbf, data_type="time")
        # hold on to the reference
        self.callbacks[pvname].append((sub_idx, cbf))
        return sub_idx

    def subscribe_custom(self, pvname: str, f: Callable):
        pv = self.kv.get_one(pvname)
        sub_idx = pv.add_callback(f, data_type="time")
        if pvname not in self.subs_custom:
            self.subs_custom[pvname] = []
        self.subs_custom[pvname].append((sub_idx, f))

    def unsubscribe_custom(self, pvname: str, f: Callable):
        pv = self.kv.get_one(pvname)
        if pvname not in self.subs_custom:
            raise RuntimeError(f'No custom subscriptions for PV {pvname}')
        s = self.subs_custom[pvname]
        for tup in s:
            if tup[1] == f:
                pv.remove_callback(tup[0])
                s.remove(tup)

    def ensure_connection(self, pvs: list[PV], timeout=2):
        if not isinstance(pvs, list):
            raise ValueError("Expected list of PVs")
        for pv in pvs:
            if pv not in self.kv.channels.values():
                raise ValueError(f"PV {pv.pvname} not managed by KV")
        if all(pv.status == 0 for pv in pvs):
            return
        for pv in pvs:
            pv.wait_for_connection(timeout=timeout)

    def ensure_connected(self, name: str | list[str], timeout=2):
        if isinstance(name, str):
            name = [name]
        pvs = self.kv.get(name)
        self.ensure_connection(pvs, timeout)

    def ensure_monitored(self, name: str | list[str], timeout=2):
        if isinstance(name, str):
            name = [name]
        pvs = self.kv.get(name, monitor=True)
        self.ensure_connection(pvs, timeout=timeout)
        for pv in pvs:
            if not self.is_monitoring(pv.pvname):
                self.subscribe(pv)
                self.kv_pvs.append(pv.pvname)

    def is_monitoring(self, name: str):
        if len(self.callbacks[name]) > 0:
            return True
        return False

    def is_connected(self, name: str):
        pv = self.kv.get_one(name)
        return pv.status == 0

    def get_pvs(self, name: str | list[str], monitor: bool = True):
        return self.kv.get(name, monitor)

    def get_buffer(self, name: str):
        return self.cbuf[name]

    def get_latest_buffer_value(self, name: str, use_local_time: bool = True) -> tuple[float, float]:
        """ Get latest value from buffer """
        if name not in self.cbuf:
            raise ValueError(f"PV {name} is not being monitored")

        buf: collections.deque = self.cbuf[name]
        dps = list(buf)

        if len(dps) == 0:
            raise ValueError(f"PV {name} has no data in buffer")

        ts, r = dps[-1]
        ref_time = r.metadata.timestamp if not use_local_time else ts
        return ref_time, r.data[0]

    def get_buffer_data(
            self, name: str, start: float = None, use_local_time: bool = True
    ) -> list:
        """ Get buffer data for a PV starting from a given timestamp """
        buf: collections.deque = self.cbuf[name]
        dps = list(buf)

        if start is None:
            return [x[1] for x in dps]

        # idx = 0
        values = []
        for j in range(len(dps) - 1, -1, -1):
            ts, r = dps[j]
            # if r.metadata.timestamp is None:
            #     raise Exception(f"Found measurement {r} without timestamp")
            ref_time = r.metadata.timestamp if not use_local_time else ts
            if ref_time > start:
                values.append(r)
            else:
                break
        return values

    def get_buffer_df(
            self,
            name: str,
            start: float = None,
            use_local_time: bool = True,
            flatten: bool = True,
            relative: bool = False,
    ):
        responses = self.get_buffer_data(name, start, use_local_time)
        if len(responses) == 0:
            df = pd.DataFrame(index=[], data=[], columns=[name])
            df.index.name = "t"
        else:
            data = np.vstack([r.data for r in responses])
            if flatten and data.shape[1] == 1:
                data = data.squeeze(1)
            timestamps = np.array([r.metadata.timestamp for r in responses])
            if relative:
                timestamps -= start
            df = pd.DataFrame(index=timestamps, data=data, columns=[name])
            df.index.name = "t"
        return df

    def await_next_event(self, name: str, sleep: float = 1e-6, timeout=5.0):
        if not self.is_monitoring(name):
            raise ValueError(f"PV {name} is not being monitored")
        cnt = self.cnts[name]
        # TODO: see if semaphore might be feasible as far as performance goes
        t1 = time.time()
        while self.cnts[name] == cnt:
            if time.time() - t1 > timeout:
                raise ValueError(f"Timeout waiting for next event on {name}")
            time.sleep(sleep)
        return self.get_latest_buffer_value(name)

    def await_event_tag(self, name: str, tag: int, sleep: float = 1e-6, timeout=5.0):
        """ Wait for a specific event tag (aka monitor counter value) on a PV """
        if not self.is_monitoring(name):
            raise ValueError(f"PV {name} is not being monitored")
        assert tag > 0, "Tag must be a positive int"
        cnt = self.cnts[name]
        if cnt >= tag:
            return self.get_latest_buffer_value(name)
        t1 = time.time()
        while self.cnts[name] < tag:
            if time.time() - t1 > timeout:
                raise ValueError(f"Timeout waiting {tag=} for {name=} - latest tag {self.cnts[name]=}")
            time.sleep(sleep)
        return self.get_latest_buffer_value(name, use_local_time=False)

    def read(self, name: str, timeout: float = 1.0):
        pv = self.kv.get_one(name)
        self.ensure_connection([pv])
        result = pv.get_with_metadata(form="time", timeout=timeout, use_monitor=False)
        if len(result.data) == 1:
            r = result.data[0]
            if isinstance(r, (np.float64, np.float32)):
                return float(r)
            elif isinstance(r, np.integer):
                return int(r)
            else:
                raise Exception(f"Unknown single value type: {type(r)}")
        else:
            return result.data

    def read_all_now(self, names: str | list[str], timeout: float = 1.0, squeeze=False):
        if isinstance(names, str):
            names = [names]
        if not isinstance(names, list):
            try:
                names = list(names)
            except TypeError:
                raise ValueError(f'{names} is not iterable')
        names = list(set(names))

        for name in names:
            pv = self.kv.get_one(name)
            self.ensure_connection([pv])

        pvs = self.kv.get(names)
        results = {pv.pvname: pv.get(use_monitor=False, timeout=timeout) for pv in pvs}
        if squeeze:
            r2 = {}
            for k, v in results.items():
                if len(v) > 1:
                    r2[k] = v
                else:
                    r2[k] = v[0]
            return r2
        return results

    read_all = read_all_now

    def read_fresh(
            self,
            channels: list[str],
            timeout: float = 1.0,
            now: float = None,
            min_readings: int = 1,
            min_time: float = None,
            max_readings: int = None,
            reduce: Optional[Literal["mean", "median"]] = "mean",
            flatten: bool = True,
            include_timestamps: bool = False,
            use_buffer: bool = True,
            force_read: bool = True,
            stop_processing_on_min_readings: bool = False,
    ):
        """
        Get fresh PV data - readings considered unique if the timestamp is unique.

        :param channels: list of PVs to read
        :param timeout: timeout in seconds
        :param now: local time to use as "now" - events before are ignored
        :param min_time: Minimum time for data collection, regardless of readings
        :param min_readings: minimum number of readings to collect (getting less will raise an error)
        :param max_readings: maximum number of readings to collect (will use most recent ones)
        :param reduce: how to reduce multiple readings (mean, median, None (as array), ensure single)
        :param flatten: whether to flatten the inner (per-response) array
        :param include_timestamps: whether to return timestamps with values
        :param use_buffer: use the history buffer first before waiting for new events
        :param force_read: force an explicit read (vs monitoring) if the buffer is insufficient
        """
        t_start = time.time()
        if now is None:
            now = t_start  # Assume roughly synced with IOC
        assert min_readings is not None and min_readings >= 0
        assert max_readings is None or max_readings >= min_readings
        assert min_time is None or (0 <= min_time <= timeout)
        assert reduce is None or reduce in ["mean", "median"]
        if max_readings is None:
            max_readings = min_readings if min_readings > 1 else 1
        if self.TRACE:
            logger.debug(
                    f"FR of ({channels}): [{min_readings}-{max_readings}] "
                    f"reads in [{timeout}]s, reducer [{reduce}]"
            )

        channels = list(set(channels))
        channels_remaining = set(channels)
        pvs_map = {}
        for cn in channels:
            pv = self.kv[cn]
            self.ensure_connection([pv])
            pvs_map[cn] = pv

        max_observed_responses = {}
        ch_completed = {}
        # completed_channels = []
        last_event_times = {}
        raw_data = {}
        last_buffer_tag = {cn: -1 for cn in channels}

        for cn in channels:
            max_observed_responses[cn] = 0

            if use_buffer:
                responses, tag = self.get_buffer_data_tagged(cn, start=now, tag=last_buffer_tag[cn])
                if tag != -1:
                    raw_data[cn] = responses
                    last_buffer_tag[cn] = tag
            else:
                responses, tag = [], -1
            last_event_times[cn] = now
            if self.TRACE:
                logger.debug(
                        f"PV [{cn}]: initial state [{len(responses)}] / [{min_readings}]"
                )

        def check_timeout():
            if time.time() - t_start > timeout:
                still_need = set(channels) - set(ch_completed.keys())
                estr = f"FR timeout (still need {len(still_need)}/{len(channels)}): "
                for cn2 in still_need:
                    estr += f"\n({cn2}: [{max_observed_responses[cn2]}/{min_readings}])"
                raise ValueError(estr)

        def check_done():
            if len(ch_completed) == len(channels):
                if min_time is not None and time.time() - t_start < min_time:
                    if self.TRACE:
                        logger.debug(
                                f"FR min time not reached [{time.time() - t_start:.3f}]s"
                        )
                    return False
                else:
                    if self.TRACE:
                        logger.debug(
                                f"FR acquisition done in [{time.time() - t_start:.3f}]s"
                        )
                    return True
            else:
                # missing = set(channels) - set(completed_channels.keys())
                # logger.debug(f'FR not done yet [{len(completed_channels)}/{len(channels)}]: [{missing}]')
                return False

        stop = False
        while not stop:
            if check_done():
                stop = True
                break
            to_remove = []
            for i, cn in enumerate(channels_remaining):
                responses = raw_data.get(cn, [])
                n_responses = len(responses)
                max_observed_responses[cn] = n_responses
                if use_buffer:
                    time.sleep(0)
                    if stop_processing_on_min_readings and cn in ch_completed:
                        # JUST STOP ITERATING
                        continue
                    tnow = time.time()
                    bt = self.get_buffer_tag(cn)
                    if last_buffer_tag[cn] != bt:
                        responses_new = self.get_buffer_data(
                                cn, start=last_event_times[cn], use_local_time=True
                        )
                        last_buffer_tag[cn] = bt
                        if len(responses_new) > 0:
                            # this is very bad for performance :(
                            existing_times = {r.metadata.timestamp for r in responses}
                            for r in responses_new:
                                if r.metadata.timestamp not in existing_times:
                                    responses.append(r)
                            # responses.extend(responses_new)
                            last_event_times[cn] = tnow

                if n_responses >= min_readings and not ch_completed.get(cn, False):
                    if self.TRACE:
                        logger.debug(
                                f"PV [{cn}]: [{len(responses)}] / [{min_readings}] -> completed"
                        )
                    ch_completed[cn] = True
                    to_remove.append(cn)

                if ch_completed.get(cn, False):
                    if min_time is None:
                        continue

                if self.TRACE:
                    logger.debug(f"PV [{cn}]: [{len(responses)}] / [{min_readings}]")

                if force_read and not ch_completed.get(cn, False):
                    r = pvs_map[cn].read(data_type="time", timeout=timeout)
                    if r.metadata.timestamp > now:
                        if len(responses) > 0:
                            if responses[-1].metadata.timestamp == r.metadata.timestamp:
                                if self.TRACE:
                                    logger.debug(
                                            f"PV [{cn}]: stale read at [{r.metadata.timestamp}] (local {time.time()})"
                                    )
                                pass
                            else:
                                assert r.status.success == 1
                                responses.append(r)
                                if self.TRACE:
                                    logger.debug(
                                            f"PV [{cn}]: fresh read [{r.data}] at [{r.metadata.timestamp}] [{len(responses)} / {min_readings}]"
                                    )
                        else:
                            assert r.status.success == 1
                            responses.append(r)

                raw_data[cn] = responses

                if check_done():
                    stop = True
                    break

                check_timeout()
                time.sleep(0)

            for cn in to_remove:
                channels_remaining.remove(cn)

            if not stop:
                check_timeout()

            time.sleep(0.01)

        # All data is available - proceed
        r_dict = {}
        for i, cn in enumerate(channels):
            responses = raw_data[cn]
            if max_readings is not None and len(responses) > max_readings:
                responses = responses[-max_readings:]
            r_dict[cn] = responses

        value_dict = {}
        for cn, responses in r_dict.items():
            if len(responses) == 0:
                assert min_readings == 0
                value = None
                timestamp = None
            else:
                data = np.vstack([r.data for r in responses])
                if flatten and data.shape[1] == 1:
                    data = data.squeeze(1)
                timestamps = np.array([r.metadata.timestamp for r in responses])
                if reduce == "mean":
                    value = np.mean(data, axis=0)
                    timestamp = np.mean(timestamps, axis=0)
                elif reduce == "median":
                    value = np.median(data, axis=0)
                    timestamp = np.median(timestamps, axis=0)
                elif reduce == 'single_only':
                    assert len(data) == 1, f"Expected single reading for {cn}"
                    value = data[-1]
                    timestamp = timestamps[-1]
                elif reduce is None:
                    value = data
                    timestamp = timestamps
                else:
                    raise Exception(f"{reduce=} ???")

            if include_timestamps:
                value_dict[cn] = (timestamp, value)
            else:
                value_dict[cn] = value

        if self.TRACE:
            logger.debug(f"FR result: [{value_dict}]")

        return value_dict

    def write(self, data: dict[str, float], timeout: float = 1.0):
        pvs = self.kv.get(list(data.keys()))
        self.ensure_connection(pvs)

        for pv, value in zip(pvs, data.values()):
            pv.put(value=value, wait=False, timeout=timeout)

    def write_and_verify(
            self,
            data_dict: dict[str, float],
            readback_map: dict[str, str] = None,
            timeout: float = 1.0,
            readback_kwargs: dict = None,
            atol_map: dict[str, float] = None,
            rtol_map: dict[str, float] = None,
            low_map: dict[str, float] = None,
            high_map: dict[str, float] = None,
            read_first: bool = True,
            delay_after_write: float = None,
            readback_timeout: float = None,
            delay_after_readback: float = None,
            total_cycle_min_time: float = None,
            try_read_now_after: float = 2.0,
    ):
        """
        Write and verify PVs

        :param data_dict: dict of channels and values to write
        :param readback_map: dict of readback PVs for each PV in data - if None, no readback is used and verification skipped
        :param timeout: timeout for overall write and verify process
        :param readback_kwargs: kwargs for read_fresh used on readback PVs
        :param atol_map: dict of absolute tolerances for each PV
        :param rtol_map: dict of relative tolerances for each PV
        :param low_map: dict of lower bounds for each PV
        :param high_map: dict of upper bounds for each PV
        :param read_first: whether to check if readback is already good before writing
        :param delay_after_write: sleep after write
        :param readback_timeout:
        :param delay_after_readback: sleep after readback
        :param total_cycle_min_time: min total command runtime
        :param try_read_now_after: delay before explicit reads are attempted
        """
        logger.debug(f"WAV: start {data_dict=}")
        readback_map = readback_map or {}
        delay_after_write = delay_after_write or AcceleratorPE.DELAY_AFTER_WRITE
        delay_after_readback = delay_after_readback or AcceleratorPE.DELAY_AFTER_RB
        readback_timeout = readback_timeout or AcceleratorPE.READBACK_OK_TIMEOUT
        readback_kwargs = readback_kwargs or dict(min_readings=1, max_readings=1,
                                                  reduce="single_only", force_read=False)
        atol_map = atol_map or {}
        rtol_map = rtol_map or {}
        readback_map = {
            **(readback_map if readback_map is not None else {}),
            **self.io_map,
        }
        low_map = {**(low_map if low_map is not None else {}), **self.iprops["low"]}
        high_map = {**(high_map if high_map is not None else {}), **self.iprops["high"]}
        delay_between_fresh_reads = 0.5
        individual_read_timeout = timeout
        last_read_now_map = {}
        t_start = time.perf_counter()

        pvdict = data_dict.copy()
        for k, v in data_dict.items():
            if k not in atol_map:
                atol_map[k] = 0.0
            if k not in rtol_map:
                rtol_map[k] = 0.0
            atol, rtol = atol_map[k], rtol_map[k]
            low, high = low_map.get(k, -np.inf), high_map.get(k, +np.inf)
            assert not np.isnan(low) and not np.isnan(high)
            assert (
                    low <= v <= high
            ), f"Desired value [{v}] outside limits [{low}]-[{high}]"
            assert atol < np.abs(
                    high - low
            ), f"Absolute tolerance is larger than full variable span???"

            cn_readback = readback_map.get(k, None)
            if read_first and cn_readback is not None:
                pv_readback = self.kv[cn_readback]
                val = pv_readback.read().data[0]
                if np.isclose(val, v, atol=atol, rtol=rtol):
                    if self.TRACE:
                        logger.debug(
                                f"WAV: [{k}]=[{val:+.5f}] ({v=:+.5f}) already good"
                        )
                    del pvdict[k]
                    continue

        all_channels = list(pvdict.keys()) + [
            readback_map[k] for k in pvdict if k in readback_map
        ]
        all_pvs = self.kv[all_channels]
        self.ensure_connection(all_pvs)
        self.write(pvdict)

        logger.debug(
                f"WAV: connected in [{time.perf_counter() - t_start}:.5f]s, writing"
        )
        for k in list(pvdict.keys()):
            if readback_map.get(k, None) is None:
                del pvdict[k]
            else:
                last_read_now_map[k] = 0.0

        logger.debug(f"WAV: after-write sleep for [{delay_after_write}]s")
        time.sleep(delay_after_write)

        t_start_rb = time.perf_counter()
        now = time.time()
        rb_results = {}
        last_read = {}
        all_reads = {cn: [] for cn in pvdict}
        remaining_rbs = {}
        for k, v in pvdict.items():
            last_read[k] = None
            if readback_map.get(k) is None:
                rb_results[k] = None
            else:
                remaining_rbs[k] = v

        while len(rb_results) < len(pvdict):
            if self.TRACE:
                logger.debug(f"RB: loop {rb_results=}")
            to_remove = []
            for cn, setp in remaining_rbs.items():
                # if cn in rb_results:
                #     raise Exception
                cn_rb = readback_map[cn]

                # Check buffer for latest value
                try:
                    do_fresh = False
                    t_now = time.perf_counter()
                    if t_now - t_start > try_read_now_after and t_now - last_read_now_map[
                        cn] > delay_between_fresh_reads:
                        do_fresh = True

                    if do_fresh:
                        # this will force a new read
                        d = self.read_all_now(cn_rb, timeout=individual_read_timeout, squeeze=True)
                        last_read_now_map[cn] = t_now
                    else:
                        # latest cached value
                        d = self.read_fresh([cn_rb], now=now, timeout=individual_read_timeout,
                                            **readback_kwargs)
                    assert len(d) == 1 and cn_rb in d
                    val = d[cn_rb]
                    last_read[cn] = val
                    all_reads[cn].append(val)
                except ValueError:
                    continue

                if np.all(np.isclose(val, setp, atol=atol_map[cn], rtol=rtol_map[cn])):
                    rb_results[cn] = val
                    if self.TRACE:
                        logger.debug(f"WAV: {cn}={val:+.5f} ({setp=:+.5f}) finished")
                    to_remove.append(cn)
                else:
                    margin = (rtol_map[cn] * abs(setp)) + atol_map[cn]
                    if self.TRACE:
                        logger.debug(
                                f"WAV: ({cn})=({val:+.5f}) ({setp=:+.5f}) ({margin=})"
                        )
                time.sleep(0)

            if len(rb_results) == len(data_dict):
                break
            for cn in to_remove:
                del remaining_rbs[cn]
            dt = time.perf_counter() - t_start
            dt_rb = time.perf_counter() - t_start_rb
            if (timeout is not None and dt > timeout) or (
                    readback_timeout is not None and dt_rb > readback_timeout
            ):
                bads = {}
                bads_read = {}
                for k, v in data_dict.items():
                    if k in rb_results:
                        continue
                    bads[k] = v
                    bads_read[k] = last_read.get(k, None)
                    logger.debug(
                            f"WAV timeout: [{k}]-> want [{data_dict[k]}] vs last [{last_read[k]}]"
                    )
                raise ValueError(f"WAV: readback timeout [{bads=}] -> [{bads_read=}]")
            time.sleep(0.1)

        if delay_after_readback is not None:
            if self.TRACE:
                logger.debug(f"WAV: after-readback sleep for [{delay_after_readback}]")
            time.sleep(delay_after_readback)

        t_spent = time.perf_counter() - t_start
        if total_cycle_min_time is not None:
            t_sleep = max(0.0, total_cycle_min_time - t_spent)
            if t_sleep > 0:
                if self.TRACE:
                    logger.debug(f"WAV: min cycle time sleep for [{t_sleep}]")
                time.sleep(t_sleep)

        if self.TRACE:
            logger.debug(f"WAV: done in [{t_spent:.3f}]s")

        # resort dict
        rb_temp = {}
        for k in data_dict:
            if k in rb_results:
                rb_temp[k] = rb_results[k]
        return rb_temp

    def wav(self, pv_write, value, timeout=1.0):
        """Set PV and verify readback is within tolerance"""
        self.write_and_verify({pv_write: value}, timeout=timeout)
