# ClickSet

ClickSet is a thin wrapper around the `click` and `confuse` libraries, combining
them both into a simple property-like interface for use with python classes.

```python
from clickset import Setting
from clickset import ClickParams
from clickset import get_config
import confuse
import click

class MyClass:
    verbose = Setting(
        # confuse storage path
        'general.verbose',

        # click boolean option
        option = ClickParams(
            '--verbose/--quiet',
            help = 'Verbose or Quiet Output'
        )
    )

    def my_func(self):
        # Get the value of a Setting
        print(f"verbose status: {self.verbose}")

        # Set the value of the property ... in memory only!
        self.verbose = False
        assert self.verbose == False

@click.command
# Load all options set in classes
@Setting.options
def main(**kw):
    # Get the default global confuse configuration singleton
    config = get_config()
    foo = MyClass()
    print(f"verbose: {foo.verbose}")
    assert foo.verbose == kw['verbose']
    assert foo.verbose == config['general']['verbose'].get()

    # confuse/click values can also be obtained directly from classes
    # ... NOTE: The value here is read-only!
    assert MyClass.verbose.get() == kw['verbose']

    # confuse/click values can also be obtained without a class
    verbose = Setting(
        # confuse storage path
        'general.verbose',

        # click boolean option
        option = ClickParams(
            '--verbose/--quiet',
            help = 'Verbose or Quiet Output'
        )
    )
    assert verbose == MyClass.verbose.get()
    assert verbose == foo.verbose

main(['--verbose'])
```

# Design Concepts

This library is built around the following design concept:

- Define app configuration in the class where it is used
- Link command line options to configuration file entries
- Permit multiple configuration files covering different purposes
- Provide a persistent application state storage mechanism
- Provide a simple interface which covers common use scenarios
- Provide as much access as possible to underlying libraries

These design concepts led me to utilizing two base libraries to provide
functionality:

- **confuse**: Provides configurable values to an application by providing multiple
  sources (memory, command line arguments, YAML files, etc.) in a priority based
  list.
- **click**: Provides a command line interface which is easily extended with
  additional funcitonality.

While both of these libraries are very powerful tools in their own right, they
both force their relevant settings into a central location.  In order to keep
all configuration settings in the location they are used, this library combines
`confuse` and `click` into a single class called `Setting`. The resulting class
has the following features:

- All data is stored using confuse
- Command line parameters provided by click are inserted into the confuse data
  store
- Data is accessed in the same mechanism as a python `property`
- Values can be overridden on a per-instance basis (same as setting a
  `property`)
- click/confuse values can obtained direclty using `Setting(...).get()` in order
  to easily obtain configured values outside of class restrictions (see the
  example above)

While this design is highly flexible, there are noteworthy drawbacks which must
be considered:

- `click` parameter definitions and `confuse` data stores must be defined as global
  singletons.
  - Generally this is acceptable as both configuration files and command line
    interfaces have one instance per application.
  - Multiple singletons can be created for both `confuse` and `click` in order
    to provide design flexibility.
- Command line options are *always* generated if the relevant class has been
  imported. This means that care must be taken with inactive code to ensure it
  is not imported by the main application.
  - This is generally a small risk if one is following good coding practices by
    importing only files which are used in a module.

