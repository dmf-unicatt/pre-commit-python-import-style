# Copyright (C) 2026 by the python-import-style pre-commit hook authors
#
# This file is part of the python-import-style pre-commit hook.
#
# SPDX-License-Identifier: MIT
"""Tests for python_import_style._prepare_file_context."""

import pathlib

import pytest
import test_utils

import python_import_style._prepare_file_context


def test_prepare_file_context_public_module_in_package_root(
    tmp_path: pathlib.Path,
) -> None:
    """Test file context creation for a public module in the package root."""
    package_name, package_root, tests_root = (
        test_utils._initialize_package_and_tests_dirs(tmp_path)
    )
    mod = package_root / "mod.py"
    mod.write_text("import os\n", encoding="utf-8")

    file_context, errors = (
        python_import_style._prepare_file_context._prepare_file_context(
            package_name=package_name,
            package_root=package_root,
            tests_root=tests_root,
            file_path=mod,
        )
    )
    assert file_context is not None
    assert len(errors) == 0

    assert file_context.in_package
    assert not file_context.in_tests
    assert not file_context.is_init
    assert not file_context.is_main
    assert file_context.subpackage_parts == ()
    assert not file_context.in_private_subpackage
    assert file_context.module_name == "mod"
    assert not file_context.is_private_module


def test_prepare_file_context_public_module_in_public_subpackage(
    tmp_path: pathlib.Path,
) -> None:
    """Test file context creation for a public module in a public subpackage.

    In particular, the subpackage_parts attribute will be a non-empty tuple.
    """
    package_name, package_root, tests_root = (
        test_utils._initialize_package_and_tests_dirs(tmp_path)
    )
    mod = package_root / "subpkg" / "mod.py"
    mod.parent.mkdir()
    mod.write_text("import os\n", encoding="utf-8")

    file_context, errors = (
        python_import_style._prepare_file_context._prepare_file_context(
            package_name=package_name,
            package_root=package_root,
            tests_root=tests_root,
            file_path=mod,
        )
    )
    assert file_context is not None
    assert len(errors) == 0

    assert file_context.in_package
    assert not file_context.in_tests
    assert not file_context.is_init
    assert not file_context.is_main
    assert file_context.subpackage_parts == ("subpkg",)
    assert not file_context.in_private_subpackage
    assert file_context.module_name == "mod"
    assert not file_context.is_private_module


def test_prepare_file_context_public_module_in_private_subpackage(
    tmp_path: pathlib.Path,
) -> None:
    """Test file context creation for a public module in a private subpackage.

    In particular, the subpackage_parts attribute will be a non-empty tuple,
    and the in_private_subpackage attribute will be True.
    """
    package_name, package_root, tests_root = (
        test_utils._initialize_package_and_tests_dirs(tmp_path)
    )
    mod = package_root / "_subpkg" / "mod.py"
    mod.parent.mkdir()
    mod.write_text("import os\n", encoding="utf-8")

    file_context, errors = (
        python_import_style._prepare_file_context._prepare_file_context(
            package_name=package_name,
            package_root=package_root,
            tests_root=tests_root,
            file_path=mod,
        )
    )
    assert file_context is not None
    assert len(errors) == 0

    assert file_context.in_package
    assert not file_context.in_tests
    assert not file_context.is_init
    assert not file_context.is_main
    assert file_context.subpackage_parts == ("_subpkg",)
    assert file_context.in_private_subpackage
    assert file_context.module_name == "mod"
    assert not file_context.is_private_module


def test_prepare_file_context_private_module_in_private_subpackage(
    tmp_path: pathlib.Path,
) -> None:
    """Test file context creation for a private module in a private subpackage.

    In particular, the subpackage_parts attribute will be a non-empty tuple,
    and both the in_private_subpackage and is_private_module attributes will
    be True.
    """
    package_name, package_root, tests_root = (
        test_utils._initialize_package_and_tests_dirs(tmp_path)
    )
    mod = package_root / "_subpkg" / "_mod.py"
    mod.parent.mkdir()
    mod.write_text("import os\n", encoding="utf-8")

    file_context, errors = (
        python_import_style._prepare_file_context._prepare_file_context(
            package_name=package_name,
            package_root=package_root,
            tests_root=tests_root,
            file_path=mod,
        )
    )
    assert file_context is not None
    assert len(errors) == 0

    assert file_context.in_package
    assert not file_context.in_tests
    assert not file_context.is_init
    assert not file_context.is_main
    assert file_context.subpackage_parts == ("_subpkg",)
    assert file_context.in_private_subpackage
    assert file_context.module_name == "_mod"
    assert file_context.is_private_module


