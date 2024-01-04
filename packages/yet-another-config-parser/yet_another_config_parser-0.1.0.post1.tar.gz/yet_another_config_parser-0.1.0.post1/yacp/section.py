"Module describing a single section of config."

from argparse import ArgumentParser
from os import environ


_AP_KEYWORDS = ['choices', 'const', 'default', 'help', 'metavar']


def _prepare_ap(dest, name_or_flags, param_type, kwargs):
    new_kwargs = {k: kwargs[k] for k in _AP_KEYWORDS if k in kwargs}
    if param_type == 'bool':
        new_kwargs['action'] = 'store_true'
    else:
        new_kwargs['action'] = 'store'
    new_kwargs['required'] = False
    new_kwargs['dest'] = dest
    if isinstance(name_or_flags, str):
        if name_or_flags[0] != '-':
            name_or_flags = f"--{name_or_flags}"
        name_or_flags = (name_or_flags,)
    return name_or_flags, new_kwargs


class Section:
    "Single section of config"

    def __init__(self, _name, config):
        self._parser = ArgumentParser()
        self._params = {}
        self._vars = {}
        self._env = {}
        self._config = config

    def add_parameter(self, name, *_args, **kwargs):
        "Add parameter to the section"
        param_type = kwargs.get('type', 'str')
        if isinstance(param_type, type):
            param_type = param_type.__name__.lower()
        self._params[name] = _mk_getter(name, param_type, **kwargs)
        if 'argument' in kwargs:
            ap_names, ap_kwargs = _prepare_ap(name, kwargs['argument'],
                                              param_type, kwargs)
            self._parser.add_argument(*ap_names, **ap_kwargs)
        if 'env' in kwargs and kwargs['env'] in environ:
            self._vars[name] = self._env[name] = environ[kwargs['env']]
        default = kwargs.get('default')
        if default is not None:
            self._config[name] = str(default)

    def read_args(self, args):
        "Read command-line arguments"
        args, _ = self._parser.parse_known_args(args)
        self._vars = {**self._env}
        self._vars.update(vars(args))

    def __getitem__(self, item):
        if item in self._params:
            return self._params[item](self._config, self._vars)
        raise KeyError(f"Key {item} is not defined in config")


def _type2func(typestr):
    match typestr:
        case "str": return "get"
        case "bool": return "getboolean"
        case _: return f"get{typestr}"


def _mk_getter(name, param_type, **kwargs):
    if param_type == 'bool':
        fallback = False
    else:
        fallback = None
    fallback = kwargs.get('default', fallback)
    funcname = _type2func(param_type)

    def getter(section_proxy, override):
        func = getattr(section_proxy, funcname)
        return func(name, vars=override, fallback=fallback)
    return getter
