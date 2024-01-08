import os
import sys
from argparse import ArgumentParser, Action
from typing import Iterable

try:
    from argcomplete import autocomplete
    from argcomplete.completers import ChoicesCompleter
except:
    def autocomplete(**kwargs) -> 'None':
        return

    class ChoicesCompleter:
        def __init__(self, choices) -> 'None':
            return


class Arg:
    '''
    See the pyi.
    '''

    @property
    def app(self) -> 'App':
        return self.__app

    @property
    def name(self) -> 'str':
        return self.__name

    @property
    def sopt(self) -> 'str | None':
        return self.__sopt

    @property
    def lopt(self) -> 'str | None':
        return self.__lopt

    @property
    def help(self) -> 'str | None':
        return self.__help

    @property
    def count(self) -> 'int | str':
        return self.__count

    @property
    def type(self) -> 'type':
        return self.__type

    @property
    def choices(self) -> 'list | dict | None':
        return self.__choices

    @property
    def default(self) -> 'object | None':
        return self.__default

    @property
    def is_optional(self) -> 'bool':
        return bool(self.sopt or self.lopt)

    @property
    def is_positional(self) -> 'bool':
        return not self.is_optional

    @property
    def is_flag(self) -> 'bool':
        return self.count == 0

    @property
    def is_single(self) -> 'bool':
        return self.count == 1 or self.count == '?'

    @property
    def is_multi(self) -> 'bool':
        return not (self.is_flag or self.is_single)

    def __init__(
        self,
        app: 'App',
        name: 'str | None' = None,
        sopt: 'str | None' = None,
        lopt: 'str | None' = None,
        help: 'str | None' = None,
        type: 'type | None' = None,
        count: 'int | str | None' = None,
        choices: 'list | dict | None' = None,
        default: 'object | None' = None,
    ) -> 'None':
        # Set immediately, so there is no need to pass the parameters.
        self.__app = app
        self.__name = name
        self.__sopt = sopt
        self.__lopt = lopt
        self.__help = help
        self.__type = type
        self.__count = count
        self.__choices = choices
        self.__default = default
        # The order matters, many fields depend on the others.
        self.__init_sopt()
        self.__init_lopt()
        self.__init_count()
        self.__init_type()
        self.__init_choices()
        self.__init_default()
        self.__init_name()
        self.__init_help()
        self.__init_app()

    def __init_sopt(self) -> 'None':
        if self.sopt == None:
            return
        name = 'Arg.sopt'
        _check_type(self.sopt,
                    name,
                    (str, None))
        _check_value(self.sopt,
                     name,
                     len(self.sopt) == 1,
                     'Must be a single character.')

    def __init_lopt(self) -> 'None':
        if self.lopt == None:
            return
        name = 'Arg.lopt'
        _check_type(self.lopt,
                    name,
                    (str, None))
        _check_value(self.lopt,
                     name,
                     len(self.lopt) != 0,
                     'Must be a non-empty str.')

    def __init_count(self) -> 'None':
        if self.count == None:
            is_iterable = isinstance(self.default, Iterable)
            is_str = isinstance(self.default, str)
            if is_iterable and not is_str:
                self.__count = '*'
            else:
                self.__count = 1
            return
        name = 'Arg.count'
        info = 'Must be non-negative int, "?", "*", "+".'
        _check_type(self.count,
                    name,
                    (int, str, None))
        if isinstance(self.count, int):
            if self.is_positional:
                _check_value(self.count,
                             name,
                             self.count != 0,
                             'Must not be 0 for positional arguments.')
            _check_value(self.count,
                         name,
                         self.count >= 0,
                         info)
        if isinstance(self.count, str):
            _check_value(self.count,
                         name,
                         self.count in ['?', '+', '*'],
                         info)

    def __init_type(self) -> 'None':
        name = 'Arg.type'
        if self.type == None:
            if self.is_flag:
                self.__type = bool
            elif self.choices and isinstance(self.choices, Iterable):
                self.__type = type(next(iter(self.choices)))
            elif self.default:
                if isinstance(self.default, Iterable):
                    self.__type = type(next(iter(self.default)))
                else:
                    self.__type = type(self.default)
            else:
                self.__type = str
        _check_type(self.type,
                    name,
                    (type, None))
        if self.is_flag:
            _check_value(self.type,
                         name,
                         issubclass(self.type, bool),
                         'Must be bool or None for flag argument.')
        else:
            _check_value(self.type,
                         name,
                         issubclass(self.type, (str, int, float, bool)),
                         'Must be str, int, float, bool or None.')

    def __init_choices(self) -> 'None':
        if self.choices == None:
            return
        name = 'Arg.choices'
        if self.is_flag:
            _check_type(self.choices,
                        f'{name} for flag',
                        (None,))
        else:
            _check_type(self.choices,
                        name,
                        (Iterable, None))
        _check_value(self.choices,
                     name,
                     len(self.choices) != 0,
                     'Must not be empty.')
        seen = set()
        name = f'item in {name}'
        for x in self.choices:
            _check_type(x,
                        name,
                        (self.type,))
            _check_value(x,
                         name,
                         x not in seen,
                         'Must be unique.')
            seen.add(x)

    def __init_default(self) -> 'None':
        name = 'Arg.default'
        if self.is_flag:
            _check_type(self.default,
                        name,
                        (bool, None))
            self.__default = bool(self.default)
            return
        if self.default == None:
            return
        if self.choices:
            choices_info = ', '.join(str(x) for x in self.choices)
            choices_info = f'Must be in Arg.choices: {choices_info}.'
        if self.is_single:
            _check_type(self.default,
                        name,
                        (self.type, None))
            if self.default != None and self.choices:
                _check_value(self.default,
                             name,
                             self.default in self.choices,
                             choices_info)
            return
        if self.is_multi:
            _check_type(self.default,
                        name,
                        (Iterable, None))
            if self.choices:
                for x in self.default:
                    _check_value(x,
                                 f'item in {name}',
                                 x in self.choices,
                                 choices_info)
            else:
                for x in self.default:
                    _check_type(x,
                                f'item in {name}',
                                (self.type,))
            if self.count == '+':
                _check_value(self.default,
                             f'{name} with Arg.count "+"',
                             len(self.default) > 0,
                             'Must not be empty.')
            if isinstance(self.count, int):
                _check_value(self.default,
                             name,
                             len(self.default) == self.count,
                             f'Must have exactly {self.count} items.')
            return

    def __init_help(self) -> 'None':
        name = 'Arg.help'
        _check_type(self.help,
                    name,
                    (str, None))
        self.__help = self.help or ''
        if self.is_flag:
            return
        if self.choices:
            if self.help:
                self.__help += '\n'
            self.__help += f'Possible values:{_choices(self.choices)}'
        if self.default != None:
            if self.help:
                self.__help += '\n'
            self.__help += 'Defaults to: '
            if self.is_single:
                self.__help += str(self.default)
            else:
                self.__help += ' '.join(str(x) for x in self.default)

    def __init_name(self) -> 'None':
        name = 'Arg.name'
        _check_type(self.name,
                    name,
                    (str, None))
        if self.name == None:
            if self.lopt != None:
                self.__name = self.lopt.upper()
            elif self.sopt != None:
                self.__name = self.sopt.upper()
            else:
                self.__name = 'ARG'
            return
        _check_value(self.name,
                     name,
                     self.name != '',
                     'Must not be empty.')

    def __init_app(self) -> 'None':
        name = 'Arg.app'
        _check_type(self.app,
                    name,
                    (App,))
        for x in self.app.args:
            name = self.app.name or 'main'
            if self.is_optional and x.is_optional:
                if self.lopt != None:
                    _check_value(self.lopt,
                                 'Arg.lopt',
                                 x.lopt != self.lopt,
                                 f'Must not repeat other Arg.lopt in {name} App.')
                if self.sopt != None:
                    _check_value(self.sopt,
                                 'Arg.sopt',
                                 x.sopt != self.sopt,
                                 f'Must not repeat other Arg.sopt in {name} App.')
            if self.is_positional and x.is_positional:
                _check_value(self.name,
                             'Arg.name',
                             x.name != self.name,
                             f'Must not repeat other Arg.name in {name} App.')
        self.app.args.append(self)

    def __call__(
        self,
        v: 'bool | str | list | None',
    ) -> 'str | int | float | bool | list | None':
        if self.is_flag:
            return self.__call_flag(v)
        if self.is_single:
            return self.__call_single(v)
        if self.is_multi:
            return self.__call_multi(v)

    def __call_flag(self, v: 'bool') -> 'bool':
        return v

    def __call_single(self, v: 'str | None') -> 'str | int | float | bool | None':
        if v == None:
            return self.default
        v = self.type(v)
        if not self.choices:
            return v
        if v in self.choices:
            return v
        name = self.lopt or self.sopt or self.name
        raise RuntimeError(
            f'Invalid value of argument {name}: {_str(v)}. '
            f'Must be one of:{_choices(self.choices)}')

    def __call_multi(self, v: 'list[str]') -> 'list[str | int | float | bool]':
        if not v:
            return self.default
        v = [self.type(x) for x in v]
        if not self.choices:
            return v
        for x in v:
            if x not in self.choices:
                name = self.lopt or self.sopt or self.name
                raise RuntimeError(
                    f'Invalid item in argument {name}: {_str(x)}. '
                    f'Must be one of:{_choices(self.choices)}')
        return v


