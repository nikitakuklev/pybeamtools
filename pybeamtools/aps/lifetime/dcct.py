import faulthandler
import logging
import os
import signal
import socket
import sys
import threading
import time
from queue import Queue

from pybeamtools.aps.daq.streamer import EPICSStreamer, ScalarLifetimeCallback
from pybeamtools.controlsdirect.clib import Accelerator
from pybeamtools.sim.softioc import DynamicIOC
from pybeamtools.utils.logging import config_root_logging

acc = Accelerator.get_singleton()
logger = logging.getLogger(__name__)


class DCCTLifetimeProcessor:
    def __init__(self, channels_map: dict,
                 lifetime_processors: dict,
                 publish_format: str = "AOP:{x}:{metric}",
                 interfaces: list[str] = None,
                 reset_logging: bool = True,
                 verbosity=logging.WARNING,
                 ioc_verbosity=logging.WARNING,
                 streamer_kwargs: dict = None,
                 ):

        if reset_logging:
            config_root_logging(reset_handlers=True)

        logging.getLogger("ray").setLevel(logging.INFO)
        logging.getLogger("pybeamtools.sim.softioc").setLevel(ioc_verbosity)
        logging.getLogger("caproto").setLevel(ioc_verbosity)

        faulthandler.enable(file=sys.stderr)

        self.channel_map = channels_map
        self.publish_format = publish_format
        self.lifetime_processors = lifetime_processors
        self.verbosity = verbosity
        self.ioc_verbosity = ioc_verbosity
        self.debug = verbosity <= logging.DEBUG
        self.streamer_kwargs = streamer_kwargs or {}
        self.streamers = {}
        self.ioc_channels = []
        self.n_agg = 0

        pvdb = {}
        for name, ch in self.channel_map.items():
            for metric in lifetime_processors[name].keys():
                channel_name = publish_format.format(x=name, metric=metric)
                pvdb[channel_name] = 0.0
                self.ioc_channels.append(channel_name)
        interfaces = interfaces or ["0.0.0.0"]
        self.sioc = DynamicIOC(data=pvdb, interfaces=interfaces)
        self.sioc.run_in_background()

        self.linfo(f"Started soft IOC with {pvdb=}")
        logger.info(f"Processor coordinates: {threading.get_ident(), os.getpid(), socket.gethostname()}")

    def ldebug(self, msg, *args, **kwargs):
        if self.verbosity <= logging.DEBUG:
            logger.debug(msg, *args, **kwargs, stacklevel=2)

    def linfo(self, msg, *args, **kwargs):
        if self.verbosity <= logging.INFO:
            logger.info(msg, *args, **kwargs, stacklevel=2)

    def setup_streamers(self):
        for name, ch in self.channel_map.items():
            try:
                self.streamers[name] = EPICSStreamer(name=name, channel=ch, buffer_size=100, debug=self.debug,)
            except Exception as ex:
                logger.error(f"Failed to connect {name}={ch} - exception {ex}")
                raise ex

        for st_name, st in self.streamers.items():
            st.connect()
            assert st.is_connected, f"Streamer [{st_name}] failed to connect"

        self.ldebug(f"Connected to {len(self.streamers)} streamers")

        self.setup_lifetime_cbs()

    def setup_lifetime_cbs(self):
        for s, v in self.streamers.items():
            ltcb = ScalarLifetimeCallback(self.lifetime_processors[s], self.debug, **self.streamer_kwargs)
            v.clear_callbacks()
            v.add_callback("lifetime", ltcb, f_kwargs=dict(st_name=s))

        self.ldebug("Added lifetime callback to streamers")

    def start_streamers(self, limit: int = None):
        def signal_handler(sig, frame):
            logger.warning("Got Ctrl+C - stopping!")
            for st in self.streamers.values():
                st.stop_monitor()
            time.sleep(0.2)
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        for name, st in self.streamers.items():
            st.start_monitor()
            self.linfo(f"Started streamer {name}")

        logger.info(f"Started monitoring {self.channel_map=}")

    def submit_pv_updates(self, streamer, results):
        pv_updates = {}
        for metric, result in results.items():
            value = result['raw']
            channel = self.publish_format.format(x=streamer.name, metric=metric)
            pv_updates[channel] = value
            self.ldebug(f"Channel {channel}={value}")

        for k, v in pv_updates.items():
            assert isinstance(v, float), f"Invalid value type for {k}={v}"
            self.sioc.send_updates(k, v)
            time.sleep(0)

    def start_aggregator_thread(self):
        def agg_logic(streamer, results):
            try:
                self.last_agg = results
                for k, v in results.items():
                    if v is None:
                        self.ldebug(f"Got blank from streamer [{k}]")
                    else:
                        self.ldebug(f">>> [{k}] {v=}")
                if not results['success']:
                    self.linfo(f"PROC | streamer [{streamer.name}] success=false")
                else:
                    cb_results = results['cbs']['lifetime']
                    if len(cb_results) > 0:
                        self.linfo(f"PROC | agg results {results}")
                        self.submit_pv_updates(streamer, cb_results)
                self.linfo("-------------------------------------")
                self.n_agg += 1
            except:
                logger.exception("Exception in aggregator thread", exc_info=True, stack_info=True)

        def f():
            t0 = time.time()
            logger.debug(f"Hello from aggregator thread at {t0}")
            self.is_agg_running = True
            self.last_tag = None

            q = Queue()

            def put_in_queue(st):
                q.put([st, st.get_callback_results()])

            for st in self.streamers.values():
                st.add_finalizer(put_in_queue)

            while self.is_agg_running:
                data = q.get()
                streamer = data[0]
                results = data[1]

                self.linfo(f"PROC | agg event at local time [{time.time()}]")
                agg_logic(streamer, results)

        self.agg_thread = threading.Thread(target=f, name="aggregator_thread", daemon=True)
        self.agg_thread.start()
        self.ldebug("Started aggregator thread")
        return self.agg_thread