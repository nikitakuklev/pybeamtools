from typing import Any, Optional

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