class App:
    '''
    See the pyi.
    '''

    @property
    def app(self) -> 'App | None':
        return self.__app

    @property
    def name(self) -> 'str | None':
        return self.__name

    @property
    def help(self) -> 'str | None':
        return self.__help

    @property
    def prolog(self) -> 'str | None':
        return self.__prolog

    @property
    def epilog(self) -> 'str | None':
        return self.__epilog

    @property
    def is_main(self) -> 'bool':
        return not self.is_sub

    @property
    def is_sub(self) -> 'bool':
        return bool(self.app)

    @property
    def args(self) -> 'list[Arg]':
        return self.__args

    @property
    def apps(self) -> 'list[App]':
        return self.__apps

    def __init__(
        self,
        app: 'App | None' = None,
        name: 'str | None' = None,
        help: 'str | None' = None,
        prolog: 'str | None' = None,
        epilog: 'str | None' = None,
    ) -> 'None':
        '''
        Construct the App and:
         * Initialize the fields.
         * Add the instance to app.apps.

        Parameters match the corresponding fields.

        Exceptions:
        1. TypeError, if the type of some parameter is invalid (see the corresponding field).
        2. ValueError, if the value of some parameter is invalid (see the corresponding field).
        '''
        # Set immediately, so there is no need to pass the parameters.
        self.__app = app
        self.__name = name
        self.__help = help
        self.__prolog = prolog
        self.__epilog = epilog
        self.__args: 'list[Arg]' = []
        self.__apps: 'list[App]' = []
        # The order matters, some fields may depend on the others.
        self.__init_help()
        self.__init_prolog()
        self.__init_epilog()
        self.__init_name()
        self.__init_app()

    def __init_help(self) -> 'None':
        _check_type(self.help,
                    'App.help',
                    (str, None))

    def __init_prolog(self) -> 'None':
        _check_type(self.prolog,
                    'App.prolog',
                    (str, None))
        if self.prolog == None:
            self.__prolog = self.help

    def __init_epilog(self) -> 'None':
        _check_type(self.epilog,
                    'App.epilog',
                    (str, None))

    def __init_name(self) -> 'None':
        name = 'App.name'
        _check_type(self.name,
                    name,
                    (str, None))
        if self.is_sub:
            _check_type(self.name,
                        name + ' for sub-command',
                        (str,))
        _check_value(self.name,
                     name,
                     self.name != '',
                     'Must not be empty.')

    def __init_app(self) -> 'None':
        name = 'Arg.app'
        _check_type(self.app,
                    name,
                    (App, None))
        if self.app == None:
            return
        for x in self.app.apps:
            name = self.app.name or 'main'
            _check_value(self.name,
                         'App.name',
                         x.name != self.name,
                         f'Must not repeat other App.name in {name} App.')
        self.app.apps.append(self)

    def __call__(
        self,
        args: 'list[str] | dict[Arg]' = None,
        apps: 'list[App]' = None,
    ) -> 'None':
        if args == None:
            args = sys.argv
        if apps:
            return
        args = [str(x) for x in args]
        args, apps = Parser(self, args)()
        try:
            for x in apps:
                x(args, apps)
        except Exception as e:
            print(e, file=sys.stderr, flush=True)
            sys.exit(1)
        sys.exit(0)


