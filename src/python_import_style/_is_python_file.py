# Copyright (C) 2026 by the python-import-style pre-commit hook authors
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT
"""Determine if a given file is a Python source file."""

import pathlib


def _is_python_file(path: pathlib.Path) -> bool:
    """Return True if `path` is a Python source file (suffix `.py`)."""
    return path.is_file() and path.suffix == ".py"
