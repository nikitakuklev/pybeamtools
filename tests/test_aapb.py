import io
import tempfile

from pybeamtools.archiver import EPICSEvent_pb2
from pybeamtools.archiver.rawdata import DBR_PB_TO_TYPE_MAP, PBFile
import pathlib
import numpy as np


def test_read():
    f = PBFile(pathlib.Path('aps/PTB2BTSEfficiencyM_2024_08_09.pb'))

    f.read_header()
    assert f.year == 2024
    assert f.pi.pvname == 'PTB2BTSEfficiencyM'

    f.read_events()
    assert len(f.events) == 4164  # line count - 1
    assert f.dti[0] > np.datetime64(f'2024-08-09T00:00')
    assert f.dti[0] < np.datetime64(f'2024-08-10T00:00')
    assert 0.0 <= f.events[0].val <= 100.0
    print(f.events[0])


def test_write():
    pb = PBFile()
    pi = EPICSEvent_pb2.PayloadInfo()
    pi.pvname = 'test'
    pi.year = 2020
    pi.type = DBR_PB_TO_TYPE_MAP[EPICSEvent_pb2.ScalarDouble]
    pb.pi = pi

    events = []
    for i in range(5):
        ev = EPICSEvent_pb2.ScalarDouble()
        ev.secondsintoyear = i
        ev.nano = i * 50 + 1
        ev.val = i * 10.0
        events.append(ev)

    pb.events = events

    buf = pb.to_bytes()
    print(buf)

    pb2 = PBFile(io.BytesIO(buf))
    pb2.read_header()
    assert pb2.pi.pvname == 'test'
    assert pb2.pi.year == 2020

    pb2.read_events()
    assert len(pb2.events) == 5
    assert pb2.events[3].val == 30.0



