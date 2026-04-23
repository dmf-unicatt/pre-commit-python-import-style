# Copyright (C) 2026 by the python-import-style pre-commit hook authors
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT
"""Tests for python_import_style._append_rule_error."""

import pathlib

import python_import_style._append_rule_error


def test_append_rule_error_with_rule_number(
    tmp_path: pathlib.Path,
) -> None:
    """Test appending a rule error with a rule number."""
    mod = tmp_path / "mod.py"
    mod.write_text("# mock file\n", encoding="utf-8")

    errors: list[str] = []
    python_import_style._append_rule_error._append_rule_error(
        errors,
        file_path=mod,
        lineno=1,
        rule_number=1,
        message="this is a rule error",
    )
    assert errors == [f"{mod}:1 -> Rule 1: this is a rule error"]


def test_append_rule_error_without_rule_number(
    tmp_path: pathlib.Path,
) -> None:
    """Test appending a rule error without a rule number."""
    mod = tmp_path / "mod.py"
    mod.write_text("# mock file\n", encoding="utf-8")

    errors: list[str] = []
    python_import_style._append_rule_error._append_rule_error(
        errors,
        file_path=mod,
        lineno=1,
        rule_number=None,
        message="this is a generic error",
    )
    assert errors == [f"{mod}:1 -> Error: this is a generic error"]
