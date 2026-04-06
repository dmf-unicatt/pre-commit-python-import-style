# Copyright (C) 2026 by Francesco Ballarin
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT

"""Tests for the python_import_style checker."""

import pathlib
import runpy
import sys

import pytest

import python_import_style
import python_import_style.__main__


def test_check_import_style_only_from_import_form() -> None:
    """Verify sources that contain only 'from ... import ...'."""
    source = """\
from module1 import object1
from module2 import object2
from module2.submodule import object3
"""
    file_name = "test_only_from_import.py"

    preferred_style = {"*": "from ... import ..."}
    errors = python_import_style.check_import_style(
        file_name, source, preferred_style
    )
    assert len(errors) == 0

    preferred_style = {"*": "import ..."}
    errors = python_import_style.check_import_style(
        file_name, source, preferred_style
    )
    assert len(errors) == 3
    assert errors[0] == (
        f"{file_name}:1 -> use 'import module1' instead of "
        "'from module1 import ...'"
    )
    assert errors[1] == (
        f"{file_name}:2 -> use 'import module2' instead of "
        "'from module2 import ...'"
    )
    assert errors[2] == (
        f"{file_name}:3 -> use 'import module2.submodule' instead of "
        "'from module2.submodule import ...'"
    )


def test_check_import_style_only_import_form() -> None:
    """Verify sources that contain only 'import ...'."""
    source = """\
import module1
import module2
import module2.submodule
"""
    file_name = "test_only_import.py"

    preferred_style = {"*": "import ..."}
    errors = python_import_style.check_import_style(
        file_name, source, preferred_style
    )
    assert len(errors) == 0

    preferred_style = {"*": "from ... import ..."}
    errors = python_import_style.check_import_style(
        file_name, source, preferred_style
    )
    assert len(errors) == 3
    assert errors[0] == (
        f"{file_name}:1 -> use 'from module1 import ...' instead of "
        "'import module1'"
    )
    assert errors[1] == (
        f"{file_name}:2 -> use 'from module2 import ...' instead of "
        "'import module2'"
    )
    assert errors[2] == (
        f"{file_name}:3 -> use 'from module2.submodule import ...' instead of "
        "'import module2.submodule'"
    )


def test_check_import_style_mixed_forms() -> None:
    """Verify sources that contain a mix of import forms."""
    source = """\
import os

import module1
from module2 import object2
from module2.submodule import object3
"""
    file_name = "test_mixed.py"

    preferred_style = {
        "*": "import ...",
        "module1": "import ...",
        "module2": "from ... import ...",
    }
    errors = python_import_style.check_import_style(
        file_name, source, preferred_style
    )
    assert len(errors) == 0

    preferred_style = {
        "*": "import ...",
        "module1": "from ... import ...",
        "module2": "from ... import ...",
    }
    errors = python_import_style.check_import_style(
        file_name, source, preferred_style
    )
    assert len(errors) == 1
    assert errors[0] == (
        f"{file_name}:3 -> use 'from module1 import ...' instead of "
        "'import module1'"
    )

    preferred_style = {
        "*": "import ...",
        "module1": "import ...",
        "module2": "import ...",
    }
    errors = python_import_style.check_import_style(
        file_name, source, preferred_style
    )
    assert len(errors) == 2
    assert errors[0] == (
        f"{file_name}:4 -> use 'import module2' instead of "
        "'from module2 import ...'"
    )
    assert errors[1] == (
        f"{file_name}:5 -> use 'import module2.submodule' instead of "
        "'from module2.submodule import ...'"
    )


def test_check_import_style_syntax_error() -> None:
    """Ensure syntax errors in source return a helpful message."""
    source = "def broken(:\n"
    errs = python_import_style.check_import_style(
        "bad.py", source, {"*": "import ..."}
    )
    assert len(errs) == 1
    assert "syntax error while parsing file" in errs[0]


def test_check_import_style_relative() -> None:
    """Verify that relative imports are rejected."""
    rel = "from .module import name\n"
    errs = python_import_style.check_import_style(
        "rel.py", rel, {"*": "import ..."}
    )
    assert len(errs) == 1
    assert "relative imports are not allowed" in errs[0]


def test_check_import_style_relative_and_future() -> None:
    """Verify that from __future__ import is allowed."""
    fut = "from __future__ import annotations\n"
    errs = python_import_style.check_import_style(
        "fut.py", fut, {"*": "import ..."}
    )
    assert errs == []


def test_run_checks_for_flat_package_layout(tmp_path: pathlib.Path) -> None:
    """Run checks against a flat package layout (package at repo root)."""
    project_root = tmp_path
    package = project_root / "my_package"
    tests_dir = project_root / "tests"

    package.mkdir()
    tests_dir.mkdir()

    (package / "service.py").write_text(
        "import my_package.utils\n",
        encoding="utf-8",
    )
    (package / "__init__.py").write_text(
        "from my_package.service import Service\n",
        encoding="utf-8",
    )
    (tests_dir / "test_service.py").write_text(
        "import my_package\n",
        encoding="utf-8",
    )

    files = [
        package / "service.py",
        package / "__init__.py",
        tests_dir / "test_service.py",
    ]

    errors = python_import_style.run_checks(
        files=files,
        root_dir=project_root,
        package_dir_prefix=".",
        package_name="my_package",
        tests_dir_name="tests",
    )
    assert errors == []


