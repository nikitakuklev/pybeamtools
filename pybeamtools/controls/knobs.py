import inspect

from pydantic import BaseModel, create_model
from ..utils.pydantic import CallableModel, PBClass


class KnobOptions(BaseModel):
    write_pv_name: str
    readback_pv_name: str
    # standard equality will be used if not
    tolerance_fun: CallableModel = None





class Knob(PBClass):
    __options_class__ = KnobOptions

    def __init__(self, options: KnobOptions = None, **kwargs):
        if options is not None:
            self.options = options
        else:
            extras = self.__set_options(**kwargs)
            self.data = extras


class KnobManager:
    def __init__(self):
        self.io_map = {}
        self.oi_map = {}
        self.knobs = []
        self.knobs_map_write = {}
        self.knobs_map_readback = {}

    def get_df(self):
        pass
        # for k in knobs:
        #     if self.df is None:
        #     df = pd.DataFrame(index=self.knobs.keys(), data=self.knobs.values())
        #     else:
        #     dft = pd.DataFrame(index=[write_pv_name], data=[data])
        #     self.df = pd.concat([self.df, dft])
