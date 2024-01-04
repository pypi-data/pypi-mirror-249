"""
Module for making objects configurable from dicts via type annotations

SPDX-License-Identifier: MIT
"""
import sys
from typing import (
    overload,
    Any,
    Callable,
    Dict,
    List,
    TYPE_CHECKING,
)

import attr

if sys.version_info < (3, 8):
    from typing_extensions import Literal
else:
    from typing import Literal

from .common import Args, Kwargs, T
from .converters import catalog_converter


__all__ = [
    "attrs",
    "field",
    "configurable"
]


def attrs(maybe_cls=None, pre_init=None, **kwargs):
    """
    Decorator that wraps attrs to allow calling a super class initializer
    BEFORE the attrs super class initializer. By default, attrs allows calling
    a super class initializer after initializing the auto created __init__, by
    implementing __attrs_post_init__.

    NOTE: pre_init must return the args and kwargs that should be passed to
    the attrs created __init__.
    """

    def wrap(cls):
        """The internal wrapper method for the decorator."""
        new_cls = attr.s(**kwargs)(cls)
        if pre_init is not None:
            # The attrs defined __init__ does not call the super class
            # initializer. It provides the __attrs_post_init__ method where a
            # super class initializer can be called manually. Unfortunately,
            # some packages have classes that require the super class to be
            # initialized first (like torch and tensorflow).
            attrs_init = getattr(new_cls, "__init__")

            def attrs_pre_init(self, *args, **kwargs):
                """
                This is a version of __init__ that calls the user defined super
                class initializer first, then calls the attrs_created
                initializer.

                NOTE: that the super class initializer may consume some args and
                kwargs that the attrs initializer does not take, so the super
                class initializer should return the args and kwargs that should
                be passed to the attrs __init__ method.
                """
                # First call the specified pre_init, which should return the
                # kwargs required by the attrs_init
                args, kwargs = pre_init(self, *args, **kwargs)

                # Then call the attrs defined init
                attrs_init(self, *args, **kwargs)

            setattr(new_cls, "__init__", attrs_pre_init)

        return new_cls

    # When the decorator is used without function call, i.e. @attrs
    if maybe_cls is None:
        return wrap

    # When the decorator is used as function call, i.e. @attrs()
    return wrap(maybe_cls)


if TYPE_CHECKING:
    from dataclasses import dataclass, field as _field, MISSING

    # When type checking treat configurable as attr.dataclass. This supports *most* of the
    # functionality and allows for type checking without having to write a mypy plugin (and
    # likely allows supporting other type checkers since they also should support dataclasses
    # from the standard library)
    configurable = dataclass

    @overload
    def field(*, default: T, converter=None, validator=None, serializer=None) -> T:
        """Define properties of a field"""
        return _field(
            default=default,
            metadata={
                "converter": converter,
                "validator": validator,
                "serializer": serializer,
            },
        )

    @overload
    def field(
        *, factory: Callable[[], T], converter=None, validator=None, serializer=None
    ) -> T:
        """Define properties of a field"""
        return _field(
            default_factory=factory,
            metadata={
                "converter": converter,
                "validator": validator,
                "serializer": serializer,
            },
        )

    @overload
    def field(*, converter=None, validator=None, serializer=None):
        """Define properties of a field"""
        return _field(
            metadata={
                "converter": converter,
                "validator": validator,
                "serializer": serializer,
            },
        )

    def field(
        *,
        default=MISSING,
        factory=None,
        converter=None,
        validator=None,
        serializer=None,
    ):
        """Define properties of a field"""
        return NotImplemented


