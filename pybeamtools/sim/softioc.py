import asyncio
import logging
from threading import Thread
from typing import Optional

import nest_asyncio
import numpy as np
from caproto.asyncio.server import run
from caproto.server import SubGroup

from pybeamtools.controls.accelerator import SimController
from sim.devices import RealisticMagnet, StaticInputDevice
from pybeamtools.controls.test_problems import Quadratic
from pybeamtools.controls.virtual_tools import EPICSVirtualInput, AdaptivePVGroup, EPICSVirtualIOC

logger = logging.getLogger(__name__)

class SimpleBeamlineSoftIOC:
    def __init__(self, variables, objectives, test_variables=None, prefix='AI:'):
        self.prefix = prefix
        self.variables = variables
        self.objectives = objectives
        self.test_variables = test_variables
        self.obj_idx_map = {o:i for i,o in enumerate(objectives)}

    def setup(self):
        controller = SimController(self.variables, self.objectives)

        def eval_fn(name):
            return controller.read(name)

        class VirtualBeamline(AdaptivePVGroup):
            pass
            #def __new__(cls, *args, **kwargs):
            #    super().__new__(cls, *args, **kwargs)

        bl = VirtualBeamline(prefix=self.prefix)

        for i, el in enumerate(self.variables):
            mag = RealisticMagnet(value=0, low=-2, high=2, noise=None, resolution=None, model='instant')
            mag_grp = SubGroup(EPICSVirtualIOC, device=mag, input_name=el+':AI', output_name=el+':AO', prefix=el)
            setattr(bl, f'variable_{i}', mag_grp)

        for i, el_name in enumerate(self.objectives):
            output = StaticInputDevice(value=1.0)
            obj_grp = SubGroup(EPICSVirtualInput, device=output, input_name=el_name, prefix=el_name)
            setattr(bl, f'objective_{i}', obj_grp)

        # for i, (el1, el2) in enumerate(self.test_variables):
        #     el = StaticInputDevice(value=1.0)
        #     el_grp = SubGroup(EPICSVirtualIOC, device=el, input_name=el2, output_name=el1)
        #     setattr(bl, f'testvariable_{i}', el_grp)

        bl.update_pvs()
        bl._create_pvdb()
        logger.info(f'Soft IOC config:')
        logger.info(f'Vars: {self.variables}')
        logger.info(f'Objectives: {self.objectives}')
        logger.info(f'Test vars: {self.test_variables}')
        logger.info(f'PVDict: {bl.__dict__}')
        logger.info(f'PVDB: {bl.pvdb}')

        problem = Quadratic(n_var=len(self.variables))

        last_inputs: Optional[np.ndarray] = None
        last_results: Optional[np.ndarray] = None

        def get_objectives(obj):
            # print('getobj1')
            nonlocal last_results, last_inputs
            assert obj in self.objectives
            # gather inputs
            inputs = np.array([bl.pvdb[var].value for var in self.variables])
            inputs = inputs[None, :]
            assert inputs.shape == (1, len(self.variables))
            if last_inputs is not None and np.array_equal(inputs, last_inputs):
                results = last_results.copy()
            else:
                results = problem._evaluate(inputs)
                # print(results)
                assert results.shape == (1, len(self.objectives))
                last_inputs = inputs.copy()
                last_results = results
            val = results[0, self.obj_idx_map[obj]]
            logger.info(f'Requested value of {obj} @ {inputs} = {val}')
            return val

        controller.eval_fn = get_objectives

        self.bl = bl
        self.controller = controller

    def run(self):
        logger.info('Starting repeater')
        #repeater.spawn_repeater()
        nest_asyncio.apply()
        logger.info('Starting loop')
        run(self.bl.pvdb, log_pv_names=True, interfaces=['0.0.0.0'])

    def run_in_background(self,daemon=True):
        def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
            asyncio.set_event_loop(loop)
            logger.info('Starting loop in separate thread')
            run(self.bl.pvdb, log_pv_names=True, interfaces=['127.0.0.1'])#
            #loop.run_forever()
        logger.info('Starting repeater')
        #repeater.spawn_repeater()
        loop = asyncio.new_event_loop()
        t = Thread(daemon=daemon, target=start_background_loop, args=(loop,))
        t.start()