class HelpFormatter:
    '''
    Generates help and usage.
    '''

    def __init__(self,  app: 'App', argv: 'list[str]') -> 'None':
        self._app = app
        self._argv = argv
        self._app_dummy = App()
        self._apps = app.apps
        self._args_opt = [x for x in app.args if x.is_optional]
        self._args_opt.insert(0, Arg(app=self._app_dummy,
                                     count=0,
                                     help='Show the help message and exit.',
                                     sopt='h',
                                     lopt='help'))
        self._args_pos = [x for x in app.args if x.is_positional]
        if app.apps:
            choices = {x.name: x.help for x in app.apps}
            self._args_pos.append(Arg(app=self._app_dummy,
                                      help=f'A sub-command to run.',
                                      choices=choices,
                                      name='CMD'))
        self.usage = self._format_usage()
        self.help = self._format_help()

    def _format_usage(self) -> 'str':
        result = ''
        app = self._app
        main = os.path.basename(self._argv[0])
        while app:
            result = f'{app.name or main} {result}'
            app = app.app
        result = result.rstrip()
        for x in self._args_pos:
            result = f'{result} {self._format_arg(x)}'
        if self._app.apps:
            result = f'{result} ...'
        return result

    def _format_help(self) -> 'str':
        usage = self.usage
        prolog = f'\n\n{self._app.prolog}' if self._app.prolog else ''
        argspos = f'\n\npositional arguments:{self._format_args(self._args_pos)}'
        argsopt = f'\n\noptional arguments:{self._format_args(self._args_opt)}'
        epilog = f'\n\n{self._app.epilog}' if self._app.epilog else ''
        if not self._args_pos:
            argspos = ''
        return f'{usage}{prolog}{argspos}{argsopt}{epilog}\n'

    def _format_arg(self, arg: 'Arg') -> 'str':
        result = ''
        if isinstance(arg.count, int):
            result = ' '.join([arg.name] * arg.count)
        if arg.count == '?':
            result = f'[{arg.name}]'
        if arg.count == '*':
            result = f'[{arg.name}...]'
        if arg.count == '+':
            result = f'{arg.name} [{arg.name}...]'
        if arg.is_optional:
            opts = []
            if arg.sopt:
                opts.append(f'-{arg.sopt}')
            if arg.lopt:
                opts.append(f'--{arg.lopt}')
            result = ', '.join(opts) + f' {result}'
        return result

    def _format_args(self, args: 'list[Arg]') -> 'str':
        result = ''
        if not args:
            return result
        if args[0].is_optional:
            w = max(len(self._format_arg(x)) for x in args)
        else:
            w = max(len(x.name) for x in args)
        for x in args:
            name = self._format_arg(x) if x.is_optional else x.name
            if x.help:
                pad = ' ' * (w + 6)
                lines = x.help.split('\n')
                result += f'\n  {name:{w}}    {lines[0]}'
                for i in range(1, len(lines)):
                    result += f'\n{pad}{lines[i]}'
            else:
                result += f'\n  {name:{w}}'
        return result