else:

    def field(
        *,
        default=attr.NOTHING,
        factory=None,
        converter=None,
        validator=None,
        serializer=None,
    ):
        """Define properties of a field"""
        return attr.ib(
            hash=False,
            default=default,
            factory=factory,
            converter=converter,
            validator=validator,
            metadata={"serializer": serializer},
        )

    def configurable(maybe_cls=None, **kwargs):
        """Make a class automatically configurable from a dict using attrs"""
        # Set default kwargs that seem most sensible
        attrs_kwargs: Dict[str, Any] = {
            "hash": False,
            "auto_detect": True,
            "auto_attribs": True,
            "collect_by_mro": True,
            "field_transformer": catalog_converter,
        }

        # Allow overriding the defaults specified in the dict above if desired
        attrs_kwargs.update(kwargs)

        # See if attrs should create an init function. If not, then do not
        # automatically create a pre_init. A user-defined init can handle it in
        # this case.
        init = attrs_kwargs.get("init", True)
        these = attrs_kwargs.get("these", {})

        def wrap(cls):
            if init:
                super_init = getattr(cls, "__super_init__", cls.__init__)
                for name, field in these.items():
                    if field.init and field.metadata.get("super_init", False):
                        raise ValueError(
                            f"{cls.__name__}.{name}: Cannot specify both init and super_init"
                        )

                def pre_init(self, *args, **kwargs):
                    """Call the super class's __init__"""
                    fields = attr.fields(cls)
                    attr_args: List[Any] = []
                    super_args: List[Any] = []
                    attr_kwargs: Dict[str, Any] = {}
                    super_kwargs: Dict[str, Any] = {}

                    min_args = 0
                    max_args = 0
                    for field in fields:
                        if not field.init and not field.metadata.get(
                            "super_init", False
                        ):
                            continue

                        if getattr(field.type, "__origin__", None) is Args:
                            min_args = 0
                            max_args = float("inf")
                            break

                        if field.kw_only:
                            continue

                        max_args += 1
                        if (
                            field.default is attr.NOTHING
                            and field.metadata.get("super_default", attr.NOTHING)
                            is attr.NOTHING
                            and field.name not in kwargs
                        ):
                            min_args += 1

                    num_args = len(args)
                    if num_args < min_args or num_args > max_args:
                        raise TypeError(
                            f"{type(self).__name__}.__init__() takes from {min_args} to"
                            f" {max_args} positional arguments but {len(args)} were given"
                        )

                    for i, (arg, field) in enumerate(zip(args, fields)):
                        if field.name in kwargs:
                            raise TypeError(
                                f"{type(self).__name__}.__init__() got multiple values for argument: {field.name}"
                            )

                        if field.init:
                            attr_args.append(arg)
                        elif field.metadata.get("super_init", False):
                            converted = field.converter(arg) if field.converter else arg
                            if isinstance(converted, Args):
                                super_args.extend(converted)
                            elif isinstance(converted, Kwargs):
                                super_kwargs.update(converted)
                            else:
                                super_args.append(converted)
                        else:
                            raise ValueError(
                                f"Unexpected positional argument #{i}: {arg}"
                            )

                    for field in fields[num_args:]:
                        if field.init:
                            if field.name not in kwargs:
                                continue

                            attr_kwargs[field.name] = kwargs.get(field.name)
                            kwargs = {
                                k: v for k, v in kwargs.items() if k != field.name
                            }

                        if field.metadata.get("super_init", False):
                            super_default = field.metadata.get(
                                "super_default", attr.NOTHING
                            )
                            super_kwarg = kwargs.get(field.name, super_default)
                            kwargs = {
                                k: v for k, v in kwargs.items() if k != field.name
                            }

                            if super_kwarg is not attr.NOTHING:
                                super_kwargs[field.name] = (
                                    field.converter(super_kwarg)
                                    if field.converter
                                    else super_kwarg
                                )

                    try:
                        super_init(self, *super_args, **super_kwargs)
                    except TypeError as exc:
                        raise TypeError(
                            f"Invalid arguments passed to {cls.__name__}.__init__: "
                            f"args={super_args}, kwargs={super_kwargs}"
                        ) from exc

                    if kwargs:
                        raise TypeError(
                            f"Unknown arguments passed to {cls.__name__}.__init__: "
                            f"kwargs={kwargs}"
                        )

                    return tuple(attr_args), attr_kwargs

                attrs_cls = attrs(maybe_cls=cls, pre_init=pre_init, **attrs_kwargs)
                setattr(attrs_cls, "__super_init__", super_init)
                return attrs_cls

            return attrs(maybe_cls=cls, **attrs_kwargs)

        # When the decorator is used without function call, i.e. @configurable
        if maybe_cls is None:
            return wrap

        # When the decorator is used as function call, i.e. @configurable()
        return wrap(maybe_cls)
