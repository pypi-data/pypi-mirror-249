#! /usr/bin/env python
"""Save command line history and provide a command line completer for python.
"""

# Standard library imports.
from atexit import register
from readline import set_pre_input_hook

# Local library imports.
from .history import History

__date__ = "2024/01/07 20:00:16 hoel"
__author__ = "Sunjoong LEE <sunjoong@gmail.com>"
__copyright__ = """Copyright © 2006 by Sunjoong LEE
Copyright © 2020, 2022, 2024 Berthold Höllmann"""
__credits__ = ["Sunjoong LEE", "Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"


__version__ = __import__("importlib.metadata", fromlist=["version"]).version(
    "pyCmdLineHistory"
)


def save_history(history_path=None):
    # Standard library imports.
    from readline import write_history_file

    # Local library imports.
    from .history import HISTORY_PATH

    if history_path is None:
        history_path = HISTORY_PATH
    write_history_file(history_path)


register(save_history)


def hook():
    # Standard library imports.
    from readline import set_pre_input_hook

    set_pre_input_hook()
    del locals()["History"]
    del locals()["__file__"]


set_pre_input_hook(hook)

locals()["__builtins__"]["history"] = History()
