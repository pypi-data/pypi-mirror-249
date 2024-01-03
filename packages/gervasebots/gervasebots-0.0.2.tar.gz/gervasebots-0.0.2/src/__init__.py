"""
GervaseBots Python API Wrapper
~~~~~~~~~~~~~~~~~~~~~~~~~
A basic wrapper for the GervaseBots API.
:copyright: (c) 2023 Tornike Bekauri & Gervase
:license: MIT, see LICENSE for more details.
"""

from collections import namedtuple

__title__ = "gervase"
__author__ = "Tornike Bekauri"
__license__ = "MIT"
__version__ = "0.0.1"

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")
major, minor, micro = (int(i) for i in __version__.split("."))
version_info = VersionInfo(
    major=major, minor=minor, micro=micro, releaselevel="final", serial=0
)

from .client import Client
from .errors import *