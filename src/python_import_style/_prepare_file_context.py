# Copyright (C) 2026 by the python-import-style pre-commit hook authors
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT
"""Prepare file context for a file being checked."""

import pathlib
import typing

import python_import_style._append_rule_error
import python_import_style._is_inside_directory


class _FileContext(typing.NamedTuple):
    """Lightweight, internal context for a file being checked."""

    # File is inside the package tree
    in_package: bool

    # File is inside the tests tree
    in_tests: bool

    # File is an __init__.py
    is_init: bool

    # File is a __main__.py
    is_main: bool

    # If the file is in the package, the parts of the subpackage path between
    # the package root and the file itself (excluded).
    subpackage_parts_: tuple[str, ...] | None

    # File lives inside a private subpackage)
    in_private_subpackage_: bool | None

    # If the file is in the package and is not __init__.py or __main__.py, the
    # module name (stem).
    module_name_: str | None

    # File is a private module (module name starts with '_', excluding
    # __init__ and __main__)
    is_private_module_: bool | None

    @property
    def subpackage_parts(self) -> tuple[str, ...]:
        """Return the subpackage parts if the file is in the package."""
        if not self.in_package:
            assert self.subpackage_parts_ is None
            raise ValueError(
                "subpackage_parts is only available for files in the package"
            )
        else:
            assert self.subpackage_parts_ is not None
            return self.subpackage_parts_

    @property
    def in_private_subpackage(self) -> bool:
        """Return whether the file is in a private subpackage."""
        if not self.in_package:
            assert self.in_private_subpackage_ is None
            raise ValueError(
                "in_private_subpackage is only available for files in "
                "the package"
            )
        else:
            assert self.in_private_subpackage_ is not None
            return self.in_private_subpackage_

    @property
    def module_name(self) -> str:
        """Return the module name if the file is in the package."""
        if not self.in_package:
            assert self.module_name_ is None
            raise ValueError(
                "module_name is only available for files in the package"
            )
        else:
            if self.is_init:
                assert self.module_name_ is None
                raise ValueError(
                    "module_name is not available for __init__.py files"
                )
            elif self.is_main:
                assert self.module_name_ is None
                raise ValueError(
                    "module_name is not available for __main__.py files"
                )
            else:
                assert self.module_name_ is not None
                return self.module_name_

    @property
    def is_private_module(self) -> bool:
        """Return whether the file is a private module."""
        if not self.in_package:
            assert self.is_private_module_ is None
            raise ValueError(
                "is_private_module is only available for files in the package"
            )
        else:
            assert self.is_private_module_ is not None
            return self.is_private_module_


def _prepare_file_context(
    package_name: str,
    package_root: pathlib.Path,
    tests_root: pathlib.Path,
    file_path: pathlib.Path,
) -> tuple[_FileContext | None, list[str]]:
    """Return the `FileContext` associated with `file_path`."""
    errors: list[str] = []

    in_package = python_import_style._is_inside_directory._is_inside_directory(
        file_path, package_root
    )
    in_tests = python_import_style._is_inside_directory._is_inside_directory(
        file_path, tests_root
    )
    if in_package and in_tests:
        python_import_style._append_rule_error._append_rule_error(
            errors,
            file_path,
            1,
            None,
            f"File {file_path} is inside both the package and the tests "
            "directories. Please ensure that the package and tests directories "
            "are separate.",
        )
        return None, errors

    is_init = file_path.name == "__init__.py"
    if is_init and not in_package:
        python_import_style._append_rule_error._append_rule_error(
            errors,
            file_path,
            1,
            None,
            f"File {file_path} is named __init__.py but is not inside the "
            "package directory.",
        )
        return None, errors

    is_main = file_path.name == "__main__.py"
    if is_main and not in_package:
        python_import_style._append_rule_error._append_rule_error(
            errors,
            file_path,
            1,
            None,
            f"File {file_path} is named __main__.py but is not inside the "
            "package directory.",
        )
        return None, errors

    if in_package:
        package_index = file_path.parts.index(package_name)
        subpackage_parts = file_path.parts[package_index + 1 : -1]
        in_private_subpackage = any(
            part.startswith("_") for part in subpackage_parts
        )
    else:
        subpackage_parts = None
        in_private_subpackage = None

    if in_package:
        if is_init or is_main:
            module_name = None
            is_private_module = False
        else:
            module_name = file_path.stem
            is_private_module = file_path.name.startswith("_")
    else:
        module_name = None
        is_private_module = None

    file_context = _FileContext(
        in_package=in_package,
        in_tests=in_tests,
        is_init=is_init,
        is_main=is_main,
        subpackage_parts_=subpackage_parts,
        in_private_subpackage_=in_private_subpackage,
        module_name_=module_name,
        is_private_module_=is_private_module,
    )
    return file_context, errors
