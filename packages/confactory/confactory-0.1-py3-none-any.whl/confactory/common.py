"""
Module for making objects configurable from dicts via type annotations

SPDX-License-Identifier: MIT
"""
import threading
from numbers import Number
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
)


__all__ = [
    "SENTINEL",
    "TypeList",
    "JSONType",
    "CatalogT",
    "ObjectHookType",
    "T",
    "Args",
    "Kwargs",
]


class Sentinel:
    """Thread-safe unique singleton used as a sentinel for defaults"""

    _singleton: Optional["Sentinel"] = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls):
        if not Sentinel._singleton:
            with Sentinel._lock:
                Sentinel._singleton = super(Sentinel, cls).__new__(cls)

        return Sentinel._singleton


SENTINEL = Sentinel()
TypeList = Union[type, Tuple[Union[type, Tuple[Any, ...]], ...]]
JSONType = Union[str, Number, bool, None, Dict[str, Any], List[Any]]
CatalogT = TypeVar("CatalogT", bound="Catalog")
ObjectHookType = TypeVar("ObjectHookType")
T = TypeVar("T")


# Would prefer to use NewType, but it doesn't support generics
# https://github.com/python/mypy/issues/3331
class Args(Tuple[T, ...]):
    """Function/method positional arguments"""


class Kwargs(Dict[str, T]):
    """Function/method keyword arguments"""
