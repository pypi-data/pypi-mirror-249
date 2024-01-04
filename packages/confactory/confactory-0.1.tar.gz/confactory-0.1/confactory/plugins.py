"""
Mypy plugin

SPDX-License-Identifier: MIT
"""
from typing import Callable, List, Optional

from mypy.plugin import Plugin
from mypy.plugins.attrs import (
    attr_class_makers,
    attr_dataclass_makers,
)

# This works just like `attr.s`.
attr_class_makers.add("config.attrs")
attr_dataclass_makers.add("config.configurable")

# Our plugin does nothing but it has to exist so this file gets loaded.
class MarshalPlugin(Plugin):
    """ Mypy plugin for @configurable """

def plugin(version: str):
    """ Defines the plugin for mypy """
    return MarshalPlugin
