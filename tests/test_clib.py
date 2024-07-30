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


def test_get_buffer_data():
    acc = Accelerator()


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
