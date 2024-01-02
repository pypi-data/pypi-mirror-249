# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/03_meta.ipynb.

# %% auto 0
__all__ = ['ModuleEnumMeta']

# %% ../nbs/03_meta.ipynb 6
import copy
from abc import ABCMeta
from enum import Enum, EnumMeta, _EnumDict, member, StrEnum, auto, IntEnum
from importlib import import_module
from functools import partial, wraps

# %% ../nbs/03_meta.ipynb 8
from types import ModuleType, FunctionType
from typing import (
    Any, Type, Self, Union, Tuple, Iterable, TypedDict, TypeAlias, 
    Callable, Generator, Optional, ParamSpec, TypeVar, TypeGuard, Literal
)

# %% ../nbs/03_meta.ipynb 10
#| export


# %% ../nbs/03_meta.ipynb 12
from nlit import VALUE, MIXINS, ASMEMBER

# %% ../nbs/03_meta.ipynb 14
from .atyp import T, P, Mixin
from .util import enumdict, evalue, missing

# %% ../nbs/03_meta.ipynb 16
class ModuleEnumMeta(EnumMeta):
    def _check_for_existing_members_(class_name, bases):
        '''Check for existing members in base classes.'''
        
    @classmethod
    def duplicate(mcls: Type[T], v: T, *args: P.args, **kwargs: P.kwargs):
        '''Duplicate a value within the enumeration dictionary.'''
        mixins: list[Mixin] = kwargs.get(MIXINS, getattr(mcls, MIXINS, []))
        asmemb = kwargs.get(ASMEMBER, False)
        copied = copy.deepcopy(evalue(v))
        for (mixtype, hook) in mixins:
            if not isinstance(copied, mixtype): continue
            copied = hook(copied, *args, **kwargs)
        return member(copied) if asmemb else copied
        
    @classmethod
    def __copydict__(mcls: Type[T], clsdict: _EnumDict, *args: P.args, **kwargs: P.kwargs) -> _EnumDict:
        '''Create a deep copy of the enumeration dictionary.'''
        newdict = enumdict(clsdict._cls_name)
        for k, v in clsdict.items(): 
            newdict[k] = mcls.duplicate(v, *args, **kwargs)
        return newdict
    
    @classmethod
    def __prepare__(mcls: Type[T], name: str, bases: tuple, **kwargs) -> _EnumDict:
        '''Prepare the enumeration dictionary before class creation.'''
        clsdict = enumdict(name)
        return clsdict
    
    def __new__(mcls: Type[T], name, bases, clsdict, **kwargs):
        '''Create a new enumeration class.'''
        newcls = super().__new__(mcls, name, bases, clsdict)
        setattr(newcls, '__module', kwargs.get('module', None))
        setattr(newcls, '__default', kwargs.get('default', None))
        return newcls

    def _default_(cls: Type[T]) -> T:
        keys = getattr(cls, '_member_names_', [None])
        return getattr(cls, '__default', keys[0])
    
    def _module_(cls: Type[T]) -> str:
        return getattr(cls, '__module', 'torch.nn')
    
    @classmethod
    def _missing_(cls: Type[T], val: str | T, default = None) -> T:
        '''Method called for missing members during lookup.

        Parameters
        ----------
        cls : Enum
            The enumeration class.
        
        val : str
            The value to check for in the enum members.
        

        Returns
        -------
        Enum member or default
            The matched enum member or the default value.
        '''
        if default is None: default = cls._default_()
        return missing(cls, val, default)
    
    def __contains__(self: T, key: str) -> TypeGuard[T]:
        '''Check if the key exists in the enumeration's members.'''
        attrs = ('_member_map_', '_member_names_')
        for (attr, case) in zip(attrs, (True, False)):
            for mem in getattr(self, attr, []):
                if case and (str(mem).casefold() == key.casefold()) or (mem == key):
                    return True
        return False

# %% ../nbs/03_meta.ipynb 18
#| export
