import logging

from caproto import CaprotoRuntimeError

from sim.devices import VirtualDevice
from caproto.server import PVGroup, SubGroup, pvproperty

logger = logging.getLogger(__name__)


class AdaptivePVGroup(PVGroup):
    def update_pvs(self):
        bases = self.__class__.__bases__
        dct = self.__dict__

        # name = self.__class__.__name__
        # cls = self

        def find_subgroups(dct):
            for attr, value in dct.items():
                if attr.startswith('_'):
                    continue
                if isinstance(value, SubGroup):
                    yield attr, value

        def find_pvproperties(dct):
            for attr, value in dct.items():
                if attr.startswith('_'):
                    continue
                if isinstance(value, pvproperty):
                    yield attr, value
                elif isinstance(value, SubGroup):
                    subgroup_cls = value.group_cls
                    if subgroup_cls is None:
                        raise CaprotoRuntimeError('Internal error; subgroup class unset?')
                    for sub_attr, value in subgroup_cls._pvs_.items():
                        yield '.'.join([attr, sub_attr]), value

        dct['_subgroups_'] = subgroups = {}
        dct['_pvs_'] = pvs = {}

        # Propagate any subgroups/PVs from base classes
        for base in bases:
            if hasattr(base, '_subgroups_'):
                dct['_subgroups_'].update(**base._subgroups_)
            if hasattr(base, '_pvs_'):
                dct['_pvs_'].update(**base._pvs_)

        for attr, prop in find_subgroups(dct):
            subgroups[attr] = prop

            # TODO a bit messy
            # propagate subgroups-of-subgroups to the top
            subgroup_cls = prop.group_cls
            if hasattr(subgroup_cls, '_subgroups_'):
                for subattr, subgroup in subgroup_cls._subgroups_.items():
                    subgroups['.'.join((attr, subattr))] = subgroup

        pvs.update(find_pvproperties(dct))
        # for attr, subgroup in self._subgroups_.items():
        #     print(attr, subgroup.prefix, subgroup.attr_name)


class EPICSVirtualGenericTrigger(PVGroup):
    counter = pvproperty(value=0, doc='simulation counter')

    def __init__(self, controller):
        self.controller = controller

    @counter.putter
    async def counter_putter(self, instance, value):
        print(f'counter_putter: {value=} {instance.value=}')
        if value > instance.value:
            print(f'counter_putter: calling controller')
            self.controller.trigger(value)
            return value
        else:
            print(f'counter_putter: not doing anything')


async def ai_getter(group, instance):
    value = group.device.read()
    logger.info(f'ai_getter {instance.pvname}: {value=}')
    return value

class EPICSVirtualInput(AdaptivePVGroup):
    ai = pvproperty(
        record='ai',
        name=':AI',
        value=0.0,
        dtype=float,
        read_only=True,
        doc="ai",
        get=ai_getter,
        )

    def __init__(self, device, input_name, *args, **kwargs):
        logger.info(f'Virtual input called with {args=} {kwargs=}')
        super().__init__(*args, **kwargs)
        self.device = device
        self.input_name = input_name
        ai = pvproperty(
            record='ai',
            name=input_name,
            value=0.0,
            dtype=float,
            read_only=True,
            doc="ai",
            get=ai_getter,
        )
        self.ai = ai
        self.update_pvs()
        self._create_pvdb()


class EPICSVirtualIOC(AdaptivePVGroup):
    async def ai_read(self, instance):
        readback = self.model.read()
        await self.ai.write(value=readback)
        print(f'ai_read: {readback=}')

    ai = pvproperty(
        record='ai',
        name=':AI',
        value=0.0,
        dtype=float,
        read_only=True,
        doc="ai",
        get=ai_read
    )

    async def ao_put(self, instance, value):
        # logger.info(f'ao_put: {instance=} {value=}')
        result = self.model.write(value)
        if result:
            logger.info(f'ao_put {instance.pvname}: {value=} setting ok')
            return value
            # await instance.write(value)
        else:
            logger.info(f'ao_put {instance.pvname}: {value=} setting failed')
            raise Exception
        # value = await self._read()
        # await self.ao.write(value=value)
        # return value

    async def ao_startup(self, instance, async_lib):
        print(f'ao_startup: {instance=} {async_lib=}')
        # instance.low_operating_range = self.model.low
        # instance.upper_alarm_limit = self.model.high
        # instance.high_operating_range = self.model.high

    ao = pvproperty(
        record='ao',
        name=':AO',
        value=0.0,
        dtype=float,
        doc="ao",
        put=ao_put,
        startup=ao_startup
    )

    def __init__(self, device: VirtualDevice, input_name, output_name, *args, **kwargs):
        self.have_new_setpoint = False
        self.model = device
        self.input_name = input_name
        self.output_name = output_name
        super().__init__(*args, **kwargs)

        # async def value_write_hook(fields, value):
        #    print(f'Value hook triggered with {fields=} {value=}')
        #    self.have_new_setpoint = True

        # ao_fields = self.ao.field_inst
        # ao_fields.value_write_hook = value_write_hook

    async def startup(self, instance, async_lib):
        print('startup')
        self.async_lib = async_lib
        await self.ao.fields.lower_ctrl_limit.write(self.model.low)
        await self.ao.fields.upper_ctrl_limit.write(self.model.high)


# class VirtualBeamline(PVGroup):
#     pass
