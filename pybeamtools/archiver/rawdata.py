from typing import Union

from . import EPICSEvent_pb2 as pbe
import io

import base64
import numpy as np
import pandas as pd
import pathlib
import datetime
from copy import deepcopy

CARRIAGERETURN_ESCAPE_CHAR = b'\x03'
CARRIAGERETURN_CHAR = b'\x0D'
NEWLINE_ESCAPE_CHAR = b'\x02'
NEWLINE_CHAR = b'\x0A'
ESCAPE_ESCAPE_CHAR = b'\x01'
ESCAPE_CHAR = b'\x1B'
ESCAPE_CHAR_SEQUENCE = b'\x1B\x01'
NEWLINE_CHAR_SEQUENCE = b'\x1B\x02'
CARRIAGERETURN_CHAR_SEQUENCE = b'\x1B\x03'

# DBR_SCALAR_STRING(0, false, "String", PayloadType.SCALAR_STRING, true),
# DBR_SCALAR_SHORT(1, false, "short", PayloadType.SCALAR_SHORT, true),
# DBR_SCALAR_FLOAT(2, false, "float", PayloadType.SCALAR_FLOAT, true),
# DBR_SCALAR_ENUM(3, false, "enum", PayloadType.SCALAR_ENUM, true),
# DBR_SCALAR_BYTE(4, false, "byte", PayloadType.SCALAR_BYTE, true),
# DBR_SCALAR_INT(5, false, "int", PayloadType.SCALAR_INT, true),
# DBR_SCALAR_DOUBLE(6, false, "double", PayloadType.SCALAR_DOUBLE, true),
# DBR_WAVEFORM_STRING(7, true, "String", PayloadType.WAVEFORM_STRING, true),
# DBR_WAVEFORM_SHORT(8, true, "short", PayloadType.WAVEFORM_SHORT, true),
# DBR_WAVEFORM_FLOAT(9, true, "float", PayloadType.WAVEFORM_FLOAT, true),
# DBR_WAVEFORM_ENUM(10, true, "enum", PayloadType.WAVEFORM_ENUM, true),
# DBR_WAVEFORM_BYTE(11, true, "byte", PayloadType.WAVEFORM_BYTE, true),
# DBR_WAVEFORM_INT(12, true, "int", PayloadType.WAVEFORM_INT, true),
# DBR_WAVEFORM_DOUBLE(13, true, "double", PayloadType.WAVEFORM_DOUBLE, true),
# DBR_V4_GENERIC_BYTES(14, true, "v4generic", PayloadType.V4_GENERIC_BYTES, false);
DBR_TYPE_TO_PB_MAP = {0: pbe.ScalarString,
                      1: pbe.ScalarShort,
                      2: pbe.ScalarFloat,
                      3: pbe.ScalarEnum,
                      4: pbe.ScalarByte,
                      5: pbe.ScalarInt,
                      6: pbe.ScalarDouble,
                      7: pbe.VectorString,
                      8: pbe.VectorShort,
                      9: pbe.VectorFloat,
                      10: pbe.VectorEnum,
                      11: pbe.VectorChar,
                      12: pbe.VectorInt,
                      13: pbe.VectorDouble,
                      14: pbe.V4GenericBytes
                      }

DBR_PB_TO_TYPE_MAP = {v: k for k, v in DBR_TYPE_TO_PB_MAP.items()}


def unescape_new_line(l, skipend=0):
    l = list(l)
    skipnext = False
    s2 = []
    for i in range(len(l) - skipend):
        if skipnext:
            skipnext = False
            continue
        if l[i] == ord(ESCAPE_CHAR):
            if l[i + 1] == ord(CARRIAGERETURN_ESCAPE_CHAR):
                s2.append(ord(CARRIAGERETURN_CHAR))
                skipnext = True
            elif l[i + 1] == ord(NEWLINE_ESCAPE_CHAR):
                s2.append(ord(NEWLINE_CHAR))
                skipnext = True
            elif l[i + 1] == ord(ESCAPE_ESCAPE_CHAR):
                s2.append(ord(ESCAPE_CHAR))
                skipnext = True
            else:
                s2.append(l[i])

        else:
            # print(l[i])
            s2.append(l[i])
    return bytes(s2)


def unescape_new_line_fast(l):
    l = l.replace(CARRIAGERETURN_CHAR_SEQUENCE, CARRIAGERETURN_CHAR)
    l = l.replace(NEWLINE_CHAR_SEQUENCE, NEWLINE_CHAR)
    l = l.replace(ESCAPE_CHAR_SEQUENCE, ESCAPE_CHAR)
    return l


