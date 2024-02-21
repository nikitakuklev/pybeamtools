import copy
import inspect
import logging
import typing
from typing import Optional, Type, Dict, Tuple, Any

from caproto import CaprotoRuntimeError, CaprotoTypeError, CaprotoValueError, ChannelData
from caproto.server import PVGroup, SubGroup, pvproperty
from caproto.server.server import T_PVGroup, T_SubGroup, PvpropertyData, PVSpec, NestedPvproperty

from ..sim.models import VirtualDevice

logger = logging.getLogger(__name__)


# class SubGroup(typing.Generic[T_PVGroup]):
#     """
#     A property-like descriptor for specifying a subgroup in a PVGroup.
#
#     Several methods of generating a SubGroup are possible. For the `group`
#     parameter, one can
#     1. Pass in a group_dict of {attr: pvspec_or_dict}
#     2. Pass in an existing PVGroup class
#     3. Use @SubGroup as a decorator on a subsequently-defined PVGroup class
#     """
#
#     # support copy.copy by keeping this here
#     _class_dict = None
#
#     _group_dict: Optional[Dict[str, ChannelData]]
#     attr_separator: Optional[str]
#     base: Tuple[Type, ...]
#     group_cls: Optional[Type[T_PVGroup]]
#     init_kwargs: Dict[str, Any]
#     macros: Dict[str, str]
#     prefix: Optional[str]
#
#     def __init__(
#         self,
#         group: Optional[Type[T_PVGroup]] = None,
#         *,
#         prefix: Optional[str] = None,
#         macros: Optional[Dict[str, str]] = None,
#         attr_separator: Optional[str] = None,
#         doc: Optional[str] = None,
#         base: Optional[Tuple[Type, ...]] = None,
#         **init_kwargs
#     ):
#         self.attr_name = None  # to be set later
#
#         # group_dict is passed in -> generate class_dict -> generate group_cls
#         self._group_dict = None
#         self._decorated_items = None
#         self.group_cls = None
#         self.prefix = prefix
#         self.macros = macros if macros is not None else {}
#         if not hasattr(self, 'attr_separator') or attr_separator is not None:
#             self.attr_separator = attr_separator
#         self.base = (PVGroup, ) if base is None else base
#         self.__doc__ = doc
#         self.init_kwargs = init_kwargs
#         # Set last with setter
#         self.group = group
#
#     @property
#     def group(self) -> Tuple[Dict[str, PvpropertyData], Type[T_PVGroup]]:
#         'Property handling either group dict or group class'
#         return (self.group_dict, self.group_cls)
#
#     @group.setter
#     def group(self, group):
#         if isinstance(group, dict):
#             # set the group dictionary last:
#             self.group_dict = group
#         elif group is not None:
#             assert inspect.isclass(group), 'Group should be dict or SubGroup'
#             assert issubclass(group, PVGroup)
#             self.group_cls = group
#         else:
#             self.group_dict = None
#             self.group_cls = None
#
#     @typing.overload
#     def __get__(self: T_SubGroup, instance: None, owner: Any) -> T_SubGroup:
#         ...
#
#     @typing.overload
#     def __get__(self, instance: PVGroup, owner: Any) -> T_PVGroup:
#         ...
#
#     def __get__(
#         self: T_SubGroup,
#         instance: Optional[PVGroup],
#         owner: Any,
#     ) -> typing.Union[T_PVGroup, T_SubGroup]:
#         if instance is None:
#             return self
#         return instance.groups[self.attr_name]
#
#     def __set__(self, instance: PVGroup, value: PVGroup):
#         instance.groups[self.attr_name] = value
#
#     def __delete__(self, instance: PVGroup):
#         del instance.groups[self.attr_name]
#
#     @staticmethod
#     def _pvspec_from_info(attr, info):
#         'Create a PVSpec from an info {dict, PVSpec, pvproperty}'
#         if isinstance(info, dict):
#             if 'attr' not in info:
#                 info['attr'] = attr
#             return PVSpec(**info)
#         if isinstance(info, PVSpec):
#             return info
#         if isinstance(info, pvproperty):
#             return info.pvspec
#         raise CaprotoTypeError(f'Unknown type for pvspec: {info!r}')
#
#     def _generate_class_dict(self):
#         'Create the class dictionary from all PVSpecs'
#         pvspecs = [self._pvspec_from_info(attr, pvspec)
#                    for attr, pvspec in self._group_dict.items()]
#
#         return {pvspec.attr: NestedPvproperty.from_pvspec(pvspec, self)
#                 for pvspec in pvspecs
#                 }
#
#     @property
#     def group_dict(self):
#         'The group attribute dictionary'
#         return self._group_dict
#
#     @group_dict.setter
#     def group_dict(self, group_dict):
#         if group_dict is None:
#             return
#
#         # Upon setting the group dictionary, generate the class
#         self._group_dict = group_dict
#         self._class_dict = self._generate_class_dict()
#
#         bad_items = set(group_dict).intersection(set(dir(self)))
#         if bad_items:
#             raise CaprotoValueError(f'Cannot use these attribute names: {bad_items}')
#
#     def __call__(self, group=None, *, prefix=None, macros=None, doc=None):
#         # handles case where a single definition is used multiple times
#         # as in SubGroup(**kw)(group_cls_or_dict) is used
#         copied = copy.copy(self)
#
#         # TODO verify the following works (or even makes sense)
#         if prefix is not None:
#             copied.prefix = prefix
#
#         if macros is not None:
#             copied.macros = macros
#
#         if doc is not None:
#             copied.__doc__ = doc
#
#         if group is not None:
#             copied.group = group
#
#         if copied.group_cls is not None and copied.attr_separator is None:
#             copied.attr_separator = getattr(copied.group_cls,
#                                             'attr_separator', ':')
#
#         return copied
#
#     def __set_name__(self, owner: Type[PVGroup], name: str):
#         self.attr_name = name
#         if self.group_cls is None:
#             # generate the group class, in the case of a dict-based subgroup
#             self.group_cls = type(self.attr_name, self.base, self._class_dict)
#
#             if self.__doc__ is None:
#                 self.__doc__ = self.group_cls.__doc__
#
#         attr_separator = getattr(self.group_cls, 'attr_separator', ':')
#         if attr_separator is not None and self.attr_separator is None:
#             self.attr_separator = attr_separator
#
#         if self.prefix is None:
#             self.prefix = name + self.attr_separator
#
#     def __getattr__(self, attr):
#         'Allow access to class_dict getter/putter/startup through decorators'
#         if self._class_dict is not None and attr in self._class_dict:
#             return self._class_dict[attr]
#         return super().__getattribute__(attr)

