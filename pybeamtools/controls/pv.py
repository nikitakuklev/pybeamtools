import json
import time
import uuid
from abc import abstractmethod
from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel

from .errors import ControlLibException, InvalidWriteError, SecurityError
from ..utils.pydantic import to_sdds

__all__ = ['SimPV', 'EPICSPV', 'PVAccess', 'PVOptions']


class PVAccess(Enum):
    RO = 1
    #    WRITE = 2
    RW = 3


class WriteResponse:
    def __init__(self, ts, data):
        self.timestamp = ts
        self.data = data


class PVOptions(BaseModel):
    name: str
    low: Union[float, int] = None
    high: Union[float, int] = None
    monitor: bool = True
    security: PVAccess = PVAccess.RO
    read_timeout: float = 2.0
    write_timeout: float = None

    class Config:
        extra = 'forbid'
        use_enum_values = True

    def sdds(self):
        return to_sdds(json.loads(self.json()))


class PV:
    def __init__(self, options: PVOptions):
        self.uuid = str(uuid.uuid4())
        self.name = options.name
        self.options = options

    @abstractmethod
    def read(self, *, wait=True, callback=None,
             timeout=None, data_type=None, data_count=None, notify=True
             ):
        pass

    def __str__(self):
        return f'{self.__class__.__name__} {self.options}'

    def __repr__(self):
        return self.__str__()

    def _check_proposed_write(self, data):
        if isinstance(data, (float, int)):
            if self.options.low and data < self.options.low:
                raise InvalidWriteError(
                        f'Value {data} below bounds ({self.options.low}|{self.options.high})')
                # return False
            if self.options.high and data > self.options.high:
                raise InvalidWriteError(
                        f'Value {data} above bounds ({self.options.low}|{self.options.high})')
        elif isinstance(data, str):
            pass
        else:
            raise ControlLibException(f'Unrecognized value  ({data=}) ({type(data)=})')


class EPICSPV(PV):
    def __init__(self, options: PVOptions):
        from .network import EPICSConnectionManager
        self.cm: Optional[EPICSConnectionManager] = None
        self.lower_ctrl_limit = self.upper_ctrl_limit = None
        super().__init__(options)

    @property
    def caproto(self):# -> Optional[caproto.threading.client.PV]:
        if self.cm is None:
            return None
        else:
            return self.cm.pv_caproto_map[self.name]

    def read(self, *, wait=True, callback=None,
             timeout=None, data_type=None, data_count=None, notify=True
             ):
        cm = self.caproto
        if cm is None:
            raise ControlLibException(f'PV is not bound to a connection manager')
        return self.caproto.read(wait=wait, callback=callback,
                                 timeout=self.options.read_timeout if timeout is None else timeout,
                                 data_type=data_type, data_count=data_count, notify=notify)

    def write(self, data, *, wait=True, callback=None,
              timeout=None, notify=None, data_type=None, data_count=None
              ):
        # Check access
        if self.options.security != PVAccess.RW.value:
            raise SecurityError(f'Writes on PV {self.name} are forbidden')
        # Propose a write - any issues will raise an Exception
        self.cm.acc.propose_writes([self.name], [data])
        # Perform write
        return self.caproto.write(data, wait=wait, callback=callback,
                                  timeout=self.options.write_timeout if timeout is None else timeout,
                                  notify=notify, data_type=data_type, data_count=data_count)


class SimPV(PV):
    def __init__(self, options: PVOptions):
        from .network import SimConnectionManager
        self.cm: Optional[SimConnectionManager] = None
        super().__init__(options)

    def read(self, *, wait=True, callback=None,
             timeout=None, data_type=None, data_count=None, notify=True
             ):
        if timeout is not None or data_type is not None or data_count is not None:
            raise
        return self.cm.sim.read_channel(self.name)

    def write(self, data, *, wait=True, callback=None,
              timeout=None, notify=None, data_type=None, data_count=None
              ) -> WriteResponse:
        if not isinstance(data, (int, float, str)):
            raise InvalidWriteError(f'Data {data} is not of valid type')
        # Check access
        if self.options.security != PVAccess.RW.value:
            raise SecurityError(f'Write on PV ({self.name}) forbidden by access mask')
        # Propose a write - any issues will raise an Exception
        self.cm.acc.propose_writes([self.name], [data])
        # Perform write
        self.cm.sim.write_channel(self.name, data)
        return WriteResponse(ts=time.time(), data=None)
