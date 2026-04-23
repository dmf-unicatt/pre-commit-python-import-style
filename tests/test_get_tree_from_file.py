# Copyright (C) 2026 by the python-import-style pre-commit hook authors
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT
"""Tests for python_import_style._get_tree_from_file."""

import pathlib

import python_import_style._get_tree_from_file


def test_get_tree_from_file_success(
    tmp_path: pathlib.Path,
) -> None:
    """Test that a AST is correctly generated for a Python file."""
    mod = tmp_path / "mod.py"
    mod.write_text("import os\n", encoding="utf-8")

    tree, errors = python_import_style._get_tree_from_file._get_tree_from_file(
        mod
    )
    assert tree is not None
    assert len(errors) == 0


def test_get_tree_from_file_failure_non_existing_file(
    tmp_path: pathlib.Path,
) -> None:
    """Test that passing a non-existing file results in an error."""
    mod = tmp_path / "non_existing.py"

    tree, errors = python_import_style._get_tree_from_file._get_tree_from_file(
        mod
    )
    assert tree is None
    assert len(errors) == 1
    assert errors[0] == (
        f"{mod}:1 -> Error: cannot read file: [Errno 2] No such "
        f"file or directory: '{mod}'"
    )


def test_get_tree_from_file_failure_non_python_file(
    tmp_path: pathlib.Path,
) -> None:
    """Test that passing a non-Python file results in an error."""
    txt = tmp_path / "file.txt"
    txt.write_text("mock file\n", encoding="utf-8")

    tree, errors = python_import_style._get_tree_from_file._get_tree_from_file(
        txt
    )
    assert tree is None
    assert len(errors) == 1
    assert errors[0] == f"{txt}:1 -> Error: not a python file"


def test_get_tree_from_file_failure_syntax_error(
    tmp_path: pathlib.Path,
) -> None:
    """Test that AST parser gives an error for syntax errors."""
    mod = tmp_path / "mod.py"
    mod.write_text("import wrong-syntax\n", encoding="utf-8")

    tree, errors = python_import_style._get_tree_from_file._get_tree_from_file(
        mod
    )
    assert tree is None
    assert len(errors) == 1
    assert errors[0] == f"{mod}:1 -> Error: syntax error while parsing file"