def escape_new_line(l):
    l = l.replace(ESCAPE_CHAR, ESCAPE_CHAR_SEQUENCE)
    l = l.replace(NEWLINE_CHAR, NEWLINE_CHAR_SEQUENCE)
    l = l.replace(CARRIAGERETURN_CHAR, CARRIAGERETURN_CHAR_SEQUENCE)
    return l


def write_new_file(pi, events):
    f = io.BytesIO()
    f.write(escape_new_line(pi.SerializeToString()))
    f.write(NEWLINE_CHAR)
    for e in events:
        f.write(escape_new_line(e.SerializeToString()))
        f.write(NEWLINE_CHAR)
    return f.getvalue()


def write_to_stream(f, pi, events):
    f.write(escape_new_line(pi.SerializeToString()))
    f.write(NEWLINE_CHAR)
    for e in events:
        f.write(escape_new_line(e.SerializeToString()))
        f.write(NEWLINE_CHAR)


def get_dti(events, year: int = 2024, verbose=True):
    """ From a list of event protobuf objects, derive a pandas DatetimeIndex """
    ty = np.datetime64(f'{year}-01-01T00:00')
    if verbose:
        e1 = events[0]
        el = events[-1]
        start_time = ty + np.timedelta64(e1.secondsintoyear, 's') + np.timedelta64(e1.nano, 'ns')
        end_time = ty + np.timedelta64(el.secondsintoyear, 's') + np.timedelta64(el.nano, 'ns')
        print(f'{start_time=} --> {end_time=}')
    # timedeltas = np.array([np.timedelta64(e.secondsintoyear*1000000000 + e.nano, 'ns') for e in events])
    timedeltas = np.array([e.secondsintoyear * 1000000000 + e.nano for e in events], dtype='timedelta64[ns]')
    timestamps = ty + timedeltas
    dti = pd.DatetimeIndex(timestamps)
    return dti


