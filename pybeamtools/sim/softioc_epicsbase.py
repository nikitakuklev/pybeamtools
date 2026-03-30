"""
Soft IOC implementation using pythonSoftIOC (Diamond Light Source).

Uses epicscorelibs to run a real EPICS IOC in-process, providing CA and PVA
access to test PVs. This is distinct from the caproto-based IOCs in softioc.py -
it runs actual EPICS base C code via Python bindings.

Requires: pip install softioc (which pulls in epicscorelibs, pvxslibs)

IMPORTANT: EPICS base can only be initialized once per process. The IOC must
run in a subprocess for test isolation.
"""

import logging
import math
import multiprocessing
import os
import threading
import time
from multiprocessing import Process, Event

logger = logging.getLogger(__name__)


def _preload_epics_libs():
    """Preload epicscorelibs and pvxslibs shared libraries via ctypes.

    The softioc package depends on shared libraries from epicscorelibs and pvxslibs
    that may not be on LD_LIBRARY_PATH. We preload them explicitly with RTLD_GLOBAL
    so that subsequent ctypes.CDLL calls (inside softioc) can resolve dependencies.
    """
    import ctypes
    import epicscorelibs.path

    # epicscorelibs: load in dependency order
    for lib_name in ["Com", "ca", "dbCore", "dbRecStd"]:
        path = epicscorelibs.path.get_lib(lib_name)
        ctypes.CDLL(path, mode=ctypes.RTLD_GLOBAL)

    # pvxslibs: load in dependency order
    import pvxslibs
    pvxs_lib_dir = os.path.join(os.path.dirname(pvxslibs.__file__), "lib")
    for lib_name in ["libevent_core.so", "libevent_pthread.so", "libpvxs.so", "libpvxsIoc.so"]:
        path = os.path.join(pvxs_lib_dir, lib_name)
        if os.path.exists(path):
            ctypes.CDLL(path, mode=ctypes.RTLD_GLOBAL)


