import functools
import logging
import os
import signal
import socket
import sys
import threading
import time
from abc import ABC, abstractmethod
from typing import Any, Optional

# os.environ['MKL_NUM_THREADS'] = '1'
# os.environ['NUMEXPR_NUM_THREADS'] = '1'
os.environ["OMP_NUM_THREADS"] = "2"
# os.environ['LD_PRELOAD'] = '/home/oxygen16/NKUKLEV/anaconda3/envs/py311ml/lib/libstdc++.so.6'
os.environ[
    'EPICS_PVA_ADDR_LIST'] = 'c2ioc02.aps4.anl.gov pslmcam1.aps4.anl.gov pslmcam2.aps4.anl.gov bslmcam1.aps4.anl.gov  daq-dss02.aps4.anl.gov daq-dss04.aps4.anl.gov daq-dss06.aps4.anl.gov daq-dss08.aps4.anl.gov daq-dss10.aps4.anl.gov daq-dss11.aps4.anl.gov daq-dss14.aps4.anl.gov daq-dss16.aps4.anl.gov daq-dss18.aps4.anl.gov daq-dss20.aps4.anl.gov daq-dss21.aps4.anl.gov daq-dss24.aps4.anl.gov daq-dss26.aps4.anl.gov daq-dss28.aps4.anl.gov daq-dss30.aps4.anl.gov daq-dss31.aps4.anl.gov daq-dss34.aps4.anl.gov daq-dss36.aps4.anl.gov daq-dss37.aps4.anl.gov daq-dss40.aps4.anl.gov daq-qss02.aps4.anl.gov daq-qss11.aps4.anl.gov daq-qss21.aps4.anl.gov daq-qss31.aps4.anl.gov llrf-amc758-7.aps4.anl.gov rfdaqsrv-1.aps4.anl.gov'
os.environ['EPICS_AR_PORT'] = '7002'

import numpy as np
from datetime import datetime

from pybeamtools.controlsdirect.clib import Accelerator
from pybeamtools.aps.daq.streamer import FakeTBTStreamer, LifetimeCallback, LifetimeTBTStreamer, RayStreamerWrapper, \
    TBTStreamer

from pybeamtools.sim.softioc import DynamicIOC
from pybeamtools.utils.logging import config_root_logging

acc = Accelerator.get_singleton()
logger = logging.getLogger(__name__)


def deep_update_dict(d, u):
    for k, v in u.items():
        if isinstance(v, dict):
            d[k] = deep_update_dict(d.get(k, {}), v)
        else:
            d[k] = v
    return d


