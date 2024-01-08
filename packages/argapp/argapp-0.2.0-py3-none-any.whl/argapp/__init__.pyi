'''
Wrapper for argparse and argcomplete.

Features the following:
 * Arg - a command line argument (positional or optional).
 * App - a command line application (main or sub-command).

Compatible with Python versions 3.6 - 3.11.
'''

from typing import overload


__all__ = [
    'Arg',
    'App',
]


class Arg:
    '''
    Represents a command line argument, optional or positional.

    A constructed instance is:
     * Added to a certain App.args as one of its command line arguments.
     * Is a key in args in App.__call__.

    The fields:
     * Are read-only and can be set once, via __init__.
     * Are validated during __init__.
     * May depend on other fields.
    '''

    @property
    def app(self) -> 'App':
        '''
        The application that contains the argument. The Arg is added to app.args.

        Must be set via __init__ as app:
         * type(app) must be App (TypeError).
         * app.args must not contain Arg with:
           1. The same lopt or sopt if is_optional is True (ValueError).
           2. The same name if is_positional is True (ValueError).
        '''

    @property
    def name(self) -> 'str':
        '''
        The value name: "URI" in "-u URI, --uri URI".

        May be set via __init__ as name:
         * type(name) must be str or None (TypeError).
         * len(name) must be greater than 0 (ValueError).

        Defaults:
        1. lopt.upper(), if lopt is not None.
        2. sopt.upper(), if sopt is not None.
        3. "ARG", if none of the above applies.
        '''

    @property
    def sopt(self) -> 'str | None':
        '''
        The short option name: "-u" in "-u URI, --uri URI".
         * The leading "-" must be ommited.
         * Makes the Arg optional.

        May be set via __init__ as sopt:
         * type(sopt) must be str or None (TypeError).
         * len(sopt) must be 1 (ValueError).
        '''

    @property
    def lopt(self) -> 'str | None':
        '''
        The long option name: "--uri" in "-u URI, --uri URI".
         * The leading "--" must be ommited.
         * Makes the Arg optional.

        May be set via __init__ as lopt:
         * type(lopt) must be str or None (TypeError).
         * len(lopt) must be greater than 0 (ValueError).
        '''

    @property
    def help(self) -> 'str':
        '''
        The help text.

        May be set via __init__ as help:
         * type(help) must be str or None (TypeError).

        If choices is not None, they are appended to the help text.
        help1 and help2 are only added if type(choices) == dict:

        Possible values:
         * value1 - help1
         * value2 - help2
         * (...)

        If default is not None, the following text is appended:

        Defaults to: value1 (value2, ...).

        Defaults:
        1. "".
        '''

    @property
    def count(self) -> 'int | str':
        '''
        The number of values consumed from the command line.

        May be set via __init__ as count:
         * type(count) must be int or str or None (TypeError).
         * If type(count) is int, count must be non-negative (ValueError).
         * If type(count) is int and is_positional is True, count must not be 0 (ValueError).
         * If type(count) is str, count must be one of: "?", "*", "+" (ValueError).

        Meaning of the string values:
         * "?" - zero or one values.
         * "*" - zero or more values.
         * "+" - one or more values.

        Defaults:
        1. "*", if type(default) is Iterable and not str.
        2. 1 otherwise.
        '''

    @property
    def type(self) -> 'type':
        '''
        The type of individual values.
        String values from the command line will be converted to this type.

        May be set via __init__ as type:
         * type(type) (type of the parameter) must be type (the built-in class) or None (TypeError).
         * If is_flag is True, type must be bool or None (ValueError).
         * type must be one of: str, int, float, bool, None (ValueError).

        Defaults:
        1. bool, if is_flag is True.
        2. type(choices[0]), if choices is not None.
        3. type(default[0]), if default is not [] and is_multi is True.
        4. type(default), if default is not None and is_single is True.
        5. str, if none of the above applies.
        '''

    @property
    def choices(self) -> 'list | dict | None':
        '''
        The list of allowed values. Can be dict, in this case:
         * keys are allowed argument values.
         * values are treated as the help text.

        May be set via __init__ as choices:
         * If is_flag is True, choices must be None (TypeError).
         * type(choices) must be Iterable or None (TypeError).
         * len(choices) must be greater than 0 (ValueError).
         * Type of each item is the same as type (TypeError).
         * Each item must be unique (ValueError).
        '''

    @property
    def default(self) -> 'object | None':
        '''
        The default value, if no values are provided for the argument.

        If is_optional is True, default is applied in both cases:
         * The argument was not mentioned at all.
         * The argument was mentioned, but without a value.
           This could be the case if count is "?" or "*".

        If is_flag is True, setting default to True changes the meaning of v in __call__:
        True means the argument was not mentioned, False - it was mentioned.

        May be set via __init__ as default, the restrictions depend on count.

        If is_flag is True:
         * default must be bool or None (TypeError).

        If is_single is True:
         * type(default) must be the same as type or None (TypeError).
         * If choices is not None, default is in choices (ValueError).

        If is_multi is True:
         * type(default) must be Iterable or None (TypeError).
         * Type of each item must be the same as type (TypeError).
         * If choices is not None, each item is in choices (ValueError).
         * If count is "+", default must not be empty (ValueError).
         * If count is int, len(default) must be equal to count (ValueError).

        Defaults to:
        1. False, if is_flag is True.
        3. None otherwise.
        '''

    @property
    def is_optional(self) -> 'bool':
        '''
        Whether the argument is optional.
         * Opposite to is_positional.
         * Cannot be set.
         * Not displayed in the usage.
         * If lopt is set, it is displayed in the help message with leading "--".
         * If sopt is set, it is displayed in the help message with leading "-".
         * The stylized name is displayed in the help message only if is_flag is False.

        Defaults:
        1. True, if sopt or lopt is not None.
        2. False otherwise.
        '''

    @property
    def is_positional(self) -> 'bool':
        '''
        Whether the argument is positional.
         * Opposite to is_optional.
         * Cannot be set.
         * The stylized name is displayed in the usage.
         * name is displayed in the help message.

        Defaults:
        1. True, if sopt and lopt are None.
        2. False otherwise.
        '''

    @property
    def is_flag(self) -> 'bool':
        '''
        Whether the argument does not consume values from the command line.
         * Cannot be True if is_single or is_multi is True.
         * Cannot be set.
         * name does not appear in the help message or the usage.

        Defaults:
        1. True, if count is 0.
        2. False otherwise.
        '''

    @property
    def is_single(self) -> 'bool':
        '''
        Whether the argument consumes at most one value from the command line.
         * Cannot be True if is_flag or is_multi is True.
         * Cannot be set.
         * The stylized name is the same as name if count is 1.
         * The stylized name is [name] if count is "?".

        Defaults:
        1. True, if count is 1 or "?".
        2. False otherwise.
        '''

    @property
    def is_multi(self) -> 'bool':
        '''
        Whether the argument may consume more than one value from the command line.
         * Cannot be True if is_flag or is_single is True.
         * Cannot be set.
         * The stylized name is name name name (repeated count times) if count is int.
         * The stylized name is [name...] if count is "*".
         * The stylized name is name [name...] if count is "+".

        Defaults:
        1. True, if count is greater than 1, or equals to "*" or "+".
        2. False otherwise.
        '''

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
        '''
        Construct the Arg and:
         * Initialize the fields.
         * Add the instance to app.args.

        Parameters match the corresponding fields.

        Exceptions:
        1. TypeError, if the type of some parameter is invalid (see the corresponding field).
        2. ValueError, if the value of some parameter is invalid (see the corresponding field).
        '''

    @overload
    def __call__(self, v: 'bool') -> 'bool':
        '''
        Parse the command line value:
         * Called if is_flag is True.
         * Can be overridden to return a custom value of any other type.
         * The base version simply returns the parameter.
         * The result is used as a value in the dictionary args in App.__call__.

        Parameters:
         *  * `v` - bool(not default), if the argument was mentioned, bool(default) otherwise.

        Returns:
         * v.
        '''

    @overload
    def __call__(self, v: 'str | None') -> 'str | int | float | bool | None':
        '''
        Parse the command line value:
         * Called if is_single is True.
         * The result is used as a value in the dictionary args in App.__call__.
         * Can be overridden to return a custom value of any other type.
           In this case, the base version should be called first to obtain the parsed value.

        The base version:
         * Checks if the value is in choices, if choices is not None.
         * Converts the value to type.

        Parameters:
         * v - The command line value. None, if the value was not provided.

        Exceptions:
         * RuntimeError, if choices is not None and v is not in choices.

        Returns:
        1. None, if v is None.
        2. v converted to type otherwise.
        '''

    @overload
    def __call__(self, v: 'list[str]') -> 'list[str | int | float | bool]':
        '''
        Parse the command line value:
         * Called if is_multi is True.
         * The result is used as a value in the dictionary args in App.__call__.
         * Can be overridden to return a custom value of any other type.
           In this case, the base version should be called first to obtain the parsed value.

        The base version:
         * Checks if each item is in choices, if choices is not None.
         * Converts the each item to type.

        Parameters:
         * v - The command line value. An empty list, if the value was not provided.

        Exceptions:
         * RuntimeError, if choices is not None and any item in v is not in choices.

        Returns:
        1. list of items from v converted to type.
        '''


