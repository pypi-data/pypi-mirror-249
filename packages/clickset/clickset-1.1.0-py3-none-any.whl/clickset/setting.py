import confuse
import click
import inspect
import typing

from collections import namedtuple
from enum import Enum

from .config import ConfigPtr

class ClickParams:
    __slots__ = ('args', 'kwargs')
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

# Create a list of confuse datatypes
# ... Source methods: confuse.Subview.as_*
# ... This is used to create an Enum type for selecting Setting get return values
_confuse_types = [
    name.replace('as_', '').upper()
    for name,value
    in
    inspect.getmembers(
        confuse.Subview,
        lambda obj: hasattr(obj, '__name__') and obj.__name__.startswith('as_')
    )
]

class Setting:
    """An application setting linked to both `confuse` and `click` libraries.

    Settings may be taken from the following sources:

    - in-app defaults (`default` keyword)
    - confuse config file values (at `path` location)
    - command line arguments (defined by `option`)
    - runtime override values (when a new value is set)
    """
    _click_options = []

    Types = Enum('Types', _confuse_types)

    def __init__(
        self,
        path:       str|None,
        /,
        config:     str               = "default",
        *,
        default:    str|int|bool|None = None,
        type:       Types|None        = None,
        get_args:   typing.Any|None   = None,
        option:     ClickParams|None  = None
    ):
        """
        :param path: A dot notation indicating a confuse storage path (e.g. "key1.key2") or None to indicate memory only storage
        :param default: The in-app default value for the setting
        :param config: The name of a global (singletion) configuraiton instance to use for storage
        :param type: A confuse automated template used for getting (`confuse.Subview.as_<type>()`)
        :param get_args: Arguments passed to the confuse `get()` function (or `as_<type>()`)
        :param option: Create a click option for this value
        """
        # Do NOT attempt to load the actual configuration object here.
        # ... Doing so will invalidate the user configuration
        # ... Rather than detect the currenet state, simply save a reference
        # ... Remaining configuration can happen as it is needed.
        self._config     = ConfigPtr(config)
        self._path       = path
        self._configname = config
        self._name       = None
        self._default    = default
        self._get_args   = get_args
        self._type       = type
        self._configured = False

        if self._path is None:
            self._config = None
            self._value  = self._default
            self._as     = None

        if option is not None:
            option.kwargs['callback'] = self._click_option_set
            click_opt = click.option(*option.args, **option.kwargs)
            self._click_options.append(click_opt)

    def __setup(self):
        """
        Configure access to the confuse data struture.
        """
        # This configuration happens only after it is needed
        # ... This permits this class to be used at the class level code
        # ... While still permitting the user to correctly setup confuse
        if not self._configured:
            if self._path is not None:
                # Find the actual object referred to by the confuse path
                # ... Simply walk "down" the path until we reach the end
                self._value  = self._config.value
                for key in self._path.split('.'):
                    self._value = self._value[key]

                # Set the default value in confuse
                # ... this way we don't need to think about defaults
                if self._default is not None:
                    self._value.set_default(self._default)

                # Save the confuse data access method
                if self._type is not None:
                    self._as = getattr(self._value, f"as_{self._type.name.lower()}")
                else:
                    self._as = self._value.get

                # Mark the class as configured, this code should only run once!
                self._configured = True

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, obj, objtype = None):
        self.__setup()
        if obj is None:
            return self
        else:
            if self._path is None:
                return self._value
            else:
                if self._get_args is None:
                    return self._as()
                else:
                    return self._as(self._get_args)

    def __set__(self, obj, value):
        self.__setup()
        if self._path is None:
            self._value = value
        else:
            self._value.set_memory(value)

    def __delete__(self, obj):
        self.__setup()
        if self._path is None:
            self._value = self._default
        else:
            self._value.delete_from_memory()

    @classmethod
    def options(cls, func):
        for option in cls._click_options:
            func = option(func)

        return func

    def _click_option_set(self, ctx, param, value):
        self.__setup()
        if value is not None:
            if self._path is None:
                self._value = value
            elif self._path is not None:
                self._value.set_cli(value)
        return value

    def get(self):
        """
        Retrieve the value as configured by confuse and/or click.

        Example usage:

        >>> class Foo:
        ...     var = Setting('my.var', default = "hello world")
        ... value = Foo.var.get()
        ... value == "hello world"
        """
        self.__setup()
        if self._get_args is None:
            return self._as()
        else:
            return self._as(self._get_args)