class DAQProcessor:
    DAQ_CYCLE = 0.100167
    STREAMER_CLASS = TBTStreamer

    def __init__(self,
                 channel_format: str = "S{s}-DAQTBT:Raw:Data",
                 sectors: Optional[list[int]] = None,
                 show_table: bool = True,
                 reset_logging: bool = True,
                 verbosity: int = logging.INFO,
                 ):

        if reset_logging:
            config_root_logging(reset_handlers=True)

        logging.getLogger('ray').setLevel(logging.INFO)

        # if verbosity >= logging.INFO:
        logging.getLogger('pybeamtools.sim.softioc').setLevel(verbosity)

        import faulthandler
        faulthandler.enable(file=sys.stderr)

        self.streamers = {}
        self.channel_format = channel_format
        self.sectors = sectors or range(1, 40, 2)
        self.streamer_sectors: dict[str, int] = {}
        self.show_table = show_table
        self.console = None
        self.verbosity = verbosity
        self.debug = verbosity <= logging.DEBUG
        # self.setup_streamers(channel_format, sectors)

    def ldebug(self, msg, *args, **kwargs):
        if self.debug:
            logger.debug(msg, *args, **kwargs, stacklevel=2)

    def linfo(self, msg, *args, **kwargs):
        if self.verbosity <= logging.INFO:
            logger.info(msg, *args, **kwargs, stacklevel=2)

    def setup_streamers(self):
        for s in self.sectors:
            try:
                c_formatted = self.channel_format.format(s=f'{s:02d}')
                st_key = f'st_{s:02d}'
                st = self.STREAMER_CLASS(name=st_key,
                                         sector=s,
                                         channel=c_formatted,
                                         debug=self.debug,
                                         )
                self.streamers[st_key] = st
                self.streamer_sectors[st_key] = s
            except Exception as ex:
                logger.error(f'Failed to connect to sector {s} - exception {ex}')
                raise ex

        for st_name, st in self.streamers.items():
            st.connect()
            assert st.is_connected, f'Streamer [{st_name}] failed to connect'

        self.ldebug(f"Connected to {len(self.streamers)} streamers")

    def start_streamers(self, limit: int = None):
        """ Start monitoring the PVA channels and processing events """

        def signal_handler(sig, frame):
            logger.warning('Got Ctrl+C - stopping!')
            for st in self.streamers.values():
                st.stop_monitor()
            time.sleep(0.2)
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        for st in self.streamers.values():
            st.start_monitor(limit=limit)
            assert st.is_monitoring, f'Streamer [{st}] failed to start!'

        logger.info(f"Started monitoring {len(self.streamers)} streamers: {self.streamers.keys()}")

        # if self.show_table:
        #     time.sleep(0.5)
        #     self.start_table_update_thread()

    def start_table_update_thread(self, period: float = 1.0):
        """ Optional thread to update a CLI table with stats for live monitoring """
        from rich.console import Console
        from rich.live import Live

        if self.show_table:
            self.console = Console()

        # self.console.clear()
        time.sleep(0.01)

        def __update():
            loopcnt = 0
            with Live(self.make_stats_table(), auto_refresh=False) as live:
                while True:
                    t1 = time.time()

                    table = self.make_stats_table()
                    live.update(table)
                    live.refresh()

                    loopcnt += 1
                    tleft = max(0.0, period - (time.time() - t1))
                    time.sleep(tleft)

        while True:
            __update()

    @abstractmethod
    def generate_table_columns(self) -> dict[str, dict[str]]:
        pass

    def make_stats_table(self):
        self.ldebug(f"Generating stats table")

        from rich.table import Table
        extra_columns = self.generate_table_columns()

        self.ldebug(f"Stats table extra columns: {extra_columns}")

        table = Table(title="Stats " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        table.add_column("Name", style="magenta")
        table.add_column("Thread")
        table.add_column("PID")
        table.add_column("Load\n(100)")
        # table.add_column("Load\n(all)")
        table.add_column("tCB\n(all)")
        table.add_column("Ev\ncnt")
        table.add_column("Evr\n(100)")
        # table.add_column("Evr\n(all)")
        # table.add_column("Faults")
        table.add_column("Max dt")
        for metric in extra_columns:
            table.add_column(metric)

        def get_ex_value(metric, s):
            mdata = extra_columns[metric]
            mvalue = mdata.get(s, f"NA for {metric}:{s}, have {mdata}")
            return mvalue

        for i, (s, st) in enumerate(self.streamers.items()):
            extra_col_vals = [f'{get_ex_value(metric, s)}' for metric in extra_columns]
            vals = st.get_perf_stats()
            table.add_row(
                    f'{s}',
                    f'{vals["event_cb_thread_id"]}',
                    f'{vals["event_cb_process_id"]}',
                    f'{vals["load"]:.3f}',
                    f'{vals["event_cb_avg_time"] * 1e3:.3f}',
                    f'{vals["event_cnt"]}',
                    f'{vals["event_rate"]:.2f}',
                    f'{max(vals["event_cb_time_history"]):.6f}',
                    *extra_col_vals
            )
        return table


def set_daq_decimator(pid, source=None, decfactor=32, avgmode='Avg', daqroot='DAQTBT'):
    assert 1 <= pid <= 5 and isinstance(pid, int) and isinstance(decfactor, int)
    d = {}
    for s in range(1, 40, 2):
        root = f'S{s:02d}-{daqroot}:Dec{pid}'
        if source is not None:
            d[f'{root}:NDArrayPortM'] = source
        d[f'{root}:AvgModeC'] = avgmode
        d[f'{root}:DecFactorC'] = decfactor
        d[f'{root}:EnableCallbacksC'] = 1
    acc.write(d)


class LifetimeProcessor(DAQProcessor, ABC):
    STREAMER_CLASS = LifetimeTBTStreamer
    EXPECTED_TBT_FRAME_LEN = 27120

    def __init__(self,
                 channel_format: str = "S{s}-DAQTBT:Raw:Data",
                 publish_format: str = "AOP:S{s}-DAQTBT:{x}",
                 sectors: list[int] = None,
                 ds_window: int = None,
                 ds_step: int = None,
                 daq_dec_factor=32,
                 lifetime_processors: dict = None,
                 trigger_mode: str = 'periodic',
                 trigger_params: dict = None,
                 show_table: bool = True,
                 reset_logging: bool = True,
                 verbosity: int = logging.INFO,
                 streamer_kwargs: dict = None
                 ):
        super().__init__(channel_format=channel_format, sectors=sectors, show_table=show_table,
                         reset_logging=reset_logging, verbosity=verbosity)
        if lifetime_processors is None:
            lifetime_processors = {  # 'Lifetime5Hz': (2, 4),
                'Lifetime1s': (5, 10),
                'Lifetime2s': (10, 20),
                # 'Lifetime5s': (50, 100)
            }
        self.streamer_kwargs = streamer_kwargs or {}
        self.ds_window = ds_window
        self.ds_step = ds_step
        self.ldebug(f"Using {ds_window=} {ds_step=} for {self.EXPECTED_TBT_FRAME_LEN//daq_dec_factor=} samples")
        self.streamer_kwargs['ds_window'] = ds_window
        self.streamer_kwargs['ds_step'] = ds_step
        self.streamer_kwargs['daq_dec_factor'] = daq_dec_factor
        self.lifetime_processors = lifetime_processors
        self.trigger_mode = trigger_mode
        if trigger_params is None:
            if trigger_mode == 'periodic':
                trigger_params = {'polling_period': 0.1}
            elif trigger_mode == 'trigger':
                trigger_params = {'trigger_channel': 'MCR-MT:EVR1:DAQClkCntM',
                                  'subsample': 5,
                                  'delay': 0.05
                                  }
        self.trigger_params = trigger_params
        self.publish_format = publish_format
        self.n_agg = 0
        self.last_agg = None
        self.is_agg_running = False
        self.agg_thread = None
        self.last_processed: dict[str, dict[str, Any]] = {}
        self.overall_processed: dict[str, dict[str, Any]] = {}

        pvdb = {}
        for x in lifetime_processors.keys():
            pvdb.update({f"AOP:S-DAQTBT:{x}": 0.0,
                         f"AOP:S-DAQTBT:{x}:Max": 0.0,
                         f"AOP:S-DAQTBT:{x}:Min": 0.0,
                         #f"AOP:S-DAQTBT:{x}:Mean": 0.0,
                         f"AOP:S-DAQTBT:{x}:Std": 0.0,
                         **{f"AOP:S{i:02d}-DAQTBT:{x}": 0.0 for i in self.sectors}
                         })
        self.sioc = sioc = DynamicIOC(data=pvdb, interfaces=["0.0.0.0"])
        sioc.run_in_background()

        self.ldebug(f"Started soft IOC with {pvdb=}")
        logger.info(f'Processor coordinates: {threading.get_ident(), os.getpid(), socket.gethostname()}')

    def setup_streamers(self):
        super().setup_streamers()
        for s, v in self.streamers.items():
            ltcb = LifetimeCallback(self.lifetime_processors, self.debug)
            v.clear_callbacks()
            # v.add_callback(functools.partial(timing_callback, k=k))
            v.add_callback('lifetime', ltcb, f_kwargs=dict(st_name=s))

        self.ldebug(f"Added lifetime callback to streamers")

    def reset_counters(self):
        for s, v in self.streamers.items():
            v.reset_counters()

    def generate_table_columns(self) -> dict[str, dict[str, str]]:
        formatter = lambda x: f"{x:.3f}"
        columns = {}

        if 'median_by_streamer' not in self.overall_processed:
            logger.warning(f"Last processed data is missing median_by_streamer")
            return columns

        for metric, v in self.overall_processed['median_by_streamer'].items():
            columns[metric] = {s: formatter(v2) for s, v2 in v.items()}

        if self.last_agg is not None:
            columns['last_tag'] = {k: v['tag'] for k, v in self.last_agg.items()}
        else:
            columns['last_tag'] = {k: 'NA' for k in self.streamers.keys()}

        self.ldebug(f"Generated extra table columns: {columns}")

        return columns

    def get_streamer_results(self, tag) -> dict[str, dict[str, Any]]:
        results = {}
        for s, v in self.streamers.items():
            results[s] = v.get_callback_results_by_tag(tag)
        return results

    def get_sector_channel(self, sector: int, mode: str) -> str:
        return self.publish_format.format(s=f'{sector:02d}', x=mode)

    def get_global_channel(self, mode: str) -> str:
        return self.publish_format.format(s='', x=mode)

    def get_current_tag(self):
        tcycle, ncycle = acc.get_latest_buffer_value('MCR-MT:EVR1:DAQClkCntM')
        tag = (int(tcycle), int((tcycle - int(tcycle)) * 1e1) * 100)
        return tag

    def get_data_tag(self, offset=1) -> Optional[tuple[int, int]]:
        buf = acc.get_buffer('MCR-MT:EVR1:DAQClkCntM')
        if buf is None:
            return None
        if len(buf) < offset + 1:
            return None
        t = buf[-offset - 1][1].metadata.timestamp
        tag = (int(t), int((t - int(t)) * 1e1) * 100)
        return tag

    def process_streamer_results(self, aggregated_results: dict[str, dict[str, Any]] = None):
        t1 = time.time()
        updates: dict[str, dict[str, float]] = {k: {} for k in self.lifetime_processors.keys()}
        updates_by_streamer: dict[str, dict[str, float]] = {k: {} for k in self.lifetime_processors.keys()}
        # active_sectors = set(x.sector for x in self.streamers.values())
        updates_by_sector = {metric: {s: {} for s in range(1, 40, 2)} for metric in self.lifetime_processors.keys()}
        for st_name, st_result in aggregated_results.items():
            if st_result is None:
                logger.warning(f"Skipping [{st_name}] with no results")
                continue
            if not st_result['success']:
                logger.warning(f"Skipping [{st_name}] with failed results")
                continue
            if 'lifetime' not in st_result['cbs']:
                logger.warning(f"Skipping [{st_name}] without lifetime data")
                continue
            tag = st_result['tag']
            ltr = st_result['cbs']['lifetime']
            # sector = self.streamers[st_name].sector
            sector = self.streamer_sectors[st_name]
            for metric in self.lifetime_processors:
                if metric in ltr:
                    if len(ltr[metric]) == 0:
                        logger.warning(f"Skipping empty data for {metric} in {st_name}")
                        continue
                    # if 'raw' not in ltr[metric]:
                    #     raise ValueError(f"Missing raw data for {metric} in {st_name} - have {ltr}")
                    # df: pd.DataFrame = ltr[metric]['df']
                    # dfdict = df.to_dict(orient='records')[0]
                    timestamp = ltr[metric]['timestamp']
                    delta = t1 - timestamp
                    if delta > 2.0:
                        logger.warning(f"Skipping old data for [{st_name}] - time delta {delta:.3f} sec")
                        continue
                    dfdict = ltr[metric]['raw']
                    updates[metric].update(dfdict)
                    # updates_by_streamer[metric][st_name] = ltr[metric]['median']
                    updates_by_streamer[metric][st_name] = np.median(list(dfdict.values()))
                    updates_by_sector[metric][sector].update(dfdict)
                    self.ldebug(f"Processed [{st_name}] [{tag=}] [{metric=}]: {dfdict=} ")
                    # self.ldebug(f"{ltr[metric]['median']=} ")

        self.last_processed = {}
        self.last_processed['median_by_streamer'] = updates_by_streamer
        self.last_processed['raw'] = updates
        self.last_processed['by_sector'] = {}
        for metric in updates_by_sector:
            self.last_processed['by_sector'][metric] = {}
            for sector, v in updates_by_sector[metric].items():
                if len(v) == 0:
                    # logger.warning(f"Skipping empty update for [{metric=}][{sector=}]")
                    continue
                self.last_processed['by_sector'][metric][sector] = np.median(list(v.values()))
            # if metric not in self.last_processed['by_sector']:
            # self.last_processed['by_sector'][metric] = {s: np.median(list(v.values())) for s, v in
            #                                                 updates_by_sector[metric].items()}

        deep_update_dict(self.overall_processed, self.last_processed)

        self.submit_pv_updates()

    def submit_pv_updates(self):
        pv_updates = {}
        # for metric, v in updates_by_streamer.items():
        #     for st_name, m in v.items():
        #         sector = self.streamers[st_name].sector
        #         pv_updates[self.get_sector_channel(sector, metric)] = m

        updates = self.last_processed['raw']
        for metric, v in updates.items():
            if len(v) == 0:
                if self.debug:
                    logger.debug(f"Skipping empty SIOC update for [{metric}]")
                continue
            mv = float(np.median(list(v.values())))
            gc = self.get_global_channel(metric)
            self.ldebug(f"Median [{metric}] value: {gc}={mv}")
            pv_updates[self.get_global_channel(metric)] = mv

        for k, v in pv_updates.items():
            assert isinstance(v, float), f"Invalid value type for {k}={v}"
            self.sioc.send_updates(k, v)
            time.sleep(0)

    def start_aggregator_thread(self):
        def agg_logic(tag):
            try:
                t1 = time.time()
                self.ldebug(f"PROC | agg gathering {self.n_agg=} at {t1=} DAQCLK {tag=}")
                results = self.get_streamer_results(tag)
                self.last_agg = results
                self.ldebug(f"Got {len(results)}/{len(self.streamers)} results")
                for k, v in results.items():
                    if v is None:
                        self.ldebug(f"Got blank from streamer [{k}]")
                        # self.ldebug(f'Available tags: {ray.get(self.streamers[k].get_available_tags.remote())}')
                    else:
                        self.ldebug(f">>> [{k}] {v=}")

                self.process_streamer_results(results)
                print_keys = ['median_by_streamer']
                tdict = {k:self.last_processed[k] for k in print_keys}
                self.linfo(f"PROC | agg results {tdict}")
                self.linfo(f"-------------------------------------")
                self.n_agg += 1
            except:
                logger.exception("Exception in aggregator thread", exc_info=True, stack_info=True)

        def f():
            t0 = time.time()
            logger.debug(f"Hello from aggregator thread at {t0}")
            acc.ensure_monitored('MCR-MT:EVR1:DAQClkCntM')
            self.is_agg_running = True
            self.last_tag = None
            if self.trigger_mode == 'periodic':
                polling_period = self.trigger_params['polling_period']
                tgoal = time.time() + polling_period
                while self.is_agg_running:
                    if self.last_tag is None:
                        self.last_tag = time.time()
                        tgoal += polling_period
                        continue
                    tag = self.get_current_tag()
                    agg_logic(self.last_tag)
                    self.last_tag = tag
                    tleft = max(0.0, tgoal - time.time())
                    tgoal += polling_period
                    time.sleep(tleft)

            elif self.trigger_mode == 'trigger':
                trigger_channel = self.trigger_params['trigger_channel']
                subsample = self.trigger_params['subsample']
                delay = self.trigger_params['delay']
                acc.ensure_monitored(trigger_channel)
                acc.await_event_tag(trigger_channel, 2)
                current_tag = acc.get_buffer_tag(trigger_channel)
                target_tag = current_tag + subsample
                while self.is_agg_running:
                    evt, evd = acc.await_event_tag(trigger_channel, target_tag)
                    data_tag = self.get_data_tag(offset=1)
                    if data_tag is None:
                        logger.warning(f"Skipping trigger event {target_tag} - no data tag")
                        target_tag += subsample
                        continue
                    self.linfo(f"PROC | agg trig [{target_tag}] (+{delay=}) on [{trigger_channel}]=[{evd}]@[{evt}] at "
                               f"local time [{time.time()}]")
                    time.sleep(delay)
                    agg_logic(data_tag)
                    target_tag += subsample
                    # else:
                    #    self.ldebug(f"PROC | agg trig {trig_cnt} on {trigger_channel} at {time.time()} (skipped)")
                    # trig_cnt += 1

        self.agg_thread = threading.Thread(target=f, name='aggregator_thread', daemon=True)
        self.agg_thread.start()
        self.ldebug(f"Started aggregator thread")
        return self.agg_thread

    def stop_aggregator_thread(self):
        self.is_agg_running = False
        self.agg_thread.join()
        self.ldebug(f"Stopped aggregator thread")


class RayLifetimeProcessor(LifetimeProcessor):
    def get_streamer_results(self, tag) -> dict[str, dict[str, Any]]:
        import ray
        results = {}
        for s, v in self.streamers.items():
            results[s] = v.get_callback_results_by_tag.remote(tag)
        futures = list(results.values())
        results_real = ray.get(futures)
        return {k: v for k, v in zip(results.keys(), results_real)}

    def setup_streamers(self):
        import ray
        for s in self.sectors:
            try:
                c_formatted = self.channel_format.format(s=f'{s:02d}')
                st_key = f'st_{s:02d}'
                st = RayStreamerWrapper(self.STREAMER_CLASS,
                                        name=st_key,
                                        sector=s,
                                        channel=c_formatted,
                                        fields=['sum'],
                                        debug=self.debug,
                                        **self.streamer_kwargs
                                        )
                self.streamers[st_key] = st
                self.streamer_sectors[st_key] = s
            except Exception as ex:
                logger.error(f'Failed to connect to sector {s} - exception {ex}')
                raise ex

        futures = {}
        for st_name, st in self.streamers.items():
            futures[st_name] = st.connect.remote()

        for st_name, st in self.streamers.items():
            ltcb = LifetimeCallback(self.lifetime_processors, self.debug)
            st.clear_callbacks.remote()
            r = st.add_callback.remote('lifetime', ltcb, f_kwargs=dict(st_name=st_name))
            ray.get(r)

        # time.sleep(0.1)

        results = {k: v for k, v in zip(futures.keys(), ray.get(list(futures.values())))}
        for k, v in results.items():
            if not v:
                logger.error(f'Streamer [{k}] failed to connect')
                raise Exception(f'Streamer [{k}] failed to connect')
            else:
                logger.info(f'Streamer [{k}]=[{v}] connected')

        #    assert st.is_connected, f'Streamer [{st_name}] failed to connect'

        self.ldebug(f"Connected to {len(self.streamers)} streamers")

    def reset_counters(self):
        import ray
        futures = {}
        for st_name, st in self.streamers.items():
            futures[st_name] = st.reset_counters.remote()

        results = {k: v for k, v in zip(futures.keys(), ray.get(list(futures.values())))}
        for k, v in results.items():
            if not v:
                logger.error(f'Streamer [{k}] failed reset')
                raise Exception(f'Streamer [{k}] failed reset')
            else:
                logger.info(f'Streamer [{k}]=[{v}] reset')

    def start_streamers(self, limit: int = None):
        """ Start monitoring the PVA channels and processing events """
        import ray

        def signal_handler(sig, frame):
            logger.warning('Got Ctrl+C - stopping!')
            self.stop_aggregator_thread()
            for st in self.streamers.values():
                st.stop_monitor.remote()
            time.sleep(0.2)
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        futures = {}
        for k, v in self.streamers.items():
            futures[k] = v.start_monitor.remote(limit=limit)

        results = {k: v for k, v in zip(futures.keys(), ray.get(list(futures.values())))}
        for k, v in results.items():
            if not v:
                logger.error(f'Streamer [{k}] failed to start')
                raise Exception(f'Streamer [{k}] failed to start')
            else:
                logger.info(f'Streamer [{k}]=[{v}] started')
        # assert st.is_monitoring, f'Streamer [{st}] failed to start!'

        logger.info(f"Started monitoring {len(self.streamers)} streamers: {self.streamers.keys()}")

    def get_current_tag(self):
        acc.await_next_event('MCR-MT:EVR1:DAQClkCntM')
        tcycle, ncycle = acc.get_latest_buffer_value('MCR-MT:EVR1:DAQClkCntM')
        return (int(tcycle), int((tcycle - int(tcycle)) * 1e1) * 100)


class FakeLifetimeProcessor(LifetimeProcessor):
    STREAMER_CLASS = FakeTBTStreamer

    def get_current_tag(self):
        t1 = time.time()
        tag = (int(t1), int((t1 - int(t1)) * 1e1) * 100)
        return tag

    def start_aggregator_thread(self):
        # import ray
        def f():
            t0 = time.time()
            logger.debug(f"Hello from aggregator thread at {t0}")
            tgoal = time.time()
            self.is_agg_running = True
            self.last_tag = None
            while self.is_agg_running:
                if self.last_tag is None:
                    self.last_tag = time.time()
                    tgoal += self.polling_period
                    continue
                try:
                    while time.time() < tgoal:
                        time.sleep(1e-3)
                    t1 = time.time()
                    tag = self.get_current_tag()
                    self.ldebug(f"AGG gathering {self.n_agg=} at {t1=} (DAQCLK {tag=} {self.n_agg=})")
                    results = self.get_streamer_results(self.last_tag)
                    self.last_tag = tag
                    self.last_agg = results
                    for k, v in results.items():
                        if v is None:
                            self.ldebug(f"Got blank from streamer [{k}]")
                            # self.ldebug(f'Available tags: {ray.get(self.streamers[k].get_available_tags.remote())}')
                        else:
                            self.ldebug(f">>> [{k}] {v=}")

                    self.process_streamer_results(results)
                    self.ldebug(f"AGG results {self.last_processed=}")

                    tleft = max(0.0, tgoal - time.time())
                    self.n_agg += 1
                    tgoal += self.polling_period
                    time.sleep(tleft)
                except Exception as ex:
                    logger.exception("Exception in aggregator thread", exc_info=True, stack_info=True)

        self.agg_thread = threading.Thread(target=f, name='aggregator_thread', daemon=True)
        self.agg_thread.start()
        self.ldebug(f"Started aggregator thread")
        return self.agg_thread


class FakeRayLifetimeProcessor(FakeLifetimeProcessor, RayLifetimeProcessor):
    STREAMER_CLASS = FakeTBTStreamer

    def get_streamer_tags(self, st_name):
        import ray
        return ray.wait(self.streamers[st_name].get_available_tags.remote())