def _ioc_process_main(
    prefix: str,
    pv_config: dict,
    ready_event,
    shutdown_event,
):
    """
    Entry point for the subprocess running the real EPICS IOC.

    Args:
        prefix: PV name prefix (e.g. "TEST:")
        pv_config: dict mapping PV suffix -> dict with keys:
            'type': 'ai' | 'ao' | 'bi' | 'bo' | 'longin' | 'longout' | 'waveform'
            'initial': initial value
            'lopr': low operating range (optional)
            'hopr': high operating range (optional)
            'linked_readback': suffix of readback PV to echo writes to (optional)
        ready_event: multiprocessing.Event to signal IOC is ready
        shutdown_event: multiprocessing.Event to signal IOC should stop
    """
    # Preload shared libraries that softioc/pvxslibs need
    _preload_epics_libs()

    from softioc import softioc, builder, asyncio_dispatcher

    builder.SetDeviceName(prefix.rstrip(":"))

    records = {}
    links = {}  # ao_suffix -> readback_suffix

    # First pass: collect linked_readback info, build records for ai/inputs first
    for suffix, cfg in pv_config.items():
        if "linked_readback" in cfg:
            links[suffix] = cfg["linked_readback"]

    def _make_updater(rb_rec_ref):
        def _on_update(value):
            rb_rec_ref.set(value)
        return _on_update

    for suffix, cfg in pv_config.items():
        pv_type = cfg.get("type", "ai")
        initial = cfg.get("initial", 0.0)
        kwargs = {}
        if "lopr" in cfg:
            kwargs["LOPR"] = cfg["lopr"]
        if "hopr" in cfg:
            kwargs["HOPR"] = cfg["hopr"]
        if "egu" in cfg:
            kwargs["EGU"] = cfg["egu"]

        if pv_type == "ai":
            records[suffix] = builder.aIn(suffix, initial_value=initial, **kwargs)
        elif pv_type == "ao":
            # Wire on_update at creation time if there's a linked readback
            on_update_fn = None
            if suffix in links:
                # The readback record must already exist or will be created -
                # we use a deferred lookup via closure
                rb_suffix = links[suffix]
                on_update_fn = lambda value, _rb=rb_suffix: records[_rb].set(value)
            if on_update_fn is not None:
                records[suffix] = builder.aOut(suffix, initial_value=initial,
                                               on_update=on_update_fn, **kwargs)
            else:
                records[suffix] = builder.aOut(suffix, initial_value=initial, **kwargs)
        elif pv_type == "bi":
            records[suffix] = builder.boolIn(suffix, initial_value=int(initial))
        elif pv_type == "bo":
            on_update_fn = None
            if suffix in links:
                rb_suffix = links[suffix]
                on_update_fn = lambda value, _rb=rb_suffix: records[_rb].set(value)
            if on_update_fn is not None:
                records[suffix] = builder.boolOut(suffix, initial_value=int(initial),
                                                   on_update=on_update_fn)
            else:
                records[suffix] = builder.boolOut(suffix, initial_value=int(initial))
        elif pv_type == "longin":
            records[suffix] = builder.longIn(suffix, initial_value=int(initial))
        elif pv_type == "longout":
            on_update_fn = None
            if suffix in links:
                rb_suffix = links[suffix]
                on_update_fn = lambda value, _rb=rb_suffix: records[_rb].set(value)
            if on_update_fn is not None:
                records[suffix] = builder.longOut(suffix, initial_value=int(initial),
                                                   on_update=on_update_fn)
            else:
                records[suffix] = builder.longOut(suffix, initial_value=int(initial))
        elif pv_type == "waveform":
            records[suffix] = builder.WaveformIn(suffix, initial_value=initial, **kwargs)
        else:
            raise ValueError(f"Unknown PV type: {pv_type}")

    dispatcher = asyncio_dispatcher.AsyncioDispatcher()
    builder.LoadDatabase()
    softioc.iocInit(dispatcher)

    # Start scanning threads for PVs with scan_period
    scan_threads = []
    for suffix, cfg in pv_config.items():
        scan_period = cfg.get("scan_period", None)
        scan_fn_name = cfg.get("scan_fn", None)
        if scan_period is not None and suffix in records:
            rec = records[suffix]

            if scan_fn_name == "counter":
                def _scan_counter(r, period, stop_ev):
                    count = 0
                    while not stop_ev.is_set():
                        count += 1
                        r.set(float(count))
                        stop_ev.wait(period)
                t = threading.Thread(target=_scan_counter,
                                     args=(rec, scan_period, shutdown_event),
                                     daemon=True)
            elif scan_fn_name == "sine":
                def _scan_sine(r, period, stop_ev):
                    t0 = time.time()
                    while not stop_ev.is_set():
                        r.set(math.sin(time.time() - t0))
                        stop_ev.wait(period)
                t = threading.Thread(target=_scan_sine,
                                     args=(rec, scan_period, shutdown_event),
                                     daemon=True)
            else:
                # Default: re-publish current value to trigger monitors
                def _scan_republish(r, period, stop_ev):
                    while not stop_ev.is_set():
                        r.set(r.get())
                        stop_ev.wait(period)
                t = threading.Thread(target=_scan_republish,
                                     args=(rec, scan_period, shutdown_event),
                                     daemon=True)

            t.start()
            scan_threads.append(t)

    ready_event.set()
    logger.info(f"IOC ready with prefix '{prefix}' and {len(records)} PVs "
                f"({len(scan_threads)} scanning)")

    # Block until shutdown is requested
    while not shutdown_event.is_set():
        time.sleep(0.1)

    # Wait for scan threads to finish
    for t in scan_threads:
        t.join(timeout=2)

    logger.info("IOC shutting down")


