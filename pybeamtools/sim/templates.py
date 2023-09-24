import logging
import time
from typing import Any, Callable

import numpy as np

from .devices import RealisticMagnet, RealisticModel, RealisticModelOptions, StaticInputDevice
from .pddevices import EngineDevice, GenericDevice, GenericDeviceOptions, ModelPairDevice, \
    ModelPairDeviceOptions, TRIG
from ..controls.test_problems import Quadratic

logger = logging.getLogger(__name__)


class MockSetupPairDevice:
    def __init__(self,
                 variables: list[str] = None,
                 objectives: list[str] = None,
                 constraints: list[str] = None,
                 readbacks: list[str] = None,
                 constants: list[str] = None,
                 extra_vars: list[str] = None,
                 variables_initial_values: dict[str, float] = None,
                 evaluation_functions: dict[str, Callable] = None,
                 evaluation_variables: dict[str, list[str]] = None,
                 noise: float = None,
                 variable_model_kwargs=None,
                 scan_period_rb: float = 0.0,
                 scan_period_obj: float = 0.0,
                 scan_period_extra: float = 0.0,
                 realtime=False
                 ):
        assert variables is not None
        assert objectives is not None
        self.variables = variables
        self.variables_initial_values = variables_initial_values or {}
        if not set(self.variables_initial_values).issubset(set(self.variables)):
            raise ValueError(f'Bad initial values {self.variables_initial_values}')
        self.readbacks = readbacks
        self.objectives = objectives
        self.constraints = constraints if constraints is not None else []
        self.constants = constants if constants is not None else []
        self.extra_vars = extra_vars if extra_vars is not None else []
        self.models_dict: dict[str, Any] = {}
        self.devices_dict: dict[str, EngineDevice] = {}
        self.obj_idx_map = {o: i for i, o in enumerate(objectives)}
        self.noise = noise
        self.default_fun = lambda: Quadratic(n_var=len(variables))

        evaluation_functions = evaluation_functions or {}
        for o in objectives:
            if o not in evaluation_functions:
                evaluation_functions[o] = Quadratic(n_var=len(variables))
        for el in constraints:
            if el not in evaluation_functions:
                evaluation_functions[o] = Quadratic(n_var=len(variables), offset=-2.0)
        assert isinstance(evaluation_functions, dict)
        self.evaluation_fuctions = evaluation_functions

        evaluation_variables = evaluation_variables or {}
        assert isinstance(evaluation_variables, dict)
        for el in objectives + constraints:
            if el not in evaluation_variables:
                evaluation_variables[el] = variables.copy()
        self.evaluation_variables = evaluation_variables

        self.last_inputs: dict[str, Any] = {o: None for o in objectives}
        self.last_results: dict[str, Any] = {o: None for o in objectives}
        self.variables_devices: list[EngineDevice] = []
        self.objectives_devices: list[EngineDevice] = []
        self.constraints_devices: list[EngineDevice] = []
        self.base_names = {}

        self.variable_model_kwargs = variable_model_kwargs or {}
        self.realtime = realtime
        self.scan_period_rb = scan_period_rb
        self.scan_period_obj = scan_period_obj
        self.scan_period_extra = scan_period_extra
        self.sim = None

    def create(self, sim=None):
        logger.info(f'Vars: {self.variables}')
        logger.info(f'Readbacks: {self.readbacks}')
        logger.info(f'Objectives: {self.objectives}')
        logger.info(f'Constraints: {self.constraints}')
        logger.info(f'Constants: {self.constants}')
        logger.info(f'EVars: {self.evaluation_variables}')

        from pybeamtools.sim.core import SimulationEngine, SignalEngineOptions
        from pybeamtools.sim.pddevices import EchoDevice, EchoDeviceOptions, SignalContext
        if sim is None:
            if self.realtime:
                t = time.time()

                def fixed_time():
                    return time.time()
            else:
                t = 0.0

                def fixed_time():
                    return t

            sim = SimulationEngine(SignalEngineOptions(time_function=fixed_time))
            sim.TRACE = True
        else:
            pass
            # t = sim.time()
        self.ctx = ctx = SignalContext(se=sim)
        self.sim = sim

        model_kwargs = dict(readback_update_rate=0.0)
        model_kwargs.update(self.variable_model_kwargs)
        for i, el in enumerate(self.variables):
            ival = self.variables_initial_values.get(el, 0.0)
            magmodel = RealisticModel(RealisticModelOptions(name='magmodel',
                                                            value=ival,
                                                            noise=self.noise,
                                                            **model_kwargs), sim.time())
            mag = ModelPairDevice(ModelPairDeviceOptions(name=f'DEV:{el}',
                                                         variable_name=self.variables[i],
                                                         readback_name=self.readbacks[i],
                                                         device=magmodel,
                                                         scan_period=self.scan_period_rb,
                                                         ))
            self.models_dict[el] = magmodel
            self.devices_dict[el] = mag
            self.variables_devices.append(mag)

        for i, el in enumerate(self.objectives):
            output = StaticInputDevice(name=el, value=1.0)
            g_obj = self.general_objective_device(el)
            self.models_dict[el] = output
            self.devices_dict[el] = g_obj
            self.objectives_devices.append(g_obj)

        for i, el in enumerate(self.constraints):
            output = StaticInputDevice(name=el, value=1.3)
            g_obj = self.general_objective_device(el)
            self.models_dict[el] = output
            self.devices_dict[el] = g_obj
            self.constraints_devices.append(g_obj)

        constants_devices = []
        for i, c in enumerate(self.constants):
            e = EchoDevice(EchoDeviceOptions(name=c, data={c: 5.0 + i * 10},
                                             scan_period=self.scan_period_extra))
            constants_devices.append(e)

        extra_channels = []
        for i, c in enumerate(self.extra_vars):
            e = EchoDevice(EchoDeviceOptions(name=c, data={c: 5.0 + i * 10},
                                             scan_period=self.scan_period_extra))
            extra_channels.append(e)

        for dev in self.variables_devices:
            sim.add_device(dev)

        for dev in self.objectives_devices:
            sim.add_device(dev)

        for dev in self.constraints_devices:
            sim.add_device(dev)

        for dev in constants_devices:
            sim.add_device(dev)

        for dev in extra_channels:
            sim.add_device(dev)

        for dev in self.variables_devices + self.objectives_devices + self.constraints_devices + \
                extra_channels + \
                   constants_devices:
            sim.enable_device(dev)

        return sim

    # def make_scan_thread(self, sim):
    #     logger.info(f'Making scan thread')
    #     if self.realtime:
    #         def time_thread():
    #             logger.debug(f'Scan start at {time.time()}')
    #             # for i in range(100):
    #             while True:
    #                 sim.process_events()
    #                 sim.scan_until(time.time())
    #                 time.sleep(0.2)
    #                 # logger.debug(f'Scan step {i}')
    #
    #         th = threading.Thread(target=time_thread, name='time_thread')
    #         th.daemon = True
    #         # th.start()
    #         return th
    #         # start_time_scan()

    def get_objective_value(self, objective: str, overrides: dict[str, float] = None):
        overrides = overrides or {}
        fun = self.evaluation_fuctions.get(objective, self.default_fun())

        assert objective in self.objectives or objective in self.constraints
        # gather inputs
        inputs_names = self.evaluation_variables[objective]
        inputs = []
        for var in inputs_names:
            if var in overrides:
                inputs.append(overrides[var])
            else:
                inputs.append(self.models_dict[var].value)
        inputs = np.array(inputs)
        inputs = inputs[None, :]
        assert inputs.shape == (1, len(self.variables))
        logger.info(f'Computing {objective} from {inputs_names}={inputs}')

        results, _ = fun.evaluate(inputs)
        #assert results.shape == (1, len(self.objectives)), f'{results=}'
        assert results.shape == (1, 1), f'{results=}'
        self.last_inputs[objective] = inputs.copy()
        self.last_results[objective] = results
        val = results[0, 0]
        if self.noise is not None and self.noise != 0.0:
            noise = np.random.normal(0, self.noise, 1)
            val += float(noise)

        logger.info(f'Value of {objective} for {inputs} = {val}')
        return val

    def general_objective_device(self, objective):
        value = {objective: None}
        latest_data = {}
        last_update_list = [0.0]

        def update_fun(ev, aux_data, device):
            assert set(aux_data).issubset(set(self.evaluation_variables[objective]))
            latest_data.update(aux_data)
            model = self.models_dict[objective]
            model_value = self.get_objective_value(objective, overrides=latest_data)
            if self.sim.TRACE:
                logger.debug(f'New data ({aux_data}) -> {objective}={model_value}')
            model.write(model_value)
            # self.devices_dict[objective].update(None, None)
            # self.devices_dict[objective].issue_full_update()
            value[objective] = model_value
            ret = value
            # ret = {}
            # if last_update_list - time.time() > 1.0:
            #    ret = value
            #    last_update_list = time.time()
            return ret

        def read_fun(ev, channel_name, device):
            assert channel_name == objective
            return value[objective]

        def scan_fun(ev, device):
            model = self.models_dict[objective]
            v = model.read()
            value[objective] = v
            if self.sim.TRACE:
                logger.debug(f'New scan {objective}={v}')
            return value

        dep_map = {var: TRIG.PROPAGATE for var in self.evaluation_variables[objective]}

        gopt = GenericDeviceOptions(name=f'DEV:{objective}',
                                    update_fun=update_fun,
                                    read_fun=read_fun,
                                    scan_fun=scan_fun,
                                    channel_map={objective: dep_map},
                                    scan_period=self.scan_period_obj)
        g = GenericDevice(gopt)
        return g


