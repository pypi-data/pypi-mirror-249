from __future__ import annotations

import logging
logger = logging.getLogger(__name__)

import collections.abc
import confuse
from pathlib import Path
from confuse import ConfigSource
from confuse import YamlSource
from confuse import Subview

_configs = {}

class ConfigNotFound(KeyError): pass

class ConfigPtr:
    """
    A pointer to a configuration singleton.

    This is designed to be used by the clickset.Setting class, so that it can store
    a reference to Configuration object before it is created.
    """
    def __init__(self,
                 name: str = 'default'
                 ):
        """
        :param name: The unique singleton name associated with the Configuration object.
        """
        self.__name = name

    @property
    def value(self):
        """Get the real Configuration object"""
        try:
            return _configs[self.__name]
        except KeyError:
            raise ConfigNotFound(f"Configuration [{self.__name}] has not been configured")

    @property
    def name(self):
        """Get the name of the Configuration singleton configured at initialization"""
        return self.__name


class CliSource(ConfigSource):
    """A source which stores command line argument values.

    This class exists for clarity only with no added funcaitonality.
    """

class MemorySource(ConfigSource):
    """A source which stores app in-memory override values.

    This class exists for clarity only with no added funcaitonality.
    """

class AppSource(ConfigSource):
    """A source which stores coded app default values.

    This class exists for clarity only with no added funcaitonality.
    """

class Subview(confuse.Subview):
    def set_default(self, value):
        self.parent.set_default({self.key: value})

    def set_cli(self, value):
        self.parent.set_cli({self.key: value})

    def set_memory(self, value):
        self.parent.set_memory({self.key: value})

    def delete_from_memory(self, path=[]):
        self.parent.delete_from_memory([self.key]+path)

    def __getitem__(self, key):
        """Get a subview of this view."""
        return Subview(self, key)


class Configuration(confuse.Configuration):
    def __init__(self, *arg, **kw):
        super().__init__(*arg, **kw)

        self._memory  = MemorySource({}, default=False)
        self._cli     = CliSource({})
        self._default = AppSource({}, default=True)

        # Unify data sources by setting the order of prefrence for obtaining values:
        #
        # - Memory (new values set by the application)
        # - Command Line (values from click)
        # - User File Values
        # - Default File Values
        # - In-Memory Defaults
        #
        # However, at initialization there are no files loaded.
        # ... Begin with memory, cli, and in-app defaults

        super().add(self._memory)
        super().add(self._cli)
        super().add(self._default)

    def __getitem__(self, key):
        """Get a subview of this view."""
        return Subview(self, key)

    @property
    def source_cli(self):
        """The source used to store command line interface (CLI) parameters"""
        return self._cli

    @property
    def source_default(self):
        """The soruce used to store in-app default configuraiton values"""
        return self._default

    @property
    def source_memory(self):
        """The source used to store in-memory override values"""
        return self._memory

    def _deep_update(self, dst, updt):
        for key, val in updt.items():
            if isinstance(val, collections.abc.Mapping):
                dst[key] = self._deep_update(dst.get(key, {}), val)
            else:
                dst[key] = val
        return dst

    def set_default(self, value):
        """Update in-application default values (lowest priority)"""
        self._deep_update(self._default, value)

    def set_cli(self, value):
        """Update Command Line Interface (CLI) values (from click)"""
        self._deep_update(self._cli, value)

    def set_memory(self, value):
        """Update in-memory values set by the application"""
        self._deep_update(self._memory, value)

    def save(self, filename: str|Path):
        """Save all current files to a file"""
        filename = Path(filename)
        with filename.open('w') as fd:
            fd.write(self.dump())

    def delete_from_memory(self, path: list[str]):
        """Delete the specified value from memory overrides

        This will not touch other sources (file, CLI, environment, etc.)
        """

        pathkeys = path[:-1]
        endkey = path[-1]

        try:
            dct = self._memory
            while len(pathkeys) > 0:
                dct = dct[pathkeys.pop(0)]
            del dct[endkey]
        except KeyError as ex:
            # If any key in the provided path does not exist, nothing to do
            # ... meaning, the value to delete does not exist in the memory source
            pass

    def add(self, obj):
        """Add a new data source ABOVE in-app default values, BELOW everything else.

        [value set] > [cli args] > [existing sources] > [this source] > [in-app defaults]
        """
        source = ConfigSource.of(obj)

        # Insert the new source object before the last source
        # ... because the last source is used for in-app defaults
        # ... and just above that are pre-existing sources
        # Intuitively, this locatino doesn't make sense.
        # ... However, the location fits the required interface specified in confuse.ConfigView
        # ... And is logically correct for a unified storage model.
        # ... 'add' simply became a misleading name in the context of this library.
        self.sources.insert(-1, source)

    def add_file(self, *arg, **kw):
        """Load a YAML file as the lowest priority loaded file.

        All options are the same as confuse.YamlSource.

        Depiction of sources ordering with this method:

        [value set] > [cli args] > [existing files] > [this file] > [in-app defaults]
        """

        # Create the new source object
        source = YamlSource(*arg, **kw)

        # Insert the new source object before the last source
        # ... because the last source is used for in-app defaults
        # ... and just above that are file sources
        self.sources.insert(-1, source)

    def set_file(self, *arg, **kw):
        """Load a YAML file as the highest priority loaded file.

        All options are the same as confuse.YamlSource.

        Depiction of sources ordering with this method:

        [value set] > [cli args] > [this file] > [existing files] > [in-app defaults]
        """

        # Create the new source object
        source = YamlSource(*arg, **kw)

        # Determine where to insert the new source
        # ... This should be immediately BEFORE the first existing YamlSource
        # ... Or second to last if there are not YamlSource sources
        try:
            index = self.sources.index(next(filter(lambda src: type(src) == YamlSource, self.sources)))
        except StopIteration:
            index = -1

        # Insert based on the detected index
        self.sources.insert(index, source)

def get_config(
    name:        str           = 'default',
    *,
    appname:     str           = __package__.split('.')[0],
    modname:     str|None      = None,
    read:        bool          = False,
    configClass: Configuration = Configuration,
    **kw
) -> Configuration:
    """Get a global singleton configuration storage object
    :param name: A unique name referencing the storage object
    :param appname: The confuse appname used for config directory discovery
    :param read: If the default config file should be loaded
    :param configClass: The confuse Configuration class to instantiate if it does not already exist
    :returns: The configuration singleton
    """
    if not issubclass(configClass, confuse.Configuration):
        raise TypeError("configClass must be a subclass of confuse.Configuration!")

    # Get the requested configuration
    # ... creating the configuration if it does not exist already
    # ... configurations are global singletons so that settings can obtain them easily
    # ... Accepted this design because configurations should be created once per appliaction
    # ... Similar logic to why the python logging module uses global singletons
    config = _configs.setdefault(name, configClass(appname, read=False, modname=modname, **kw))

    # The configuration may already exist with a different appname
    # ... In this case, trust the user and change the appname
    # ... But also warn the user that this change happened
    if config.appname != appname:
        logger.warning(f"appname changed: [{config.appname}] => [{appname}]")
        config.appname = appname

    # The configuration may already exist with a different module search name
    # ... In this case, trust the user and change the appname
    # ... But also warn the user that this change happened
    if config.modname != modname:
        logger.warning(f"modname changed: [{config.modname}] => [{modname}]")
        config.modname = modname

    # NOTE: reading the config file (read=True) is deliberately handled after Configuration creation
    # ... This permits greater control over file loading
    # ... And ensures default confuse behavior does not override our customizations
    if read:
        config.read()

    return config

