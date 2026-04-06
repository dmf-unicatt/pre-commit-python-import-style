# Copyright (C) 2026 by Francesco Ballarin
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT
"""Import-style checker package.

This module provides a small AST-based checker used by the pre-commit/prek
hook to enforce the project's import style rules.
"""

import ast
import collections.abc
import pathlib
import typing

IMPORT_STYLE = "import ..."
FROM_IMPORT_STYLE = "from ... import ..."


def check_import_style(
    file_name: str,
    source: str,
    preferred_style: collections.abc.Mapping[str, str],
) -> list[str]:
    """Check that imports follow the configured preferred style."""
    try:
        tree = ast.parse(source, filename=file_name)
    except SyntaxError as exc:
        line = exc.lineno or 1
        return [f"{file_name}:{line} -> syntax error while parsing file"]

    errors: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.level > 0 or node.module is None:
                errors.append(
                    f"{file_name}:{node.lineno} -> "
                    "relative imports are not allowed; use absolute imports"
                )
                continue

            module = node.module
            if module == "__future__":
                # Allow 'from __future__ import ...'
                continue
            expected_style = preferred_style.get(
                module.split(".")[0], preferred_style["*"]
            )
            actual_style = FROM_IMPORT_STYLE

            if actual_style != expected_style:
                errors.append(
                    f"{file_name}:{node.lineno} -> "
                    f"use 'import {module}' instead of "
                    f"'from {module} import ...'"
                )
        elif isinstance(node, ast.Import):
            for alias in node.names:
                module = alias.name
                expected_style = preferred_style.get(
                    module.split(".")[0], preferred_style["*"]
                )
                actual_style = IMPORT_STYLE

                if actual_style != expected_style:
                    errors.append(
                        f"{file_name}:{node.lineno} -> "
                        f"use 'from {module} import ...' instead of "
                        f"'import {module}'"
                    )

    return errors


def _is_python_file(path: pathlib.Path) -> bool:
    return path.is_file() and path.suffix == ".py"


def _style_for_file(
    file_path: pathlib.Path,
    root_dir: pathlib.Path,
    package_dir_prefix: str,
    package_name: str,
    tests_dir_name: str,
) -> dict[str, str] | None:
    resolved = file_path.resolve()
    package_root = (root_dir / package_dir_prefix / package_name).resolve()
    tests_root = (root_dir / tests_dir_name).resolve()

    try:
        resolved.relative_to(package_root)
        if resolved.name == "__init__.py":
            return {"*": IMPORT_STYLE, package_name: FROM_IMPORT_STYLE}
        return {"*": IMPORT_STYLE, package_name: IMPORT_STYLE}
    except ValueError:
        pass

    try:
        resolved.relative_to(tests_root)
        return {"*": IMPORT_STYLE}
    except ValueError:
        return None


def run_checks(
    files: list[pathlib.Path],
    root_dir: pathlib.Path,
    package_dir_prefix: str,
    package_name: str,
    tests_dir_name: str,
) -> list[str]:
    """Run import style checks on a list of files."""
    errors: list[str] = []

    for file_path in files:
        if not _is_python_file(file_path):
            continue

        preferred_style = _style_for_file(
            file_path=file_path,
            root_dir=root_dir,
            package_dir_prefix=package_dir_prefix,
            package_name=package_name,
            tests_dir_name=tests_dir_name,
        )
        if preferred_style is None:
            continue

        try:
            source = file_path.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"{file_path}:{1} -> cannot read file: {exc}")
            continue

        errors.extend(
            check_import_style(
                file_name=str(file_path),
                source=source,
                preferred_style=preferred_style,
            )
        )

    return errors
