"""
This module contains unit tests for the PythonClient class in the cdh_python_client module.
"""

import pytest
import os
import math
from cdh_dav_python.python_service.python_client import PythonClient


def test_list_classes_existing_module():
    """
    Test the 'list_classes' method when the module exists.
    """
    module_name = "os"
    expected_classes = [
        "DirEntry",
        "GenericAlias",
        "Mapping",
        "MutableMapping",
        "PathLike",
        "_AddedDllDirectory",
        "_Environ",
        "_wrap_close",
        "error",
        "stat_result",
        "statvfs_result",
        "terminal_size",
        "times_result",
        "uname_result",
    ]  # Expected list of classes in the 'os' module

    obj_python_client = PythonClient()

    classes = obj_python_client.list_classes(module_name)

    assert classes == expected_classes


def test_list_classes_nonexistent_module():
    """
    Test the 'list_classes' method when the module does not exist.
    """
    module_name = "nonexistent_module"

    obj_python_client = PythonClient()
    result = obj_python_client.list_classes(module_name)

    assert result == "Module 'nonexistent_module' not found."


def test_list_user_defined_classes_empty_module():
    """
    Test the 'list_classes' method when the module exists but has no classes.
    """
    module_name = "math"

    obj_python_client = PythonClient()
    classes = obj_python_client.list_user_defined_classes(module_name)

    assert classes == []


if __name__ == "__main__":
    pytest.main()
