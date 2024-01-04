"""
Automatic converters for attrs wrapped types

SPDX-License-Identifier: MIT
"""
import sys
from itertools import zip_longest
from typing import Any, Callable, ClassVar, Dict, Iterable, List, Mapping, Optional, OrderedDict, Sequence, Tuple, Union

from .catalog import Catalog
from .common import Args, Kwargs


__all__ = [
    "catalog_converter",
    "get_base_type",
    "get_any_converter",
    "get_union_converter",
    "get_tuple_converter",
    "get_sequence_converter",
    "get_mapping_converter",
]


def get_base_type(type_):
    """Inspect typing types to get the underlying type (what a mouthful)!"""
    origin = getattr(type_, "__origin__", None)
    if origin:
        return origin

    if sys.version_info < (3, 7) and isinstance(type_, type(ClassVar)):
        # Handle python 3.6 which uses an object of type _ClassVar to represent a ClassVar
        return ClassVar

    facsimile = Catalog.facsimile(type_)
    if facsimile:
        return facsimile

    return type_


def get_any_converter(type_) -> Optional[Callable[[Any], Any]]:
    """Convert any type into a Catalog subclass"""
    base_type = get_base_type(type_)
    if base_type is Union:
        return get_union_converter(type_)

    if base_type is Any or issubclass(base_type, type(None)):
        # no need to convert
        return None

    if issubclass(base_type, slice):
        return lambda x: x if isinstance(x, slice) else slice(*x)

    if issubclass(base_type, tuple):
        tuple_converter = get_tuple_converter(type_)
        if tuple_converter and base_type is Args:
            # For some reason mypy states tuple_converter is None
            return lambda x: Args(tuple_converter(x))  # type:ignore[misc]

        return tuple_converter

    if issubclass(base_type, Catalog):
        return base_type.from_args

    if issubclass(base_type, Mapping):
        mapping_converter = get_mapping_converter(type_)
        if mapping_converter and base_type is Kwargs:
            # For some reason mypy states mapping_converter is None
            return lambda x: Kwargs(mapping_converter(x))  # type:ignore[misc]

        return mapping_converter

    if issubclass(base_type, Iterable) or issubclass(base_type, Sequence):
        sequence_converter = get_sequence_converter(type_)
        if sequence_converter and base_type is Args:
            # For some reason mypy states sequence_converter is None
            return lambda x: Args(sequence_converter(x))  # type:ignore[misc]

        return sequence_converter

    return lambda x: x if isinstance(x, base_type) else base_type(x)


def get_union_converter(type_: Union) -> Optional[Callable[[Any], Any]]:
    """Potentially convert a union of types into a Catalog subclass"""

    value_types = getattr(type_, "__args__")

    # Ignore the style issue, see:
    # https://github.com/PyCQA/pycodestyle/issues/945
    value_types = sorted(value_types, key=lambda vt: vt is not type(None))  # noqa: E721

    value_converters = {
        get_base_type(vt): get_any_converter(vt) for vt in value_types
    }

    if not any(value_converters.values()):
        return None

    if any(issubclass(t, Mapping) for t in value_converters.keys()) and any(
        issubclass(t, Catalog) for t in value_converters.keys()
    ):
        # User defined a type annotation that contains a union of a Mapping and
        # a Catalog. This is ambiguous because a Mapping can be converted to a
        # Catalog.
        raise TypeError(
            "Ambiguous type annotation! You must provider your own converter."
        )

    def _convert(value: Any):
        """The actual converter"""
        errors = []
        for value_type, value_converter in value_converters.items():
            if isinstance(value, value_type):
                if value_converter and (
                    isinstance(value, Sequence) or isinstance(value, Mapping)
                ):
                    # Potentially convert the elements in the container
                    return value_converter(value)

                return value

            try:
                if value_converter:
                    return value_converter(value)
            except (ValueError, TypeError) as e:
                    errors.append(e)

        raise TypeError(f"Unable to convert value of type({type(value)}): {errors}")

    return _convert


