"""
Integration tests for controlsdirect (Accelerator and AcceleratorPE).

Uses a real EPICS IOC via pythonSoftIOC running in a subprocess.
Tests both caproto-based and pyepics-based implementations against
the same IOC to verify API parity and correctness.
"""

import os
import time

import numpy as np
import pytest

os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "no"
os.environ["EPICS_CA_ADDR_LIST"] = "127.0.0.1"

from pybeamtools.sim.softioc_epicsbase import make_test_ioc, EpicsBaseIOC

PREFIX = "CLIBTEST"


@pytest.fixture(scope="module")
def epics_ioc():
    ioc = make_test_ioc(prefix=PREFIX, n_channels=3)
    ioc.start(timeout=15)
    time.sleep(1)
    yield ioc
    ioc.stop()


def _pv(suffix):
    return f"{PREFIX}:{suffix}"


# ---------------------------------------------------------------------------
# caproto Accelerator tests
# ---------------------------------------------------------------------------

class TestAcceleratorCaproto:
    @pytest.fixture(autouse=True)
    def setup(self, epics_ioc):
        from pybeamtools.controlsdirect.clib import Accelerator
        self.acc = Accelerator()
        yield

    def test_read_static(self):
        val = self.acc.read(_pv("STATIC"))
        assert val == pytest.approx(42.0)

    def test_read_initial(self):
        val = self.acc.read(_pv("X0"))
        assert isinstance(val, (int, float))

    def test_ensure_connection(self):
        pvs = self.acc.kv.get([_pv("X0"), _pv("X1")])
        self.acc.ensure_connection(pvs, timeout=5)
        assert all(pv.connected for pv in pvs)

    def test_ensure_connected_by_name(self):
        self.acc.ensure_connected([_pv("X0"), _pv("STATIC")])

    def test_write_and_read(self):
        self.acc.write({_pv("X0"): 7.5})
        time.sleep(0.3)
        val = self.acc.read(_pv("X0"))
        assert val == pytest.approx(7.5)

    def test_write_readback_link(self):
        self.acc.write({_pv("X1"): 2.5})
        time.sleep(0.5)
        val = self.acc.read(_pv("X1:RB"))
        assert val == pytest.approx(2.5)

    def test_subscribe_and_buffer(self):
        pv_name = _pv("X0")
        self.acc.ensure_monitored(pv_name)

        self.acc.write({pv_name: 1.0})
        time.sleep(0.5)

        buf = self.acc.get_buffer(pv_name)
        assert len(buf) > 0, "Buffer should have data after subscription + write"

    def test_ensure_monitored(self):
        pv_name = _pv("X2")
        self.acc.ensure_monitored(pv_name)
        assert self.acc.is_monitoring(pv_name)

    def test_read_all_now(self):
        names = [_pv("X0"), _pv("STATIC")]
        results = self.acc.read_all_now(names)
        assert _pv("X0") in results
        assert _pv("STATIC") in results

    def test_read_all_now_squeeze(self):
        results = self.acc.read_all_now([_pv("STATIC")], squeeze=True)
        val = results[_pv("STATIC")]
        assert val == pytest.approx(42.0)

    def test_read_fresh(self):
        pv_name = _pv("X0")
        self.acc.ensure_monitored(pv_name)
        now = time.time()
        self.acc.write({pv_name: 42.0})
        time.sleep(0.5)
        result = self.acc.read_fresh(
            [pv_name], timeout=5.0, now=now, min_readings=1, reduce="mean"
        )
        assert pv_name in result
        assert result[pv_name] == pytest.approx(42.0)

    def test_read_fresh_with_timestamps(self):
        pv_name = _pv("X1")
        self.acc.ensure_monitored(pv_name)
        now = time.time()
        self.acc.write({pv_name: 9.0})
        time.sleep(0.5)
        result = self.acc.read_fresh(
            [pv_name], timeout=5.0, now=now, min_readings=1, reduce="mean",
            include_timestamps=True,
        )
        ts, val = result[pv_name]
        assert ts > 0
        assert val == pytest.approx(9.0, abs=0.1)

    def test_write_and_verify(self):
        sp = _pv("X2")
        rb = _pv("X2:RB")
        self.acc.ensure_monitored([sp, rb])
        time.sleep(0.5)

        result = self.acc.write_and_verify(
            data_dict={sp: 5.55},
            readback_map={sp: rb},
            atol_map={sp: 0.01},
            timeout=10.0,
            readback_timeout=10.0,
            delay_after_write=0.3,
            delay_after_readback=0.1,
            read_first=False,
            try_read_now_after=0.0,
        )
        assert sp in result
        assert result[sp] == pytest.approx(5.55, abs=0.01)

    def test_subscribe_custom(self):
        pv_name = _pv("X1")
        received = []

        def my_callback(sub, response):
            received.append(response.data[0])

        self.acc.subscribe_custom(pv_name, my_callback)
        self.acc.write({pv_name: 99.0})
        time.sleep(0.5)
        self.acc.unsubscribe_custom(pv_name, my_callback)

        assert len(received) > 0
        assert any(abs(v - 99.0) < 0.01 for v in received)

    def test_get_buffer_data(self):
        pv_name = _pv("X2")
        self.acc.ensure_monitored(pv_name)
        t_before = time.time()
        self.acc.write({pv_name: 3.0})
        time.sleep(0.5)
        data = self.acc.get_buffer_data(pv_name, start=t_before)
        assert len(data) > 0

    def test_get_latest_buffer_value(self):
        pv_name = _pv("X0")
        self.acc.ensure_monitored(pv_name)
        self.acc.write({pv_name: 11.0})
        time.sleep(0.5)
        ts, val = self.acc.get_latest_buffer_value(pv_name)
        assert ts > 0
        assert val == pytest.approx(11.0)

    def test_await_next_event(self):
        pv_name = _pv("X0")
        self.acc.ensure_monitored(pv_name)
        self.acc.write({pv_name: 0.0})
        time.sleep(0.3)

        self.acc.write({pv_name: 20.0})
        ts, val = self.acc.await_next_event(pv_name, timeout=5.0)
        assert val == pytest.approx(20.0)

    # -- Scanning PV tests (IOC-driven periodic updates) --------------------

    def test_scanning_pv_buffer_accumulation(self):
        """COUNTER scans at 0.5s - verify buffer accumulates multiple readings."""
        pv_name = _pv("COUNTER")
        self.acc.ensure_monitored(pv_name)
        t_start = time.time()
        time.sleep(3.0)  # wait for ~6 scan periods

        data = self.acc.get_buffer_data(pv_name, start=t_start)
        assert len(data) >= 4, f"Expected >=4 buffered readings from 0.5s scan over 3s, got {len(data)}"

        # get_buffer_data returns newest-first, reverse for chronological order
        data = data[::-1]

        # Values should be monotonically increasing (counter)
        values = [r.data[0] for r in data]
        for i in range(1, len(values)):
            assert values[i] > values[i - 1], \
                f"Counter not monotonic: {values}"

        # Timestamps should be monotonically increasing
        timestamps = [r.metadata.timestamp for r in data]
        for i in range(1, len(timestamps)):
            assert timestamps[i] > timestamps[i - 1], \
                f"Timestamps not monotonic: {timestamps}"

    def test_scanning_pv_read_fresh_multiple(self):
        """Collect multiple fresh readings from a scanning PV."""
        pv_name = _pv("SINE")
        self.acc.ensure_monitored(pv_name)
        now = time.time()
        time.sleep(1.5)  # SINE scans at 0.2s, so ~7 readings

        result = self.acc.read_fresh(
            [pv_name], timeout=5.0, now=now,
            min_readings=3, max_readings=5, reduce="mean",
        )
        assert pv_name in result
        # Sine values should be in [-1, 1]
        assert -1.0 <= result[pv_name] <= 1.0

    def test_scanning_pv_await_event(self):
        """await_next_event should return promptly for a scanning PV."""
        pv_name = _pv("COUNTER")
        self.acc.ensure_monitored(pv_name)
        time.sleep(0.6)  # let at least one scan happen

        t_before = time.time()
        ts, val = self.acc.await_next_event(pv_name, timeout=3.0)
        elapsed = time.time() - t_before
        assert elapsed < 2.0, f"await_next_event took too long: {elapsed}s"
        assert val > 0

    def test_scanning_pv_buffer_time_window(self):
        """get_buffer_data with time window on scanning PV."""
        pv_name = _pv("COUNTER")
        self.acc.ensure_monitored(pv_name)
        time.sleep(2.0)

        t_mid = time.time()
        time.sleep(2.0)

        # Only get data from the second half
        data = self.acc.get_buffer_data(pv_name, start=t_mid)
        assert len(data) >= 2, f"Expected >=2 readings in 2s window, got {len(data)}"

    def test_read_fresh_timestamps_are_after_now(self):
        """read_fresh must only return data with timestamps after 'now'."""
        pv_name = _pv("COUNTER")
        self.acc.ensure_monitored(pv_name)
        time.sleep(1.0)  # let buffer fill with old data

        now = time.time()
        time.sleep(1.5)  # let new readings arrive

        result = self.acc.read_fresh(
            [pv_name], timeout=5.0, now=now,
            min_readings=2, max_readings=3, reduce=None,
            include_timestamps=True,
        )
        timestamps, values = result[pv_name]
        assert len(timestamps) >= 2, f"Expected >=2 readings, got {len(timestamps)}"
        for ts in timestamps:
            assert ts >= now, f"Timestamp {ts} is before now={now} - stale data leaked through"

    def test_read_fresh_consecutive_calls_get_newer_data(self):
        """Consecutive read_fresh calls should return progressively newer timestamps."""
        pv_name = _pv("COUNTER")
        self.acc.ensure_monitored(pv_name)
        time.sleep(0.6)

        now1 = time.time()
        time.sleep(1.0)
        r1 = self.acc.read_fresh(
            [pv_name], timeout=5.0, now=now1,
            min_readings=1, max_readings=1, reduce="mean",
            include_timestamps=True,
        )
        ts1, val1 = r1[pv_name]

        now2 = time.time()
        time.sleep(1.0)
        r2 = self.acc.read_fresh(
            [pv_name], timeout=5.0, now=now2,
            min_readings=1, max_readings=1, reduce="mean",
            include_timestamps=True,
        )
        ts2, val2 = r2[pv_name]

        assert ts2 > ts1, f"Second read_fresh timestamp ({ts2}) not newer than first ({ts1})"
        assert val2 > val1, f"Counter value did not increase: {val1} -> {val2}"

    def test_read_fresh_rejects_stale_data(self):
        """read_fresh with a recent 'now' must not return old buffered data."""
        pv_name = _pv("COUNTER")
        self.acc.ensure_monitored(pv_name)
        time.sleep(1.0)  # let buffer fill

        # Record current counter value
        val_before = self.acc.read(pv_name)
        time.sleep(0.1)

        # Set 'now' to current time - only future readings qualify
        now = time.time()
        time.sleep(1.5)

        result = self.acc.read_fresh(
            [pv_name], timeout=5.0, now=now,
            min_readings=1, max_readings=1, reduce="mean",
            include_timestamps=True,
        )
        ts, val = result[pv_name]
        assert ts >= now, f"Got stale timestamp {ts} < now={now}"
        assert val > val_before, \
            f"Value {val} should be newer than pre-existing {val_before}"


