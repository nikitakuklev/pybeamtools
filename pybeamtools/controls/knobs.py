import pandas as pd
from pydantic import BaseModel

from ..utils.pydantic import CallableModel, PBClass


def add_dicts(d1, d2):
    # combine dicts, adding values if both have the key
    d = d1.copy()
    for k, v in d2.items():
        if k in d:
            d[k] += v
        else:
            d[k] = v
    return d


def multiply_dict(d, m):
    return {k: v * m for k, v in d.items()}


class Group:
    def __init__(self, name: str, channel_coefficients: dict[str, float]):
        """
        Group is a collection of channels and their coefficients that can be used in multiple knobs
        :param name:
        :param channel_coefficients:
        """
        for k, v in channel_coefficients.items():
            assert isinstance(k, str)
            assert isinstance(v, (float, int))
        self.name = name
        self.channel_coefficients = channel_coefficients

    def __eq__(self, other):
        return self.name == other.name and self.channel_coefficients == other.channel_coefficients

    def __hash__(self):
        return hash(self.name) + hash(frozenset(self.channel_coefficients.items()))

    def __repr__(self):
        return f'Group [{self.name}] ({self.channel_coefficients})'


class Knob:
    # A mapping that represents a set of groups and their coefficients
    def __init__(self, name: str, group_coefficients: dict[Group, float]):
        assert all(isinstance(k, Group) for k in group_coefficients.keys())
        self.name: str = name
        self.group_coefficients: dict[Group, float] = group_coefficients

    def __eq__(self, other):
        return self.name == other.name and self.group_coefficients == other.group_coefficients

    def __hash__(self):
        return hash(self.name) + hash(frozenset(self.group_coefficients.items()))

    @property
    def groups(self):
        return list(self.group_coefficients.keys())

    def get_channel_coefficients(self):
        data = {}
        for g, c in self.group_coefficients.items():
            print(self.name, g, c, g.channel_coefficients)
            if c == 0:
                continue
            data = add_dicts(data, multiply_dict(g.channel_coefficients, c))
        return data


class KnobManager:
    def __init__(self, knobs_map: dict[str, Knob] = None, groups_map: dict[str, Group] = None):
        self.knobs_map: dict[str, Knob] = knobs_map or {}
        self.groups_map: dict[str, Group] = groups_map or {}
        self.validate()

    @property
    def group_names(self) -> list[str]:
        return list(self.groups_map.keys())

    @property
    def knob_names(self) -> list[str]:
        return list(self.knobs_map.keys())

    @property
    def groups(self) -> list[Group]:
        return list(self.groups_map.values())

    @property
    def knobs(self) -> list[Knob]:
        return list(self.knobs_map.values())

    @property
    def knobs_matrix(self) -> pd.DataFrame:
        # Make a matrix of knob coefficients (groups as rows, knobs as columns)
        data = {}
        for k, v in self.knobs_map.items():
            data[k] = v.group_coefficients
        all_keys = set()
        all_keys = all_keys.union(*[v.keys() for v in data.values()])
        for k, v in data.items():
            for ak in all_keys:
                if ak not in v:
                    v[ak] = 0.0
        return pd.DataFrame(data)

    @property
    def knobs_matrix_str(self) -> pd.DataFrame:
        kb = self.knobs_matrix
        kb.index = [g.name for g in kb.index]
        return kb

    @property
    def groups_matrix(self) -> pd.DataFrame:
        data = {}
        for k, v in self.groups_map.items():
            data[k] = v.channel_coefficients
        all_keys = set()
        all_keys = all_keys.union(*[v.keys() for v in data.values()])
        for k, v in data.items():
            for ak in all_keys:
                if ak not in v:
                    v[ak] = 0.0
        return pd.DataFrame(data)

    def validate(self):
        """ Validate current group and knob mappings for consistency """
        gnames = self.group_names
        for k in self.knobs:
            for g in k.groups:
                if g.name not in gnames:
                    raise Exception(f'Knob {k} has undefined group {g}')

    def add_group(self, group: Group):
        self.groups_map[group.name] = group

    def add_knob(self, knob: Knob):
        gnames = set(self.group_names)
        for g in knob.groups:
            if g.name not in gnames:
                self.add_group(g)
            else:
                if g not in self.groups_map.values():
                    raise Exception(f'Group {g} has duplicate name')

        self.knobs_map[knob.name] = knob

    def compute_channels(self, knob_values: dict[str, float]) -> dict[str, float]:
        assert all(k in self.knobs_map for k in knob_values.keys()), 'Knobs not found'
        data = {}
        for k, v in knob_values.items():
            knob = self.knobs_map[k]
            #print(k, v, knob.get_channel_coefficients())
            if v == 0:
                continue
            data = add_dicts(data, multiply_dict(knob.get_channel_coefficients(), v))
        return data

# def make_knob_groups(groups: dict[str, list[str]], knob_matrix: pd.DataFrame, postfix=''):
#     """ Take groups dict and knob dataframe, make knob groups """
#     assert len(groups) == knob_matrix.shape[0]
#
#     knob_groups = {}
#     for c in knob_matrix.columns:
#         data = {}
#         for g, sextupoles in groups.items():
#             for s in sextupoles:
#                 data[s + postfix] = knob_matrix.loc[g, c]
#         knob_groups[c] = data
#     return knob_groups
#
#
# def knob_strengths_to_group_strengths(knob_matrix: pd.DataFrame, knob_dict: dict[str, float]):
#     """ Take knob dataframe, output per-family strengths """
#     assert len(knob_dict) == knob_matrix.shape[1]
#
#     data = {k: 0.0 for k in knob_matrix.index}
#     for c in knob_matrix.columns:
#         for g in knob_matrix.index:
#             data[g] += knob_matrix.loc[g, c] * knob_dict[c]
#     return data

# class KnobOptions(BaseModel):
#     write_pv_name: str
#     readback_pv_name: str
#     # standard equality will be used if not
#     tolerance_fun: CallableModel = None
#
#
# class Knob(PBClass):
#     __options_class__ = KnobOptions
#
#     def __init__(self, options: KnobOptions = None, **kwargs):
#         if options is not None:
#             self.options = options
#         else:
#             extras = self.__set_options(**kwargs)
#             self.data = extras
