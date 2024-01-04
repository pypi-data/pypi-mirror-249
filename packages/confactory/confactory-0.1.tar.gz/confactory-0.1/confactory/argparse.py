"""
Utilities to work with argparse

SPDX-License-Identifier: MIT
"""
import sys
from argparse import _SubParsersAction, ArgumentParser, SUPPRESS
from typing import cast, Any, Callable, Dict, List, Optional, overload, Union

from .jsonnet import JsonnetImporter, read_config
from .common import JSONType, ObjectHookType, SENTINEL


__all__ = ["parse_args"]


@overload
def parse_args(
    parser: ArgumentParser,
    key: str = "command",
    bindings: Optional[Dict[str, Any]] = None,
    ext_vars: Optional[Dict[str, Any]] = None,
    import_callback: Optional[JsonnetImporter] = None,
) -> Dict[str, Any]:
    ...


@overload
def parse_args(
    parser: ArgumentParser,
    key: str = "command",
    bindings: Optional[Dict[str, Any]] = None,
    ext_vars: Optional[Dict[str, Any]] = None,
    import_callback: Optional[JsonnetImporter] = None,
    object_hook: Callable[[Dict[str, Any]], ObjectHookType] = ...,
) -> ObjectHookType:
    ...


def parse_args(
    parser: ArgumentParser,
    key: str = "command",
    bindings: Optional[Dict[str, Any]] = None,
    ext_vars: Optional[Dict[str, Any]] = None,
    import_callback: Optional[JsonnetImporter] = None,
    object_hook: Optional[Callable[[Dict[str, Any]], ObjectHookType]] = None,
) -> Union[Dict[str, Any], ObjectHookType]:
    """Convert from Namespace to json config"""
    # Allow reading arguments from a config file. Arguments specified on the
    # command-line will override those from the file.
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Location of a configuration file to read command-line arguments",
    )

    args = parser.parse_args()
    ungrouped = ("positional arguments", "optional arguments", "options")

    defaults: JSONType = {}
    config_path = vars(args).pop("config")
    if config_path:
        defaults = read_config(
            config_path,
            bindings=bindings,
            ext_vars=ext_vars,
            import_callback=import_callback,
        )

    def extract(groups, defaults=defaults, object_hook=object_hook) -> Dict[str, Any]:
        """
        Extract namespaces from the parser
        """
        namespaces = {}
        for group in groups:
            if not group.title:
                raise ValueError("Must specify a title for the subgroup!")

            group_dict = {}
            for action in group._group_actions:
                if not hasattr(args, action.dest):
                    continue

                default = SENTINEL
                group_defaults = (
                    defaults
                    if group.title in ungrouped
                    else defaults.get(group.title, SENTINEL)
                )
                if group_defaults is not SENTINEL:
                    default = group_defaults.get(action.dest, SENTINEL)
                    if default is SENTINEL:
                        for option_string in action.option_strings:
                            if option_string.startswith("--"):
                                default = group_defaults.get(
                                    option_string[2:], SENTINEL
                                )

                            if default is not SENTINEL:
                                break

                if default is not SENTINEL and all(
                    opt not in sys.argv for opt in action.option_strings
                ):
                    group_dict[action.dest] = default
                else:
                    arg = getattr(args, action.dest, SENTINEL)
                    if arg is SENTINEL:
                        if action.default is not SUPPRESS:
                            group_dict[action.dest] = action.default
                    else:
                        group_dict[action.dest] = arg

            if group._action_groups:
                group_dict.update(
                    extract(
                        group._action_groups,
                        defaults=defaults[group.title],
                        object_hook=object_hook,
                    )
                )

            if not group_dict:
                continue

            if group.title in ungrouped:
                namespaces.update(group_dict)
            else:
                namespaces[group.title] = (
                    object_hook(group_dict) if object_hook else group_dict
                )

        return namespaces

    namespaces = extract(parser._action_groups)
    if parser._subparsers and parser._subparsers._group_actions:
        subparsers_list = cast(
            List[_SubParsersAction], parser._subparsers._group_actions
        )

        for subparsers in subparsers_list:
            for name, subparser in subparsers.choices.items():
                if name != getattr(args, key):
                    # Only extract args from the chosen subparser
                    continue

                extracted = extract(subparser._action_groups)
                if not extracted:
                    raise ValueError("Unable to extract subparser arguments!")

                namespaces.update(extracted)
                namespaces.update(
                    {
                        k: getattr(args, k)
                        for k, v in subparser._defaults.items()
                    }
                )

    return object_hook(namespaces) if object_hook else namespaces
