import collections
import random
import threading
import time

from pybeamtools.controlsdirect import Accelerator
from pybeamtools.controlsdirect.clib import RingBuffer


def test_dequeue_perf():
    dq = collections.deque(maxlen=Accelerator.CBUF_SIZE)
    rb = RingBuffer(Accelerator.CBUF_SIZE)

    t1 = time.perf_counter()
    for i in range(1000000):
        dq.append(i)

    t2 = time.perf_counter()
    print(f"Deque append: {t2 - t1}")

    t1 = time.perf_counter()
    for i in range(1000000):
        rb.append(i)
    t2 = time.perf_counter()
    print(f"RingBuffer append: {t2 - t1}")

    t1 = time.perf_counter()
    for i in range(1000000):
        l = list(dq)
    t2 = time.perf_counter()
    print(f"Deque to list: {t2 - t1}")

    t1 = time.perf_counter()
    for i in range(1000000):
        for j in range(Accelerator.CBUF_SIZE):
            l = dq[j]
    t2 = time.perf_counter()
    print(f"Deque by index: {t2 - t1}")

    t1 = time.perf_counter()
    for i in range(1000000):
        l = rb.to_list()
    t2 = time.perf_counter()
    print(f"RingBuffer to list: {t2 - t1}")


def test_get_buffer_data_chronological_order():
    """get_buffer_data with start= must return results oldest-first."""
    from types import SimpleNamespace
    acc = Accelerator()
    pv_name = "TEST:ORDER"
    acc.cbuf[pv_name] = collections.deque(maxlen=Accelerator.CBUF_SIZE)
    acc.cnts[pv_name] = 0

    # Insert 5 entries with known increasing timestamps
    base_ts = 1000.0
    for i in range(5):
        ts = base_ts + i
        response = SimpleNamespace(
            data=[float(i)],
            metadata=SimpleNamespace(timestamp=ts),
        )
        acc.cbuf[pv_name].append((ts, response))

    # Query with start before all entries
    data = acc.get_buffer_data(pv_name, start=base_ts - 1, use_local_time=True)
    assert len(data) == 5

    # Must be chronological: oldest first, newest last
    timestamps = [r.metadata.timestamp for r in data]
    assert timestamps == sorted(timestamps), \
        f"Expected chronological order, got {timestamps}"
    assert timestamps[0] == base_ts
    assert timestamps[-1] == base_ts + 4

    # Query with start in the middle — should only return entries after start
    data = acc.get_buffer_data(pv_name, start=base_ts + 2, use_local_time=True)
    assert len(data) == 2
    timestamps = [r.metadata.timestamp for r in data]
    assert timestamps == [base_ts + 3, base_ts + 4]

    # Query with start=None returns all in chronological order
    data = acc.get_buffer_data(pv_name, start=None)
    assert len(data) == 5
    timestamps = [r.metadata.timestamp for r in data]
    assert timestamps == sorted(timestamps)


class FakeResponse:
    def __init__(self, ch, response):
        self.name = ch
        self.response = response
        self.data = [response]
        self.metadata = None


class FakeChannel:
    def __init__(self, ch):
        self.name = ch

    def read(self, data_type="time", timeout=1):
        return FakeResponse(self.name, 3.5)

    def wait_for_connection(self, timeout):
        pass

    def wait_for_search(self, timeout):
        pass


def test_read_fresh():
    acc = Accelerator()

    def fake_source(ch):
        acc.cbuf[ch] = collections.deque(maxlen=Accelerator.CBUF_SIZE)
        acc.cnts[ch] = 0
        acc.kv.channels[ch] = FakeChannel(ch)
        while True:
            response = FakeResponse(ch, 3.5)
            acc.cbuf[ch].append((time.time(), response))
            acc.cnts[ch] += 1
            time.sleep(1)

    t = threading.Thread(target=fake_source, args=('ch1',))
    t.daemon = True
    t.start()

    time.sleep(2)
    assert acc.read('ch1')