class MockGeneratorEvents:
    def __init__(self,
                 variables: list[str] = None,
                 readbacks: list[str] = None,
                 objectives: list[str] = None,
                 constants=None,
                 extra_vars=None,
                 variable_initial_values: dict[str, float] = None,
                 evaluation_functions: dict[str, Callable] = None,
                 evaluation_variables: dict[str, list[str]] = None,
                 noise: float = None,
                 trace: bool = False
                 ):
        self.TRACE = trace
        assert variables is not None
        assert objectives is not None
        self.variables = variables  # or ['X0', 'X1']
        self.variable_initial_values = variable_initial_values or {}
        self.readbacks = readbacks
        self.objectives = objectives  # or ['OBJ0']
        self.constants = constants if constants is not None else []  # ['C:0', 'C:1']
        self.extra_vars = extra_vars if extra_vars is not None else []  # ['ECHO:0', 'ECHO:1']

        self.models_dict: dict[str, Any] = {}
        self.devices_dict: dict[str, EngineDevice] = {}
        self.obj_idx_map = {o: i for i, o in enumerate(objectives)}
        self.noise = noise
        # self.in_ext = ''  #:AI
        # self.out_ext = ':AO'

        self.default_fun = lambda: Quadratic(n_var=len(variables))

        if evaluation_functions is None:
            evaluation_functions = {o: Quadratic(n_var=len(variables)) for o in objectives}
        assert isinstance(evaluation_functions, dict)
        self.evaluation_fuctions = evaluation_functions
        if evaluation_variables is None:
            evaluation_variables = {}
        assert isinstance(evaluation_variables, dict)
        self.evaluation_variables = evaluation_variables

        self.last_inputs: dict[str, Any] = {o: None for o in objectives}
        self.last_results: dict[str, Any] = {o: None for o in objectives}
        self.variables_devices: list[EngineDevice] = []
        self.objectives_devices: list[EngineDevice] = []
        self.base_names = {}
        self.pair_device = {}

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
        from pybeamtools.sim.pddevices import EchoDevice, EchoDeviceOptions

        for i, el in enumerate(self.variables):
            ival = self.variable_initial_values.get(el, 0.0)
            mag = RealisticMagnet(name=el, value=ival, low=-10.0, high=10.0, noise=self.noise,
                                  resolution=None, model='instant')
            g_in = self.general_variable_input_device(el, mag, self.input_var_change_callback)
            self.models_dict[el] = mag
            self.devices_dict[el] = g_in
            self.variables_devices.append(g_in)
            self.base_names[el] = el
            if self.readbacks is not None and self.readbacks[i] is not None:
                rb = self.readbacks[i]
                g_out = self.general_variable_output_device(rb, mag)
                self.models_dict[rb] = mag
                self.devices_dict[rb] = g_out
                self.variables_devices.append(g_out)
                self.base_names[rb] = el
                self.pair_device[g_in] = g_out
            else:
                self.pair_device[g_in] = None

        for i, el in enumerate(self.objectives):
            output = StaticInputDevice(name=el, value=0.0)
            g_obj = self.general_objective_device(output)
            self.models_dict[el] = output
            self.devices_dict[el] = g_obj
            self.objectives_devices.append(g_obj)

        constants_devices = []
        for i, c in enumerate(self.constants):
            e = EchoDevice(EchoDeviceOptions(name=c, data={c: 5 + i * 10}))
            constants_devices.append(e)

        extra_channels = []
        for i, c in enumerate(self.extra_vars):
            e = EchoDevice(EchoDeviceOptions(name=c, data={c: 5 + i * 10}))
            extra_channels.append(e)

        for dev in self.variables_devices:
            sim.add_device(dev)
            # ctx.issue_update(dev.name)

        for dev in self.objectives_devices:
            sim.add_device(dev)

        for dev in self.variables_devices + self.objectives_devices:
            sim.enable_device(dev)

        return sim

    def get_objective_value(self, objective, overrides: dict[str, float] = None):
        overrides = overrides or {}
        fun = self.evaluation_fuctions.get(objective, self.default_fun())

        assert objective in self.objectives
        # gather inputs
        if objective in self.evaluation_variables:
            inputs_names = self.evaluation_variables[objective]
            inputs = []
            for var in inputs_names:
                full_var_name = var
                if full_var_name in overrides:
                    inputs.append(overrides[full_var_name])
                else:
                    inputs.append(self.models_dict[var].read())
            inputs = np.array(inputs)
            if self.TRACE:
                logger.info(f'Computing {objective} from {inputs_names}')
        else:
            inputs = np.array(
                    [self.models_dict[var].read() for var in self.variables])
            if self.TRACE:
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

    # def input_var_change_callback(self, device):
    #     # for k in device.channel_map:
    #     device.issue_full_update()
    #     self.pair_device[device].issue_full_update()
    #     # device.ctx.issue_update(k)
    #     # device.ctx.issue_update(self.base_names[k] + self.out_ext)
    #     for objective in self.objectives:
    #         if objective in self.evaluation_variables:
    #             if self.base_names[device.name] not in self.evaluation_variables[objective]:
    #                 continue
    #         model = self.models_dict[objective]
    #         model.write(self.get_objective_value(objective))
    #         # self.devices_dict[objective].ctx.issue_update(objective)
    #         self.devices_dict[objective].update(None, None)
    #         self.devices_dict[objective].issue_full_update()

    def input_var_change_callback(self, device):
        device.issue_full_update()
        pair = self.pair_device[device]
        if pair is not None:
            self.pair_device[device].update(None, {})
            self.pair_device[device].issue_full_update()
        for objective in self.objectives:
            if objective in self.evaluation_variables:
                if self.base_names[device.name] not in self.evaluation_variables[objective]:
                    continue
            model = self.models_dict[objective]
            model_value = self.get_objective_value(objective)
            logger.debug(f'Writing {model}={model_value}')
            model.write(model_value)
            self.devices_dict[objective].update(None, {})
            self.devices_dict[objective].issue_full_update()

    def general_variable_output_device(self, cn, model: RealisticMagnet):
        value = {cn: model.read()}

        def update_fun(ev, dep_data, self):
            value[cn] = model.read()
            return value

        def read_fun(ev, channel_name, self):
            return value[cn]

        gopt = GenericDeviceOptions(name=cn, update_fun=update_fun, read_fun=read_fun,
                                    channel_map={cn: {}})
        g = GenericDevice(gopt)
        g._src = cn
        return g

    def general_variable_input_device(self, cn, model: RealisticMagnet, callback):
        value = {cn: model.setpoint}

        def update_fun(ev, dep_data, self):
            value[cn] = model.setpoint
            return value

        def read_fun(ev, channel_name, self):
            return value[cn]

        def write_fun(ev, value_dict, aux_dict, dself):
            model.write(value_dict[cn])
            value[cn] = model.setpoint
            callback(dself)
            # device = dself
            # device.issue_full_update()
            # self.pair_device[device].issue_full_update()
            # for objective in self.objectives:
            #     if objective in self.evaluation_variables:
            #         if self.base_names[device.name] not in self.evaluation_variables[objective]:
            #             continue
            #     dmodel = self.models_dict[objective]
            #     dmodel.write(self.get_objective_value(objective))
            #     self.devices_dict[objective].issue_full_update()

        gopt = GenericDeviceOptions(name=cn, update_fun=update_fun, read_fun=read_fun,
                                    write_fun=write_fun,
                                    channel_map={cn: {}})
        g = GenericDevice(gopt)
        g._src = cn  # el
        return g

    def general_objective_device(self, model):
        el = model.name
        value = {el: model.read()}

        def update_fun(ev, dep_data, self):
            value[el] = model.read()
            return value.copy()

        def read_fun(ev, channel_name, self):
            return value[el]

        gopt = GenericDeviceOptions(name=el,
                                    update_fun=update_fun,
                                    read_fun=read_fun,
                                    channel_map={el: {}})
        g = GenericDevice(gopt)
        g._src = el
        return g

# def make_sioc(channels: list[str], channels_to_mo)
