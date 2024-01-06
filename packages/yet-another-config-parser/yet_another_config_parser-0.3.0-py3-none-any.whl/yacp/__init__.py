"""Main module of YetAnotherConfigParser package."""

from configparser import ConfigParser
from itertools import chain
from sys import argv

from .section import Section


__all__ = ["ArgumentParser"]


class ArgumentParser:
    "Mostly uses the same interface as ArgumentParser"

    def __init__(self, *,
                 envvar_prefix=None,
                 envvar_sep='__',
                 root_section_name="yacp-root",
                 converters=None):
        if converters is None:
            converters = {}
        self._config = ConfigParser(converters=converters, strict=False)
        self._sections = {}
        self._root_name = root_section_name
        self._envvar_prefix = envvar_prefix and envvar_prefix+'_'
        self._envvar_sep = envvar_sep
        self._root_section = self._create_section(self._root_name, True)

    def add_argument(self, *args, **kwargs):
        "Add argument to default section."
        return self._root_section.add_argument(*args, **kwargs)

    def add_section(self, name):
        "Register new section for config or return existing one"
        if name not in self._sections:
            self._sections[name] = self._create_section(name)
        return self._sections[name]

    def _create_section(self, name, is_root=False):
        if self._envvar_prefix is None:
            envvar_data = None
        else:
            prefixes = [name.lower().replace('-', '_')]
            if is_root:
                prefixes.append(None)
            envvar_data = (self._envvar_prefix, self._envvar_sep, prefixes)
        if name not in self._config:
            self._config.add_section(name)
        self._sections[name] = Section(name, self._config[name], envvar_data)
        return self._sections[name]

    def parse_args(self, args=None):
        "Read command-line arguments"
        if args is None:
            args = argv[1:]
        else:
            args = list(args)
        for section in self._sections.values():
            # pylint: disable=protected-access
            section._read_args(args)
            # pylint: enable=protected-access

    def __getitem__(self, item):
        if item in self._sections:
            return self._sections[item]
        # pylint: disable=protected-access
        if self._root_section._has_declared_option(item):
            return self._root_section[item]
        # pylint: disable=protected-access
        if item in self._config:  # it is a section found in config
            return self.add_section(item)
        return self._root_section[item]

    def __getattr__(self, item):
        return self[item]

    def read_string(self, config_string):
        "Read config string"
        config_string = f"[{self._root_name}]\n{config_string}"
        return self._config.read_string(config_string)

    def read_file(self, file):
        "Read config from iterable"
        return self._config.read_file(chain([f"[{self._root_name}]\n"], file))

    def read(self, filenames):
        "Read config from files"
        return self._config.read(filenames)

    def write(self, file):
        "Write config to file"
        return self._config.write(file)