class EpicsBaseIOC:
    """
    Manages a real EPICS IOC running in a subprocess via pythonSoftIOC.

    Usage:
        ioc = EpicsBaseIOC(prefix="TEST:")
        ioc.add_pv("SETPOINT", type="ao", initial=0.0, linked_readback="READBACK")
        ioc.add_pv("READBACK", type="ai", initial=0.0)
        ioc.start()
        # ... use PVs via caproto or pyepics ...
        ioc.stop()
    """

    def __init__(self, prefix: str = "TEST:"):
        self.prefix = prefix
        self.pv_config: dict[str, dict] = {}
        self._process: Process | None = None
        self._ready_event = multiprocessing.Event()
        self._shutdown_event = multiprocessing.Event()

    def add_pv(self, suffix: str, **kwargs):
        """
        Add a PV to the IOC configuration. Must be called before start().

        Args:
            suffix: PV name suffix (full name will be PREFIX:SUFFIX)
            type: 'ai', 'ao', 'bi', 'bo', 'longin', 'longout', 'waveform'
            initial: initial value
            lopr: low operating range
            hopr: high operating range
            linked_readback: suffix of ai PV to echo writes to
        """
        if self._process is not None:
            raise RuntimeError("Cannot add PVs after IOC has started")
        self.pv_config[suffix] = kwargs

    def pv_name(self, suffix: str) -> str:
        """Get the full PV name for a suffix."""
        prefix = self.prefix.rstrip(":")
        return f"{prefix}:{suffix}"

    def start(self, timeout: float = 10.0):
        """Start the IOC subprocess and wait for it to be ready."""
        if self._process is not None:
            raise RuntimeError("IOC already started")

        self._ready_event.clear()
        self._shutdown_event.clear()

        self._process = Process(
            target=_ioc_process_main,
            args=(self.prefix, self.pv_config, self._ready_event, self._shutdown_event),
            daemon=True,
        )
        self._process.start()

        if not self._ready_event.wait(timeout=timeout):
            self._process.kill()
            self._process.join(timeout=5)
            self._process = None
            raise TimeoutError(f"IOC did not become ready within {timeout}s")

        # Give CA server a moment to start accepting connections
        time.sleep(0.5)
        logger.info(f"IOC subprocess started (pid={self._process.pid})")

    def stop(self, timeout: float = 5.0):
        """Stop the IOC subprocess."""
        if self._process is None:
            return

        self._shutdown_event.set()
        self._process.join(timeout=timeout)

        if self._process.is_alive():
            logger.warning("IOC did not stop gracefully, killing")
            self._process.kill()
            self._process.join(timeout=2)

        self._process = None
        logger.info("IOC stopped")

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()


def make_test_ioc(prefix: str = "CLIBTEST", n_channels: int = 2) -> EpicsBaseIOC:
    """
    Create a standard test IOC with setpoint/readback pairs.

    Creates PVs:
        {prefix}:X0, {prefix}:X0:RB  (ao/ai pair, linked)
        {prefix}:X1, {prefix}:X1:RB  (ao/ai pair, linked)
        ...
        {prefix}:STATIC  (ai, read-only, initial=42.0)
    """
    ioc = EpicsBaseIOC(prefix=prefix)

    for i in range(n_channels):
        rb_suffix = f"X{i}:RB"
        ioc.add_pv(f"X{i}", type="ao", initial=0.0,
                   lopr=-100.0, hopr=100.0,
                   linked_readback=rb_suffix)
        ioc.add_pv(rb_suffix, type="ai", initial=0.0,
                   lopr=-100.0, hopr=100.0)

    ioc.add_pv("STATIC", type="ai", initial=42.0)

    # Scanning PVs - IOC updates these periodically
    ioc.add_pv("COUNTER", type="ai", initial=0.0,
               scan_period=0.5, scan_fn="counter")
    ioc.add_pv("SINE", type="ai", initial=0.0,
               scan_period=0.2, scan_fn="sine")

    return ioc