def test_run_checks_for_src_package_layout(tmp_path: pathlib.Path) -> None:
    """Run checks against a `src/` package layout."""
    project_root = tmp_path
    src_dir = project_root / "src"
    package = src_dir / "my_package"
    tests_dir = project_root / "tests"

    src_dir.mkdir()
    package.mkdir()
    tests_dir.mkdir()

    (package / "service.py").write_text(
        "import my_package.utils\n",
        encoding="utf-8",
    )
    (package / "__init__.py").write_text(
        "from my_package.service import Service\n",
        encoding="utf-8",
    )
    (tests_dir / "test_service.py").write_text(
        "import my_package\n",
        encoding="utf-8",
    )

    files = [
        package / "service.py",
        package / "__init__.py",
        tests_dir / "test_service.py",
    ]

    errors = python_import_style.run_checks(
        files=files,
        root_dir=project_root,
        package_dir_prefix="src",
        package_name="my_package",
        tests_dir_name="tests",
    )
    assert errors == []


def test_run_checks_skips_non_files(
    tmp_path: pathlib.Path,
) -> None:
    """Ensure that run_checks skips non-files."""
    # non-file (directory)
    d = tmp_path / "somedir"
    d.mkdir()
    errors = python_import_style.run_checks(
        [d],
        root_dir=tmp_path,
        package_dir_prefix=".",
        package_name="pkg",
        tests_dir_name="tests",
    )
    assert errors == []


def test_run_checks_skips_python_and_outside_package(
    tmp_path: pathlib.Path,
) -> None:
    """Ensure that run_checks skips python files not in package/tests."""
    f = tmp_path / "outside.py"
    f.write_text("from os import path\n", encoding="utf-8")
    errors = python_import_style.run_checks(
        [f],
        root_dir=tmp_path,
        package_dir_prefix=".",
        package_name="pkg",
        tests_dir_name="tests",
    )
    assert errors == []


def test_run_checks_skips_non_python_files(
    tmp_path: pathlib.Path,
) -> None:
    """Ensure that run_checks skips non-python files."""
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    f = pkg / "file.txt"
    f.write_text("not python code\n", encoding="utf-8")
    errors = python_import_style.run_checks(
        [f],
        root_dir=tmp_path,
        package_dir_prefix=".",
        package_name="pkg",
        tests_dir_name="tests",
    )
    assert errors == []


def test_run_checks_read_text_oserror(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Verify that OSError is reported in the errors list."""
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    f = pkg / "broken.py"
    f.write_text("import os\n", encoding="utf-8")

    real_read_text = pathlib.Path.read_text

    def broken_read_text(
        self,  # noqa: ANN001
        encoding: str | None = None,
        errors: str | None = None,
    ) -> str:
        """Simulate an OSError when trying to read the file."""
        if self.resolve() == f.resolve():
            raise OSError("nope")
        return real_read_text(self, encoding=encoding, errors=errors)

    monkeypatch.setattr(pathlib.Path, "read_text", broken_read_text)

    errors = python_import_style.run_checks(
        [f],
        root_dir=tmp_path,
        package_dir_prefix=".",
        package_name="pkg",
        tests_dir_name="tests",
    )
    assert len(errors) == 1
    assert "cannot read file" in errors[0]


def test___main__cli_success_and(tmp_path: pathlib.Path) -> None:
    """Call the package CLI main() for a successful case."""
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    f = pkg / "file.py"
    f.write_text("import os\n", encoding="utf-8")
    rc = python_import_style.__main__.main(
        [str(f), "--root-dir", str(tmp_path), "--package-name", "pkg"]
    )
    assert rc == 0


def test___main__cli_failure(tmp_path: pathlib.Path) -> None:
    """Call the package CLI main() for a failing case."""
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    f = pkg / "file.py"
    f.write_text("from .x import y\n", encoding="utf-8")
    rc = python_import_style.__main__.main(
        [str(f), "--root-dir", str(tmp_path), "--package-name", "pkg"]
    )
    assert rc == 1


def test_run_module_executes_main(tmp_path: pathlib.Path) -> None:
    """Running the package with runpy as __main__ should execute and exit."""
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    f = pkg / "file.py"
    f.write_text("import os\n", encoding="utf-8")

    # Temporarily remove package modules from sys.modules to avoid the
    # RuntimeWarning that appears when runpy executes __main__ while the
    # package is already imported in the test process.
    removed = {}
    for k in list(sys.modules):
        if k == "python_import_style" or k.startswith("python_import_style."):
            removed[k] = sys.modules.pop(k)

    old_argv = sys.argv.copy()
    sys.argv[:] = [
        "python_import_style",
        str(f),
        "--root-dir",
        str(tmp_path),
        "--package-name",
        "pkg",
    ]
    try:
        with pytest.raises(SystemExit) as exc:
            runpy.run_module("python_import_style", run_name="__main__")
        assert exc.value.code == 0
    finally:
        sys.argv[:] = old_argv
        sys.modules.update(removed)
