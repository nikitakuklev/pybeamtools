import inspect
import json
import logging
from importlib import import_module
from types import FunctionType, MethodType
from typing import Callable, TypeVar, Any, List

import numpy as np
import pandas as pd
from pydantic import BaseModel, Extra, root_validator, create_model, Field

# ObjType = TypeVar("ObjType")
logger = logging.getLogger(__name__)


def get_fully_qualified_name(x):
    cl = x.__class__
    module = cl.__module__
    if module == 'builtins':
        return cl.__qualname__
    return module + ':' + cl.__qualname__


JSON_ENCODERS = {
    FunctionType: lambda x: get_fully_qualified_name(x),
    MethodType: lambda x: get_fully_qualified_name(x),
    Callable: lambda x: f"{x.__module__}:{type(x).__qualname__}",
    type: lambda x: get_fully_qualified_name(x),
    np.ndarray: lambda x: x.tolist(),
    np.int64: lambda x: int(x),
    np.float64: lambda x: float(x),
    pd.DataFrame: lambda x: x.to_json(),
    Any: lambda x: f"{x.__class__.__module__}.{x.__class__.__qualname__}",
}


class SerializableBaseModel(BaseModel):
    class Config:
        extra = Extra.forbid
        json_encoders = JSON_ENCODERS


def _escape_sdds_string(s):
    return s.translate(str.maketrans({"\\": r"\\"}))


def to_sdds(options: dict):
    parameters = []
    prefix = 'pybeamtools:'

    def _to_sdds_inner(root, opts):
        for k, v in opts.items():
            assert isinstance(k, str)
            if isinstance(v, dict):
                _to_sdds_inner(root + k + ':', v)
            elif isinstance(v, list):
                full_name = _escape_sdds_string(root + k)
                parameters.append((full_name, json.dumps(v)))
            elif isinstance(v, (int, float, str)):
                full_name = _escape_sdds_string(root + k)
                parameters.append((full_name, str(v)))
            elif v is None:
                full_name = _escape_sdds_string(root + k)
                parameters.append((full_name, 'None'))
            else:
                raise ValueError(f'Unknown mapping {k=} {v=} {type(v)=}')
    _to_sdds_inner(prefix, options)
    return parameters

def get_callable_from_string(callable: str, bind: Any = None) -> Callable:
    """Get callable from a string. In the case that the callable points to a bound method,
    the function returns a callable taking the bind instance as the first arg.

    Args:
        callable: String representation of callable abiding convention
             __module__:callable
        bind: Class to bind as self

    Returns:
        Callable
    """
    callable_split = callable.rsplit(":", 1)

    if len(callable_split) != 2:
        raise ValueError(f"Improperly formatted callable string: {callable_split}")

    module_name, callable_name = callable_split
    try:
        module = import_module(module_name)
    except ModuleNotFoundError as err:
        logger.error("Unable to import module %s", module_name)
        raise err
        # try:
        #     module_split = module_name.rsplit(".", 1)
        #
        #     if len(module_split) != 2:
        #         raise ValueError(f"Unable to access: {callable}")
        #
        #     module_name, class_name = module_split
        #
        #     module = import_module(module_name)
        #     callable_name = f"{class_name}.{callable_name}"
        #
        # except ModuleNotFoundError as err:
        #     logger.error("Unable to import module %s", module_name)
        #     raise err
        #
        # except ValueError as err:
        #     logger.error(err)
        #     raise err

    # construct partial in case of bound method
    if "." in callable_name:
        bound_class, callable_name = callable_name.rsplit(".")

        try:
            bound_class = getattr(module, bound_class)
        except AttributeError as e:
            logger.error("Unable to get %s from %s", bound_class, module_name)
            raise e

        # require right partial for assembly of callable
        # https://funcy.readthedocs.io/en/stable/funcs.html#rpartial
        def rpartial(func, *args):
            return lambda *a: func(*(a + args))

        callable = getattr(bound_class, callable_name)
        params = inspect.signature(callable).parameters

        # check bindings
        is_bound = params.get("self", None) is not None
        if not is_bound and bind is not None:
            raise ValueError("Cannot bind %s to %s.", callable_name, bind)

        # bound, return partial
        if bind is not None:
            if not isinstance(bind, (bound_class,)):
                raise ValueError(
                    "Provided bind %s is not instance of %s",
                    bind,
                    bound_class.__qualname__,
                )

        if is_bound and isinstance(callable, (FunctionType,)) and bind is None:
            callable = rpartial(getattr, callable_name)

        elif is_bound and isinstance(callable, (FunctionType,)) and bind is not None:
            callable = getattr(bind, callable_name)

    else:
        if bind is not None:
            raise ValueError("Cannot bind %s to %s.", callable_name, type(bind))

        try:
            callable = getattr(module, callable_name)
        except Exception as e:
            logger.error("Unable to get %s from %s", callable_name, module_name)
            raise e

    return callable