@pytest.mark.parametrize("subpackage_name", ["", "subpkg", "_subpkg"])
@pytest.mark.parametrize("main_or_init", ["__init__.py", "__main__.py"])
def test_prepare_file_context_init_main_file(
    tmp_path: pathlib.Path,
    subpackage_name: str,
    main_or_init: str,
) -> None:
    """Test file context creation for an __init__.py or __main__.py file.

    In particular, the is_init or is_main attribute will be True, and
    the module_name attribute will raise a ValueError.
    """
    package_name, package_root, tests_root = (
        test_utils._initialize_package_and_tests_dirs(tmp_path)
    )
    mod = package_root / subpackage_name / main_or_init
    if subpackage_name != "":
        mod.parent.mkdir()
    mod.write_text("import os\n", encoding="utf-8")

    file_context, errors = (
        python_import_style._prepare_file_context._prepare_file_context(
            package_name=package_name,
            package_root=package_root,
            tests_root=tests_root,
            file_path=mod,
        )
    )
    assert file_context is not None
    assert len(errors) == 0

    assert file_context.in_package
    assert not file_context.in_tests
    if main_or_init == "__init__.py":
        assert file_context.is_init
        assert not file_context.is_main
    else:
        assert not file_context.is_init
        assert file_context.is_main
    if subpackage_name == "":
        assert file_context.subpackage_parts == ()
    else:
        assert file_context.subpackage_parts == (subpackage_name,)
    if subpackage_name == "_subpkg":
        assert file_context.in_private_subpackage
    else:
        assert not file_context.in_private_subpackage
    with pytest.raises(ValueError):
        _ = file_context.module_name
    assert not file_context.is_private_module


@pytest.mark.parametrize("in_tests", [True, False])
@pytest.mark.parametrize("mod_name", ["mod.py", "_mod.py"])
def test_prepare_file_context_module_outside_package_root(
    tmp_path: pathlib.Path,
    in_tests: bool,
    mod_name: str,
) -> None:
    """Test file context creation for a module outside of the package root."""
    package_name, package_root, tests_root = (
        test_utils._initialize_package_and_tests_dirs(tmp_path)
    )
    if in_tests:
        mod = tests_root / mod_name
    else:
        mod = tmp_path / "another_directory" / mod_name
        mod.parent.mkdir()
    mod.write_text("import os\n", encoding="utf-8")

    file_context, errors = (
        python_import_style._prepare_file_context._prepare_file_context(
            package_name=package_name,
            package_root=package_root,
            tests_root=tests_root,
            file_path=mod,
        )
    )
    assert file_context is not None
    assert len(errors) == 0

    assert not file_context.in_package
    if in_tests:
        assert file_context.in_tests
    else:
        assert not file_context.in_tests
    assert not file_context.is_init
    assert not file_context.is_main
    with pytest.raises(ValueError):
        _subpackage_parts = file_context.subpackage_parts
    with pytest.raises(ValueError):
        _in_private_subpackage = file_context.in_private_subpackage
    with pytest.raises(ValueError):
        _module_name = file_context.module_name
    with pytest.raises(ValueError):
        _is_private_module = file_context.is_private_module


def test_prepare_file_context_module_in_both_package_root_and_tests_root(
    tmp_path: pathlib.Path,
) -> None:
    """Test file context creation gives an error when a file is inside both the package and tests directories."""  # noqa: E501, W505
    package_name = "my_package"
    wrong_package_root = tmp_path
    wrong_tests_root = tmp_path
    mod = tmp_path / "mod.py"
    mod.write_text("import os\n", encoding="utf-8")

    file_context, errors = (
        python_import_style._prepare_file_context._prepare_file_context(
            package_name=package_name,
            package_root=wrong_package_root,
            tests_root=wrong_tests_root,
            file_path=mod,
        )
    )
    assert file_context is None
    assert len(errors) == 1
    assert (
        f"File {mod} is inside both the package and the tests directories"
        in errors[0]
    )


@pytest.mark.parametrize("in_tests", [True, False])
@pytest.mark.parametrize("mod_name", ["__init__.py", "__main__.py"])
def test_prepare_file_context_init_main_outside_package_root(
    tmp_path: pathlib.Path,
    in_tests: bool,
    mod_name: str,
) -> None:
    """Test file context creation gives an error for a __init__.py or __main__.py outside of the package root."""  # noqa: E501, W505
    package_name, package_root, tests_root = (
        test_utils._initialize_package_and_tests_dirs(tmp_path)
    )
    if in_tests:
        mod = tests_root / mod_name
    else:
        mod = tmp_path / "another_directory" / mod_name
        mod.parent.mkdir()
    mod.write_text("import os\n", encoding="utf-8")

    file_context, errors = (
        python_import_style._prepare_file_context._prepare_file_context(
            package_name=package_name,
            package_root=package_root,
            tests_root=tests_root,
            file_path=mod,
        )
    )
    assert file_context is None
    assert len(errors) == 1
    assert (
        f"File {mod} is named {mod_name} but is not inside the package "
        "directory" in errors[0]
    )
