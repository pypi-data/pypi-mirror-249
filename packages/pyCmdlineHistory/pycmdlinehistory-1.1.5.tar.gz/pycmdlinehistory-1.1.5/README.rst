..
  :Time-stamp: <2024-01-06 19:05:38 hoel>

pyCmdlineHistory
================

Shield: |CC BY-SA 4.0|

This work is licensed under a `Creative Commons Attribution-ShareAlike
4.0 International
License <http://creativecommons.org/licenses/by-sa/4.0/>`__.

|image1|

Save command line history and provide a command line completer for
python.

Original code is from `ActiveState Code »
Recipes <http://code.activestate.com/recipes/496822-completer-with-history-viewer-support-and-more-fea/>`__
2006.06.29 by `Sunjoong LEE <sunjoong@gmail.com>`__. ActiveState content
is published under `CC BY-SA
3.0 <http://creativecommons.org/licenses/by-sa/3.0/>`__.

Usage
-----

Insert the lines

.. code-block:: python

   import sys
   import subprocess

   try:
       import berhoel.cmd_line_history
   except ImportError:
       # checking if python is running under virtualenv of venv
       is_venv = (
           # This handles PEP 405 compliant virtual environments.
           (sys.prefix != getattr(sys, "base_prefix", sys.prefix))
           or
           # This handles virtual environments created with pypa's virtualenv.
           hasattr(sys, "real_prefix")
       )

       subprocess.check_call(
           [sys.executable, "-m", "pip", "install"]
           + ([] if is_venv else ["--user"])
           + ["pyCmdlineHistory",]
       )

to “~/.pystartup” file, and set an environment variable to point to it:

.. code-block:: shell

   export PYTHONSTARTUP=${HOME}/.pystartup

in bash.

This will locally install the module for each python you are calling.

Documentation
-------------

Documentation can be found `here <https://berhoel.gitlab.io/python/pyCmdlineHistory/>`_

References
----------

-  Guido van Rossum. Python Tutorial. Python Software Foundation, 2005.
   86
-  Jian Ding Chen. Indentable rlcompleter. Python Cookbook Recipe 496812
-  Guido van Rossum. rlcompleter.py. Python Software Foundation, 2005

2006.06.29 Sunjoong LEE sunjoong@gmail.com
2020 - 2023 Berthold Höllmann berhoel@gmail.com

.. |CC BY-SA 4.0| image:: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg
   :target: http://creativecommons.org/licenses/by-sa/4.0/
.. |image1| image:: https://licensebuttons.net/l/by-sa/4.0/88x31.png
   :target: http://creativecommons.org/licenses/by-sa/4.0/

..
  Local Variables:
  mode: rst
  compile-command: "make -C docs html"
  coding: utf-8
  End:
