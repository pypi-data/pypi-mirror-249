# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/04_emod.ipynb.

# %% auto 0
__all__ = ['ModuleEnum']

# %% ../nbs/04_emod.ipynb 6
import copy
from abc import ABCMeta
from enum import Enum, EnumMeta, _EnumDict, member, StrEnum, auto, IntEnum
from importlib import import_module
from functools import partial, wraps

# %% ../nbs/04_emod.ipynb 8
from types import ModuleType, FunctionType
from typing import (
    Any, Type, Self, Union, Tuple, Iterable, TypedDict, TypeAlias, 
    Callable, Generator, Optional, ParamSpec, TypeVar, TypeGuard, Literal
)

# %% ../nbs/04_emod.ipynb 10
#| export


# %% ../nbs/04_emod.ipynb 12
from nlit import VALUE, MIXINS, ASMEMBER

# %% ../nbs/04_emod.ipynb 14
from .atyp import T, P
from .meta import ModuleEnumMeta
from .util import missing

# %% ../nbs/04_emod.ipynb 16
class ModuleEnum(Enum, metaclass=ModuleEnumMeta):
    @classmethod
    def _missing_(cls: Type[T], val: str | T, default = None) -> T:
        '''Method called for missing members during lookup.'''
        if default is None: default = cls._default_()
        return missing(cls, val, default)
    
    @classmethod
    def safe(cls: Type[T], key: T) -> T:
        '''Take a key and return the corresponding enum member if it exists, otherwise return the default member'''
        try: return cls(key)
        except ValueError: ...
        try: return cls(cls._default_())
        except ValueError: cls._default_()
        
    @classmethod
    def module(cls: Type[T]) -> ModuleType:
        '''Return the module from which to load members corresponding to the enum class'''
        try: return import_module(cls._module_())
        except: return None
         
    @classmethod
    def imp(cls: Type[T], key: T | None = None, *args: P.args, **kwargs: P.kwargs) -> Callable:
        '''Import the class or function corresponding to the enum member, or the default member of the enum class'''
        ins = cls.safe(key)
        mod = cls.module()
        if isinstance(ins, cls): ins = ins.name
        if not isinstance(ins, str): ins = str(ins)
        return getattr(mod, ins)
    
    @classmethod
    def init(cls: Type[T], key: T | None = None, *args: P.args, **kwargs: P.kwargs):
        '''Initalize the class or function corresponding to the enum member, or the default member of the enum class with the given arguments'''
        fn = cls.imp(key, *args, **kwargs)
        return fn(*args, **kwargs)
    
    def get(self: T, *args: P.args, **kwargs: P.kwargs) -> Callable:
        '''Import the class or function of this enum member'''
        return self.imp(self, *args, **kwargs)
    
    def make(self: T, *args: P.args, **kwargs: P.kwargs):
        '''Initalize the class or function corresponding with the given arguments of this enum member'''
        return self.init(self, *args, **kwargs)

# %% ../nbs/04_emod.ipynb 18
#| export
