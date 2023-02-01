import logging
import random
import time
from typing import Any, Callable, Optional

import numpy as np
from .pddevices import EngineDevice, GenericDevice, GenericDeviceOptions

from .devices import RealisticMagnet, StaticInputDevice
from ..controls.test_problems import Quadratic

logger = logging.getLogger(__name__)


class MockGeneratorEvents:
    def __init__(self, variables=None, objectives=None, constants=None, extra_vars=None,
                 evaluation_functions: dict[str, Callable] = None,
                 evaluation_variables: dict[str, list[str]] = None,
                 initial_values: dict[str, float] = None,
                 noise: float = None
                 ):
        assert variables is not None
        assert objectives is not None
        self.variables = variables or ['X0', 'X1']
        self.objectives = objectives or ['OBJ0']
        self.constants = constants if constants is not None else ['C:0', 'C:1']
        self.extra_vars = extra_vars if extra_vars is not None else ['ECHO:0', 'ECHO:1']

        self.models_dict: dict[str, Any] = {}
        self.devices_dict: dict[str, EngineDevice] = {}
        self.obj_idx_map = {o: i for i, o in enumerate(objectives)}
        self.noise = noise
        self.out_ext = ':AO'
        self.in_ext = ':AI'

        self.default_fun = lambda: Quadratic(n_var=len(variables))

        if evaluation_functions is None:
            evaluation_functions = {o: Quadratic(n_var=len(variables)) for o in objectives}
        assert isinstance(evaluation_functions, dict)
        self.evaluation_fuctions = evaluation_functions
        if evaluation_variables is None:
            evaluation_variables = {}
        assert isinstance(evaluation_variables, dict)
        self.evaluation_variables = evaluation_variables
        self.initial_values = initial_values if initial_values is not None else {}

        self.last_inputs: dict[str, Any] = {o: None for o in objectives}
        self.last_results: dict[str, Any] = {o: None for o in objectives}
        self.variables_devices = []
        self.objectives_devices = []
        self.base_names = {}

    def create(self, sim=None):
        logger.info(f'Vars: {self.variables}')
        logger.info(f'Objectives: {self.objectives}')
        logger.info(f'Constants: {self.constants}')

        t = 0.0

        def fixed_time():
            return t

        from pybeamtools.sim.core import SimulationEngine, SignalEngineOptions
        if sim is None:
            sim = SimulationEngine(SignalEngineOptions(time_function=fixed_time))
            sim.TRACE = True
        from pybeamtools.sim.pddevices import EchoDevice, EchoDeviceOptions, SignalContext
        ctx = SignalContext(se=sim)

        for i, el in enumerate(self.variables):
            ival = self.initial_values.get(el, 0.0)
            mag = RealisticMagnet(name=el, value=ival, low=-10.0, high=10.0, noise=self.noise,
                                  resolution=None, model='instant')

            g_out = self.general_variable_output_device(mag)
            g_in = self.general_variable_input_device(mag, self.callback)
            self.models_dict[el + self.in_ext] = mag
            self.models_dict[el + self.out_ext] = mag
            self.devices_dict[el + self.in_ext] = g_in
            self.devices_dict[el + self.out_ext] = g_out
            self.variables_devices.append(g_in)
            self.variables_devices.append(g_out)
            self.base_names[el + self.out_ext] = el
            self.base_names[el + self.in_ext] = el

        for i, el in enumerate(self.objectives):
            output = StaticInputDevice(name=el, value=1.0)
            g_obj = self.general_objective_device(output)
            self.models_dict[el] = output
            self.devices_dict[el] = g_obj
            self.objectives_devices.append(g_obj)

        constants_devices = []
        for i, c in enumerate(self.constants):
            e = EchoDevice(ctx, options=EchoDeviceOptions(name=c, data={c: 5 + i * 10}))
            constants_devices.append(e)

        extra_channels = []
        for i, c in enumerate(self.extra_vars):
            e = EchoDevice(ctx, options=EchoDeviceOptions(name=c, data={c: 5 + i * 10}))
            extra_channels.append(e)

        for dev in self.variables_devices:
            dev.ctx = ctx
            ctx.add_device(dev)
            # ctx.issue_update(dev.name)

        for dev in self.objectives_devices:
            dev.ctx = ctx
            ctx.add_device(dev)

        for dev in self.variables_devices + self.objectives_devices:
            ctx.issue_update(dev.name)

        return sim

    def get_objective_value(self, objective):
        fun = self.evaluation_fuctions.get(objective, self.default_fun())

        assert objective in self.objectives
        # gather inputs
        if objective in self.evaluation_variables:
            inputs_names = self.evaluation_variables[objective]
            inputs = np.array(
                    [self.models_dict[var + self.in_ext].read() for var in
                     inputs_names])
            logger.info(f'Computing {objective} from {inputs_names}')
        else:
            inputs = np.array(
                    [self.models_dict[var + self.in_ext].read() for var in self.variables])
            logger.info(f'Computing {objective} from {self.variables}')
        inputs = inputs[None, :]
        # assert inputs.shape == (1, len(self.variables))
        li = self.last_inputs[objective]
        if li is not None and np.array_equal(inputs, li):
            results = self.last_results[objective].copy()
        else:
            results = fun._evaluate(inputs)
            # assert results.shape == (1, len(self.objectives))
            self.last_inputs[objective] = inputs.copy()
            self.last_results[objective] = results
        val = results[0, 0]
        logger.info(f'Value of {objective} for {inputs} = {val}')
        return val

    def callback(self, device):
        for k in device.channel_map:
            device.ctx.issue_update(k)
            device.ctx.issue_update(self.base_names[k] + self.out_ext)
        for objective in self.objectives:
            if objective in self.evaluation_variables:
                if self.base_names[device.name] not in self.evaluation_variables[objective]:
                    continue
            model = self.models_dict[objective]
            model.write(self.get_objective_value(objective))
            self.devices_dict[objective].ctx.issue_update(objective)

    def general_variable_output_device(self, model: RealisticMagnet):
        el = model.name
        cn = el + self.out_ext
        value = {cn: model.read()}

        def update_fun(t_sched, t_run, dep_data, self):
            value[cn] = model.read()
            return value

        def read_fun(t_sched, t_run, channel_name, self):
            return value[cn]

        gopt = GenericDeviceOptions(name=cn, update_fun=update_fun, read_fun=read_fun,
                                    channel_map={cn: {}})
        g = GenericDevice(ctx=None, options=gopt)
        g._src = el
        return g

    def general_variable_input_device(self, model: RealisticMagnet, callback):
        el = model.name
        cn = el + self.in_ext
        value = {cn: model.setpoint}

        def update_fun(t_sched, t_run, dep_data, self):
            value[cn] = model.setpoint
            return value

        def read_fun(t_sched, t_run, channel_name, self):
            return value[cn]

        def write_fun(t_sched, t_run, value_dict, self):
            model.write(value_dict[cn])
            callback(self)

        gopt = GenericDeviceOptions(name=cn, update_fun=update_fun, read_fun=read_fun,
                                    write_fun=write_fun,
                                    channel_map={cn: {}})
        g = GenericDevice(ctx=None, options=gopt)
        g._src = el
        return g

    def general_objective_device(self, dev):
        el = dev.name
        value = {el: dev.read()}

        def update_fun(t_sched, t_run, dep_data, self):
            value[el] = dev.read()
            return value.copy()

        def read_fun(t_sched, t_run, channel_name, self):
            return value[el]

        gopt = GenericDeviceOptions(name=el,
                                    update_fun=update_fun,
                                    read_fun=read_fun,
                                    channel_map={el: {}})
        g = GenericDevice(ctx=None, options=gopt)
        g._src = el
        return g
