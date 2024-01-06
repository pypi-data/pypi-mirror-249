from importlib import metadata

# Single source the version string from package metadata
__version__ = metadata.version(__package__)

# Delete the metadata package to keep the main package import clean
del metadata

from .config import ConfigNotFound
from .config import Configuration
from .config import get_config
from .setting import ClickParams
from .setting import Setting

# Provide cick and confuse for ease of use with this package

import click
import confuse
