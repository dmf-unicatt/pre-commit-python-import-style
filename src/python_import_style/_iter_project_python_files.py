# Copyright (C) 2026 by the python-import-style pre-commit hook authors
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT
"""Return a list of Python source files under the project root."""

import pathlib

import python_import_style._exclude_ignore_paths


def _iter_project_python_files(
    project_root: pathlib.Path,
) -> list[pathlib.Path]:
    """Return a list of Python source files under `project_root`."""
    return python_import_style._exclude_ignore_paths._exclude_ignore_paths(
        project_root, [project_root / p for p in project_root.rglob("*.py")]
    )
