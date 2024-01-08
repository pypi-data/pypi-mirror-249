#! /usr/bin/env python
"""Handle command line history.
"""

# Standard library imports.
import sys
from pathlib import Path
from readline import (
    clear_history,
    set_completer,
    parse_and_bind,
    get_history_item,
    read_history_file,
    set_history_length,
    write_history_file,
    get_completer_delims,
    set_completer_delims,
    get_current_history_length,
)
from tempfile import mktemp
from itertools import count as icount

# Local library imports.
from .irl_completer import IrlCompleter

__date__ = "2024/01/07 20:00:15 hoel"
__author__ = "Sunjoong LEE <sunjoong@gmail.com>"
__copyright__ = """Copyright © 2006 by Sunjoong LEE
Copyright © 2020, 2022, 2024 Berthold Höllmann"""
__credits__ = ["Sunjoong LEE", "Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"

HISTORY_PATH = Path.home() / f".pyhistory{sys.version_info.major}"
HISTORY_LENGTH = 100


class History:
    def __init__(self):
        self.recall()
        set_history_length(HISTORY_LENGTH)

        parse_and_bind("tab: complete")
        delims = get_completer_delims()
        set_completer_delims(delims)
        set_completer(IrlCompleter().complete)

    def __repr__(self):
        """print out current history information"""
        length = get_current_history_length()
        if length > 1:
            try:
                return "\n".join(get_history_item(i) for i in range(1, length))
            except UnicodeDecodeError:
                return b"\n".join(get_history_item(i) for i in range(1, length))
        else:
            return ""

    def __call__(self):
        """print out current history information with line number"""
        length = get_current_history_length()
        if length > 1:
            kount = icount(1)
            for command in [get_history_item(i) for i in range(1, length)]:
                try:
                    print("{}\t{}".format(next(kount), command))
                except UnicodeDecodeError:
                    print(b"{}\t{}".format(next(kount), command))

    @staticmethod
    def save(filename, pos=None, end=None):
        """write history number from pos to end into filename file"""
        length = get_current_history_length()
        if length > 1:
            if not pos:
                pos = 1
            elif pos >= length - 1:
                pos = length - 1
            elif pos < 1:
                pos = length + pos - 1
            if not end:
                end = length
            elif end >= length:
                end = length
            if end < 0:
                end = length + end
            else:
                end = end + 1

            with open(filename, "w") as f_p:
                if pos < end:
                    for i in range(pos, end):
                        f_p.write("{}\n".format(get_history_item(i)))
                else:
                    f_p.write("{}\n".format(get_history_item(pos)))

    @staticmethod
    def clear():
        """save the current history and clear it"""
        write_history_file(HISTORY_PATH)
        clear_history()

    @staticmethod
    def recall(history_path=HISTORY_PATH):
        """clear the current history and recall it from saved"""
        clear_history()
        if history_path.exists():
            read_history_file(history_path)

    @staticmethod
    def execute(pos, end=None):
        """execute history number from pos to end"""
        length = get_current_history_length()
        if length > 1:
            if pos >= length - 1:
                pos = length - 1
            elif pos < 1:
                pos = length + pos - 1
            if not end:
                end = pos + 1
            elif end >= length:
                end = length
            if end < 0:
                end = length + end
            else:
                end = end + 1

            filename = Path(mktemp())
            with open(filename, "w") as f_p:
                for i in range(pos, end):
                    f_p.write(f"{get_history_item(i)}\n")
            try:
                with open(filename, "rb") as f_p:
                    exec(compile(f_p.read(), filename, "exec"), locals())
                read_history_file(filename)
            except Exception:
                pass
            filename.unlink()