class AdaptivePVGroupFactory(type):
    @staticmethod
    def find_subgroups(
        dct: Dict[str, Any]
    ) -> typing.Generator[Tuple[str, SubGroup], None, None]:
        for attr, value in dct.items():
            if attr.startswith('_'):
                continue

            if isinstance(value, SubGroup):
                yield attr, value

    @staticmethod
    def find_pvproperties(
        dct: Dict[str, Any]
    ) -> typing.Generator[Tuple[str, pvproperty], None, None]:
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

    @staticmethod
    def update(cls):
        bases = cls.__bases__
        dct = cls.__dict__
        subgroups = {}
        setattr(cls, '_subgroups_', subgroups)
        pvs = {}
        setattr(cls, '_pvs_', pvs)

        # Propagate any subgroups/PVs from base classes
        for base in bases:
            base_subgroups = getattr(base, "_subgroups_", None)
            if base_subgroups is not None:
                subgroups.update(**base_subgroups)
            base_pvs = getattr(base, "_pvs_", None)
            if base_pvs is not None:
                pvs.update(**base_pvs)

        for attr, prop in AdaptivePVGroupFactory.find_subgroups(dct):
            # module_logger.debug('class %s subgroup attr %s: %r', name, attr,
            #                     prop)
            subgroups[attr] = prop
            # propagate subgroups-of-subgroups to the top
            subgroup_cls = prop.group_cls
            if subgroup_cls is not None and hasattr(subgroup_cls, "_subgroups_"):
                for subattr, subgroup in subgroup_cls._subgroups_.items():
                    subgroups['.'.join((attr, subattr))] = subgroup

        pvs.update(AdaptivePVGroupFactory.find_pvproperties(dct))
        return cls