# ---------------------------------------------------------------------------
# pyepics AcceleratorPE tests
# ---------------------------------------------------------------------------

class TestAcceleratorPyepics:
    @pytest.fixture(autouse=True)
    def setup(self, epics_ioc):
        from pybeamtools.controlsdirect.clib_pyepics import AcceleratorPE
        self.acc = AcceleratorPE()
        yield

    def test_read_static(self):
        val = self.acc.read(_pv("STATIC"))
        assert val == pytest.approx(42.0)

    def test_read_initial(self):
        val = self.acc.read(_pv("X0"))
        assert isinstance(val, (int, float))

    def test_ensure_connected_by_name(self):
        self.acc.ensure_connected([_pv("X0"), _pv("STATIC")])

    def test_write_and_read(self):
        self.acc.write({_pv("X0"): 7.5})
        time.sleep(0.3)
        val = self.acc.read(_pv("X0"))
        assert val == pytest.approx(7.5)

    def test_write_readback_link(self):
        self.acc.write({_pv("X1"): 2.5})
        time.sleep(0.5)
        val = self.acc.read(_pv("X1:RB"))
        assert val == pytest.approx(2.5)

    def test_subscribe_and_buffer(self):
        pv_name = _pv("X0")
        self.acc.ensure_monitored(pv_name)

        self.acc.write({pv_name: 1.0})
        time.sleep(0.5)

        buf = self.acc.get_buffer(pv_name)
        assert len(buf) > 0, "Buffer should have data after subscription + write"

    def test_ensure_monitored(self):
        pv_name = _pv("X2")
        self.acc.ensure_monitored(pv_name)
        assert self.acc.is_monitoring(pv_name)

    def test_read_all_now(self):
        names = [_pv("X0"), _pv("STATIC")]
        results = self.acc.read_all_now(names)
        assert _pv("X0") in results
        assert _pv("STATIC") in results

    def test_read_all_now_squeeze(self):
        results = self.acc.read_all_now([_pv("STATIC")], squeeze=True)
        val = results[_pv("STATIC")]
        assert val == pytest.approx(42.0)

    def test_read_fresh(self):
        pv_name = _pv("X0")
        self.acc.ensure_monitored(pv_name)
        now = time.time()
        self.acc.write({pv_name: 42.0})
        time.sleep(0.5)
        result = self.acc.read_fresh(
            [pv_name], timeout=5.0, now=now, min_readings=1, reduce="mean"
        )
        assert pv_name in result
        assert result[pv_name] == pytest.approx(42.0)

    def test_read_fresh_with_timestamps(self):
        pv_name = _pv("X1")
        self.acc.ensure_monitored(pv_name)
        now = time.time()
        self.acc.write({pv_name: 9.0})
        time.sleep(0.5)
        result = self.acc.read_fresh(
            [pv_name], timeout=5.0, now=now, min_readings=1, reduce="mean",
            include_timestamps=True,
        )
        ts, val = result[pv_name]
        assert ts > 0
        assert val == pytest.approx(9.0, abs=0.1)

    def test_write_and_verify(self):
        sp = _pv("X2")
        rb = _pv("X2:RB")
        self.acc.ensure_monitored([sp, rb])
        time.sleep(0.5)

        result = self.acc.write_and_verify(
            data_dict={sp: 5.55},
            readback_map={sp: rb},
            atol_map={sp: 0.01},
            timeout=10.0,
            readback_timeout=10.0,
            delay_after_write=0.3,
            delay_after_readback=0.1,
            read_first=False,
            try_read_now_after=0.0,
        )
        assert sp in result
        assert result[sp] == pytest.approx(5.55, abs=0.01)

    def test_subscribe_custom(self):
        pv_name = _pv("X1")
        received = []

        def my_callback(pvname=None, value=None, **kwargs):
            received.append(value)

        self.acc.subscribe_custom(pv_name, my_callback)
        self.acc.write({pv_name: 99.0})
        time.sleep(0.5)
        self.acc.unsubscribe_custom(pv_name, my_callback)

        assert len(received) > 0
        assert any(np.isclose(v, 99.0, atol=0.01) for v in received)

    def test_get_buffer_data(self):
        pv_name = _pv("X2")
        self.acc.ensure_monitored(pv_name)
        t_before = time.time()
        self.acc.write({pv_name: 3.0})
        time.sleep(0.5)
        data = self.acc.get_buffer_data(pv_name, start=t_before)
        assert len(data) > 0

    def test_get_latest_buffer_value(self):
        pv_name = _pv("X0")
        self.acc.ensure_monitored(pv_name)
        self.acc.write({pv_name: 11.0})
        time.sleep(0.5)
        ts, val = self.acc.get_latest_buffer_value(pv_name)
        assert ts > 0
        assert val == pytest.approx(11.0)

    def test_await_next_event(self):
        pv_name = _pv("X0")
        self.acc.ensure_monitored(pv_name)
        self.acc.write({pv_name: 0.0})
        time.sleep(0.3)

        self.acc.write({pv_name: 20.0})
        ts, val = self.acc.await_next_event(pv_name, timeout=5.0)
        assert val == pytest.approx(20.0)

    # -- Scanning PV tests (IOC-driven periodic updates) --------------------

    def test_scanning_pv_buffer_accumulation(self):
        """COUNTER scans at 0.5s - verify buffer accumulates multiple readings."""
        pv_name = _pv("COUNTER")
        self.acc.ensure_monitored(pv_name)
        t_start = time.time()
        time.sleep(3.0)

        data = self.acc.get_buffer_data(pv_name, start=t_start)
        assert len(data) >= 4, f"Expected >=4 buffered readings from 0.5s scan over 3s, got {len(data)}"

        # get_buffer_data returns newest-first, reverse for chronological order
        data = data[::-1]

        values = [r.data[0] for r in data]
        for i in range(1, len(values)):
            assert values[i] > values[i - 1], \
                f"Counter not monotonic: {values}"

        timestamps = [r.metadata.timestamp for r in data]
        for i in range(1, len(timestamps)):
            assert timestamps[i] > timestamps[i - 1], \
                f"Timestamps not monotonic: {timestamps}"

    def test_scanning_pv_read_fresh_multiple(self):
        """Collect multiple fresh readings from a scanning PV."""
        pv_name = _pv("SINE")
        self.acc.ensure_monitored(pv_name)
        now = time.time()
        time.sleep(1.5)

        result = self.acc.read_fresh(
            [pv_name], timeout=5.0, now=now,
            min_readings=3, max_readings=5, reduce="mean",
        )
        assert pv_name in result
        assert -1.0 <= result[pv_name] <= 1.0

    def test_scanning_pv_await_event(self):
        """await_next_event should return promptly for a scanning PV."""
        pv_name = _pv("COUNTER")
        self.acc.ensure_monitored(pv_name)
        time.sleep(0.6)

        t_before = time.time()
        ts, val = self.acc.await_next_event(pv_name, timeout=3.0)
        elapsed = time.time() - t_before
        assert elapsed < 2.0, f"await_next_event took too long: {elapsed}s"
        assert val > 0

    def test_scanning_pv_buffer_time_window(self):
        """get_buffer_data with time window on scanning PV."""
        pv_name = _pv("COUNTER")
        self.acc.ensure_monitored(pv_name)
        time.sleep(2.0)

        t_mid = time.time()
        time.sleep(2.0)

        data = self.acc.get_buffer_data(pv_name, start=t_mid)
        assert len(data) >= 2, f"Expected >=2 readings in 2s window, got {len(data)}"

    def test_read_fresh_timestamps_are_after_now(self):
        """read_fresh must only return data with timestamps after 'now'."""
        pv_name = _pv("COUNTER")
        self.acc.ensure_monitored(pv_name)
        time.sleep(1.0)

        now = time.time()
        time.sleep(1.5)

        result = self.acc.read_fresh(
            [pv_name], timeout=5.0, now=now,
            min_readings=2, max_readings=3, reduce=None,
            include_timestamps=True,
        )
        timestamps, values = result[pv_name]
        assert len(timestamps) >= 2, f"Expected >=2 readings, got {len(timestamps)}"
        for ts in timestamps:
            assert ts >= now, f"Timestamp {ts} is before now={now} - stale data leaked through"

    def test_read_fresh_consecutive_calls_get_newer_data(self):
        """Consecutive read_fresh calls should return progressively newer timestamps."""
        pv_name = _pv("COUNTER")
        self.acc.ensure_monitored(pv_name)
        time.sleep(0.6)

        now1 = time.time()
        time.sleep(1.0)
        r1 = self.acc.read_fresh(
            [pv_name], timeout=5.0, now=now1,
            min_readings=1, max_readings=1, reduce="mean",
            include_timestamps=True,
        )
        ts1, val1 = r1[pv_name]

        now2 = time.time()
        time.sleep(1.0)
        r2 = self.acc.read_fresh(
            [pv_name], timeout=5.0, now=now2,
            min_readings=1, max_readings=1, reduce="mean",
            include_timestamps=True,
        )
        ts2, val2 = r2[pv_name]

        assert ts2 > ts1, f"Second read_fresh timestamp ({ts2}) not newer than first ({ts1})"
        assert val2 > val1, f"Counter value did not increase: {val1} -> {val2}"

    def test_read_fresh_rejects_stale_data(self):
        """read_fresh with a recent 'now' must not return old buffered data."""
        pv_name = _pv("COUNTER")
        self.acc.ensure_monitored(pv_name)
        time.sleep(1.0)

        val_before = self.acc.read(pv_name)
        time.sleep(0.1)

        now = time.time()
        time.sleep(1.5)

        result = self.acc.read_fresh(
            [pv_name], timeout=5.0, now=now,
            min_readings=1, max_readings=1, reduce="mean",
            include_timestamps=True,
        )
        ts, val = result[pv_name]
        assert ts >= now, f"Got stale timestamp {ts} < now={now}"
        assert val > val_before, \
            f"Value {val} should be newer than pre-existing {val_before}"