class HelpAction(Action):
    def __call__(self, *args: 'list', **kwargs: 'dict') -> 'None':
        print(self.help)
        exit(0)


class Parser:
    '''
    Encapsulates argparse and argcomplete. Not exposed to the user.
    '''

    def __init__(self, app: 'App', argv: 'list[str]') -> 'None':
        self.app = app
        self.argv = argv
        self.parser = self._construct(app, ArgumentParser(add_help=False))
        self.parser.prog = self.app.name or os.path.basename(self.argv[0])

    def __call__(self) -> 'tuple[dict[Arg], list[App]]':
        autocomplete(
            argument_parser=self.parser,
            always_complete_options=False,
        )
        parsed = self.parser.parse_args(self.argv[1:])
        apps: 'list[App]' = []
        args: 'dict[Arg]' = {}
        app = self.app
        while True:
            apps.append(app)
            # Parse arguments.
            for x in app.args:
                value = getattr(parsed, str(id(x)), None)
                if x.is_flag:
                    value = bool(value)
                    if x.default:
                        value = not value
                if x.count == 1 and value:
                    value = value[0]
                args[x] = x(value)
            # Continue with a sub-command.
            name = getattr(parsed, str(id(app)), None)
            if name == None:
                break
            for x in app.apps:
                if name == x.name:
                    app = x
                    break
        return (args, apps)

    def _construct(
        self,
        app: 'App',
        parser: 'ArgumentParser',
    ) -> 'ArgumentParser':
        # Set fields of the ArgumentParser.
        kwargs = Parser._app(app)
        formatter = HelpFormatter(app, self.argv)
        parser.usage = formatter.usage
        for k, v in kwargs.items():
            setattr(parser, k, v)
        # Add arguments to the ArgumentParser.
        parser.add_argument('-h', '--help',
                            action=HelpAction,
                            help=formatter.help,
                            nargs=0)
        for arg in app.args:
            kwargs = Parser._arg(arg)
            args = kwargs.pop('args')
            completer = kwargs.pop('completer')
            o = parser.add_argument(*args, **kwargs)
            setattr(o, 'completer', completer)
        # Recursively construct the sub-commands.
        if app.apps:
            sub = parser.add_subparsers(**Parser._sub(app))
            for x in app.apps:
                self._construct(x, sub.add_parser(x.name, add_help=False))
        return parser

    @staticmethod
    def _arg(o: 'Arg') -> 'dict[str]':
        '''
        Translate Arg to args and kwargs for ArgumentParser.add_argument().
        Note that the result contains two keys that must be used separately:
         * args      - must be used as positional args. Always present.
         * completer - must be set after the argument construction, because
                       argparse does not support custom fields.
        '''
        args = []
        kwargs = {
            'args': args,
            'dest': str(id(o)),
            'metavar': o.name,
            'nargs': o.count,
            'completer': None,
        }
        if o.choices:
            kwargs['completer'] = ChoicesCompleter([*o.choices])
        if o.is_optional:
            if o.sopt:
                args.append(f'-{o.sopt}')
            if o.lopt:
                args.append(f'--{o.lopt}')
            if o.is_flag:
                kwargs.pop('metavar')
                kwargs.pop('nargs')
                kwargs['action'] = 'store_true'
        return kwargs

    @staticmethod
    def _app(o: 'App') -> 'dict[str]':
        '''
        Translate App to kwargs for ArgumentParser.
        '''
        return {
            'prog': o.name,
        }

    @staticmethod
    def _sub(o: 'App') -> 'dict[str]':
        '''
        Translate App to kwargs for ArgumentParser.add_subparsers().
        Supposed to be used only for Apps with sub-commands.
        '''
        # Return kwargs.
        kwargs = {
            'dest': str(id(o)),
            'metavar': 'CMD',
        }
        if sys.version_info.minor >= 7:
            kwargs['required'] = True
        return kwargs


