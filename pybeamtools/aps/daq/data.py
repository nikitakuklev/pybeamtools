import logging
from typing import Any, Optional

import numpy as np
from pydantic import BaseModel


class StreamerCallbackData(BaseModel):
    """Data from the APS DAQ system."""

    success: bool
    tag: Optional[float]
    data: dict[str, dict[str, Any]]


class PerformanceData(BaseModel):
    """Performance data from the APS DAQ system."""

    cb_thread_id: int
    cb_process_id: int
    event_rate: float
    event_cnt: int
    cb_time_total: float
    cb_avg_time: float
    avg_load: float
    connection_state_changes: list[tuple[float, bool]]
    cb_timestamps: list[float]
    cb_time_history: list[float]


class FakePvObject:
    def __init__(self, data):
        self.data = data

    def toDict(self):
        return self.data

    def keys(self):
        return self.data.keys()


def get_bpm_fields(c) -> list[str]:
    struct = c.getIntrospectionDict()
    found_fields = [x for x in struct.keys() if is_bpm_field(x)]
    return found_fields


def is_bpm_field(x):
    return x[0] == "s" and len(x) == 6


def get_bpm_channel_properties(c, devices, fields: list[str], time_field="time", extra_fields=None):
    if devices is None:
        bpms = get_bpm_fields(c)
    else:
        bpms = devices
    fl = []
    fp = {}
    for field in fields:
        fl.extend([f"{x}.{field}" for x in bpms])
        fp[field] = [(x, field) for x in bpms]
    if time_field is not None:
        fl.insert(0, "time")
    if extra_fields is not None:
        fl.extend(extra_fields)
    fstr = ", ".join(fl)
    return fp, f"field({fstr})"


# def get_ps_channel_properties(c, fields: list[str], add_time=True):
#     bpms = get_bpm_fields(c)
#     fl = []
#     fp = {}
#     for field in fields:
#         fl.extend([f"{x}.{field}" for x in bpms])
#         fp[field] = [(x, field) for x in bpms]
#     if add_time:
#         fl.insert(0, "time")
#     fstr = ", ".join(fields)
#     return fp, f"field({fstr})"

def post_process_daq_object_via_paths(
        data: dict,
        field_paths: dict[str, list[str]],
        ignore_errors=True,
        time_field: str = "time",
        tag_field: str = "acqClkTimestamp",
        frame_len: int = None,
        debug=False,
        trace=False,
        # tag_function: Optional[Callable] = None,
) -> tuple[list[np.ndarray], np.ndarray, list[str], tuple[int, int]]:
    """Process the data dictionary from the PV using the field paths to traverse the structure."""
    arrays = {field: [] for field in field_paths}
    channels = []
    datafields = list(data.keys())
    logger = logging.getLogger(__name__)
    if debug:
        logger.debug(f"PVO processing | analyzing {len(datafields)} channels")
        if trace:
            logger.debug(f"Have {datafields=}, will search for {field_paths=}")
    for field, path_list in field_paths.items():
        for fp in path_list:
            arr = data.get(fp[0], None)
            if arr is None:
                raise Exception(f"Bad device path {fp=}, have {data.keys()}")
            for p in fp[1:]:
                arr = arr.get(p, None)
                if arr is None:
                    raise Exception(f"Bad path {fp=} - no data")
            larr = len(arr)
            if frame_len is not None and larr != frame_len:
                if larr == 0:
                    pass
                else:
                    logger.error(f"Bad length {larr=} vs {frame_len=}")
                    if not ignore_errors:
                        raise Exception(f"Bad length {larr}, expected {frame_len}")
            if larr > 0:
                if trace:
                    logger.debug(f"Found path {fp=}")
                arrays[field].append(arr)
                channels.append(fp[0])
            else:
                if not ignore_errors:
                    raise ValueError(f"Bad channel {fp[0]=}")

    time_array = data[time_field].copy()
    time_tag = data[tag_field]
    tag = (time_tag["secondsPastEpoch"], (time_tag["nanoseconds"] // 10000000) * 10)

    final_matrices = []
    for field in field_paths:
        if len(arrays[field]) == 0:
            final_matrices.append(None)
            continue

        # convert to float due to possible overflow for int32
        # float32 is also faster and has enough precision
        # np.nextafter(59852530.0, 59852530.0+1) = 59852528.00000001
        if (s := set([len(x) for x in arrays[field]])) != {len(arrays[field][0])}:
            print(f"Have nonuniform lengths {s}")
        mat = np.row_stack(arrays[field]).astype(np.float32).T  # this now has F order for column-wise mean
        assert mat.flags["F_CONTIGUOUS"]
        # mat = np.column_stack(arrays).astype(np.float64)
        # assert mat.flags['C_CONTIGUOUS']# and mat.flags['OWNDATA']

        del arrays[field]
        final_matrices.append(mat)

    # bpm_names = [SR_BPMS_DAQ_TO_NAME[x] for x in bpms]
    assert time_array.flags["C_CONTIGUOUS"] and time_array.flags["OWNDATA"]

    return final_matrices, time_array, channels, tag