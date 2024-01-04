"""
Module for making objects configurable from dicts via type annotations

SPDX-License-Identifier: MIT
"""
import os
import sys
import json
import argparse
import threading
from functools import partial
from numbers import Number
from typing import (
    cast,
    overload,
    Any,
    Callable,
    ClassVar,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    TYPE_CHECKING,
    Union,
)

if sys.version_info < (3, 8):
    from typing_extensions import Literal
else:
    from typing import Literal

import attr
import _jsonnet

from .common import Sentinel, SENTINEL, TypeList, JSONType, CatalogT, ObjectHookType
from .jsonnet import JsonnetImporter, read_config

__all__ = ["Catalog"]

type_of = type  # we override the name type in some places


class Catalog:
    """Mixin that makes an object loadable from a catalog"""

    CATALOGS: ClassVar[Dict[str, Type]] = {}
    ARCHETYPES: ClassVar[Dict[Type, Type]] = {}
    SEQUENCE_TYPES: ClassVar[TypeList] = (Sequence,)
    MAPPING_TYPES: ClassVar[TypeList] = (Mapping,)

    @classmethod
    def __init_subclass__(cls, name: Optional[str] = None, archetype: Optional[Type] = None):
        """Register any new subclass into the catalog"""
        Catalog.register(cls.__name__, cls, archetype=archetype)

        if name:
            Catalog.register(name, cls, archetype=archetype)

    @classmethod
    def register(cls, name, sub_cls, archetype: Optional[Type] = None):
        """Register the given sub_cls into the catalog"""
        if name in Catalog.CATALOGS:
            raise ValueError(f"{name} already exists in the list of catalogs.")

        if Catalog in sub_cls.__bases__:
            sub_cls.CATALOG = {}
            Catalog.CATALOGS[name] = sub_cls
        else:
            catalog = getattr(cls, "CATALOG", None)
            if catalog is None:
                for parent_cls in Catalog.CATALOGS.values():
                    if sub_cls is parent_cls or issubclass(sub_cls, parent_cls):
                        catalog = parent_cls.CATALOG

            if catalog is None:
                raise ValueError(f"Cannot find parent catalog for {name}!")

            catalog[name] = sub_cls

        if archetype:
            Catalog.ARCHETYPES[archetype] = sub_cls

    @classmethod
    def retrieve(cls: Type[CatalogT], name: str) -> Type[CatalogT]:
        """Retrieve the named sub class from the catalog"""
        if name in Catalog.CATALOGS:
            raise ValueError(f"{name} is an abstract catalog type!")

        catalog = getattr(cls, "CATALOG", None)
        if catalog is None:
            raise ValueError(f"{cls.__name__} does not contain a catalog!")

        sub_cls = catalog.get(name, None)
        if sub_cls is None:
            raise ValueError(f"{name} is not registered in the catalog!")

        return sub_cls

    @classmethod
    def facsimile(cls: Type[CatalogT], archetype: Type) -> Optional[Type[CatalogT]]:
        """Retrieve the facsimile of the archetype if it exists"""
        return cls.ARCHETYPES.get(archetype, None)

    @classmethod
    def list_all(cls):
        """List all catalogs"""
        catalog = ""
        for parent_name, parent_cls in cls.CATALOGS.items():
            catalog += f"{parent_name}:\n"
            for name in parent_cls.CATALOG.keys():
                catalog += f" {name}\n"

        return catalog

    @classmethod
    def list(cls):
        """List catalog"""
        if cls is Catalog:
            return cls.list_all()

        for parent_name, parent_cls in cls.CATALOGS.items():
            if cls == parent_cls or issubclass(cls, parent_cls):
                catalog = f"{parent_name}:\n"
                for name in parent_cls.CATALOG.keys():
                    catalog += f" {name}\n"

                return catalog

        return ""

    @classmethod
    def from_args(
        cls: Type[CatalogT],
        *args,
        type: Union[str, Type[CatalogT], Sentinel] = SENTINEL,
        **kwargs,
    ) -> CatalogT:
        """Create a configurable object from the provided mapping"""
        num_args = len(args)
        if not kwargs and num_args == 1 and type is SENTINEL:
            if isinstance(args[0], Dict) and "type" in args[0]:
                type = args[0]["type"]
                # Make a copy of the args dict rather than popping
                args = ({k: v for k, v in args[0].items() if k != "type"}, *args[1:])
            elif isinstance(args[0], cls):
                type = type_of(args[0])

        if isinstance(type, str):
            sub_cls = cls.retrieve(type)
        elif isinstance(type, Sentinel):
            sub_cls = cls
        elif issubclass(type, cls):
            sub_cls = type
        else:
            raise TypeError(f"Unsupported type: {type}")

        if sub_cls is Catalog or sub_cls.__name__ in Catalog.CATALOGS:
            raise TypeError(
                f"Cannot instantiate top-level class {sub_cls.__name__}."
                " Maybe configuration is missing a 'type' field?"
            )

        if num_args == 1 and not kwargs:
            if isinstance(args[0], cls):
                # It is an already instantiated object, ensure it's an instance
                # of the specified sub_cls as well
                assert isinstance(args[0], sub_cls)
                return args[0]

            if isinstance(args[0], Dict):
                # Check for a dict of initialization parameters, possible
                # scenarios to detect:
                #
                # 1) any kw-only parameter without a default
                # 2) fewer than min positional_or_keyword args without a default
                # 3) more than the maximum number of positional args
                is_param_dict = True
                param_dict = args[0]
                for field in attr.fields(sub_cls):
                    if field.name not in param_dict and (
                        (field.init and field.default is attr.NOTHING)
                        or (
                            field.metadata.get("super_init", False)
                            and field.metadata.get("super_default", attr.NOTHING)
                            is attr.NOTHING
                        )
                    ):
                        # If fields are missing assume it is not a param dict
                        is_param_dict = False
                        break

                if is_param_dict:
                    if "args" in param_dict:
                        # support varargs initializers
                        # Make a copy of the param_dict rather than popping
                        args = (param_dict["args"],)
                        kwargs = {k: v for k, v in param_dict.items() if k != "args"}
                    else:
                        args = tuple()
                        kwargs = param_dict
        elif num_args == 0 and "args" in kwargs:
            # support varargs initializers
            # Make a copy of kwargs rather than popping
            args = (kwargs["args"],)
            kwargs = {k: v for k, v in kwargs.items() if k != "args"}

        return sub_cls(*args, **kwargs)  # type:ignore[call-arg]

    @classmethod
    def from_list(
        cls: Type[CatalogT],
        seq: Sequence[Union[Dict[str, Any], CatalogT]],
        *args,
        **kwargs,
    ) -> List[CatalogT]:
        """Convert a list of module dicts"""
        return [
            cls.from_args(*args, **dict_or_catalog, **kwargs)
            if isinstance(dict_or_catalog, Dict)
            else dict_or_catalog
            for dict_or_catalog in seq
        ]

    @overload
    @classmethod
    def from_config(
        cls: Type[CatalogT],
        path_or_snippet: Union[str, Dict[str, Any]],
        *args,
        allow_multiple: Optional[Literal[False]] = None,
        object_hook=None,
        bindings: Optional[Dict[str, Any]] = None,
        ext_vars: Optional[Dict[str, Any]] = None,
        import_callback: Optional[JsonnetImporter] = None,
        **kwargs,
    ) -> CatalogT:
        ...

    @overload
    @classmethod
    def from_config(
        cls: Type[CatalogT],
        path_or_snippet: Union[str, Dict[str, Any]],
        *args,
        allow_multiple: Literal[True] = True,
        object_hook=None,
        bindings: Optional[Dict[str, Any]] = None,
        ext_vars: Optional[Dict[str, Any]] = None,
        import_callback: Optional[JsonnetImporter] = None,
        **kwargs,
    ) -> Union[CatalogT, List[CatalogT]]:
        ...

    @classmethod
    def from_config(
        cls: Type[CatalogT],
        path_or_snippet: Union[str, Dict[str, Any]],
        *args,
        allow_multiple: Optional[bool] = None,
        object_hook=None,
        bindings: Optional[Dict[str, Any]] = None,
        ext_vars: Optional[Dict[str, Any]] = None,
        import_callback: Optional[JsonnetImporter] = None,
        **kwargs,
    ) -> Union[CatalogT, List[CatalogT]]:
        """Load the model list from the configuration at the given path or snippet"""
        # First read the config for parameters
        config = read_config(
            path_or_snippet,
            object_hook=object_hook,
            bindings=bindings,
            ext_vars=ext_vars,
            import_callback=import_callback,
        ) if isinstance(path_or_snippet, str) else path_or_snippet

        if isinstance(config, List):
            if allow_multiple:
                return cls.from_list(config, *args, **kwargs)

            raise TypeError("Recieved a list, but allow_multiple is false!")

        if isinstance(config, Dict):
            try:
                return cls.from_args(*args, **config, **kwargs)
            except TypeError as e:
                if allow_multiple:
                    return {
                        k: cls.from_args(*args, **dict_or_catalog, **kwargs)
                        if isinstance(dict_or_catalog, Dict)
                        else dict_or_catalog
                        for k, dict_or_catalog in config.items()
                    }

        return cls.from_args(config, *args, **kwargs)

    def asdict(self) -> Union[List[Any], Dict[str, Any], Any]:
        """Return the dictionary version of an object"""

        def serialize(obj: Any, attribute: attr.Attribute):
            """Run the serializer if needed"""
            value = getattr(obj, attribute.name, attr.NOTHING)
            serializer = attribute.metadata.get("serializer", None)
            if serializer:
                return serializer(obj, attribute, value)

            return value

        def attributes(obj: Any):
            """Return a list of attributes and their values"""
            return [
                (attribute, serialize(obj, attribute))
                for attribute in attr.fields(obj.__class__)
                if attribute.init or attribute.metadata.get("super_init", False)
            ]

        def to_dict(obj) -> Union[List[Any], Dict[str, Any], Any]:
            """A recursive conversion to dict"""
            if attr.has(obj):
                obj_dict = {
                    attribute.name: to_dict(value)
                    for attribute, value in attributes(obj)
                    if value is not attr.NOTHING
                }
                obj_dict["type"] = type(obj).__name__
                return obj_dict

            if isinstance(obj, (bytes, str)):
                # Special handling of strings and bytes since they are Sequence
                # types, but iteration returns a subsequence, not an element,
                # thus leading to infinite recursion.
                return obj

            if isinstance(obj, type(self).SEQUENCE_TYPES):
                return [to_dict(v) for v in obj]

            if isinstance(obj, type(self).MAPPING_TYPES):
                return {k: to_dict(v) for k, v in obj.items()}

            return obj

        return to_dict(self)
