import fnmatch
import logging
import time
import uuid
from abc import ABC, abstractmethod
from typing import Any, Optional

from pydantic import BaseModel, NonNegativeFloat, NonNegativeInt, field_validator, model_validator

from .errors import ControlLibException


class WildcardPV:
    def __init__(self, pattern):
        self.pattern = pattern


class InterlockOptions(BaseModel):
    pv_list: list[str]
    read_events: list[str] = None
    write_events: list[str] = None
    priority: NonNegativeInt = 0
    ilock_type: str = ''

    @model_validator(mode='after')
    def check(self):
        reads = self.read_events
        writes = self.write_events
        reads_set = set(reads)
        pv_set = set(self.pv_list)
        assert reads_set.issubset(pv_set)
        assert set(writes).issubset(pv_set)
        return values


class InterlockInternalError(ControlLibException):
    pass


class Interlock(ABC):
    def __init__(self, options: InterlockOptions):
        self.options = options
        if options.read_events is not None:
            for pv in options.read_events:
                if pv not in options.pv_list:
                    raise InterlockInternalError(f'PV {pv} subscription requested but not in PV list')
        if options.write_events is not None:
            for pv in options.write_events:
                if pv not in options.pv_list:
                    raise InterlockInternalError(f'PV {pv} subscription requested but not in PV list')
        self.uuid = uuid.uuid4().hex[:12]

    @abstractmethod
    def callback_read(self, trigger_pvs, data, timestamps):
        pass

    @abstractmethod
    def callback_write(self, trigger_pvs, data, timestamps):
        pass

    def check_match_write(self, pvs_names: list[str], pvs_data: list):
        """ Check if interlock is interested in proposed writes """
        for pv_name in pvs_names:
            for pv_name_trigger in self.options.write_events:
                if '*' in pv_name_trigger:
                    if fnmatch.fnmatch(pv_name, pv_name_trigger):
                        return True
                else:
                    if pv_name == pv_name_trigger:
                        return True
        return False

    def filter_pv_names(self, candidate_pv_names: list[str]):
        """ Selects any PVs of interest for this interlock """
        result = []
        for pv_name in candidate_pv_names:
            for pv_name_trigger in self.options.pv_list:
                if '*' in pv_name_trigger:
                    if fnmatch.fnmatch(pv_name, pv_name_trigger):
                        result.append(pv_name)
                        break
                else:
                    if pv_name == pv_name_trigger:
                        result.append(pv_name)
                        break
        return list(set(result))


class LimitInterlockOptions(InterlockOptions):
    ilock_type: str = 'limit'
    limits: dict[str, tuple[Optional[float], Optional[float]]]
    block_all_writes: bool = False

    @field_validator('limits')
    def check_limits(cls, v):
        if v is not None:
            assert len(v) > 0
            for tpl in v.values():
                assert len(tpl) == 2
                if tpl[0] is not None and tpl[1] is not None:
                    assert tpl[0] <= tpl[1]
            return v


