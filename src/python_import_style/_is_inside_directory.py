# Copyright (C) 2026 by the python-import-style pre-commit hook authors
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT
"""Determine if a file is inside a directory."""

import pathlib


def _is_inside_directory(
    file_path: pathlib.Path, dir_path: pathlib.Path
) -> bool:
    """Determine if `file_path` is inside the `dir_path` directory."""
    assert dir_path.is_absolute(), "Directory paths must be absolute"
    assert file_path.is_absolute(), "File paths must be absolute"
    assert dir_path.is_dir(), f"{dir_path} is not a directory"
    try:
        file_path.relative_to(dir_path)
    except ValueError:
        return False
    else:
        return True
