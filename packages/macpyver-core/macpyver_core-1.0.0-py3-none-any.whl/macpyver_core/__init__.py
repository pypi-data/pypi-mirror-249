"""MacPyVer Core.

Core library for MacPyVer. Contains all the classes that are needed to retrieve
software from specific sources. There are no sources included in this library.
"""

from .model import Software  # noqa: F401
from .macpyver import MacPyVer  # noqa: F401
from .version_source import VersionSource  # noqa: F401

__version__ = '1.0.0'
