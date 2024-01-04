"""
Module to wrap jsonnet functionality

SPDX-License-Identifier: MIT
"""
import json
import logging
import os
from typing import Any, Callable, Dict, List, Optional, overload, Sequence, Union

from _jsonnet import evaluate_file, evaluate_snippet

from .common import JSONType, ObjectHookType


__all__ = ["JsonnetImporter", "read_config"]


class JsonnetImporter:
    """
    Acts as a jsonnet import callback which also tracks which files were
    imported and allows for specifying a list of import directories.
    """

    def __init__(self, search_paths: Optional[Union[str, Sequence[str]]] = None):
        self.imports: List[str] = []
        self.search_paths = (
            (search_paths,)
            if isinstance(search_paths, str)
            else (tuple() if not search_paths else tuple(search_paths))
        )

    @staticmethod
    def try_load(directory: str, relative_path: str):
        """Try to load the relative_path from the associated directory"""
        if not relative_path:
            raise RuntimeError("Got an invalid filename (the empty string).")

        full_path = (
            relative_path
            if relative_path.startswith("/")
            else os.path.join(directory, relative_path)
        )

        if full_path.endswith("/"):
            raise RuntimeError(f"Attempted to import a directory: {full_path}.")

        if not os.path.isfile(full_path):
            return full_path, None

        with open(full_path, "rt") as file:
            return full_path, file.read().encode("utf-8")

    def __call__(self, directory: str, relative_path: str):
        full_path, content = self.try_load(directory, relative_path)
        if content:
            self.imports.append(full_path)
            return full_path, content

        for path in self.search_paths:
            full_path, content = self.try_load(path, relative_path)
            if content:
                self.imports.append(full_path)
                return full_path, content

        raise RuntimeError(f"File not found: {relative_path}")


@overload
def read_config(
    path_or_snippet: str,
    bindings: Optional[Dict[str, Any]] = None,
    ext_vars: Optional[Dict[str, Any]] = None,
    import_callback: Optional[JsonnetImporter] = None,
) -> JSONType:
    ...


@overload
def read_config(
    path_or_snippet: str,
    bindings: Optional[Dict[str, Any]] = None,
    ext_vars: Optional[Dict[str, Any]] = None,
    import_callback: Optional[JsonnetImporter] = None,
    object_hook: Callable[[Dict[str, Any]], ObjectHookType] = ...,
) -> ObjectHookType:
    ...


def read_config(
    path_or_snippet: str,
    bindings: Optional[Dict[str, Any]] = None,
    ext_vars: Optional[Dict[str, Any]] = None,
    import_callback: Optional[JsonnetImporter] = None,
    object_hook: Optional[Callable[[Dict[str, Any]], ObjectHookType]] = None,
) -> Union[ObjectHookType, JSONType]:
    """Load the configuration from the given path or jsonnet snippet"""
    if os.path.isfile(path_or_snippet):
        args = [path_or_snippet]
        evaluate_jsonnet = evaluate_file
    else:
        args = ["snippet.jsonnet", path_or_snippet]
        evaluate_jsonnet = evaluate_snippet

    # jsonnet is a little finicky about passed in parameters as it's written
    # entirely using the C API. That means Python's None isn't explicitly
    # accounted for, which means we need to be careful about passing None for
    # things like import_callback (it will complain that None is not callable).
    # Instead, just omit unspecified parameters from the keyword arguments.
    kwargs: Dict[str, Any] = {}
    if import_callback:
        kwargs["import_callback"] = import_callback

    if bindings:
        kwargs["tla_codes"] = {k: json.dumps(v) for k, v in bindings.items()}

    if ext_vars:
        kwargs["ext_codes"] = {k: json.dumps(v) for k, v in ext_vars.items()}

    try:
        jsonnet_str = evaluate_jsonnet(*args, **kwargs)
    except RuntimeError as rte:
        logging.fatal(
            "Unable to parse jsonnet. Double check the path exists or the snippet is valid."
        )
        logging.fatal("path_or_snippet='%s'", path_or_snippet)
        raise rte

    if object_hook:
        return json.loads(jsonnet_str, object_hook=object_hook)

    return json.loads(jsonnet_str)
