"""
Common code used in multiple modules.
"""
import types
import uuid
import inspect
import datetime
import builtins
from collections import OrderedDict
from types import FunctionType, ModuleType, MethodType

##; @formatter:on
##; 不可变的简单类型（基本类型)
##; cannot import name 'NoneType' from 'types' !!!
K_Python_Basic_Types = (
    type(None),
    str,
    int,
    bool,
    float,
    bytes,

)
##; 复合类型（或容器类型） 
K_Python_Composite_types = (
    set,
    list,
    dict,
    tuple,  # ; immutable
    complex,  # ; immutable
)

K_Python_Common_Types = (
    *K_Python_Basic_Types,
    *K_Python_Composite_types,

    frozenset,
    bytearray,
    uuid.UUID,
    datetime.datetime,
    datetime.timedelta,
    datetime.date,
)


##; @formatter:off

def list_builin_type_names():
    attr_list = dir(builtins)
    basic_types = [name for name in attr_list if isinstance(getattr(builtins, name), type)]
    return basic_types


def is_ignored_attr(
    k, v,
    nullable=True,
    _ignore_type=True,
    _ignore_function=True,
    _ignore_attr_=True,
    _ignore_module=True,
    _ignore_method=True,
):
    """
    @k: attr_name
    @v: attr_value
    @return: bool: is_ignored
    """
    ret = False
    if _ignore_attr_ and k.startswith('_'):
        ret = True
    elif _ignore_type and isinstance(v, type):
        ret = True
    elif _ignore_function and isinstance(v, FunctionType):
        ## common function + staticmethod 
        ret = True
    elif _ignore_method and inspect.ismethod(v):
        ## instance_method + classmethod
        ret = True
    elif _ignore_attr_ and isinstance(v, ModuleType):
        ret = True
    if not ret and not nullable:
        if v is None:
            ret = True
    return ret


def trim_dict(origin_dct, nullable=False, verbose=0, ignore_func=None,
              **kws
              ):
    data = dict()
    if ignore_func is None:
        ignore_func = is_ignored_attr
    for k, v in origin_dct.items():
        if v is None:
            if nullable:
                data[k] = v
        elif verbose <= 0:
            if isinstance(v, K_Python_Common_Types):
                data[k] = v
        elif not ignore_func(k, v):
            data[k] = v
    return data


def brief_object(obj, ordered=False, **kwargs):
    data = OrderedDict() if ordered else dict()
    for attr in dir(obj):
        if not attr.startswith('_'):
            value = getattr(obj, attr)
            if not callable(value):
                data[attr] = value
    return data


class CommonException(Exception):
    description = "PycoBaseError"
    errno = 40000
    error_msg = "customized details of error message"

    def __init__(self, error_msg=error_msg, **kwargs):
        self.error_msg = error_msg
        self.errno = kwargs.pop("errno", self.errno)
        self._kwargs = kwargs

    def to_dict(self):
        ## v3
        return dict(
            errno=self.errno,
            error_msg=self.error_msg,
            error_kws=self._kwargs
        )