class App:
    '''
    Represents a command line application (main or sub-command).

    The instance:
     * Works only with both the raw and the parsed command line if it is a main App.
     * Works only with the parsed command line if it is a sub-command App.
     * Is an item in apps in __call__.

    The fields:
     * Are read-only and can be set once, via __init__.
     * Are validated during __init__.
     * May depend on other fields.

    Instances of this class are internally converted to argparse.ArgumentParser:
     * Any App will provide the help message mechanism via an automatic argument "-h, --help".
       The default generation from argparse is not used, but the differences are small and mostly related to style.
     * If apps not empty, the App will provide the sub-commands mechanism via an automatic argument "CMD".
       Under the hood, argparse.ArgumentParser.add_subparsers is used to add the commands.
    '''

    @property
    def app(self) -> 'App | None':
        '''
        The parent application. The App is added to app.apps.

        May be set via __init__ as app:
         * type(app) must be App or None (TypeError).
         * app.apps must not contain App with the same name (ValueError).
        '''

    @property
    def name(self) -> 'str | None':
        '''
        The command's name, "git" in "git --version".

        May be set via __init__ as name:
         * type(name) must be str or None (TypeError).
         * If type(app) is App, name must not be None (TypeError).
         * len(name) must be greater than 0 (ValueError).

        If None, the command line help displays the first command line value as the application name.
        '''

    @property
    def help(self) -> 'str | None':
        '''
        The help text for a sub-command.

        May be set via __init__ as help:
         * type(help) must be str or None (TypeError).
        '''

    @property
    def prolog(self) -> 'str | None':
        '''
        The detailed help text before the argument lists.

        May be set via __init__ as prolog:
         * type(prolog) must be str or None (TypeError).

        Defaults:
        1. help.
        '''

    @property
    def epilog(self) -> 'str | None':
        '''
        The detailed help text after the argument lists.

        May be set via __init__ as epilog:
         * type(epilog) must be str or None (TypeError).
        '''

    @property
    def is_main(self) -> 'bool':
        '''
        Whether App is a main application.
         * Opposite to is_sub.
         * Cannot be set.

        Defaults:
        1. True, if app is None.
        2. False otherwise.
        '''

    @property
    def is_sub(self) -> 'bool':
        '''
        Whether App is a sub-command.
         * Opposite to is_main.
         * Cannot be set.

        Defaults:
        1. True, if app is not None.
        2. False otherwise.
        '''

    @property
    def args(self) -> 'list[Arg]':
        '''
        A list of App's arguments (Arg).
         * Populated by constructing an Arg with app set to the instance.
         * Must not be modified directly.

        Each Arg:
         * Is used for the help message generation: "usage", "positional arguments", "optional arguments".
         * Used as a key in the dictionary after the command line parsing.

        There are two automatic arguments that are never on the list:
         * -h, --help - Display the help message and exit, always the first optional argument.
         * CMD        - A sub-command to run, always the last positional argument. Appears only if apps is not empty.

        Defaults:
        1. [].
        '''

    @property
    def apps(self) -> 'list[App]':
        '''
        A list of App's sub-commands (App).
         * Populated by constructing an App with app set to the instance.
         * Must not be modified directly.

        Each App:
         * Is used for the help message generation.
         * Appears in its parent's help text for the "CMD" (see args).
         * Used as an item in the list after the command line parsing if called.

        Defaults:
        1. [].
        '''

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

    def __call__(
        self,
        argv: 'list[str]' = None,
    ) -> 'None':
        '''
        An overload of __call__ for the raw command line.
        It should never be overridden, use the other overload's signature for overriding.

        The functionality is as follows:
        1. Parse the provided command line (argv) into args (dict[Arg]) and apps (list[App]).
        2. If "-h, --help" is encountered, display the help message and exit with code 0.
        3. If there are any issues with parsing, display the usage message, the error, and exit with non-zero code.
        4. For each App in apps, call the other overload of __call__ passing args and apps as the parameter values.
        5. Exit with code 0 if there are no issues.
        6. Exit with code 1 and print an error if there are any issues.

        The help message structure is the same as in argparse, but there are specifics:
         * The usage shows only positional arguments.
         * All arguments are displayed in their respective sections in the order they were added.
           As for the automatic arguments:
           1. "-h, --help" is the very first argument.
           2. "CMD" is the very last argument, if present. Note that in the usage it appears as "CMD ...".
         * Optional arguments are displayed as "-a, --arg ARG", not "-a ARG, --arg ARG".
         * Newlines, spaces, tabs in the individual help texts are retained.
         * All arguments are aligned section-wise. Their help texts are properly padded.
         * An argument and its help text are always on the same line, no matter how wide the argument is.

        Parameters:
         * argv - A raw command line as list[str]. Effectively defaults to sys.argv, if None.
           The first item in the list must be the application name.

        Exceptions:
         * SystemExit, regardless of success (code 0) or failure (code 1).
        '''

    def __call__(
        self,
        args: 'dict[Arg]' = None,
        apps: 'list[App]' = None,
    ) -> 'None':
        '''
        An overload of __call__ for the parsed command line. The default implementation does nothing.
        It should be overridden, use this signature for overriding.

        It is mandatory to call super().__call__(args, apps) in the body before accessing args or apps.

        Parameters:
         * args - A dictionary containing each Arg and its value.
           The value is guaranteed to be set (can be None), so it is safe to use operator [].
         * apps - A call stack of Apps.
           The first item is the main App, the other items are sub-commands.
           The left-to-right order is preserved. Consider "git remote add":
           1. apps[0].name - "git"
           2. apps[1].name - "remote"
           3. apps[2].name - "add"
        '''
