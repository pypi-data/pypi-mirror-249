from importlib.metadata import version

__version__ = version('auror')

from auror import *

# This installs a slick, informational tracebacks
from rich.traceback import install

install(show_locals=True)
