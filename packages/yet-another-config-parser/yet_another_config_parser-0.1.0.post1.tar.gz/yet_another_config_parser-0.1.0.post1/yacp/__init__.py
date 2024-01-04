"""Main module of YetAnotherConfigParser package."""

from configparser import ConfigParser
from itertools import chain

from .section import Section


__all__ = ["ArgumentParser"]

_ROOT_NAME = "yacp-root"


class ArgumentParser:
    "Mostly uses the same interface as ArgumentParser"

    def __init__(self, converters=None):
        if converters is None:
            converters = {}
        self._config = ConfigParser(converters=converters)
        self._sections = {}
        self._root_section = self.add_section(_ROOT_NAME)
        self.read_string("")

    def add_parameter(self, name, *_args, **kwargs):
        "Register new parameter for root section"
        return self._root_section.add_parameter(name, *_args, **kwargs)

    def add_section(self, name):
        "Register new section for config"
        self._config.add_section(name)
        self._sections[name] = Section(name, self._config[name])
        return self._sections[name]

    def read_args(self, args):
        "Read command-line arguments"
        for section in self._sections.values():
            section.read_args(args)

    def __getitem__(self, item):
        if item in self._sections:
            return self._sections[item]
        return self._root_section[item]

    def read_string(self, config_string):
        "Read config string"
        return self._config.read_string(f"[{_ROOT_NAME}]\n{config_string}")

    def read_file(self, file):
        "Read config from iterable"
        return self._config.read_file(chain([f"[{_ROOT_NAME}]\n"], file))

    def read(self, filenames):
        "Read config from files"
        return self._config.read(filenames)

    def write(self, file):
        "Write config to file"
        return self._config.write(file)
