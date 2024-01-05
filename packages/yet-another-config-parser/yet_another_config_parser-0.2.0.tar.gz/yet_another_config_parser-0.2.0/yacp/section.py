"Module describing a single section of config."

from argparse import ArgumentParser
from collections import namedtuple
from os import environ


_FlagIsSet = namedtuple("_FlagIsSet", ["value"])


class Section:
    "Single section of config"

    def __init__(self, name, config):
        self._name = name
        self._parser = ArgumentParser()
        self._params = {}
        self._vars = {}
        self._env = {}
        self._config = config

    def add_argument(self, *args, **kwargs):
        """Add argument to the section."""
        action, const = _update_kwargs_from_action(kwargs)
        if args:
            result = self._parser.add_argument(*args,
                                               action=action,
                                               const=const,
                                               dest=kwargs.get('dest'))
            name = result.dest
        elif 'dest' in kwargs:
            name = kwargs["dest"]
        else:
            raise TypeError("Missing both *args and dest")
        if name not in self._params:
            self._params[name] = _mk_getter(name, kwargs)
        if 'env' in kwargs and kwargs['env'] in environ:
            self._vars[name] = self._env[name] = environ[kwargs['env']]
        if 'default' in kwargs and name not in self._config:
            self._config[name] = str(kwargs['default'])

    def _has_declared_option(self, option):
        return option in self._params

    def _read_args(self, args):
        args, _ = self._parser.parse_known_args(args)
        self._vars = {**self._env}
        for k, v in vars(args).items():
            match v:
                case _FlagIsSet(value): self._vars[k] = value
                case None: pass
                case _: self._vars[k] = v

    def __getitem__(self, item):
        if item in self._params:
            return self._params[item](self._config, self._vars)
        if item in self._config:
            return self._config[item]
        raise KeyError(f"Key {item} is not defined in config")

    def __getattr__(self, item):
        return self[item]


def _get_func(kwargs):
    fallback_type = next((type(kwargs[k])
                          for k in ('default', 'const')
                          if k in kwargs),
                         'str')
    param_type = kwargs.get('type', fallback_type)
    if isinstance(param_type, type):
        param_type = param_type.__name__
    match param_type.lower():
        case "str": return "get"
        case "bool": return "getboolean"
        case other: return f"get{other}"


def _mk_getter(name, kwargs):
    fallback = kwargs.get('default')
    funcname = _get_func(kwargs)

    def getter(section_proxy, override):
        func = getattr(section_proxy, funcname)
        if override.get(name) is None:
            override = None
        return func(name, vars=override, fallback=fallback)
    return getter


def _update_kwargs_from_action(kwargs):
    match kwargs.get('action'):
        case 'store_true':
            kwargs.setdefault('default', False)
            return 'store_const', _FlagIsSet('true')
        case 'store_false':
            kwargs.setdefault('default', True)
            return 'store_const', _FlagIsSet('false')
        case 'store_const' if 'const' in kwargs:
            return 'store_const', _FlagIsSet(str(kwargs['const']))
        case action:
            return action, None
