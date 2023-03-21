# mimics pymoo style
from typing import Tuple

import numpy as np


class Problem:
    def __init__(self, n_var, n_obj) -> None:
        self.n_var = n_var
        self.n_obj = n_obj


class Quadratic(Problem):
    name = 'Quadratic'
    _optimal_value = 0.0

    def __init__(self, n_var=2, scale=1.0, offset=0.2) -> None:
        super().__init__(n_var, n_obj=1)
        self.scale = scale
        self.offset = offset

    def _evaluate(self, x, *args, **kwargs):
        assert x.shape[1] == self.n_var
        # x = x[0,:]
        objective = self.scale * np.linalg.norm(x - self.offset, axis=1, keepdims=True) ** 2
        return objective

    def evaluate(self, x) -> Tuple[Tuple, Tuple]:
        assert x.shape[-1] == self.n_var
        size = x.shape[-1]
        return self._evaluate(x)
