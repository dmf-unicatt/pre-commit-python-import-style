# Copyright (C) 2026 by the python-import-style pre-commit hook authors
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT
"""Tests for python_import_style._exclude_ignore_paths."""

import pathlib
import subprocess

import pytest

import python_import_style._exclude_ignore_paths


def test_exclude_ignore_paths(
    tmp_path: pathlib.Path,
) -> None:
    """Test that ignored files are excluded."""
    mod1 = tmp_path / "mod1.py"
    mod1.write_text("# mock file 1\n", encoding="utf-8")
    mod2 = tmp_path / "mod2.py"
    mod2.write_text("# mock file 2\n", encoding="utf-8")
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text("mod2.py\n", encoding="utf-8")
    subprocess.run(
        ["git", "init"],
        cwd=str(tmp_path),
        check=True,
    )

    assert python_import_style._exclude_ignore_paths._exclude_ignore_paths(
        tmp_path, [mod1, mod2]
    ) == [mod1]


def test_exclude_ignore_paths_no_gitignore(
    tmp_path: pathlib.Path,
) -> None:
    """Test that no files are ignored if there is no .gitignore file."""
    mod1 = tmp_path / "mod1.py"
    mod1.write_text("# mock file 1\n", encoding="utf-8")
    subprocess.run(
        ["git", "init"],
        cwd=str(tmp_path),
        check=True,
    )

    assert python_import_style._exclude_ignore_paths._exclude_ignore_paths(
        tmp_path, [mod1]
    ) == [mod1]


def test_exclude_ignore_paths_no_git_repository(
    tmp_path: pathlib.Path,
) -> None:
    """Test that an error is raised if there is no git repository."""
    mod1 = tmp_path / "mod1.py"
    mod1.write_text("# mock file 1\n", encoding="utf-8")

    with pytest.raises(RuntimeError):
        python_import_style._exclude_ignore_paths._exclude_ignore_paths(
            tmp_path, [mod1]
        )
