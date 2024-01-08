#! /usr/bin/env python
"""Tests for `cmd_line_history`.
"""

# Standard library imports.
from pathlib import Path

# Third party library imports.
import toml
import pytest

# First party library imports.
from berhoel import cmd_line_history

__date__ = "2024/01/07 20:00:16 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2020, 2024 by Berthold Höllmann"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"


@pytest.fixture
def base_path():
    result = Path(__file__).parent
    while not (result / "pyproject.toml").is_file():
        result = result.parent
    return result


@pytest.fixture
def config(base_path):
    return base_path / "pyproject.toml"


@pytest.fixture
def toml_data(config):
    return toml.load(config.open("r"))


def test_version(toml_data):
    """Testing for consistent version number."""
    assert cmd_line_history.__version__ == toml_data["tool"]["poetry"]["version"]
