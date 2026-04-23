# Copyright (C) 2026 by the python-import-style pre-commit hook authors
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT
"""Tests for python_import_style._is_python_file."""

import pathlib

import python_import_style._is_python_file


def test_is_python_file_success(
    tmp_path: pathlib.Path,
) -> None:
    """Test that a Python file is correctly identified."""
    mod = tmp_path / "mod.py"
    mod.write_text("# mock file\n", encoding="utf-8")

    assert python_import_style._is_python_file._is_python_file(mod)


def test_is_python_file_failure(
    tmp_path: pathlib.Path,
) -> None:
    """Test that a non-Python file is correctly identified."""
    txt = tmp_path / "file.txt"
    txt.write_text("mock file\n", encoding="utf-8")

    assert not python_import_style._is_python_file._is_python_file(txt)
