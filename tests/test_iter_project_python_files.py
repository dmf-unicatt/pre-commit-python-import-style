# Copyright (C) 2026 by the python-import-style pre-commit hook authors
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT
"""Tests for python_import_style._iter_project_python_files."""

import pathlib
import subprocess

import python_import_style._iter_project_python_files


def test_iter_project_python_files(
    tmp_path: pathlib.Path,
) -> None:
    """Test listing all Python files under the project root."""
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

    assert (
        python_import_style._iter_project_python_files._iter_project_python_files(
            tmp_path
        )
        == [mod1]
    )
