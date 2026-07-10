"""VDA5050 Python bindings.

Top-level package re-exporting the native client and Open-RMF migration
APIs.

Attributes
----------
__doc__ : str
    Module documentation string from the native extension.
__version__ : str
    Package version string.
"""

from __future__ import annotations

from ._client import *
from ._rmf_migration import *

__doc__: str
__version__: str