class PBFile:
    """
    Object representing a file with a header and a series of protobuf events.
    To read, use:
        pbfile.read_header()
        pbfile.read_events()

    Alternatively, iterator interface is available

    To write, use extgernal function:
        write_to_stream(f, pbfile.pi, pbfile.events)
    """

    def __init__(self, f: Union[pathlib.Path, io.BytesIO] = None):
        """
        Create a new PBFile object with a path. No data is written or read unless read_header is True.
        :param f: pathlib.Path
        """
        if f is not None:
            assert isinstance(f, (pathlib.Path, io.BytesIO))
        self.f = f
        self.events = None
        self.year = None
        self.pb_class = None
        self.pi = None
        self.stream = None
        self.faults = 0
        self.pos = 0
        self.last_good_line = None
        self._dti = None
        self.unescape = unescape_new_line_fast

    def read_header(self):
        if isinstance(self.f, pathlib.Path):
            assert self.f.is_file()
            self.stream = s = open(self.f, 'rb')
        elif isinstance(self.f, io.BytesIO):
            self.stream = s = self.f
        header = s.readline()[:-1]
        # print(f'{header=}')
        header = self.unescape(header)
        # print(f'{header=}')
        self.pi = payload_info = pbe.PayloadInfo()
        payload_info.ParseFromString(header)
        # print(f'{payload_info=}')

        self.pb_class = DBR_TYPE_TO_PB_MAP[payload_info.type]
        self.year = payload_info.year
        # print(f'{payload_info.type=} {self.pb_class=}')

    @property
    def n_events(self):
        if self.events is not None:
            return len(self.events)
        else:
            return None

    @property
    def dti(self):
        if self._dti is None:
            self._process_event_ts()
        return self._dti

    @property
    def dta(self):
        if self._dta is None:
            self._process_event_ts()
        return self._dta

    def __iter__(self):
        return self

    def __next__(self):
        # n = self.next_event()
        # if n is None:
        while ((n := self.next_event()) is None):
            pass
        return n

    def close(self):
        self.stream.close()

    def string_to_event(self, next_line: bytes):
        """
        Do actual protobuf conversion after unescaping the string
        """
        # ll = next_line[:-1]
        # ll = bytes(memoryview(next_line)[:-1])
        ll = next_line[:-1]
        ll = self.unescape(ll)

        c = self.pb_class()
        try:
            c.ParseFromString(ll)
        except:
            print(
                    f'{self.pi.pvname} | Failed to parse {next_line=} {len(next_line)} {base64.b64encode(next_line)} {ll=} {len(ll)} {base64.b64encode(ll)} at {self.pos=} {self.stream.tell()=} | {self.last_good_line=} {len(self.last_good_line)} {base64.b64encode(self.last_good_line)}')
            self.faults += 1
            return None
        self.last_good_line = ll
        return c

    def next_event(self):
        """
        Read the next event from the stream
        """
        if self.stream is None:
            self.read_header()

        next_line = self.stream.readline()
        self.pos += 1
        if next_line == b'':
            raise StopIteration
        # assert len(next_line) >= 6, f'Line too short ????'

        c = self.string_to_event(next_line)
        # if self.pos % 100000 == 0:
        #    print(self.pos, c.secondsintoyear)
        assert not isinstance(c, bool), "wtf???"
        return c

    def read_events(self):
        """
        Read all events in the file and return them as a list
        """
        if self.events is not None:
            return self.events
        if self.stream is None:
            self.read_header()

        self.last_good_line = None
        self.events = []
        while ((next_line := self.stream.readline()) != b''):
            self.pos += 1
            c = self.string_to_event(next_line)
            assert not isinstance(c, bool), "wtf???"
            if c is not None:
                self.events.append(c)
        return self.events

    def to_bytes(self):
        """
        Serialize the header and events to a byte string
        """
        assert self.events is not None and self.pi is not None
        f = io.BytesIO()
        f.write(escape_new_line(self.pi.SerializeToString()))
        f.write(NEWLINE_CHAR)
        for e in self.events:
            f.write(escape_new_line(e.SerializeToString()))
            f.write(NEWLINE_CHAR)
        return f.getvalue()

    def _process_event_ts(self):
        events = self.events or self.read_events()
        # e1 = events[0]
        # el = events[-1]
        ty = np.datetime64(f'{self.year}-01-01T00:00')
        # start_time = ty + np.timedelta64(e1.secondsintoyear, 's') + np.timedelta64(e1.nano, 'ns')
        # end_time = ty + np.timedelta64(el.secondsintoyear, 's') + np.timedelta64(el.nano, 'ns')
        # print(f'{self.f}: {start_time=} --> {end_time=}')
        timestamps = np.array([ty + np.timedelta64(e.secondsintoyear * 1000000000 + e.nano, 'ns') for e in events])
        dti = pd.DatetimeIndex(timestamps)
        self._dta = timestamps
        self._dti = dti
        return dti

    def to_monthly(self, root_dir):
        """
        Convert the events in this file to monthly partitioned PBfiles
        """
        root_dir = pathlib.Path(root_dir)
        if self.dti is None:
            dti = self._process_event_ts()
        else:
            dti = self.dti
        events = self.events
        months = dti.month
        unique, unique_counts = np.unique(months, return_counts=True)
        indices = np.arange(len(events))
        print(f'{unique=} with {unique_counts=}')
        index_sets = [indices[months == i] for i in unique]
        new_objects = []
        for u, s in zip(unique, index_sets):
            es = [events[i] for i in s]
            ts_str = datetime.datetime(2024, u, 1, 0, 0, 0, 0).strftime('%Y_%m')
            child_path = root_dir / (self.f.name.split(':')[0] + ":" + ts_str)
            print(f'Making {u} {s} into {child_path}')
            pbi_child = PBFile(child_path)
            pbi_child.events = es
            pbi_child.year = self.year
            pbi_child.pi = deepcopy(self.pi)
            new_objects.append(pbi_child)

        return new_objects

    def to_daily(self, root_dir, verbose=True):
        """
        Convert the events in this file to daily partitioned AA PBfiles
        """
        root_dir = pathlib.Path(root_dir)
        dti = self.dti
        events = self.events
        months = dti.month
        days = dti.day
        unique, unique_counts = np.unique(list(zip(months, days)), return_counts=True, axis=0)
        indices = np.arange(len(events))
        if verbose:
            print(f'{unique=} with {unique_counts=}')
        index_sets = [indices[(months == i[0]) & (days == i[1])] for i in unique]
        new_objects = []
        for u, s in zip(unique, index_sets):
            es = [events[i] for i in s]
            ts_str = datetime.datetime(2024, u[0], u[1], 0, 0, 0, 0).strftime('%Y_%m_%d')
            child_path = root_dir / (self.f.name.split(':')[0] + ":" + ts_str + '.pb')
            if verbose:
                print(f'Making {u} {s} into {child_path}')
            pbi_child = PBFile(child_path)
            pbi_child.events = es
            pbi_child.year = self.year
            pbi_child.pi = deepcopy(self.pi)
            new_objects.append(pbi_child)

        return new_objects

    def to_daily_rolling(self, root_dir, year=2024, verbose=True):
        """
        Alternative to PBFile.to_daily that does rolling partitioning. This is useful for files where timestamps are not
        monotonic due to IOC issues. It creates next partition as soon as at least 1 event in the next day is found.
        """
        root_dir = pathlib.Path(root_dir)
        if self.dti is None:
            dti = self._process_event_ts()
        else:
            dti = self.dti
        # months = dti.month
        days = dti.dayofyear
        nev = len(self.events)
        idx1 = idx2 = 0
        ty = np.datetime64(f'{year}-01-01T00:00:00')
        subsets = []
        while True:
            day = days[idx1]
            while idx2 < nev and days[idx2] == day:
                idx2 += 1
            tday = ty + np.timedelta64(day - 1, 'D')
            ptday = pd.to_datetime(tday)
            daymo = ptday.day
            mo = ptday.month
            if verbose:
                print(f'Found segment from {idx1=} to {idx2=} for {day=} = {daymo=} {mo=}')
            subsets.append([idx1, idx2, day, (daymo, mo), self.events[idx1:idx2]])
            if idx2 == len(self.events):
                break
            idx1 = idx2

        # index_sets = [indices[(months == i[0]) & (days == i[1])] for i in unique]
        new_objects = []
        for idx1, idx2, day, (daymo, mo), subevents in subsets:
            ts_str = datetime.datetime(2024, mo, daymo, 0, 0, 0, 0).strftime('%Y_%m_%d')
            child_path = root_dir / (self.f.name.split(':')[0] + ":" + ts_str + '.pb')  # root_dir / (
            if verbose:
                print(f'Making {daymo} {mo} into {child_path}')
            pbi_child = PBFile(child_path)
            pbi_child.events = subevents
            pbi_child.year = year
            pbi_child.pi = deepcopy(self.pi)
            new_objects.append(pbi_child)

        return new_objects


