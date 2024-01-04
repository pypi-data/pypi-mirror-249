"""
A few standard validators

SPDX-License-Identifier: MIT
"""
import operator
from functools import partial
from typing import Optional, Type, Union

import attr


__all__ = ["is_number", "is_int", "is_float"]

OPERATORS = {
    operator.lt: "<",
    operator.le: "<=",
    operator.gt: ">",
    operator.ge: ">=",
}

def _get_operator_min(value, type):
    min_operator = operator.lt
    if isinstance(value, str):
        min_operator = operator.le if value.startswith("-") else min_operator
        value = type(value)

    return value, min_operator


def _get_operator_max(value, type):
    max_operator = operator.gt
    if isinstance(value, str):
        max_operator = operator.ge if value.startswith("+") else max_operator
        value = type(value)

    return value, max_operator


def is_number(
    type: Union[Type[float], Type[int]] = float,
    min: Optional[Union[int, float, str]] = None,
    max: Optional[Union[int, float, str]] = None,
):
    """Method to validate the passed in value is a number within the specified range"""
    min, min_operator = _get_operator_min(min, type)
    max, max_operator = _get_operator_max(max, type)

    def _validator(value):
        value = type(value)
        if min is not None and min_operator(value, min):
            raise ValueError(f"{value} must be {OPERATORS[min_operator]} {min}")

        if max is not None and max_operator(value, max):
            raise ValueError(f"{value} must be {OPERATORS[max_operator]} {max}")

        return value

    return attr.validators.and_(attr.validators.instance_of(type), _validator)


is_int = partial(is_number, type=int)
is_float = partial(is_number, type=float)