class AdaptivePVGroup(PVGroup):
    def update_pvs(self):
        bases = self.__class__.__bases__
        dct = self.__dict__

        # logger.debug(f'{bases=}')

        # name = self.__class__.__name__
        # cls = self

        def find_subgroups(kv):
            for attr2, value in kv.items():
                if attr2.startswith('_'):
                    continue
                if isinstance(value, SubGroup):
                    yield attr2, value

        def find_pvproperties(kv):
            for attr2, value in kv.items():
                if attr2.startswith('_'):
                    continue
                if isinstance(value, pvproperty):
                    yield attr2, value
                elif isinstance(value, SubGroup):
                    subgroup_cls2 = value.group_cls
                    if subgroup_cls2 is None:
                        raise CaprotoRuntimeError('Internal error; subgroup class unset?')
                    for sub_attr, value2 in subgroup_cls2._pvs_.items():
                        yield '.'.join([attr2, sub_attr]), value2

        dct['_subgroups_'] = subgroups = {}
        dct['_pvs_'] = pvs = {}

        # Propagate any subgroups/PVs from base classes
        for base in bases:
            base_subgroups = getattr(base, "_subgroups_", None)
            if base_subgroups is not None:
                subgroups.update(**base_subgroups)
            base_pvs = getattr(base, "_pvs_", None)
            if base_pvs is not None:
                logger.debug(f'PVs update: {base_pvs=}')
                pvs.update(**base_pvs)

        # for base in bases:
        #     if hasattr(base, '_subgroups_'):
        #         dct['_subgroups_'].update(**base._subgroups_)
        #     if hasattr(base, '_pvs_'):
        #         dct['_pvs_'].update(**base._pvs_)

        for attr, prop in find_subgroups(dct):
            subgroups[attr] = prop
            # propagate subgroups-of-subgroups to the top
            subgroup_cls = prop.group_cls
            if subgroup_cls is not None and hasattr(subgroup_cls, "_subgroups_"):
                for subattr, subgroup in subgroup_cls._subgroups_.items():
                    subgroups['.'.join((attr, subattr))] = subgroup

        # for attr, prop in find_subgroups(dct):
        #     subgroups[attr] = prop
        #
        #     # TODO a bit messy
        #     # propagate subgroups-of-subgroups to the top
        #     subgroup_cls = prop.group_cls
        #     if hasattr(subgroup_cls, '_subgroups_'):
        #         for subattr, subgroup in subgroup_cls._subgroups_.items():
        #             subgroups['.'.join((attr, subattr))] = subgroup
        results_props = dict(find_pvproperties(dct))
        logger.info(f'From properties, found {results_props=}')
        pvs.update(results_props)
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


class EchoFactory:
    """
    caproto metaclassing inspection system is really really bad...
    to create dynamicly define groups, we create custom classes
    with appropriate properties (TODO: see if modifying metaclass is easier)
    """
    @staticmethod
    def make(channels):
        cls = EPICSEchoGroup
        #logger.debug(f'Before {cls.__dict__=}')

        # for i, ch in enumerate(channels):
        #     setattr(cls, f'property_{i}', pvproperty(record='ai',
        #                                              name=ch,
        #                                              value=0.0,
        #                                              dtype=float,
        #                                              ))
        #https://stackoverflow.com/questions/9541025/how-to-copy-a-class
        # We make it inherit instead of straight copy to allow super() calls
        clsnew = type('EPICSEchoGroupMod', (cls,), dict(cls.__dict__))
        #logger.debug(f'{cls.__bases__=} {cls.__mro__=}')
        for k,v in channels.items():
            setattr(clsnew, k, v)
        AdaptivePVGroupFactory.update(clsnew)
        #logger.debug(f'After {clsnew.__dict__=} {clsnew.__mro__=}')
        return clsnew


class EPICSEchoGroup(AdaptivePVGroup):
    def __init__(self, *args, **kwargs):
        #logger.info(f'Echo group called with {args=} {kwargs=}')
        #logger.info(f'Echo status {self.__dict__=} {self.__class__.__bases__=}')
        super().__init__(prefix=kwargs['prefix'], macros=kwargs['macros'],
                         parent=kwargs['parent'], name=kwargs['name'])
        self.channel = kwargs['channel']



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
