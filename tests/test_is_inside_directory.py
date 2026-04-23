# Copyright (C) 2026 by the python-import-style pre-commit hook authors
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT
"""Tests for python_import_style._is_inside_directory."""

import pathlib

import python_import_style._is_inside_directory


def test_is_inside_directory_success(
    tmp_path: pathlib.Path,
) -> None:
    """Test that a file inside a directory is correctly identified."""
    dir_path = tmp_path / "subdir"
    dir_path.mkdir()
    file_path = dir_path / "file.py"
    file_path.write_text("# mock file\n", encoding="utf-8")

    assert python_import_style._is_inside_directory._is_inside_directory(
        file_path, dir_path
    )


def test_is_inside_directory_failure(
    tmp_path: pathlib.Path,
) -> None:
    """Test that a file outside a directory is correctly identified."""
    dir_path = tmp_path / "subdir"
    dir_path.mkdir()
    file_path = tmp_path / "file.py"
    file_path.write_text("# mock file\n", encoding="utf-8")

    assert not python_import_style._is_inside_directory._is_inside_directory(
        file_path, dir_path
    )