def get_tuple_converter(type_: Tuple) -> Optional[Callable[[Any], Tuple[Any, ...]]]:
    """Potentially convert a union of types into a Catalog subclass"""
    if not hasattr(type_, "__args__"):
        # If the tuple does not have __args__ then we cannot automatically
        # convert it
        return None

    zip_fn: Callable = zip
    tuple_type = get_base_type(type_)
    if tuple_type is Tuple:
        # Tuple cannot be directly instantiated, but subclasses can be
        tuple_type = tuple

    value_types = getattr(type_, "__args__")
    if tuple_type is Args or (len(value_types) == 2 and value_types[1] == Ellipsis):
        zip_fn = zip_longest
        value_converter = get_any_converter(value_types[0])
        value_converters = {get_base_type(vt): value_converter for vt in value_types}
    else:
        value_converters = {
            get_base_type(vt): get_any_converter(vt) for vt in value_types
        }

    if not any(value_converters.values()):
        return None

    def _convert(values: Tuple):
        """The actual converter"""
        converted = []
        for value, converter_pair in zip_fn(values, value_converters.items()):
            if converter_pair is not None:
                (value_type, value_converter) = converter_pair

            if isinstance(value, value_type):
                if value_converter and (
                    isinstance(value, Sequence) or isinstance(value, Mapping)
                ):
                    # Potentially convert the elements in the container
                    converted.append(value_converter(value))
                    continue

                converted.append(value)
                continue

            if value_converter:
                converted.append(value_converter(value))

        return tuple_type(converted)

    return _convert


def get_sequence_converter(type_: Sequence) -> Optional[Callable[[Any], List[Any]]]:
    """Potentially convert a sequence of types into a sequence of Catalog subclass"""
    if not hasattr(type_, "__args__"):
        # If the sequence does not have __args__ then we cannot automatically
        # convert it
        return None

    (value_type,) = getattr(type_, "__args__")
    value_converter = get_any_converter(value_type)

    if value_converter:
        # For some reason mypy states value_converter is None
        return lambda x: [value_converter(v) for v in x]  # type:ignore[misc]

    return None  # required to appease mypy


def get_mapping_converter(
    type_: Mapping,
) -> Optional[Callable[[Any], Mapping[Any, Any]]]:
    """Potentially convert a mapping of types into a mapping of Catalog subclass"""
    if not hasattr(type_, "__args__"):
        # If the mapping does not have __args__ then we cannot automatically
        # convert it
        return None

    if getattr(type_, "__origin__") is Kwargs:
        (value_type,) = getattr(type_, "__args__")

        key_converter = None
        value_converter = get_any_converter(value_type)
    else:
        key_type, value_type = getattr(type_, "__args__")

        key_converter = get_any_converter(key_type)
        value_converter = get_any_converter(value_type)

    to_map = (
        OrderedDict if issubclass(getattr(type_, "__origin__"), OrderedDict) else dict
    )
    if key_converter and value_converter:
        return lambda x: to_map(
            {
                # For some reason mypy states key_converter is None
                key_converter(k): value_converter(v)  # type:ignore[misc]
                for k, v in (x.items() if isinstance(x, Mapping) else x)
            }
        )

    if key_converter:
        return lambda x: to_map(
            {
                # For some reason mypy states key_converter is None
                key_converter(k): v  # type:ignore[misc]
                for k, v in (x.items() if isinstance(x, Mapping) else x)
            }
        )

    if value_converter:
        return lambda x: to_map(
            {
                # For some reason mypy states value_converter is None
                k: value_converter(v)  # type:ignore[misc]
                for k, v in (x.items() if isinstance(x, Mapping) else x)
            }
        )

    return None  # required to appease mypy


def catalog_converter(cls, fields):
    """Automatically convert Catalog types"""
    results = []
    for field in fields:
        if field.type is None or field.converter is not None:
            results.append(field)
            continue

        converter = get_any_converter(field.type)
        if converter:
            results.append(field.evolve(converter=converter))
            continue

        results.append(field)

    return results
