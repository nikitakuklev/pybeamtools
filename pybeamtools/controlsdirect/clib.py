import logging
import time
from typing import Literal, Optional, TYPE_CHECKING

import numpy as np
import pandas as pd
import collections

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from caproto.threading.client import PV
    from caproto.threading.client import Batch


class Accelerator:
    DELAY_AFTER_WRITE = 0.1  # s, mandatory sleep time after setting inputs
    READBACK_OK_TIMEOUT = 60  # s, error if readback doesn't match after this long
    DELAY_AFTER_RB = 0.1  # s, minimum time to wait after readback confirmed
    READBACK_TOTAL_SET_TIME_MIN = 2  # s, minimum overall cycle time (to keep pacing roughly same)
    CBUF_SIZE = 100
    TRACE = False

    __slots__ = 'cbuf', 'df', 'ctx', '__dict__'

    class KV:
        def __init__(self, ctx, acc) -> None:
            self.ctx = ctx
            self.acc = acc
            pass

        def __getitem__(self, name: str):
            return self.get(name)

        def get(self, name: str, monitor: bool = True):
            if isinstance(name, list):
                pvs = self.ctx.get_pvs(*name, priority=99)
                if monitor:
                    for pv in pvs:
                        if pv.name not in self.acc.kv_pvs:
                            self.acc.subscribe(pv)
                            self.acc.kv_pvs.append(pv.name)
                return pvs
            elif isinstance(name, str):
                pv = self.ctx.get_pvs(name, priority=99)[0]
                if monitor:
                    if pv.name not in self.acc.kv_pvs:
                        self.acc.subscribe(pv)
                        self.acc.kv_pvs.append(pv.name)
                return pv
            else:
                raise Exception(f'{name} is not a list or string for PV')

    def __init__(self, ctx=None) -> None:
        if ctx is None:
            from caproto.threading.client import Context
            ctx = Context()
        self.ctx = ctx
        self.kv = self.KV(ctx, self)
        self.kv_pvs = []
        self.knobs = {}
        self.io_map = {}
        self.oi_map = {}
        self.pv_io_map = {}
        self.iprops = {'low': {}, 'high': {}, 'atol': {}, 'rtol': {}}
        self.df = None
        self.cbuf = {}
        self.callbacks = {}
        self.subs = {}

    def subscribe(self, pv):
        if pv.name not in self.cbuf:
            self.cbuf[pv.name] = collections.deque(maxlen=Accelerator.CBUF_SIZE)
        if pv.name not in self.callbacks:
            self.callbacks[pv.name] = []

        def callback(sub, response):
            name = sub.pv.name
            self.cbuf[name].append((time.time(), response))

        sub = pv.subscribe(data_type='time')
        self.subs[pv.name] = sub
        cb = callback
        sub.add_callback(cb)
        assert len(self.callbacks[pv.name]) == 0
        self.callbacks[pv.name].append(cb)

    def ensure_connection(self, pvs: list['PV'], timeout=2):
        for pv in pvs:
            pv.wait_for_search(timeout=timeout)
        for pv in pvs:
            pv.wait_for_connection(timeout=timeout)

    def add_knob(self, knob_name, readback_name, low, high, **kwargs):
        data = {}
        knob = self.kv[knob_name]
        readback = self.kv[readback_name]
        self.io_map[knob_name] = readback_name
        self.oi_map[readback_name] = knob_name
        self.pv_io_map[knob] = readback
        for k, v in kwargs.items():
            if k not in self.iprops:
                self.iprops[k] = {}
            self.iprops[k][knob_name] = v

        knob_start = data['input_start'] = knob.read(data_type='control')
        readback_start = data['readback_start'] = readback.read(data_type='control')
        knob_low = knob_start.metadata.lower_ctrl_limit
        knob_high = knob_start.metadata.upper_ctrl_limit
        if knob_low < low or knob_high > high:
            raise Exception(f'Bad limits found for {knob}: {knob_low=} to {knob_high=}')
        data['ca_low'] = knob_low
        data['ca_high'] = knob_high
        data['input_start'] = knob_start.data[0]
        data['readback_start'] = readback_start.data[0]
        data['input'] = knob.name
        data['readback'] = self.io_map[knob.name]
        data['pv_input'] = knob
        data['pv_readback'] = readback
        self.knobs[knob_name] = data
        if self.df is None:
            self.df = pd.DataFrame(index=self.knobs.keys(), data=self.knobs.values())
        else:
            dft = pd.DataFrame(index=[knob_name], data=[data])
            self.df = pd.concat([self.df, dft])

        # self.subscribe(knob)
        # self.subscribe(readback)

    def get_knob_df(self):
        # df = pd.DataFrame(index=self.knobs.keys(), data=self.knobs.values())
        return self.df

    def get_buffer_data(self, name: str, start: float = None, use_local_time: bool = True):
        buf = self.cbuf[name]
        dps = list(buf)
        idx = 0
        for dp in dps[::-1]:
            ts, r = dp
            if r.metadata.timestamp is None:
                raise Exception(f'Found measurement {r} without timestamp')
            ref_time = r.metadata.timestamp if not use_local_time else ts
            if start is None or ref_time > start:
                idx += 1
            else:
                break

        if idx > 0:
            # print(f'PV {name}: buffer had {idx} readings past {start} ({[r.metadata.timestamp for r in responses[-idx:]]})')
            return [x[1] for x in dps[-idx:]]
        else:
            # print(f'PV {name}: buffer had {idx} readings past {start} ({[]})')
            return []

    def get_buffer_df(self, name: str, start: float = None, use_local_time: bool = True,
                      flatten: bool = True, relative: bool = False):
        responses = self.get_buffer_data(name, start, use_local_time)
        if len(responses) == 0:
            df = pd.DataFrame(index=[], data=[], columns=[name])
            df.index.name = 't'
        else:
            data = np.vstack([r.data for r in responses])
            if flatten and data.shape[1] == 1:
                data = data.squeeze(1)
            timestamps = np.array([r.metadata.timestamp for r in responses])
            if relative:
                timestamps -= start
            df = pd.DataFrame(index=timestamps, data=data, columns=[name])
            df.index.name = 't'
        return df

    def read_now(self, name:str):
        return self.kv[name].read(data_type='time').data[0]

    def read_fresh(self,
                   channels: list[str],
                   timeout: float = 1.0,
                   now: float = None,
                   min_readings: int = 1,
                   max_readings: int = None,
                   reduce: Optional[Literal['mean', 'median']] = 'mean',
                   flatten: bool = True,
                   include_timestamps: bool = False,
                   use_buffer: bool = True,
                   force_read: bool = True):
        """
        Read fresh PV data or timeout
        Data is considered unique if the timestamp is unique

        :param channels: list of PVs to read
        :param timeout: timeout in seconds
        :param now: time to use as "now" for reading - everything before is ignored
        :param min_readings: minimum number of readings to collect
        :param max_readings: maximum number of readings to collect
        :param reduce: how to reduce multiple readings (mean or median or return all as array)
        :param flatten: whether to flatten the inner (per-response) array
        :param include_timestamps: whether to return timestamps with values
        :param use_buffer: whether to use the history buffer for reading
        :param force_read: whether to force an explicit read if the buffer is insufficient
        """
        t_start = time.time()
        if now is None:
            now = t_start  # Assume roughly synced with IOC
        assert min_readings is not None and min_readings >= 1
        assert max_readings is None or max_readings >= min_readings
        assert reduce is None or reduce in ['mean', 'median']
        if max_readings is None:
            max_readings = min_readings
        if self.TRACE:
            logger.debug(f'FR of ({channels}): [{min_readings}-{max_readings}] '
                         f'reads in [{timeout}]s, reducer [{reduce}]')
        pvs_map = {cn: self.kv[cn] for cn in channels}

        max_observed_responses = {}
        completed_channels = []
        last_event_times = {}
        raw_data = {}

        for cn in channels:
            max_observed_responses[cn] = 0

            if use_buffer:
                responses = self.get_buffer_data(cn, start=now, use_local_time=True)
            else:
                responses = []
            raw_data[cn] = responses
            last_event_times[cn] = now
            if self.TRACE:
                logger.debug(f'PV [{cn}]: initial state [{len(responses)}] / [{min_readings}]')

        while True:
            if len(completed_channels) == len(channels):
                break

            for i, cn in enumerate(channels):
                if cn in completed_channels:
                    continue
                responses = raw_data[cn]
                if use_buffer:
                    tnow = time.time()
                    responses_new = self.get_buffer_data(cn, start=last_event_times[cn], use_local_time=True)
                    if len(responses_new) > 0:
                        # this is very bad for performance :(
                        existing_times = {r.metadata.timestamp for r in responses}
                        for r in responses_new:
                            if r.metadata.timestamp not in existing_times:
                                responses.append(r)
                        # responses.extend(responses_new)
                        last_event_times[cn] = tnow

                max_observed_responses[cn] = len(responses)
                if len(responses) >= min_readings:
                    completed_channels.append(cn)
                    continue

                if self.TRACE:
                    logger.debug(f'PV [{cn}]: [{len(responses)}] / [{min_readings}]')
                if force_read:
                    r = pvs_map[cn].read(data_type='time', timeout=timeout)
                    if r.metadata.timestamp > now:
                        if len(responses) > 0:
                            if responses[-1].metadata.timestamp == r.metadata.timestamp:
                                if self.TRACE:
                                    logger.debug(
                                        f'PV [{cn}]: stale read at [{r.metadata.timestamp}] (local {time.time()})')
                                pass
                            else:
                                assert r.status.success == 1
                                responses.append(r)
                                if self.TRACE:
                                    logger.debug(
                                        f'PV [{cn}]: fresh read [{r.data}] at [{r.metadata.timestamp}] [{len(responses)} / {min_readings}]')
                        else:
                            assert r.status.success == 1
                            responses.append(r)

                if time.time() - t_start > timeout:
                    still_need = set(channels) - set(completed_channels)
                    estr = f'FR timeout: '
                    for cn2 in still_need:
                        estr += f'\n({cn2}: [{max_observed_responses[cn2]}/{min_readings}])'
                    raise ValueError(estr)
                raw_data[cn] = responses
                time.sleep(0.02)

            # while len(responses) < min_readings:
            #     r = pv.read(data_type='time', timeout=timeout)
            #     if r.metadata.timestamp > now:
            #         if len(responses) > 0:
            #             if responses[-1].metadata.timestamp == r.metadata.timestamp:
            #                 # print(f'PV {pv.name}: stale read at ts {r.metadata.timestamp}')
            #                 pass
            #             else:
            #                 assert r.status.success == 1
            #                 responses.append(r)
            #                 # print(f'PV {pv.name}: fresh read {r.data} at ts {r.metadata.timestamp} ({len(responses)} of {min_readings})')
            #         else:
            #             assert r.status.success == 1
            #             responses.append(r)
            #     if time.perf_counter() - t_start > timeout:
            #         raise Exception(
            #             f'PV {pv.name} read timed out at {time.time()} (record time {r.metadata.timestamp})')
            #     # print(f'Continuing PV read {pv.name} at {time.time()} (record time {r.metadata.timestamp})')
            #     time.sleep(0.01)

        # All data is available - proceed
        r_dict = {}
        for i, cn in enumerate(channels):
            responses = raw_data[cn]
            if max_readings is not None and len(responses) > max_readings:
                responses = responses[-max_readings:]
            r_dict[cn] = responses

        value_dict = {}
        for cn, responses in r_dict.items():
            data = np.vstack([r.data for r in responses])
            if flatten and data.shape[1] == 1:
                data = data.squeeze(1)
            timestamps = np.array([r.metadata.timestamp for r in responses])
            if reduce == 'mean':
                value = np.mean(data, axis=0)
                timestamp = np.mean(timestamps, axis=0)
            elif reduce == 'median':
                value = np.median(data, axis=0)
                timestamp = np.median(timestamps, axis=0)
            elif reduce is None:
                value = data
                timestamp = timestamps
            else:
                raise Exception(f'{reduce=} ???')

            if include_timestamps:
                value_dict[cn] = (timestamp, value)
            else:
                value_dict[cn] = value

        if self.TRACE:
            logger.debug(f'FR result: [{value_dict}]')

        return value_dict

    def write_and_verify(self,
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
        :param timeout: timeout for write
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
        logger.debug(f'WAV: start {data_dict=}')
        readback_map = readback_map or {}
        delay_after_write = delay_after_write or Accelerator.DELAY_AFTER_WRITE
        delay_after_readback = delay_after_readback or Accelerator.DELAY_AFTER_RB
        readback_timeout = readback_timeout or Accelerator.READBACK_OK_TIMEOUT
        readback_kwargs = readback_kwargs or dict(min_readings=1)
        atol_map = atol_map or {}
        rtol_map = rtol_map or {}
        readback_map = {**(readback_map if readback_map is not None else {}), **self.io_map}
        low_map = {**(low_map if low_map is not None else {}), **self.iprops['low']}
        high_map = {**(high_map if high_map is not None else {}), **self.iprops['high']}
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
            assert low <= v <= high, f'Desired value [{v}] outside limits [{low}]-[{high}]'
            assert atol < np.abs(high - low), f'Absolute tolerance is larger than full variable span???'

            cn_readback = readback_map.get(k, None)
            if read_first and cn_readback is not None:
                pv_readback = self.kv[cn_readback]
                val = pv_readback.read().data[0]
                if np.isclose(val, v, atol=atol, rtol=rtol):
                    if self.TRACE:
                        logger.debug(f'WAV: [{k}]=[{val:+.5f}] ({v=:+.5f}) already good')
                    del pvdict[k]
                    continue

        all_channels = list(pvdict.keys()) + [readback_map[k] for k in pvdict if k in readback_map]
        all_pvs = list([self.kv[cn] for cn in all_channels])
        self.ensure_connection(all_pvs)

        from caproto.threading.client import Batch
        with Batch(timeout=timeout) as b:
            for (pvn, value) in pvdict.items():
                pv_input = self.kv[pvn]
                b.write(pv_input, value)

        logger.debug(f'WAV: connected in [{time.perf_counter()-t_start}:.5f]s, writing')
        for k in list(pvdict.keys()):
            if readback_map.get(k, None) is None:
                del pvdict[k]
            else:
                last_read_now_map[k] = 0.0

        logger.debug(f'WAV: after-write sleep for [{delay_after_write}]s')
        time.sleep(delay_after_write)

        t_start_rb = time.perf_counter()
        now = time.time()
        rb_results = {}
        last_read = {}
        all_reads = {cn: [] for cn in pvdict}
        while len(rb_results) < len(pvdict):
            if self.TRACE:
                logger.debug(f'RB: loop {rb_results=}')

            for (cn, setp) in pvdict.items():
                if cn in rb_results:
                    continue
                if cn not in readback_map or readback_map[cn] is None:
                    rb_results[cn] = last_read[cn] = None
                    continue
                cn_rb = readback_map[cn]

                # Check buffer for latest value
                try:
                    do_fresh = False
                    if time.perf_counter() - t_start > try_read_now_after:
                        if time.perf_counter() - last_read_now_map[cn] > 2.0:
                            do_fresh = True

                    if do_fresh:
                        # this will force a new read
                        d = self.read_fresh([cn_rb])
                        last_read_now_map[cn] = time.perf_counter()
                    else:
                        # latest cached value
                        d = self.read_fresh([cn_rb], now=now, **readback_kwargs)
                    assert len(d) == 1 and cn_rb in d
                    val = d[cn_rb]
                    last_read[cn] = val
                    all_reads[cn].append(val)
                except ValueError:
                    last_read[cn] = None
                    continue

                if np.all(np.isclose(val, setp, atol=atol_map[cn], rtol=rtol_map[cn])):
                    rb_results[cn] = val
                    if self.TRACE:
                        logger.debug(f'WAV: {cn}={val:+.5f} ({setp=:+.5f}) finished')
                else:
                    margin = (rtol_map[cn] * abs(setp)) + atol_map[cn]
                    if self.TRACE:
                        logger.debug(f'WAV: ({cn})=({val:+.5f}) ({setp=:+.5f}) ({margin=})')
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
                    logger.debug(f'WAV timeout: [{k}]-> want [{data_dict[k]}] vs last [{last_read[k]}]')
                raise ValueError(f'WAV: readback timeout [{bads=}] -> [{bads_read=}]')
            time.sleep(0.1)

        if delay_after_readback is not None:
            if self.TRACE:
                logger.debug(f'WAV: after-readback sleep for [{delay_after_readback}]')
            time.sleep(delay_after_readback)

        t_spent = time.perf_counter() - t_start
        if total_cycle_min_time is not None:
            t_sleep = max(0.0, total_cycle_min_time - t_spent)
            if t_sleep > 0:
                if self.TRACE:
                    logger.debug(f'WAV: min cycle time sleep for [{t_sleep}]')
                time.sleep(t_sleep)

        if self.TRACE:
            logger.debug(f'WAV: done in [{t_spent:.3f}]s')

        # resort dict
        rb_temp = {}
        for k in data_dict:
            if k in rb_results:
                rb_temp[k] = rb_results[k]
        return rb_temp

    def set_and_verify_multiple(self, pvdict, timeout=1.0, readback_kwargs=None):
        kv = self.kv
        df = self.df
        readback_kwargs = readback_kwargs or dict(min_readings=1)
        assert all(k in self.df.index for k in pvdict.keys())
        t_start = time.perf_counter()
        for (pvn, value) in pvdict.items():
            pv_input = kv[pvn]
            pv_read = df.loc[pv_input.name, 'pv_readback']
            low = df.loc[pv_input.name, 'low']
            high = df.loc[pv_input.name, 'high']
            atol = df.loc[pv_input.name, 'atol']
            if np.isnan(atol):
                raise Exception(f'Please provide tolerance for {pvn}')
            assert not np.isnan(low) and not np.isnan(high)
            assert low <= value <= high
            assert atol < np.abs(high - low)
            val = pv_read.read().data[0]
            if np.isclose(val, value, atol=atol, rtol=0):
                # del pvdict[pvn]
                pass

        with Batch(timeout=timeout) as b:
            for (pvn, value) in pvdict.items():
                pv_input = self.kv[pvn]
                b.write(pv_input, value)
                # assert r.status.success == 1

        time.sleep(self.DELAY_AFTER_WRITE)
        now = time.time()
        values = {}
        last_read = {}
        while len(values) < len(pvdict):
            # print(f'set outer loop {len(values)=}')
            for (pvn, value) in pvdict.items():
                if pvn in values:
                    continue
                # print(f'set loop {pvn=}')
                pv_input = self.kv[pvn]
                pv_read = df.loc[pv_input.name, 'pv_readback']
                atol = df.loc[pv_input.name, 'atol']
                val = self.read_fresh(pv_read, timeout=timeout, now=now, **readback_kwargs)[0]
                last_read[pvn] = val
                if np.all(np.isclose(val, value, atol=atol, rtol=0)):
                    values[pvn] = val
            # print(f'set outer loop 2 {len(values)=} {last_read=}')
            if time.perf_counter() - t_start > self.READBACK_OK_TIMEOUT:
                for (pvnl, valuel) in pvdict.items():
                    pv_inputl = self.kv[pvnl]
                    atoll = df.loc[pv_inputl.name, 'atol']
                    print(f'{pvnl:20}: {valuel=} {last_read[pvnl]=} {(valuel - last_read[pvnl])=} {atoll=}')
                raise IOError(f'Setting {pv_input.name} failed - readback {pv_read.name} ({val}) bad (want {value})')
            time.sleep(0.1)

        t_spent = time.perf_counter() - t_start
        t_sleep = max(self.DELAY_AFTER_RB, self.READBACK_TOTAL_SET_TIME_MIN - t_spent)
        time.sleep(t_sleep)
        return values

    def wav(self, pv_write, value, timeout=1.0):
        """ Set PV and verify readback is within tolerance """
        self.write_and_verify({pv_write: value}, timeout=timeout)
