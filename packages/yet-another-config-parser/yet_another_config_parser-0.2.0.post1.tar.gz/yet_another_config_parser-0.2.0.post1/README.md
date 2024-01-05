# Yet another python config library

This library is designed to unify configuration parser, environment
variables and argument parser.

Usage:

    parser = ArgumentParser()
    section = parser.add_section("my_section")
    section.add_argument("--my-arg", dest="my_argument", type=int, default=42)
    
    parser.read_args(["--my-arg", "15"])
    
    # parser.my_section.my_argument is now an int equal to 15

Every parameter that is expected in configuration file should be
declared. Any undeclared paremeters are available as strings but can
be declared to apply proper type conversion. Parameter can optionally
be bound to an argument flag and/or to environment variable. Setting
through argument flag has priority over environment variable which has
priority over any configuration file.


## Classes

### ArgumentParser

#### `ArgumentParser(*, root_section_name="yacp-root", converters=None)`
Creates a new `ArgumentParser` object.
- `root_section_name` is the name of the section to store parameters
  added directly to the `ArgumentParser` object.
- `converters` is a dictionary of names and appropriate callables used
  to convert the value from string.

#### `add_argument(self, [name_or_flags], **kwargs)`
Add new argument to the root section of the configuration. See
`section.add_argument` below.

#### `add_section(self, name)`
Create a new config section and returns a handle to created section.
If section with the same name was already declared, return that
section instead. See `Section` class below.

#### `parse_args(self, args=None)`
Loads configuration from supplied list of arguments or `sys.argv[1:]`.

#### `read_string(self, config_string)`
Loads configuration from string as if it was loaded from file. Note:
root section parameters can be supplied without section header.

#### `read_file(self, fh)`
Loads configuration from an opened file handle. Note: root section
parameters can be supplied without section header.

#### `read(self, filenames)`
Loads configuration from list of files. If `filenames` is a single
string it is processed as a single configuration file. Note: unlike
`read_string` and `read_file` root section needs an explicit section
header.

#### `write(self, fh)`
Writes current configuration to an opened file handle. Note: only
writes values loaded from files or default values, not values from
arguments or environment.

#### `__getitem__(self, option)` (usually `self[option]`)
or
#### `__getattr__(self, option)` (usually `self.option`)
Returns either a root option or a section. Order of lookup:
- declared section
- declared root parameter
- undeclared section
- undeclared root parameter

Section or parameter is declared if it was registered using
`add_section`/`add_argument` and undeclared if it was only present in
a config file. It is possible to declare section or parameter after
reading the configuration. Getting an undeclared section automatically
declares it.

### Section

#### `add_argument(self, [name_or_flags], **kwargs)`
Adds a new parameter to the section. If `name_or_flags` is specified,
the argument is also registered as a command-line argument. `**kwargs`
can include the following:
- `action`: See [argparse action documentation]. Supported actions are
  `store` (default), `store_true`, `store_false` and `store_const`.
- `dest`: Name of the config parameter. Mandatory if `name_or_flags`
  is not specified.
- `env`: name of environment variable to load the parameter value
  - Note: the variable will only be checked once -- when the parameter
    is registered.
- `type`: (type or string) parameter type
  - `str`: string parameter, no processing
  - `int`: integer parameter
  - `float`: float parameter
  - `bool`: boolean parameter
  - anything else: appropriate converter is required (see
    ArgumentParser constructor above)
- `default`, `const`: See [argparse documentation].

Note: If `name_or_flags` is not provided and action is `store_const`,
actual `const` value will only be used to infer the parameter type.

Note: If `type` is not provided, type of `default` or `const` value
will be used. If neither is provided, type will be `'str'`.

Note: It is possible to add an argument after reading a configuration
file. This would apply correct type and environment variable override
(if any) to the value. However to apply command line argument
overrides, command line arguments have to be parsed again.

Note: `default` and `const` values are internally stored as strings.
For types where `str(value)` is not compatible with provided
converter, `default` and/or `const` should be provided in a format
suitable for converter with explicit `type` set.

Example:

    # given converter 'timedelta': lambda s: timedelta(seconds=int(s))

    section.add_argument("--delay", default=timedelta(seconds=10)) # ERROR
    section.add_argument("--delay", type=timedelta, default=10)    # ok

#### `__getitem__(self, option)` (usually `self[option]`)
or
####`__getattr__(self, option)` (usually `self.option`)
Returns value of `option` in this section. If parameter was added
using `add_argument`, it will be converted to either declared or
inferred type. If parameter was only present in the configuration
file, it will be returned as string.

[argparse action documentation]: https://docs.python.org/3/library/argparse.html#action
[argparse documentation]: https://docs.python.org/3/library/argparse.html#the-add-argument-method
