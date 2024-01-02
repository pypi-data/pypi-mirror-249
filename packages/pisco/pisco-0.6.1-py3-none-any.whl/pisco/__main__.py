"""Command-line entrypoint for pisco.

This module is executed when running `python -m pisco` from the command line.
"""

from pisco.user_interface import command_line_interface

command_line_interface.run()