def validate_and_compose_signature(callable: Callable, *args, **kwargs):
    # try partial bind to validate
    signature = inspect.signature(callable)
    bound_args = signature.bind_partial(*args, **kwargs)
    sig_kw = bound_args.arguments.get("kwargs", {})
    sig_args = bound_args.arguments.get("args", [])
    sig_kwargs = {}
    # Now go parameter by parameter and assemble kwargs
    for i, param in enumerate(signature.parameters.values()):

        if param.kind in [param.POSITIONAL_OR_KEYWORD, param.KEYWORD_ONLY]:
            # if param not bound use default/ compose field rep
            if not sig_kw.get(param.name):

                # create a field representation
                if param.default == param.empty:
                    sig_kwargs[param.name] = param.empty

                else:
                    sig_kwargs[param.name] = param.default

            else:
                sig_kwargs[param.name] = sig_kw.get(param.name)

            # assign via binding
            if param.name in bound_args.arguments:
                sig_kwargs[param.name] = bound_args.arguments[param.name]

    # create pydantic model
    pydantic_fields = {
        "args": (List[Any], Field(list(sig_args))),
        "kwarg_order": Field(list(sig_kwargs.keys()), exclude=True),
    }
    for key, value in sig_kwargs.items():
        if isinstance(value, (tuple,)):
            pydantic_fields[key] = (tuple, Field(None))

        elif value == inspect.Parameter.empty:
            pydantic_fields[key] = (inspect.Parameter.empty, Field(value))

        else:
            # assigning empty default
            if value is None:
                pydantic_fields[key] = (inspect.Parameter.empty, Field(None))

            else:
                pydantic_fields[key] = value

    model = create_model(
        f"Kwargs_{callable.__qualname__}", __base__=SignatureModel, **pydantic_fields
    )

    return model()


class SignatureModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    def build(self, *args, **kwargs):
        stored_kwargs = self.dict()
        stored_args = []
        if "args" in stored_kwargs:
            stored_args = stored_kwargs.pop("args")

        # adjust for positional
        args = list(args)
        n_pos_only = len(stored_args)
        positional_kwargs = []
        if len(args) < n_pos_only:
            stored_args[:n_pos_only] = args
        else:
            stored_args = args[:n_pos_only]
            positional_kwargs = args[n_pos_only:]

        stored_kwargs.update(kwargs)

        # exclude empty parameters
        stored_kwargs = {
            key: value
            for key, value in stored_kwargs.items()
            if not value == inspect.Parameter.empty
        }
        for i, positional_kwarg in enumerate(positional_kwargs):
            stored_kwargs[self.kwarg_order[i]] = positional_kwarg

        return stored_args, stored_kwargs


class CallableModel(BaseModel):
    callable: Callable
    signature: SignatureModel

    class Config:
        arbitrary_types_allowed = True
        json_encoders = JSON_ENCODERS
        extra = Extra.forbid

    @root_validator(pre=True)
    def validate_all(cls, values):
        callable = values.pop("callable")

        if not isinstance(callable, (str, Callable), ):
            raise ValueError(
                "Callable must be object or a string. Provided %s", type(callable)
            )

        # parse string to callable
        if isinstance(callable, (str,)):

            # for function loading
            if "bind" in values:
                callable = get_callable_from_string(callable, bind=values.pop("bind"))

            else:
                callable = get_callable_from_string(callable)

        values["callable"] = callable

        # for reloading:
        kwargs = {}
        args = []
        if "args" in values:
            args = values.pop("args")

        if "kwargs" in values:
            kwargs = values.pop("kwargs")

        if "signature" in values:
            if "args" in values["signature"]:
                args = values["signature"].pop("args")

            # not needed during reserialization
            if "kwarg_order" in values["signature"]:
                values["signature"].pop("kwarg_order")

            if "kwargs" in values:
                kwargs = values["signature"]["kwargs"]

            else:
                kwargs = values["signature"]

        values["signature"] = validate_and_compose_signature(callable, *args, **kwargs)

        return values

    def __call__(self, *args, **kwargs):
        if kwargs is None:
            kwargs = {}

        fn_args, fn_kwargs = self.signature.build(*args, **kwargs)

        return self.callable(*fn_args, **fn_kwargs)


class PBClass:
    """ Inheriting from this class allows storing attributes
    in the model configured with __options_model__. All other attributes
    will be stored in the class as usual. """

    ___options_model__: BaseModel = None

    def __init__(self, options=None, **kwargs):
        print(f'__init__ {options=} {kwargs=}')
        assert isinstance(options, BaseModel)
        if options is None:
            self.__set_options(**kwargs)
        else:
            object.__setattr__(self, 'options', options)

    # Called first, need to be careful to avoid recursion
    def __getattribute__(self, item):
        print(f'__getattribute__ {item=}')
        try:
            opt = super(PBClass, self).__getattribute__('options')
            if item in opt.__fields__:
            #if hasattr(opt, item):
                # Options model can get accessed as usual
                return getattr(opt, item)#super(PBClass, self).__getattribute__(opt, item)
        except AttributeError:
            pass
        except Exception as ex:
            print(f'__getattribute__ produced exception {ex=}')
            raise ex
        finally:
            return super(PBClass, self).__getattribute__(item)

    def __setattr__(self, item, value):
        # Can also access __dict__ directly
        if item == 'options':
            object.__setattr__(self, item, value)
        else:
            opt = object.__getattribute__(self, 'options')
            if hasattr(opt, item):
                setattr(opt, item, value)
            else:
                object.__setattr__(self, item, value)

    # def parse_opt_signature(self):
    #     signature = inspect.signature(object.__getattribute__(self, '__options_model__'))
    #     parameter_names = list(signature.parameters.keys())
    #     parameter_set = set(parameter_names)
    #     print(f'parse_opt {parameter_set=}')
    #     return parameter_set

    def get_user_attributes(cls):
        boring = dir(type('dummy', (object,), {}))
        return [item
                for item in inspect.getmembers(cls)
                if item[0] not in boring]

    def __set_options(self, **kwargs):
        options_class = object.__getattribute__(self, '__options_model__')
        signature = inspect.signature(options_class)

        parameter_names = list(signature.parameters.keys())
        parameter_set = set(parameter_names)
        print(f'parse_opt {parameter_set=}')

        # params = self.parse_opt_signature()
        opt_kwargs = {k: v for k, v in kwargs.items() if k in parameter_set}
        extra_kwargs = {k: v for k, v in kwargs.items() if k not in parameter_set}

        self.options = options_class.parse_obj(opt_kwargs)
        return extra_kwargs

    def serialize(self):
        pass