# FOR REFERENCE - the method used to split up annual files into daily ones

# def break_file(f):
#     n_events = 0
#     written = {}
#     success = {}
#     fails = {}
#     not_sorted = {}
#     try:
#         fstr = str(f)
#         t1 = time.time()
#         pbi = PBFile(f, autoread=True)
#         name_path = f.relative_to('/adata/aop/archiver/storage/replica/storage/lts')
#         events = pbi.read_events()
#         nev = len(events)
#         n_events += nev
#
#         print(
#             f'File size {sizeof_fmt(f.stat().st_size)=} {len(events)=} {(time.time() - t1) / len(events) * 1e6:.3f} us now | {f=}')
#
#         dti = get_dti(events, verbose=False)
#         # dti = pbi._process_event_ts()
#         order = dti[:-1] <= dti[1:]
#         is_sorted = np.all(order)
#         if not is_sorted:
#             not_sorted[fstr] = np.sum(order) - len(dti) - 1
#             # print(f'WARNING: {f=} NOT SORTED PROPERLY')
#
#         if pbi.faults == 0 and is_sorted:
#             success[fstr] = len(events)
#             plist = events_by_day(events, pbi.pi, f, dti=dti, root_dir=str(out_folder / name_path.parent),
#                                   verbose=False)
#             assert sum(len(e.events) for e in plist) == len(events)
#             print(f'SUCCESS - {out_folder / name_path.parent=} {len(plist)=} {plist[0].f=}')
#             for pbis in plist:
#                 if pbis.f in written:
#                     continue
#                 elif pbis.f.is_file():
#                     continue
#                 pbis.f.parent.mkdir(exist_ok=True, parents=True)
#                 with open(pbis.f, 'wb') as stream:
#                     write_to_stream(stream, pbis.pi, pbis.events)
#                     print(f'Wrote {pbis.f=} with {pbis.n_events=}')
#                     written[str(pbis.f)] = pbis.n_events
#         else:
#             fails[fstr] = (len(events), pbi.faults, is_sorted)
#             print(f'FAULTY FILE: {f=} {f.stat().st_size=} {pbi.faults=}')
#             print('----------------')
#         del pbi
#         return success, fails, written, not_sorted
#     except Exception as ex:
#         print(f'FAILED FILE: {f=} {f.stat().st_size=} {ex=}')
#         print('----------------')
#         raise ex