def _check_type(
    var: 'object',
    name: 'str',
    expected: 'Iterable[type]',
) -> 'None':
    types = []
    for x in expected:
        if x is None:
            x = type(None)
        if isinstance(var, x):
            return
        types.append('None' if x is type(None) else x.__name__)
    info = ", ".join(types)
    t = type(var).__name__ if var != None else 'None'
    raise TypeError(f'Invalid type of {name}: {t}. Expected: {info}.')


def _check_value(
    var: 'object',
    name: 'str',
    expected: 'bool',
    info: 'str',
) -> 'None':
    if expected:
        return
    raise ValueError(f'Invalid value of {name}: {_str(var)}. {info}')


def _str(v: 'object') -> 'str':
    if isinstance(v, str):
        return f'"{v}"'
    if isinstance(v, type):
        return v.__name__
    return str(v)


def _choices(choices: 'list | dict') -> 'str':
    result = ''
    if isinstance(choices, dict):
        w = max(len(str(x)) for x in choices)
        for x in choices:
            if choices[x]:
                help = '\n   '.join(str(choices[x]).split('\n'))
                result += f'\n * {str(x):{w}} - {help}'
            else:
                result += f'\n * {str(x):{w}}'
    else:
        result += '\n * '
        result += '\n * '.join(str(x) for x in choices)
    return result
