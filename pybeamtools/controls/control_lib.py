import logging
import queue
import time
from typing import Literal

import numpy as np

from pydantic import BaseModel, Field

from .errors import InterlockWriteError, ControlLibException, WrappedException
from .interlocks import Interlock, InterlockOptions

from .distributed import ProcessManager
from .knobs import Knob, KnobManager
from .network import EPICSConnectionManager, PVOptions, SimConnectionManager


class ReadbackOptions(BaseModel):
    delay_after_write: float = Field(1.0,
                                     description="mandatory sleep time after setting inputs")
    readback_match_timeout: float = Field(60.0,
                                          description="error if readback doesn't match after this long")
    delay_after_readback: float = Field(3.0,
                                        description="minimum time to wait after readback confirmed")
    total_set_and_readback_cycle_min_time: float = Field(None,
                                                         description="minimum overall cycle time (to keep pacing roughly same)")


class WriteOptions(BaseModel):
    pass


class ConnectionOptions(BaseModel):
    network: Literal['epics', 'dummy'] = 'dummy'


class AcceleratorOptions(BaseModel):
    write_settings: WriteOptions = WriteOptions()
    readback_settings: ReadbackOptions = ReadbackOptions()
    connection_settings: ConnectionOptions = ConnectionOptions()
    interlocks: list[InterlockOptions] = []
    pvs: list[PVOptions] = []