class LimitInterlock(Interlock):
    options: LimitInterlockOptions

    def __init__(self, options: LimitInterlockOptions):
        # pv_list = options.pv_list
        # limits = options.limits
        # data = {'low': [limits[k][0] if k in limits else None for k in pv_list],
        #         'high': [limits[k][1] if k in limits else None for k in pv_list]}
        # self.df: pd.DataFrame = pd.DataFrame(index=pv_list, data=data)
        self.logger = logging.getLogger(self.__class__.__name__)
        assert isinstance(options, LimitInterlockOptions)
        super().__init__(options)

    def callback_read(self, trigger_pvs, data, timestamps):
        raise InterlockInternalError(f'Internal failure')

    def callback_write(self, trigger_pvs: dict[str, Any], data: dict[str, Any],
                       timestamps: dict[str, float]) -> dict:
        #self.logger.debug(f'Interlock ({self.uuid}) write callback with {self.options} | {data}')
        self.logger.debug(f'Interlock ({self.uuid}) write callback')
        assert isinstance(data, dict)
        assert all(isinstance(x, str) for x in data.keys())
        assert isinstance(trigger_pvs, dict)
        assert all(isinstance(x, str) for x in trigger_pvs.keys())
        assert set(data.keys()) == set(self.options.pv_list)
        try:
            if self.options.block_all_writes:
                for pv_name in self.options.pv_list:
                    bounds = self.options.limits.get(pv_name, None)
                    if bounds is not None:
                        value = data[pv_name]
                        low = bounds[0]
                        high = bounds[1]
                        self.logger.debug(f'Interlock ({self.uuid}) {low=} {value=} {high=}')
                        if low <= value <= high:
                            continue
                        else:
                            raise InterlockInternalError(f'PV ({pv_name}) at ({value}), outside ({low}|{high}), blocking all')

            for pv_name, value in trigger_pvs.items():
                assert isinstance(pv_name, str)
                if pv_name in self.options.write_events:
                    bounds = self.options.limits.get(pv_name, None)
                    if bounds is not None:
                        low = bounds[0]
                        high = bounds[1]
                        if high is not None and value > high:
                            raise InterlockInternalError(f'PV ({pv_name}) change to ({value}), outside ({low}|{high})')
                        if low is not None and value < low:
                            raise InterlockInternalError(f'PV ({pv_name}) change to ({value}), outside ({low}|{high})')
                else:
                    raise Exception(f'PV ({pv_name}) encountered that was not declared')
        except Exception as ex:
            #if not isinstance(ex, InterlockInternalError):
            #    self.logger.error(f'Unexpected exception ({ex})')
            return {'result': False, 'ex': ex, 'reason': 'ex'}
        return {'result': True, 'ex': None, 'reason': None}


class DenyInterlockOptions(InterlockOptions):
    pass


class DenyInterlock(Interlock):
    def __init__(self, options: DenyInterlockOptions):
        self.logger = logging.getLogger(self.__class__.__name__)
        assert isinstance(options, DenyInterlockOptions)
        assert options.pv_list == options.write_events
        assert options.read_events is None
        super().__init__(options)

    def callback_read(self, trigger_pvs, data, timestamps):
        raise InterlockInternalError(f'Internal failure')

    def callback_write(self, trigger_pvs: list[str], data: dict[str, Any], timestamps):
        assert isinstance(data, dict) and all(isinstance(x, str) for x in data.keys())
        assert isinstance(trigger_pvs, list) and all(isinstance(x, str) for x in trigger_pvs)
        self.logger.debug(f'Interlock ({self.uuid}) write input_var_change_callback evaluation with {self.options} {data}')
        return {'result': False, 'ex': None, 'reason': None}


class RatelimitInterlockOptions(InterlockOptions):
    ilock_type: str = 'ratelimit'
    min_delay: NonNegativeFloat


class RatelimitInterlock(Interlock):
    def __init__(self, options: RatelimitInterlockOptions):
        self.logger = logging.getLogger(self.__class__.__name__)
        assert isinstance(options, RatelimitInterlockOptions)
        self.last_trigger_times: dict[str, float] = {}
        self.time_start = now = time.time()
        for pv_name in options.write_events:
            self.last_trigger_times[pv_name] = now
        super().__init__(options)

    def callback_read(self, trigger_pvs: list[str], data: dict[str, Any], timestamps):
        raise InterlockInternalError(f'Internal failure')

    def callback_write(self, trigger_pvs: dict[str, Any], data: dict[str, Any],
                       timestamps: dict[str, float]) -> dict:
        assert isinstance(data, dict)
        assert all(isinstance(x, str) for x in data.keys())
        assert isinstance(trigger_pvs, dict)
        assert all(isinstance(x, str) for x in trigger_pvs.keys())
        assert set(data.keys()) == set(self.options.pv_list)
        self.logger.debug(f'Interlock ({self.uuid}) write input_var_change_callback evaluation with {self.options} {data}')
        now = time.time()
        if self.time_start + self.options.min_delay < now:
            # allow
            self.time_start = now
            return {'result': True, 'ex': None, 'reason': None}
        else:
            return {'result': False, 'ex': None,
                    'reason': f'Rate throttled (delay {now-self.time_start}, require {self.options.min_delay})'}