class Accelerator:
    def __init__(self, options: AcceleratorOptions = None, ctx=None) -> None:
        # config_root_logging()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info('Control lib init')
        if options is None:
            options = AcceleratorOptions()

        self.options = options
        self.knobs = {}
        self.df = None
        self.TRACE = False

        self.pm = ProcessManager()
        if options.connection_settings.network == 'epics':
            self.cm = EPICSConnectionManager(acc=self, ctx=ctx)
        elif options.connection_settings.network == 'dummy':
            self.cm = SimConnectionManager(acc=self, ctx=ctx)
        self.km = KnobManager()

        self.interlocks: list[Interlock] = []
        self.pvn_to_ilocks_map = {}

        # self.logger.info('Spawning repeater')
        # from caproto.sync import repeater
        # repeater.spawn_repeater()
        self.logger.info('Startup finished')

    def __getitem__(self, item):
        return self.cm.get_pvs([item])[0]

    @property
    def pv_names(self):
        return list(self.cm.pv_map.keys())

    def add_pv_object(self, *args, **kwargs):
        return self.cm.add_pvs_objects(*args, **kwargs)

    def add_pv(self, *args, **kwargs):
        """ Add PVs by name """
        return self.cm.add_pvs(*args, **kwargs)

    def add_pvs(self, *args, **kwargs):
        """ Add PVs by name """
        return self.cm.add_pvs(*args, **kwargs)

    def get_pv(self, pv_name):
        return self.cm.get_pvs([pv_name])[0]

    def get_pvs(self, pvs_names):
        """ Get PV objects from EPICS channel names"""
        return self.cm.get_pvs(pvs_names)

    def add_knob(self,
                 write_pv_name: str,
                 readback_pv_name: str = None,
                 store_current_values: bool = False):
        assert write_pv_name in self.cm, f'Write PV {write_pv_name} has not been added'
        assert readback_pv_name in self.cm, f'Readback PV {readback_pv_name} has not been added'
        data = {}
        knob = self.get_pv(write_pv_name)

        data['ca_low'] = knob.lower_ctrl_limit
        data['ca_high'] = knob.upper_ctrl_limit
        data['write_start'] = np.nan
        if store_current_values:
            data['write_start'] = knob.read().data[0]
        data['input'] = write_pv_name
        data['pv_input'] = knob

        if readback_pv_name is not None:
            # data['readback_start'] = np.nan
            # if store_current_values:
            #     data['readback_start'] = knob.read().data[0]
            readback = self.get_pv(readback_pv_name)
            self.km.io_map[write_pv_name] = readback_pv_name
            self.km.oi_map[readback_pv_name] = write_pv_name
            # data['readback_start'] = readback.read().data[0]
            data['pv_readback'] = readback
            data['readback'] = readback_pv_name
        else:
            # data['readback_start'] = np.nan
            data['pv_readback'] = None
            data['readback'] = None

        knob = Knob(write_pv_name=write_pv_name,
                    readback_pv_name=readback_pv_name)
        self.km.knobs_map_write[write_pv_name] = knob
        self.km.knobs_map_readback[readback_pv_name] = knob
        self.km.knobs.append(knob)

    @property
    def knob_df(self):
        return self.km.get_df()

    def ensure_connection(self, pvs, timeout=2):
        if not isinstance(pvs, list):
            pvs = [pvs]
        for pv in pvs:
            pv.wait_for_search(timeout=timeout)
            pv.wait_for_connection(timeout=timeout)

    def get_knob_df(self):
        """ Retrieve dataframe that contains all knobs added so far along with EPICS info """
        # df = pd.DataFrame(index=self.knobs.keys(), data=self.knobs.values())
        return self.df

    def propose_write(self, pvs_name: list[str], pvs_data: list):
        for pv_name, data in zip(pvs_name, pvs_data):
            assert pv_name in self.cm.pv_map
            pv = self.cm.pv_map[pv_name]
            pv._check_proposed_write(data)
        self.logger.debug(f'Individual PV validation passed')
        triggered_interlocks = [i for i in self.interlocks if i.check_match_write(pvs_name, pvs_data)]
        # triggered_uuids = [i.uuid for i in triggered_interlocks]
        self.logger.info(
            f'Write on ({pvs_name}) triggered ({len(triggered_interlocks)}) of ({len(self.interlocks)}) interlocks')
        if len(triggered_interlocks) == 0:
            self.logger.debug('No interlocks triggered, skip polling stage')
            return
        data_packages = []
        all_known_pvs = list(self.cm.pv_map.keys())
        for i in triggered_interlocks:
            filtered_pv_names = i.filter_pv_names(all_known_pvs)
            triggered_pvs = {}
            for pv_name, data in zip(pvs_name, pvs_data):
                if pv_name in i.options.write_events:
                    triggered_pvs[pv_name] = data
            pv_data = {}
            for k in filtered_pv_names:
                v = self.cm.last_results_map.get(k, None)
                if v is None:
                    self.logger.warning(f'No last value available for PV ({k})')
                    raise ControlLibException(
                        f'No values available for PV ({k}), make sure to read or enable monitoring')
                    # data[k] = v
                else:
                    pv_data[k] = v
            data_packages.append({'trigger_pvs': triggered_pvs, 'data': pv_data, 'timestamps': None})
        self.logger.debug(f'Polling process manager with data packages of sizes ({[len(d) for d in data_packages]})')
        self.logger.debug(f'{data_packages=}')
        t1 = time.perf_counter()
        responses = self.pm.poll(interlocks_list=triggered_interlocks, data_list=data_packages)
        self.logger.info(f'Polling completed in {(time.perf_counter() - t1) * 1000:.2f}ms')
        failed_ex = False
        failed_result = False
        for (uuid, r) in responses:
            if isinstance(r, Exception):
                failed_ex = True
                if isinstance(r, WrappedException):
                    self.logger.warning(f'Interlock ({uuid}) raised exception {r.ex}')
                    self.logger.error(f'{r.tb}')
                elif isinstance(r, queue.Empty):
                    self.logger.error(f'Interlock ({uuid}) did not respond in time')
                else:
                    self.logger.error(f'Interlock ({uuid}) exception', exc_info=r)
            else:
                if not r.data['result']:
                    self.logger.error(f'Interlock ({r.uuid}) rejected proposed write - result was ({r.data})')
                    failed_result = True

        if failed_ex:
            raise InterlockWriteError(
                f'Write on ({pvs_name}) of ({pvs_data}) failed due to exceptions raised by interlocks')
        if failed_result:
            raise InterlockWriteError(f'Write on ({pvs_name}) of ({pvs_data}) failed due to interlock rejection')

    def add_interlock(self, interlock: Interlock):
        for pv_name in interlock.options.pv_list:
            if pv_name not in self.cm.pv_map:
                raise Exception(f'PV ({pv_name}) has not been defined')
        for i in self.interlocks:
            if i.uuid == interlock.uuid:
                raise ControlLibException(f'Interlock ({interlock.uuid}) is already added')
        self.pm.start_interlock(interlock)
        self.interlocks.append(interlock)
        self.logger.info(f'Interlock ({interlock.uuid}) with PV list ({interlock.options.pv_list}) added')

    def remove_interlock(self, interlock: Interlock):


    def read_fresh(self, pvs_read, timeout=1.0, now=None, min_readings=1, max_readings=None,
                   reduce='mean', include_timestamps=False, use_buffer=True):
        """ Read next PV update or timeout """
        if now is None:
            now = time.time()  # Assume roughly synced with IOC
        t_start = time.perf_counter()
        assert min_readings is not None and min_readings >= 1
        assert max_readings is None or max_readings >= min_readings
        if max_readings is None:
            max_readings = min_readings
        if not isinstance(pvs_read, list):
            pvs_read = [pvs_read]
        values = [None] * len(pvs_read)
        for i, pv in enumerate(pvs_read):
            if use_buffer:
                responses = self._get_recent_buffer_data(pv.name, start=now)
            else:
                responses = []
            if max_readings is not None and len(responses) > max_readings:
                responses = responses[-max_readings:]
            # print(f'PV {pv.name}: got {len(responses)} buffered responses of {min_readings}')
            while len(responses) < min_readings:
                r = pv.read(data_type='time', timeout=timeout)
                if r.metadata.timestamp > now:
                    if len(responses) > 0:
                        if responses[-1].metadata.timestamp == r.metadata.timestamp:
                            # print(f'PV {pv.name}: stale read at ts {r.metadata.timestamp}')
                            pass
                        else:
                            assert r.status.success == 1
                            responses.append(r)
                            # print(f'PV {pv.name}: fresh read {r.data} at ts {r.metadata.timestamp} ({len(responses)} of {min_readings})')
                    else:
                        assert r.status.success == 1
                        responses.append(r)
                if time.perf_counter() - t_start > timeout:
                    raise Exception(
                        f'PV {pv.name} read timed out at {time.time()} (record time {r.metadata.timestamp})')
                # print(f'Continuing PV read {pv.name} at {time.time()} (record time {r.metadata.timestamp})')
                time.sleep(0.01)

            data = np.vstack([r.data for r in responses])
            timestamps = np.vstack([r.metadata.timestamp for r in responses])
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
                values[i] = (timestamp, value)
            else:
                values[i] = value
        return values

    def read(self, pvs_read: list[str], timeout=1.0, include_timestamps=False, force=True):
        """ Read PVs immediately """
        if not isinstance(pvs_read, list):
            pvs_read = [pvs_read]
        values = [None] * len(pvs_read)
        for i, pv in enumerate(pvs_read):
            r = pv.read(data_type='time', timeout=timeout)
            assert r.status.success == 1
            value = r.data
            timestamp = r.metadata.timestamp
            if include_timestamps:
                values[i] = (timestamp, value)
            else:
                values[i] = value
        return values

    def set_and_verify_multiple(self, pvdict, timeout=1.0, readback_kwargs=None, readback_delay_min=None,
                                readback_delay_max=None):
        """ Set PVs and verify readbacks if available """
        from caproto.threading.client import Batch
        kv = self.kv
        df = self.df
        readback_delay_min = readback_delay_min or self.READBACK_DELAY_MIN
        readback_delay_max = readback_delay_max or self.READBACK_DELAY_MAX
        assert self.df is not None
        readback_kwargs = readback_kwargs or dict(min_readings=1)
        assert all(k in df.index for k in pvdict.keys())
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
            assert low <= value <= high, f'PV {pv_input} value {value} outside {low}<->{high}'
            assert atol < np.abs(high - low), f'PV {pv_input} tolerance {atol} larger than limit range {low}<->{high}'
            # val = pv_read.read().data[0]
            # if np.isclose(val, value, atol=atol, rtol=0):
            #     #del pvdict[pvn]
            #     pass

        with Batch(timeout=timeout) as b:
            for (pvn, value) in pvdict.items():
                pv_input = self.kv[pvn]
                r = b.write(pv_input, value)
                # assert r.status.success == 1

        time.sleep(readback_delay_min)
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
                if pv_read is None:
                    continue
                atol = df.loc[pv_input.name, 'atol']
                val = self.read_fresh(pv_read, timeout=timeout, now=now, **readback_kwargs)[0]
                last_read[pvn] = val
                if np.all(np.isclose(val, value, atol=atol, rtol=0)):
                    values[pvn] = val
            # print(f'set outer loop 2 {len(values)=} {last_read=}')
            if time.perf_counter() - t_start > readback_delay_max:
                for (pvnl, valuel) in pvdict.items():
                    pv_inputl = self.kv[pvnl]
                    atoll = df.loc[pv_inputl.name, 'atol']
                    print(f'{pvnl:20}: {valuel=} {last_read[pvnl]=} {(valuel - last_read[pvnl])=} {atoll=}')
                raise IOError(f'Setting {pv_input.name} failed - readback {pv_read.name} ({val}) bad (want {value})')
            time.sleep(0.1)

        t_spent = time.perf_counter() - t_start
        if self.READBACK_TOTAL_SET_TIME_MIN is not None:
            t_sleep = max(self.READBACK_DELAY_POST_MIN, self.READBACK_TOTAL_SET_TIME_MIN - t_spent)
            time.sleep(t_sleep)
        return values

    def set_and_verify(self, pv_write, value, timeout=1.0):
        """ Set PV and verify readback is within tolerance """
        self.set_and_verify_multiple(dict(pv_write=value))
