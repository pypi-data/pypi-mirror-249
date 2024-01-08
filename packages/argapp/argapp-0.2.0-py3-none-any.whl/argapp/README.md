# argapp - A Python package for CLI application development

# Overview

argapp is an OOP wrapper for [argparse](https://docs.python.org/3/library/argparse.html) and [argcomplete](https://pypi.org/project/argcomplete):
 * Allows writing CLI applications using OOP - encapsulates argparse API.
 * Optionally supports shell completion via argcomplete - encapsulates its API.

## Features

 * Offers several classes that allow building a Python CLI application in OOP style.
    * `Arg` represents optional and positional arguments, with the most essential use cases covered.
    * `App` represents a main appplication or a sub-command.
    * Instances of the classes are immutable.
    * The fields are validated upon construction, raising an `Exception` in case of any issues.
    * The command line parsing can be overridden to return custom values for a specific `Arg`.
 * Offers shell completion support if argcomplete is installed:
    * The required API calls are already in place. It is only required to install argcomplete and add the `PYTHON_ARGCOMPLETE_OK` comment.
    * Specific completions (like from choices) are added automatically.

## Dependencies

 * Linux
 * Python 3
    * 3.6
    * 3.7
    * 3.8
    * 3.9
    * 3.10
    * 3.11

## Limitations

 * No "required" optional arguments.
 * No value aggregation (like for compilation flags).
 * No argument groups of any kind.
 * Choices are restrictive (cannot be disabled).
 * Completions cannot be customized.

# Installation

 * The package can be installed globally by running:
   ```shell
   pip3 install argapp
   ```
 * The Git [repository](https://github.com/deohayer/argapp) can be used directly if a specific version is needed.<br>
   The repository layout is designed with exactly this use case in mind.
 * For the argcomplete installation, please follow the official [documentation](https://pypi.org/project/argcomplete).

# API

## `argapp`

The package is the module by itself. It only exports its classes to not pollute the namespace.

### Example: Hello, world!

Below is `argapp.py` which prints a hello message with the given argument.

```python
#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

from argapp import Arg, App


class ExampleApp(App):  # Inherit App to override the construction and the runtime.
    def __init__(self) -> None:
        super().__init__(help='A minimalistic App.', epilog='Bottom text.')
        # Define a positional argument.
        self.arg = Arg(app=self,         # This is mandatory, adds Arg to App.
                       count='?',        # Make this argument non-required.
                       default='world',  # Provide a default value.
                       name='WHO')       # Provide a unique name (for the help message).

    def __call__(
        self,
        args: dict[Arg] = None,
        apps: list[App] = None,
    ) -> None:
        # A mandatory call to super(). The default implementation:
        #  * Parses the raw command line to populate args and apps.
        #  * Calls this method again with args and apps properly set.
        super().__call__(args, apps)
        # Retrieve the value using self.arg as the key, and print the message:
        print(f'Hello, {args[self.arg]}!')


# Construct and call.
ExampleApp()()
```

The help:

```shell
./argapp.py -h
# The output:
argapp.py [WHO]

A minimalistic App.

positional arguments:
  WHO    Defaults to: world

optional arguments:
  -h, --help     Show the help message and exit.

Bottom text.
```

The usage:

```shell
# No argument.
./argapp.py
# self.arg defaults to "world":
Hello, world!

#--------------------------------------------------------

# With argument.
./argapp.py John
# self.arg is "John":
Hello, John!
```

The completion:

```shell
./argapp.py -
# Upon pressing TAB, the following is displayed:
-h      --help
```

### `Arg`

Represents a command line argument, optional or positional.

A constructed instance is:
 * Added to a certain `App.args` as one of its command line arguments.
 * Used as a key in the dictionary `args` in `App.__call__`.

The fields:
 * Are read-only and can be set once, via `Arg.__init__`.
 * Are validated during `Arg.__init__`.
 * May depend on other fields.

#### Declaration

```python
class Arg:
    ...
```

#### Example

There are several best practices to follow:
 * Sub-class `Arg` to customize the construction or parsing.
 * Create `Arg` instances inside the `App` that will contain it (that is, in `App.__init__`).
 * Save the created `Arg` into an `App` field. In the dictionary of parsed values, `Arg` itself is the key, not its name.

Below is `argapp.py` which adds two integer values and prints the result.

```python
#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

from argapp import Arg, App


class ExampleArg(Arg):
    def __init__(self, app: App, name: str) -> None:
        # Encapsulate the construction.
        # Note that type is set to int for automatic conversion.
        super().__init__(app=app,
                         name=name,
                         type=int,
                         help=f'An example Arg: {name}.')


class ExampleApp(App):
    def __init__(self) -> None:
        super().__init__(help='Add a and b.')
        # Construct the Args.
        self.arg_a = ExampleArg(self, 'a')
        self.arg_b = ExampleArg(self, 'b')

    def __call__(
        self,
        args: dict[Arg] = None,
        apps: list[App] = None,
    ) -> None:
        super().__call__(args, apps)
        # Print the sum.
        a = args[self.arg_a]
        b = args[self.arg_b]
        print(f'a + b = {a} + {b} = {a + b}')


# Construct and call.
ExampleApp()()
```

The help:

```shell
./argapp.py -h
# The output:
argapp.py a b

Add a and b.

positional arguments:
  a    An example Arg: a.
  b    An example Arg: b.

optional arguments:
  -h, --help     Show the help message and exit.
```

The usage:

```shell
./argapp.py 6 -10
# The output:
a + b = 6 + -10 = -4
```

### `Arg.app`

The application that contains the argument. The `Arg` is added to `app.args`.

Must be set via `Arg.__init__` as `app`:
 * `type(app)` must be `App` (`TypeError`).
 * `app.args` must not contain `Arg` with:
   1. The same `Arg.lopt` or `Arg.sopt` if `Arg.is_optional` is `True` (`ValueError`).
   2. The same `Arg.name` if `Arg.is_positional` is `True` (`ValueError`).

#### Declaration

```python
@property
def app(self) -> App:
    ...
```

#### Example

```python
class ExampleApp(App):
    def __init__(self) -> None:
        super().__init__(name='argapp.py')
        # OK:
        #  * name of positional Args are different.
        #  * sopt and lopt of optional Args are different.
        #  * name of optional Args are not considered.
        #  * sopt, lopt, name of the same object do not clash.
        #  * Optional and positional Args cannot clash.
        self.arg_p1 = Arg(app=self,
                          name='a')
        self.arg_p2 = Arg(app=self,
                          name='b')
        self.arg_o1 = Arg(app=self,
                          name='a',
                          sopt='a',
                          lopt='a')
        self.arg_o2 = Arg(app=self,
                          name='b',
                          sopt='b',
                          lopt='b')
        self.arg_o3 = Arg(app=self,
                          name='a',
                          sopt='c',
                          lopt='c')
        # TypeError: Invalid type of Arg.app: None. Expected: App.
        self.arg2 = Arg(app=None)
        # TypeError: Invalid type of Arg.app: bool. Expected: App.
        self.arg2 = Arg(app=False)
        # ValueError: Invalid value of Arg.name: "a". Must not repeat other Arg.name in argapp.py App.
        self.arg1 = Arg(app=self,
                        name='a')
        self.arg2 = Arg(app=self,
                        name='a')
        # ValueError: Invalid value of Arg.sopt: "a". Must not repeat other Arg.sopt in argapp.py App.
        self.arg1 = Arg(app=self,
                        sopt='a')
        self.arg2 = Arg(app=self,
                        sopt='a')
        # ValueError: Invalid value of Arg.lopt: "a". Must not repeat other Arg.lopt in argapp.py App.
        self.arg1 = Arg(app=self,
                        lopt='a')
        self.arg2 = Arg(app=self,
                        lopt='a')
```

### `Arg.name`

The value name: `"URI"` in `"-u URI, --uri URI"`.

May be set via `Arg.__init__` as `name`:
 * `type(name)` must be `str` or `None` (`TypeError`).
 * `len(name)` must be greater than 0 (`ValueError`).

Defaults:
1. `Arg.lopt.upper()`, if `Arg.lopt` is not `None`.
2. `Arg.sopt.upper()`, if `Arg.sopt` is not `None`.
3. `"ARG"`, if none of the above applies.

#### Declaration

```python
@property
def name(self) -> str:
    ...
```

#### Example

```python
class ExampleApp(App):
    def __init__(self) -> None:
        super().__init__(name='argapp.py')
        # OK, the trivial case.
        self.arg = Arg(app=self,
                       name='arg')
        # OK, the name defaults to "ARG".
        self.arg = Arg(app=self)
        # OK, the name defaults to "O".
        self.arg = Arg(app=self,
                       sopt='o')
        # OK, the name defaults to "OPT".
        self.arg = Arg(app=self,
                       lopt='opt')
        # OK, the name defaults to "OPT" (lopt prioritized).
        self.arg = Arg(app=self,
                       sopt='o',
                       lopt='opt')
        # TypeError: Invalid type of Arg.name: bool. Expected: str, None.
        self.arg = Arg(app=self,
                       name=False)
        # ValueError: Invalid value of Arg.name: "". Must not be empty.
        self.arg = Arg(app=self,
                       name='')
```

### `Arg.sopt`

The short option name: `"-u"` in `"-u URI, --uri URI"`.
 * The leading `"-"` must be ommited.
 * Makes the `Arg` optional.

May be set via `Arg.__init__` as `sopt`:
 * `type(sopt)` must be `str` or `None` (`TypeError`).
 * `len(sopt)` must be 1 (`ValueError`).

#### Declaration

```python
@property
def sopt(self) -> str | None:
    ...
```

#### Example

```python
class ExampleApp(App):
    def __init__(self) -> None:
        super().__init__(name='argapp.py')
        # OK, the trivial case.
        self.arg = Arg(app=self,
                       sopt='a')
        # OK, sopt is None and the Arg is not optional.
        self.arg = Arg(app=self,
                       sopt=None)
        # TypeError: Invalid type of Arg.sopt: bool. Expected: str, None.
        self.arg = Arg(app=self,
                       sopt=False)
        # ValueError: Invalid value of Arg.sopt: "". Must be a single character.
        self.arg = Arg(app=self,
                       sopt='')
        # ValueError: Invalid value of Arg.sopt: "arg". Must be a single character.
        self.arg = Arg(app=self,
                       sopt='arg')
```

### `Arg.lopt`

The long option name: `"--uri"` in `"-u URI, --uri URI"`.
 * The leading `"--"` must be ommited.
 * Makes the `Arg` optional.

May be set via `Arg.__init__` as `lopt`:
 * `type(lopt)` must be `str` or `None` (`TypeError`).
 * `len(lopt)` must be greater than 0 (`ValueError`).

#### Declaration

```python
@property
def lopt(self) -> str | None:
    ...
```

#### Example

```python
class ExampleApp(App):
    def __init__(self) -> None:
        super().__init__(name='argapp.py')
        # OK, the trivial case.
        self.arg = Arg(app=self,
                       lopt='arg')
        # OK, lopt is None and the Arg is not optional.
        self.arg = Arg(app=self,
                       lopt=None)
        # TypeError: Invalid type of Arg.lopt: bool. Expected: str, None.
        self.arg = Arg(app=self,
                       lopt=False)
        # ValueError: Invalid value of Arg.lopt: "". Must be a non-empty str.
        self.arg = Arg(app=self,
                       lopt='')
```

### `Arg.help`

The help text.

May be set via `Arg.__init__` as `help`:
 * `type(help)` must be `str` or `None` (`TypeError`).

If `Arg.choices` is not `None`, the items are appended to the help text.
`help1` and `help2` are only added if `type(Arg.choices) == dict`:

```text
Possible values:
 * value1 - help1
 * value2 - help2
 * (...)
 ```

If `Arg.default` is not `None`, the following text is appended:

```text
Defaults to: value1 (value2, ...).
```

Defaults:
1. `""`.

#### Declaration

```python
@property
def help(self) -> str:
    ...
```

#### Example

```python
class ExampleApp(App):
    def __init__(self) -> None:
        super().__init__(name='argapp.py')
        # OK, the trivial case:
        #   ARG    A help text.
        self.arg = Arg(app=self,
                       help='A help text.')
        # OK, the newlines are retained and properly padded:
        #   ARG    This is a:
        #          1. Multiline.
        #          2. Help.
        #          3. Text.
        self.arg = Arg(app=self,
                       help=str(
                           'This is a:\n'
                           '1. Multiline.\n'
                           '2. Help.\n'
                           '3. Text.'))
        # OK, help defaults to "":
        #   ARG
        self.arg = Arg(app=self)
        # OK, choices list is appended:
        #   ARG    Possible values:
        #           * value1
        #           * value2
        self.arg = Arg(app=self,
                       choices=['value1', 'value2'])
        # OK, choices dict is appended:
        #   ARG    An Arg with choices.
        #          Possible values:
        #           * value1
        #           * value2 - help2
        self.arg = Arg(app=self,
                       help='An Arg with choices.',
                       choices={'value1': '', 'value2': 'help2'})
        # OK, default is appended:
        #   ARG    Defaults to: arg
        self.arg = Arg(app=self,
                       default='arg')
        # OK, default list is appended:
        #   ARG    An Arg with default.
        #          Defaults to: value1 value2
        self.arg = Arg(app=self,
                       count='*',
                       help='An Arg with default.',
                       default=['value1', 'value2'])
        # OK, both are appended:
        #   ARG    An Arg with both.
        #          Possible values:
        #           * value1
        #           * value2 - help2
        #          Defaults to: value1 value2
        self.arg = Arg(app=self,
                       count='*',
                       help='An Arg with both.',
                       choices={'value1': '', 'value2': 'help2'},
                       default=['value1', 'value2'])
        # TypeError: Invalid type of Arg.help: bool. Expected: str, None.
        self.arg = Arg(app=self,
                       help=False)
```

### `Arg.count`

The number of values consumed from the command line.

May be set via `Arg.__init__` as `count`:
 * `type(count)` must be `int` or `str` or `None` (`TypeError`).
 * If `type(count)` is `int`, `count` must be non-negative (`ValueError`).
 * If `type(count)` is `int` and `Arg.is_positional` is `True`, `count` must not be 0 (`ValueError`).
 * If `type(count)` is `str`, `count` must be one of: `"?"`, `"*"`, `"+"` (`ValueError`).<br>
   Meaning of the string values:
    * `"?"` - zero or one values.
    * `"*"` - zero or more values.
    * `"+"` - one or more values.

Defaults:
1. `"*"`, if `type(default)` is `Iterable` and not `str`.
2. 1 otherwise.

#### Declaration

```python
@property
def count(self) -> int | str:
    ...
```

#### Example

```python
class ExampleApp(App):
    def __init__(self) -> None:
        super().__init__(name='argapp.py')
        # OK, count deduced to 1.
        self.arg = Arg(app=self)
        # OK, count deduced to 1, even though str is Iterable.
        self.arg = Arg(app=self,
                       default='value')
        # OK, count deduced to "*".
        self.arg = Arg(app=self,
                       default=['value1', 'value2'])
        # OK, an explicit single value.
        self.argp = Arg(app=self,
                        count=1)
        self.argo = Arg(app=self,
                        count=1,
                        lopt='arg')
        # OK, a specific number of multiple values.
        self.argp = Arg(app=self,
                        count=2)
        self.argo = Arg(app=self,
                        count=2,
                        lopt='arg')
        # OK, an optional single value '?'.
        self.argp = Arg(app=self,
                        count='?')
        self.argo = Arg(app=self,
                        count='?',
                        lopt='arg')
        # OK, optional multiple values '*'.
        self.argp = Arg(app=self,
                        count='*')
        self.argo = Arg(app=self,
                        count='*',
                        lopt='arg')
        # OK, at least one value: '+'.
        self.argp = Arg(app=self,
                        count='+')
        self.argo = Arg(app=self,
                        count='+',
                        lopt='arg')
        # OK, zero values for optional - a flag.
        self.arg = Arg(app=self,
                       count=0,
                       lopt='arg')
        # ValueError: Invalid value of Arg.count: 0. Must not be 0 for positional arguments.
        self.arg = Arg(app=self,
                       count=0)
        # ValueError: Invalid value of Arg.count: -4. Must be non-negative int, "?", "*", "+".
        self.arg = Arg(app=self,
                       count=-4)
        # ValueError: Invalid value of Arg.count: "%". Must be non-negative int, "?", "*", "+".
        self.arg = Arg(app=self,
                       count='%')
        # TypeError: Invalid type of Arg.count: float. Expected: int, str, None.
        self.arg = Arg(app=self,
                       count=1.)
```

### `Arg.type`

The type of individual values.
String values from the command line will be converted to this type.

May be set via `Arg.__init__` as `type`:
 * `type(type)` (type of the parameter) must be `type` (the built-in class) or `None` (`TypeError`).
 * If `Arg.is_flag` is `True`, `type` must be `bool` or `None` (`ValueError`).
 * `type` must be one of: `str`, `int`, `float`, `bool`, `None` (`ValueError`).

Defaults:
1. `bool`, if `Arg.is_flag` is `True`.
2. `type(Arg.choices[0])`, if `Arg.choices` is not `None`.
3. `type(Arg.default[0])`, if `Arg.default` is not `[]` and `Arg.is_multi` is `True`.
4. `type(Arg.default)`, if `Arg.default` is not `None` and `Arg.is_single` is `True`.
5. `str`, if none of the above applies.

#### Declaration

```python
@property
def type(self) -> type:
    ...
```

#### Example

```python
class ExampleApp(App):
    def __init__(self) -> None:
        super().__init__(name='argapp.py')
        # OK, all trivial cases.
        self.arg1 = Arg(app=self,
                        type=str,
                        name='arg1')
        self.arg2 = Arg(app=self,
                        type=int,
                        name='arg2')
        self.arg3 = Arg(app=self,
                        type=float,
                        name='arg3')
        self.arg4 = Arg(app=self,
                        type=bool,
                        name='arg4')
        # OK, bool for flag explicitly.
        self.arg = Arg(app=self,
                       count=0,
                       type=bool,
                       lopt='arg')
        # OK, type is bool for flag.
        self.arg = Arg(app=self,
                       count=0,
                       lopt='arg')
        # OK, type is int - from choices.
        self.arg = Arg(app=self,
                       choices=[1, 2, 3])
        # OK, type is bool - from default (single).
        self.arg = Arg(app=self,
                       default=True,
                       lopt='arg')
        # OK, type is float - from default (multi).
        self.arg = Arg(app=self,
                       default=[1.0, 1.5, 2.0],
                       lopt='arg')
        # OK, type is str by default.
        self.arg = Arg(app=self)
        # TypeError: Invalid type of Arg.type: bool. Expected: type, None.
        self.arg = Arg(app=self,
                       type=False)
        # ValueError: Invalid value of Arg.type: int. Must be bool or None for flag argument.
        self.arg = Arg(app=self,
                       count=0,
                       type=int,
                       lopt='arg')
        # ValueError: Invalid value of Arg.type: list. Must be str, int, float, bool or None.
        self.arg = Arg(app=self,
                       type=list)
```

### `Arg.choices`

The list of allowed values. Can be `dict`, in this case:
 * `keys` are allowed argument values.
 * `values` are treated as the help text.

See `Arg.help` for the details.

May be set via `Arg.__init__` as `choices`:
 * If `Arg.is_flag` is `True`, `choices` must be `None` (`TypeError`).
 * `type(choices)` must be `Iterable` or `None` (`TypeError`).
 * `len(choices)` must be greater than 0 (`ValueError`).
 * Type of each item is the same as `Arg.type` (`TypeError`).
 * Each item must be unique (`ValueError`).

#### Declaration

```python
@property
def choices(self) -> list | dict | None:
    ...
```

#### Example

```python
class ExampleApp(App):
    def __init__(self) -> None:
        super().__init__(name='argapp.py')
        # OK, the list case:
        #   ARG    Possible values:
        #           * 1
        #           * 2
        #           * 3
        self.arg = Arg(app=self,
                       choices=[1, 2, 3])
        # OK, the dict case: the values are converted to str, can be complex objects:
        #   ARG    Possible values:
        #           * 1 - 100
        #           * 2 - 200
        #           * 3 - 300
        self.arg = Arg(app=self,
                       choices={1: 100, 2: 200, 3: 300})
        # OK, str is Iterable: equivalent to ['a', 'b', 'c']:
        #   ARG    Possible values:
        #           * a
        #           * b
        #           * c
        self.arg = Arg(app=self,
                       choices='abc')
        # TypeError: Invalid type of Arg.choices for flag: list. Expected: None.
        self.arg = Arg(app=self,
                       choices=[False, True],
                       count=0,
                       lopt='arg')
        # TypeError: Invalid type of Arg.choices: bool. Expected: Iterable, None.
        self.arg = Arg(app=self,
                       choices=False,
                       lopt='arg')
        # ValueError: Invalid value of Arg.choices: []. Must not be empty.
        self.arg = Arg(app=self,
                       choices=[],
                       lopt='arg')
        # TypeError: Invalid type of item in Arg.choices: str. Expected: int.
        self.arg = Arg(app=self,
                       choices=[1, '2'],
                       lopt='arg')
        # ValueError: Invalid value of item in Arg.choices: 1. Must be unique.
        self.arg = Arg(app=self,
                       choices=[1, 1],
                       lopt='arg')
```

### `Arg.default`

The default value, if no values are provided for the argument.

If `Arg.is_optional` is `True`, `Arg.default` is applied in both cases:
 * The argument was not mentioned at all.
 * The argument was mentioned, but without a value.
   This could be the case if `Arg.count` is `"?"` or `"*"`.

If `Arg.is_flag` is `True`, setting `Arg.default` to `True` changes the meaning of `v` in `Arg.__call__`:<br>
`True` means the argument was not mentioned, `False` - it was mentioned.

May be set via `Arg.__init__` as `default`, the restrictions depend on `Arg.count`.

If `Arg.is_flag` is `True`:
 * `default` must be `bool` or `None` (`TypeError`).

If `Arg.is_single` is `True`:
 * `type(default)` must be the same as `Arg.type` or `None` (`TypeError`).
 * If `Arg.choices` is not `None`, `default` is in `Arg.choices` (`ValueError`).

If `Arg.is_multi` is `True`:
 * `type(default)` must be `Iterable` or `None` (`TypeError`).
 * Type of each item must be the same as `Arg.type` (`TypeError`).
 * If `Arg.choices` is not `None`, each item is in `choices` (`ValueError`).
 * If `Arg.count` is `"+"`, `default` must not be empty (`ValueError`).
 * If `Arg.count` is `int`, `len(default)` must be equal to `Arg.count` (`ValueError`).

Defaults to:
1. `False`, if `Arg.is_flag` is `True`.
2. `[]`, if `Arg.is_multi` is `True`.
3. `None` otherwise.

#### Declaration

```python
@property
def choices(self) -> list | dict | None:
    ...
```

#### Example: `Arg.is_flag == True`

```python
class ExampleApp(App):
    def __init__(self) -> None:
        super().__init__(name='argapp.py')
        # OK, default is False.
        self.arg = Arg(app=self,
                       count=0,
                       lopt='arg')
        # OK, explicit False.
        self.arg = Arg(app=self,
                       default=False,
                       count=0,
                       lopt='arg')
        # OK, change the meaning: True - not mentioned, False - mentioned.
        self.arg = Arg(app=self,
                       default=True,
                       count=0,
                       lopt='arg')
        # TypeError: Invalid type of Arg.default: int. Expected: bool, None.
        self.arg = Arg(app=self,
                       default=0,
                       count=0,
                       lopt='arg')
```

#### Example: `Arg.is_single == True`

```python
class ExampleApp(App):
    def __init__(self) -> None:
        super().__init__(name='argapp.py')
        # OK, the trivial case.
        self.arg = Arg(app=self,
                       default='value',
                       lopt='arg')
        # OK, default is None.
        self.arg = Arg(app=self,
                       lopt='arg')
        # OK, default is in choices.
        self.arg = Arg(app=self,
                       default=2,
                       choices=[1, 2, 3],
                       lopt='arg')
        # TypeError: Invalid type of Arg.default: list. Expected: str, None.
        self.arg = Arg(app=self,
                       count=1,
                       default=[],
                       lopt='arg')
        # TypeError: Invalid type of Arg.default: str. Expected: int, None.
        self.arg = Arg(app=self,
                       type=int,
                       default='0',
                       lopt='arg')
        # ValueError: Invalid value of Arg.default: "d". Must be in Arg.choices: a, b, c.
        self.arg = Arg(app=self,
                       choices='abc',
                       default='d',
                       lopt='arg')
```

#### Example: `Arg.is_multi == True`

```python
class ExampleApp(App):
    def __init__(self) -> None:
        super().__init__(name='argapp.py')
        # OK, the trivial case.
        self.arg = Arg(app=self,
                       default=[1, 2, 3],
                       lopt='arg')
        # OK, default is None.
        self.arg = Arg(app=self,
                       count='+',
                       lopt='arg')
        # OK, default matches the explicit type.
        self.arg = Arg(app=self,
                       type=int,
                       default=[1, 2, 3],
                       lopt='arg')
        # OK, default is in choices.
        self.arg = Arg(app=self,
                       choices=[1, 2, 3],
                       default=[1, 3],
                       lopt='arg')
        # OK, default has the exact number of elements.
        self.arg = Arg(app=self,
                       count=2,
                       default=[1, 3],
                       lopt='arg')
        # OK, default has at least one element for "+".
        self.arg = Arg(app=self,
                       count='+',
                       default=[1],
                       lopt='arg')
        # OK, default may be empty for "*".
        self.arg = Arg(app=self,
                       count='*',
                       default=[],
                       lopt='arg')
        # OK, default has at least one element.
        self.arg = Arg(app=self,
                       count='+',
                       default=[1],
                       lopt='arg')
        # TypeError: Invalid type of Arg.default: bool. Expected: Iterable, None.
        self.arg = Arg(app=self,
                       count='+',
                       default=False,
                       lopt='arg')
        # TypeError: Invalid type of item in Arg.default: str. Expected: int.
        self.arg = Arg(app=self,
                       default=[1, 2, '3'],
                       lopt='arg')
        # ValueError: Invalid value of item in Arg.default: 4. Must be in Arg.choices: 1, 2, 3.
        self.arg = Arg(app=self,
                       choices=[1, 2, 3],
                       default=[1, 4],
                       lopt='arg')
        # ValueError: Invalid value of Arg.default with Arg.count "+": []. Must not be empty.
        self.arg = Arg(app=self,
                       count='+',
                       default=[],
                       lopt='arg')
        # ValueError: Invalid value of Arg.default: [1, 2, 3]. Must have exactly 2 items.
        self.arg = Arg(app=self,
                       count=2,
                       default=[1, 2, 3],
                       lopt='arg')
```

### `Arg.is_optional`

Whether the argument is optional.
 * Opposite to `Arg.is_positional`.
 * Cannot be set.
 * Not displayed in the usage.
 * If `Arg.lopt` is set, it is displayed in the help message with the leading `"--"`.
 * If `Arg.sopt` is set, it is displayed in the help message with the leading `"-"`.
 * The stylized `Arg.name` is displayed in the help message only if `Arg.is_flag` is `False`.

Defaults:
1. `True`, if `Arg.sopt` or `Arg.lopt` is not `None`.
2. `False` otherwise.

#### Declaration

```python
@property
def is_optional(self) -> bool:
    ...
```

#### Example

```python
#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

from argapp import Arg, App


class ExampleApp(App):
    def __init__(self) -> None:
        super().__init__(name='argapp.py')
        # Flag, does not have name.
        self.arg_flag = Arg(app=self,
                            help='A flag argument.',
                            count=0,
                            sopt='f',
                            lopt='flag')
        # Single-value, only sopt.
        self.arg_osingle = Arg(app=self,
                               help='A single-value optional argument.',
                               sopt='s')
        # Multi-value, only lopt.
        self.arg_omulti = Arg(app=self,
                              help='A multi-value optional argument.',
                              count='*',
                              lopt='multi')
        # Single-value, positional.
        self.arg_psingle = Arg(app=self,
                               help='A single-value positional argument.',
                               count='?',
                               name='psingle')
        # Multi-value, positional.
        self.arg_pmulti = Arg(app=self,
                              help='A multi-value positional argument.',
                              count='?',
                              name='pmulti')

    def __call__(
        self,
        args: dict[Arg] = None,
        apps: list[App] = None,
    ) -> None:
        super().__call__(args, apps)
        # Alignment for names - pretty output.
        w = max(len(x.lopt or x.sopt or x.name) for x in args) + 3
        for arg in args:
            # Determine and quote the name.
            name = f'"{arg.lopt or arg.sopt or arg.name}"'
            # Print whether the arguments are optional using Arg.is_optional.
            result = "optional" if arg.is_optional else "positional"
            print(f'Argument {name:{w}}: {result}.')


# Construct and call.
ExampleApp()()
```

The help:

```shell
./argapp.py -h
# The output:
argapp.py [psingle] [pmulti]

positional arguments:
  psingle    A single-value positional argument.
  pmulti     A multi-value positional argument.

optional arguments:
  -h, --help            Show the help message and exit.
  -f, --flag            A flag argument.
  -s S                  A single-value optional argument.
  --multi [MULTI...]    A multi-value optional argument.
```

The usage:

```shell
./argapp.py
# The output:
Argument "flag"    : optional.
Argument "s"       : optional.
Argument "multi"   : optional.
Argument "psingle" : positional.
Argument "pmulti"  : positional.
```

### `Arg.is_positional`

Whether the argument is positional.
 * Opposite to `Arg.is_optional`.
 * Cannot be set.
 * The stylized `Arg.name` is displayed in the usage.
 * `Arg.name` is displayed in the help message.

Defaults:
1. `True`, if `Arg.sopt` and `Arg.lopt` are `None`.
2. `False` otherwise.

#### Declaration

```python
@property
def is_positional(self) -> bool:
    ...
```

#### Example

```python
#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

from argapp import Arg, App


class ExampleApp(App):
    def __init__(self) -> None:
        super().__init__(name='argapp.py')
        # Flag, does not have name.
        self.arg_flag = Arg(app=self,
                            help='A flag argument.',
                            count=0,
                            sopt='f',
                            lopt='flag')
        # Single-value, only sopt.
        self.arg_osingle = Arg(app=self,
                               help='A single-value optional argument.',
                               sopt='s')
        # Multi-value, only lopt.
        self.arg_omulti = Arg(app=self,
                              help='A multi-value optional argument.',
                              count='*',
                              lopt='multi')
        # Single-value, positional.
        self.arg_psingle = Arg(app=self,
                               help='A single-value positional argument.',
                               count='?',
                               name='psingle')
        # Multi-value, positional.
        self.arg_pmulti = Arg(app=self,
                              help='A multi-value positional argument.',
                              count='?',
                              name='pmulti')

    def __call__(
        self,
        args: dict[Arg] = None,
        apps: list[App] = None,
    ) -> None:
        super().__call__(args, apps)
        # Alignment for names - pretty output.
        w = max(len(x.lopt or x.sopt or x.name) for x in args) + 3
        for arg in args:
            # Determine and quote the name.
            name = f'"{arg.lopt or arg.sopt or arg.name}"'
            # Print whether the arguments are positional using Arg.is_positional.
            result = "positional" if arg.is_positional else "optional"
            print(f'Argument {name:{w}}: {result}.')


# Construct and call.
ExampleApp()()
```

The help:

```shell
./argapp.py -h
# The output:
argapp.py [psingle] [pmulti]

positional arguments:
  psingle    A single-value positional argument.
  pmulti     A multi-value positional argument.

optional arguments:
  -h, --help            Show the help message and exit.
  -f, --flag            A flag argument.
  -s S                  A single-value optional argument.
  --multi [MULTI...]    A multi-value optional argument.
```

The usage:

```shell
./argapp.py
# The output:
Argument "flag"    : optional.
Argument "s"       : optional.
Argument "multi"   : optional.
Argument "psingle" : positional.
Argument "pmulti"  : positional.
```

### `Arg.is_flag`

Whether the argument does not consume values from the command line.
 * Cannot be `True` if `Arg.is_single` or `Arg.is_multi` is `True`.
 * Cannot be set.
 * `Arg.name` does not appear in the help message or the usage.

Defaults:
1. `True`, if `Arg.count` is 0.
2. `False` otherwise.

#### Declaration

```python
@property
def is_flag(self) -> bool:
    ...
```

#### Example

```python
#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

from argapp import Arg, App


class ExampleApp(App):
    def __init__(self) -> None:
        super().__init__(name='argapp.py')
        self.arg_of = Arg(app=self,
                          help='Flag optional, count 0.',
                          count=0,
                          sopt='f',
                          lopt='flag')
        self.arg_oss = Arg(app=self,
                           help='Single-value optional, count 1.',
                           count=1,
                           sopt='s',
                           lopt='single')
        self.arg_osq = Arg(app=self,
                           help='Single-value optional, count "?".',
                           count='?',
                           sopt='q',
                           lopt='qmark')
        self.arg_omt = Arg(app=self,
                           help='Multi-value optional, count 2.',
                           count=2,
                           sopt='t',
                           lopt='two')
        self.arg_omp = Arg(app=self,
                           help='Multi-value optional, count "+".',
                           count='+',
                           sopt='p',
                           lopt='plus')
        self.arg_oma = Arg(app=self,
                           help='Multi-value optional, count "*".',
                           count='*',
                           sopt='a',
                           lopt='astra')
        self.arg_pss = Arg(app=self,
                           help='Single-value positional, count 1.',
                           count=1,
                           name='SINGLE')
        self.arg_psq = Arg(app=self,
                           help='Single-value positional, count "?".',
                           count='?',
                           name='QMARK')
        self.arg_pmt = Arg(app=self,
                           help='Multi-value positional, count 2.',
                           count=2,
                           name='TWO')
        self.arg_pmp = Arg(app=self,
                           help='Multi-value positional, count "+".',
                           count='+',
                           name='PLUS')
        self.arg_pma = Arg(app=self,
                           help='Multi-value positional, count "*".',
                           count='*',
                           name='ASTRA')

    def __call__(
        self,
        args: dict[Arg] = None,
        apps: list[App] = None,
    ) -> None:
        super().__call__(args, apps)
        # Alignment for names - pretty output.
        w = max(len(x.lopt or x.name) for x in args) + 3
        for arg in args:
            # Determine and quote the name.
            name = f'"{arg.lopt or arg.name}"'
            # Print whether the arguments are flags using Arg.is_flag.
            result = "a flag" if arg.is_flag else "not a flag"
            print(f'Argument {name:{w}}: {result}.')


# Construct and call.
ExampleApp()()
```

The help:

```shell
./argapp.py -h
# The output:
argapp.py SINGLE [QMARK] TWO TWO PLUS [PLUS...] [ASTRA...]

positional arguments:
  SINGLE    Single-value positional, count 1.
  QMARK     Single-value positional, count "?".
  TWO       Multi-value positional, count 2.
  PLUS      Multi-value positional, count "+".
  ASTRA     Multi-value positional, count "*".

optional arguments:
  -h, --help                   Show the help message and exit.
  -f, --flag                   Flag optional, count 0.
  -s, --single SINGLE          Single-value optional, count 1.
  -q, --qmark [QMARK]          Single-value optional, count "?".
  -t, --two TWO TWO            Multi-value optional, count 2.
  -p, --plus PLUS [PLUS...]    Multi-value optional, count "+".
  -a, --astra [ASTRA...]       Multi-value optional, count "*".
```

The usage:

```shell
# Supply dummy values for positionals.
../argapp.py 0 0 0 0 0
# The output:
Argument "flag"   : a flag.
Argument "single" : not a flag.
Argument "qmark"  : not a flag.
Argument "two"    : not a flag.
Argument "plus"   : not a flag.
Argument "astra"  : not a flag.
Argument "SINGLE" : not a flag.
Argument "QMARK"  : not a flag.
Argument "TWO"    : not a flag.
Argument "PLUS"   : not a flag.
Argument "ASTRA"  : not a flag.
```

### `Arg.is_single`

Whether the argument consumes at most one value from the command line.
 * Cannot be `True` if `Arg.is_flag` or `Arg.is_multi` is `True`.
 * Cannot be set.
 * The stylized `Arg.name` is the same as `Arg.name` if `Arg.count` is 1.
 * The stylized `Arg.name` is `[Arg.name]` if `Arg.count` is `"?"`.

Defaults:
1. `True`, if `Arg.count` is 1 or `"?"`.
2. `False` otherwise.

#### Declaration

```python
@property
def is_single(self) -> bool:
    ...
```

#### Example

```python
#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

from argapp import Arg, App


class ExampleApp(App):
    def __init__(self) -> None:
        super().__init__(name='argapp.py')
        self.arg_of = Arg(app=self,
                          help='Flag optional, count 0.',
                          count=0,
                          sopt='f',
                          lopt='flag')
        self.arg_oss = Arg(app=self,
                           help='Single-value optional, count 1.',
                           count=1,
                           sopt='s',
                           lopt='single')
        self.arg_osq = Arg(app=self,
                           help='Single-value optional, count "?".',
                           count='?',
                           sopt='q',
                           lopt='qmark')
        self.arg_omt = Arg(app=self,
                           help='Multi-value optional, count 2.',
                           count=2,
                           sopt='t',
                           lopt='two')
        self.arg_omp = Arg(app=self,
                           help='Multi-value optional, count "+".',
                           count='+',
                           sopt='p',
                           lopt='plus')
        self.arg_oma = Arg(app=self,
                           help='Multi-value optional, count "*".',
                           count='*',
                           sopt='a',
                           lopt='astra')
        self.arg_pss = Arg(app=self,
                           help='Single-value positional, count 1.',
                           count=1,
                           name='SINGLE')
        self.arg_psq = Arg(app=self,
                           help='Single-value positional, count "?".',
                           count='?',
                           name='QMARK')
        self.arg_pmt = Arg(app=self,
                           help='Multi-value positional, count 2.',
                           count=2,
                           name='TWO')
        self.arg_pmp = Arg(app=self,
                           help='Multi-value positional, count "+".',
                           count='+',
                           name='PLUS')
        self.arg_pma = Arg(app=self,
                           help='Multi-value positional, count "*".',
                           count='*',
                           name='ASTRA')

    def __call__(
        self,
        args: dict[Arg] = None,
        apps: list[App] = None,
    ) -> None:
        super().__call__(args, apps)
        # Alignment for names - pretty output.
        w = max(len(x.lopt or x.name) for x in args) + 3
        for arg in args:
            # Determine and quote the name.
            name = f'"{arg.lopt or arg.name}"'
            # Print whether the arguments are single using Arg.is_single.
            result = "single" if arg.is_single else "not single"
            print(f'Argument {name:{w}}: {result}.')


# Construct and call.
ExampleApp()()
```

The help:

```shell
./argapp.py -h
# The output:
argapp.py SINGLE [QMARK] TWO TWO PLUS [PLUS...] [ASTRA...]

positional arguments:
  SINGLE    Single-value positional, count 1.
  QMARK     Single-value positional, count "?".
  TWO       Multi-value positional, count 2.
  PLUS      Multi-value positional, count "+".
  ASTRA     Multi-value positional, count "*".

optional arguments:
  -h, --help                   Show the help message and exit.
  -f, --flag                   Flag optional, count 0.
  -s, --single SINGLE          Single-value optional, count 1.
  -q, --qmark [QMARK]          Single-value optional, count "?".
  -t, --two TWO TWO            Multi-value optional, count 2.
  -p, --plus PLUS [PLUS...]    Multi-value optional, count "+".
  -a, --astra [ASTRA...]       Multi-value optional, count "*".
```

The usage:

```shell
# Supply dummy values for positionals.
../argapp.py 0 0 0 0 0
# The output:
Argument "flag"   : not single.
Argument "single" : single.
Argument "qmark"  : single.
Argument "two"    : not single.
Argument "plus"   : not single.
Argument "astra"  : not single.
Argument "SINGLE" : single.
Argument "QMARK"  : single.
Argument "TWO"    : not single.
Argument "PLUS"   : not single.
Argument "ASTRA"  : not single.
```

### `Arg.is_multi`

Whether the argument may consume more than one value from the command line.
 * Cannot be `True` if `Arg.is_flag` or `Arg.is_single` is `True`.
 * Cannot be set.
 * The stylized `Arg.name` is `Arg.name Arg.name Arg.name` (repeated `Arg.count` times) if `Arg.count` is `int`.
 * The stylized `Arg.name` is `[Arg.name...]` if `Arg.count` is `"*"`.
 * The stylized `Arg.name` is `Arg.name [Arg.name...]` if `Arg.count` is `"+"`.

Defaults:
1. `True`, if `Arg.count` is greater than 1, or equals to `"*"` or `"+"`.
2. `False` otherwise.

#### Declaration

```python
@property
def is_multi(self) -> bool:
    ...
```

#### Example

```python
#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

from argapp import Arg, App


class ExampleApp(App):
    def __init__(self) -> None:
        super().__init__(name='argapp.py')
        self.arg_of = Arg(app=self,
                          help='Flag optional, count 0.',
                          count=0,
                          sopt='f',
                          lopt='flag')
        self.arg_oss = Arg(app=self,
                           help='Single-value optional, count 1.',
                           count=1,
                           sopt='s',
                           lopt='single')
        self.arg_osq = Arg(app=self,
                           help='Single-value optional, count "?".',
                           count='?',
                           sopt='q',
                           lopt='qmark')
        self.arg_omt = Arg(app=self,
                           help='Multi-value optional, count 2.',
                           count=2,
                           sopt='t',
                           lopt='two')
        self.arg_omp = Arg(app=self,
                           help='Multi-value optional, count "+".',
                           count='+',
                           sopt='p',
                           lopt='plus')
        self.arg_oma = Arg(app=self,
                           help='Multi-value optional, count "*".',
                           count='*',
                           sopt='a',
                           lopt='astra')
        self.arg_pss = Arg(app=self,
                           help='Single-value positional, count 1.',
                           count=1,
                           name='SINGLE')
        self.arg_psq = Arg(app=self,
                           help='Single-value positional, count "?".',
                           count='?',
                           name='QMARK')
        self.arg_pmt = Arg(app=self,
                           help='Multi-value positional, count 2.',
                           count=2,
                           name='TWO')
        self.arg_pmp = Arg(app=self,
                           help='Multi-value positional, count "+".',
                           count='+',
                           name='PLUS')
        self.arg_pma = Arg(app=self,
                           help='Multi-value positional, count "*".',
                           count='*',
                           name='ASTRA')

    def __call__(
        self,
        args: dict[Arg] = None,
        apps: list[App] = None,
    ) -> None:
        super().__call__(args, apps)
        # Alignment for names - pretty output.
        w = max(len(x.lopt or x.name) for x in args) + 3
        for arg in args:
            # Determine and quote the name.
            name = f'"{arg.lopt or arg.name}"'
            # Print whether the arguments are multi using Arg.is_multi.
            result = "multi" if arg.is_multi else "not multi"
            print(f'Argument {name:{w}}: {result}.')


# Construct and call.
ExampleApp()()
```

The help:

```shell
./argapp.py -h
# The output:
argapp.py SINGLE [QMARK] TWO TWO PLUS [PLUS...] [ASTRA...]

positional arguments:
  SINGLE    Single-value positional, count 1.
  QMARK     Single-value positional, count "?".
  TWO       Multi-value positional, count 2.
  PLUS      Multi-value positional, count "+".
  ASTRA     Multi-value positional, count "*".

optional arguments:
  -h, --help                   Show the help message and exit.
  -f, --flag                   Flag optional, count 0.
  -s, --single SINGLE          Single-value optional, count 1.
  -q, --qmark [QMARK]          Single-value optional, count "?".
  -t, --two TWO TWO            Multi-value optional, count 2.
  -p, --plus PLUS [PLUS...]    Multi-value optional, count "+".
  -a, --astra [ASTRA...]       Multi-value optional, count "*".
```

The usage:

```shell
# Supply dummy values for positionals.
../argapp.py 0 0 0 0 0
# The output:
Argument "flag"   : not multi.
Argument "single" : not multi.
Argument "qmark"  : not multi.
Argument "two"    : multi.
Argument "plus"   : multi.
Argument "astra"  : multi.
Argument "SINGLE" : not multi.
Argument "QMARK"  : not multi.
Argument "TWO"    : multi.
Argument "PLUS"   : multi.
Argument "ASTRA"  : multi.
```

### `Arg.__init__`

Construct an `Arg` instance and:
 * Initialize the fields.
 * Add the instance to `app.args`.

Parameters match the corresponding fields.

Exceptions:
1. `TypeError`, if the type of some parameter is invalid (see the corresponding field).
2. `ValueError`, if the value of some parameter is invalid (see the corresponding field).

#### Declaration

```python
def __init__(
    self,
    app: App,
    name: str | None = None,
    sopt: str | None = None,
    lopt: str | None = None,
    help: str | None = None,
    type: type | None = None,
    count: int | str | None = None,
    choices: list | dict | None = None,
    default: object | None = None,
) -> None:
    ...
```

#### Example

Refer to the fields' documentation for the code related to errors.

```python
#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

from argapp import Arg, App


class ExampleApp(App):
    def __init__(self) -> None:
        super().__init__(name='argapp.py')
        # A positional argument with the mandatory app.
        self.arg_one = Arg(app=self)
        # An optional argument with all fields set.
        self.arg_all = Arg(app=self,
                           name='VAL',
                           sopt='a',
                           lopt='argument',
                           help='This is an optional argument.',
                           count='+',
                           type=int,
                           choices={1: 'The first.', 2: 'The second.'},
                           default=[1, 2])

    def __call__(
        self,
        args: dict[Arg] = None,
        apps: list[App] = None,
    ) -> None:
        super().__call__(args, apps)
        # Print all the fields for the parameters.
        for arg in self.args:
            # Pick the name.
            name = arg.lopt or arg.name
            # Format the help text (padding).
            pad = ' ' * (len(name) + 17)
            help = f'\n{pad}'.join(arg.help.split('\n'))
            # FPrint the values.
            print('-----------------------------------------------------------')
            print(f'{name} value         : {args[arg]}')
            print(f'{name}.app           : {arg.app.name}')
            print(f'{name}.name          : {arg.name}')
            print(f'{name}.sopt          : {arg.sopt}')
            print(f'{name}.lopt          : {arg.lopt}')
            print(f'{name}.help          : {help}')
            print(f'{name}.count         : {arg.count}')
            print(f'{name}.type          : {arg.type.__name__}')
            print(f'{name}.choices       : {arg.choices}')
            print(f'{name}.default       : {arg.default}')
            print(f'{name}.is_optional   : {arg.is_optional}')
            print(f'{name}.is_positional : {arg.is_positional}')
            print(f'{name}.is_flag       : {arg.is_flag}')
            print(f'{name}.is_single     : {arg.is_single}')
            print(f'{name}.is_multi      : {arg.is_multi}')


# Construct and call.
ExampleApp()()
```

The help:

```shell
./argapp.py -h
# The output:
argapp.py ARG

positional arguments:
  ARG

optional arguments:
  -h, --help                     Show the help message and exit.
  -a, --argument VAL [VAL...]    This is an optional argument.
                                 Possible values:
                                  * 1 - The first.
                                  * 2 - The second.
                                 Defaults to: 1 2
```

The usage:

```shell
# Supply a value for the positional argument.
../argapp.py 0
# The output:
-----------------------------------------------------------
ARG value         : 0
ARG.app           : argapp.py
ARG.name          : ARG
ARG.sopt          : None
ARG.lopt          : None
ARG.help          : 
ARG.count         : 1
ARG.type          : str
ARG.choices       : None
ARG.default       : None
ARG.is_optional   : False
ARG.is_positional : True
ARG.is_flag       : False
ARG.is_single     : True
ARG.is_multi      : False
-----------------------------------------------------------
argument value         : [1, 2]
argument.app           : argapp.py
argument.name          : VAL
argument.sopt          : a
argument.lopt          : argument
argument.help          : This is an optional argument.
                         Possible values:
                          * 1 - The first.
                          * 2 - The second.
                         Defaults to: 1 2
argument.count         : +
argument.type          : int
argument.choices       : {1: 'The first.', 2: 'The second.'}
argument.default       : [1, 2]
argument.is_optional   : True
argument.is_positional : False
argument.is_flag       : False
argument.is_single     : False
argument.is_multi      : True
```

### `Arg.__call__(bool)`

Parse the command line value. Called if `Arg.is_flag` is `True`:
 * Can be overridden to return a custom value of any other type.
 * The base version simply returns the parameter.
 * The result is used as a value in the dictionary `args` in `App.__call__`.

Parameters:
 * `v` - `bool(not Arg.default)` if the argument was mentioned, `bool(Arg.default)` otherwise.

Returns:
 * `v`.

#### Declaration

```python
@overload
def __call__(self, v: bool) -> bool:
    ...
```

#### Example

```python
#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

from argapp import Arg, App

class ExampleObject:
    def __init__(self, data: str) -> None:
        self.data = data

    def __str__(self) -> str:
        return self.data


class ExampleArg(Arg):
    def __init__(
        self,
        app: App,
        default: bool,
    ) -> None:
        # Construct a flag with customized parsing.
        super().__init__(app=app,
                         count=0,
                         help=f'{not default} if present.',
                         lopt=str(not default).lower(),
                         default=default)

    def __call__(self, v: 'bool') -> 'bool':
        # Call the base to obtain the vanilla value.
        v = super().__call__(v)
        # Return a custom object.
        data = 'TRUE' if v else 'FALSE'
        return ExampleObject(data)


class ExampleApp(App):
    def __init__(self) -> None:
        super().__init__(name='argapp.py')
        # Normal flag.
        self.true = ExampleArg(self, False)
        # Reversed flag.
        self.false = ExampleArg(self, True)

    def __call__(
        self,
        args: dict[Arg] = None,
        apps: list[App] = None,
    ) -> None:
        super().__call__(args, apps)
        # Print all the values.
        for arg in self.args:
            # Retrieve the object: args contains ExampleObject, not bool.
            o: ExampleObject = args[arg]
            # Pick the name.
            print(f'Value of {arg.lopt:6}: {o.data}')


# Construct and call.
ExampleApp()()
```

The help:

```shell
./argapp.py -h
# The output:
argapp.py

optional arguments:
  -h, --help     Show the help message and exit.
  --true         True if present.
  --false        False if present.
```

The usage:

```shell
# No flags.
./argapp.py
# The output:
Value of true  : FALSE
Value of false : TRUE

#--------------------------------------------------------

# Both flags.
./argapp.py --true --false
# The output:
Value of true  : TRUE
Value of false : FALSE
```

### `Arg.__call__(str)`

Parse the command line value.
 * Called if `Arg.is_single` is `True`.
 * The result is used as a value in the dictionary args in `App.__call__`.
 * Can be overridden to return a custom value of any other type.<br>
   In this case, the base version should be called first to obtain the parsed value.

The base version:
 * Checks if the value is in `Arg.choices`, if `Arg.choices` is not `None`.
 * Converts the value to `Arg.type`.

Parameters:
 * v - The command line value. `None`, if the value was not provided.

Exceptions:
 * `RuntimeError`, if `Arg.choices` is not `None` and `v` is not in `choices`.

Returns:
1. `None`, if `v` is `None`.
2. `v` converted to `Arg.type` otherwise.

#### Declaration

```python
@overload
def __call__(self, v: str | None) -> str | int | float | bool | None:
    ...
```

#### Example

```python
#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

from argapp import Arg, App


class ExampleObject:
    def __init__(self, data: str) -> None:
        self.data = data


class ExampleArg(Arg):
    def __init__(self, app: App) -> None:
        # Construct a positional argument of int type.
        super().__init__(app=app,
                         type=int,
                         choices={0: 255, 1: 256, 2: 65535, 3: 65536},
                         help=f'A value to convert to hex.')

    def __call__(self, v: str | None) -> ExampleObject:
        # Call the base implementation for parsing and checks.
        v = super().__call__(v)
        # Return a custom object.
        return ExampleObject(hex(self.choices[v]))


class ExampleApp(App):
    def __init__(self) -> None:
        super().__init__(name='argapp.py')
        self.arg = ExampleArg(self)

    def __call__(
        self,
        args: dict[Arg] = None,
        apps: list[App] = None,
    ) -> None:
        super().__call__(args, apps)
        # Retrieve and print the object: args contains ExampleObject, not int.
        o: ExampleObject = args[self.arg]
        print(f'Value of {self.arg.name}: {o.data}')


# Construct and call.
ExampleApp()()
```

The help:

```shell
./argapp.py -h
# The output:
argapp.py ARG

positional arguments:
  ARG    A value to convert to hex.
         Possible values:
          * 0 - 255
          * 1 - 256
          * 2 - 65535
          * 3 - 65536

optional arguments:
  -h, --help     Show the help message and exit.
```

The usage:

```shell
# Valid, in choices.
./argapp.py 3
# The output:
Value of ARG: 0x10000

#--------------------------------------------------------

# Invalid, not in choices.
./argapp.py 5
# The output:
(stack trace)
RuntimeError: Invalid value of argument ARG: 5. Must be one of:
 * 0 - 255
 * 1 - 256
 * 2 - 65535
 * 3 - 65536
```

### `Arg.__call__(list[str])`

Parse the command line value:
 * Called if `Arg.is_multi` is `True`.
 * The result is used as a value in the dictionary `args` in `App.__call__`.
 * Can be overridden to return a custom value of any other type.
   In this case, the base version should be called first to obtain the parsed value.

The base version:
 * Checks if each item is in `Arg.choices`, if `Arg.choices` is not `None`.
 * Converts the each item to `Arg.type`.

Parameters:
 * `v` - The command line value. An empty `list`, if the value was not provided.

Exceptions:
 * `RuntimeError`, if `Arg.choices` is not `None` and any item in `v` is not in `choices`.

Returns:
1. `list` of items from `v` converted to `Arg.type`.

#### Declaration

```python
@overload
def __call__(self, v: list[str]) -> list[str | int | float | bool]:
    ...
```

#### Example

```python
#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

from argapp import Arg, App


class ExampleObject:
    def __init__(self, data: str) -> None:
        self.data = data


class ExampleArg(Arg):
    def __init__(self, app: App) -> None:
        # Construct a positional argument of int type, multiple values.
        super().__init__(app=app,
                         type=int,
                         count='*',
                         choices={0: 255, 1: 256, 2: 65535, 3: 65536},
                         help=f'A value to convert to hex.')

    def __call__(self, v: list[str]) -> list[ExampleObject]:
        # Call the base implementation for parsing and checks.
        v = super().__call__(v)
        # Return a custom object.
        return [ExampleObject(hex(self.choices[x])) for x in v]


class ExampleApp(App):
    def __init__(self) -> None:
        super().__init__(name='argapp.py')
        self.arg = ExampleArg(self)

    def __call__(
        self,
        args: dict[Arg] = None,
        apps: list[App] = None,
    ) -> None:
        super().__call__(args, apps)
        # Retrieve and print the object: args contains ExampleObject, not int.
        o: list[ExampleObject] = args[self.arg]
        for x in o:
            print(f'Value of {self.arg.name}: {x.data}')


# Construct and call.
ExampleApp()()
```

The help:

```shell
./argapp.py -h
# The output:
argapp.py [ARG...]

positional arguments:
  ARG    A value to convert to hex.
         Possible values:
          * 0 - 255
          * 1 - 256
          * 2 - 65535
          * 3 - 65536

optional arguments:
  -h, --help     Show the help message and exit.
```

The usage:

```shell
# A single value.
./argapp.py 3
# The output:
Value of ARG: 0x10000

#--------------------------------------------------------

# Multiple values.
./argapp.py 1 0 3
# The output:
Value of ARG: 0x100
Value of ARG: 0xff
Value of ARG: 0x10000

#--------------------------------------------------------

# One of the values not in choices.
./argapp.py 1 4 2
# The output:
(stack trace)
RuntimeError: Invalid item in argument ARG: 4. Must be one of:
 * 0 - 255
 * 1 - 256
 * 2 - 65535
 * 3 - 65536
```

### `App`

Represents a command line application (main or sub-command).

The instance:
 * Works only with both the raw and the parsed command line if it is a main `App`.
 * Works only with the parsed command line if it is a sub-command `App`.
 * Is an item in `apps` in `App.__call__`.

The fields:
 * Are read-only and can be set once, via `App.__init__`.
 * Are validated during `App.__init__`.
 * May depend on other fields.

Instances of this class are internally converted to `argparse.ArgumentParser`:
 * Any `App` will provide the help message mechanism via an automatic argument `"-h, --help"`.<br>
   The default generation from argparse is not used, but the differences are small and mostly related to style.
 * If `apps` not empty, the `App` will provide the sub-commands mechanism via an automatic argument `"CMD"`.<br>
   Under the hood, `argparse.ArgumentParser.add_subparsers` is used to add the commands.

#### Example

There are several best practices to follow:
 * Sub-class `App` to customize the construction or execution.
 * Create `App` instances inside the `App` that will contain it (that is, in `App.__init__`).

Below is `argapp.py` which features a main application with two sub-commands.

```python
#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

from argapp import Arg, App


class ExampleSub(App):
    def __init__(self, app: App, name: str) -> None:
        super().__init__(app=app,
                         name=name,
                         help=f'An example sub-command: {name}.')

    def __call__(
        self,
        args: dict[Arg] = None,
        apps: list[App] = None,
    ) -> None:
        super().__call__(args, apps)
        # Print the name.
        print(f'I am {self.name}.')


class ExampleApp(App):
    def __init__(self) -> None:
        super().__init__(help='The main app.')
        # Construct the Apps.
        ExampleSub(self, 'sub_a')
        ExampleSub(self, 'sub_b')


# Construct and call.
ExampleApp()()
```

The help:

```shell
./argapp.py -h
# The output:
argapp.py CMD ...

The main app.

positional arguments:
  CMD    A sub-command to run.
         Possible values:
          * sub_a - An example sub-command: sub_a.
          * sub_b - An example sub-command: sub_b.

optional arguments:
  -h, --help     Show the help message and exit.
```

The usage:

```shell
./argapp.py sub_a
# The output:
I am sub_a.

#--------------------------------------------------------

./argapp.py sub_b
# The output:
I am sub_b.
```

The completion:

```shell
./argapp.py
# Upon pressing TAB, the command line is filled:
./argapp.py sub_
# Upon pressing TAB, the following is displayed:
sub_a  sub_b
```

### `App.app`

The parent application. The `App` is added to `app.apps`.

May be set via `App.__init__` as `app`:
 * `type(app)` must be `App` or `None` (`TypeError`).
 * `app.apps` must not contain `App` with the same `App.name` (`ValueError`).

#### Declaration

```python
@property
def app(self) -> App | None:
    ...
```

#### Example

```python
# OK, the main App.
main = App()
# OK, a sub-command for main.
app = App(app=main,
          name='app')
# TypeError: Invalid type of Arg.app: bool. Expected: App, None.
app = App(app=False,
          name='app')
# ValueError: Invalid value of App.name: "app1". Must not repeat other App.name in main App.
app1 = App(app=main,
          name='app1')
app2 = App(app=main,
          name='app1')
```

### `App.name`

The command's name, `"git"` in `"git --version"`.

May be set via `App.__init__` as `name`:
 * `type(name)` must be `str` or `None` (`TypeError`).
 * If `type(app)` is `App`, name must not be `None` (`TypeError`).
 * `len(name)` must be greater than 0 (`ValueError`).

If `None`, the command line help displays the first command line value as the application name.

#### Declaration

```python
@property
def name(self) -> str | None:
    ...
```

#### Example

```python
# OK, the main App with the name for from the command line.
main = App()
# OK, the main App with the custom name.
main = App(name='argapp.py')
# OK, a sub-command of main.
app = App(app=main,
          name='app')
# TypeError: Invalid type of App.name: bool. Expected: str, None.
app = App(app=main,
          name=False)
# TypeError: Invalid type of App.name for sub-command: None. Expected: str.
app = App(app=main)
# ValueError: Invalid value of App.name: "". Must not be empty.
app = App(app=main,
          name='')
```

### `App.help`

The help text for a sub-command.

May be set via `App.__init__` as `help`:
 * `type(help)` must be `str` or `None` (`TypeError`).

#### Declaration

```python
@property
def help(self) -> str | None:
    ...
```

#### Example

```python
# OK, the main App without help.
main = App()
# OK, a sub-commands of main. The help message of main contains:
# ...
# positional arguments:
#   CMD    A sub-command to run.
#          Possible values:
#           * app1 - The first sub-command.
#           * app2 - The second sub-command.
# ...
app1 = App(app=main,
           help='The first sub-command.',
           name='app1')
app2 = App(app=main,
           help='The second sub-command.',
           name='app2')
# TypeError: Invalid type of App.help: bool. Expected: str, None.
app = App(app=main,
          help=False)
```

### `App.prolog`

The detailed help text before the argument lists.

May be set via `App.__init__` as `prolog`:
 * `type(prolog)` must be `str` or `None` (`TypeError`).

Defaults:
1. `App.help`.

#### Declaration

```python
@property
def prolog(self) -> str | None:
    ...
```

#### Example

```python
# OK, the main App without prolog:
# argapp.py
#
# optional arguments:
#   -h, --help     Show the help message and exit.
main = App()
# OK, the main App with prolog:
# argapp.py
#
# This is prolog.
#
# optional arguments:
#   -h, --help     Show the help message and exit.
main = App(prolog='This is prolog.')
# OK, the main App with help:
# argapp.py
#
# This is help.
#
# optional arguments:
#   -h, --help     Show the help message and exit.
main = App(help='This is help.')
# OK, the sub-command with both.
# Main help:
# argapp.py CMD ...
#
# This is help.
#
# positional arguments:
#   CMD    A sub-command to run.
#          Possible values:
#           * app - This is sub-command help.
#
# optional arguments:
#   -h, --help     Show the help message and exit.
# ------------------------------------------------
# Sub-command help:
# argapp.py app
#
# This is sub-command prolog.
#
# optional arguments:
#   -h, --help     Show the help message and exit.
app = App(app=main,
          help='This is sub-command help.',
          prolog='This is sub-command prolog.',
          name='app')
# TypeError: Invalid type of App.prolog: bool. Expected: str, None.
app = App(app=main,
          prolog=False,
          name='app')
```

### `App.epilog`

The detailed help text after the argument lists.

May be set via `App.__init__` as `epilog`:
 * `type(epilog)` must be `str` or `None` (`TypeError`).

#### Declaration

```python
@property
def epilog(self) -> str | None:
    ...
```

#### Example

```python
# OK, the main App without epilog:
# argapp.py
#
# optional arguments:
#   -h, --help     Show the help message and exit.
main = App()
# OK, the main App with epilog:
# argapp.py
#
# optional arguments:
#   -h, --help     Show the help message and exit.
#
# This is epilog.
main = App(epilog='This is epilog.')
# TypeError: Invalid type of App.epilog: bool. Expected: str, None.
main = App(epilog=False)
```

### `App.is_main`

Whether `App` is a main application.
 * Opposite to `App.is_sub`.
 * Cannot be set.

Defaults:
1. `True`, if `App.app` is `None`.
2. `False` otherwise.

#### Declaration

```python
@property
def is_main(self) -> bool:
    ...
```

#### Example

```python
#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

from argapp import Arg, App


class ExampleApp(App):
    def __init__(self) -> None:
        super().__init__(name='argapp.py')
        app1 = App(app=self,
                   name='app1')
        app2 = App(app=app1,
                   name='app2')
        app3 = App(app=app2,
                   name='app3')

    def __call__(self, args: dict[Arg] = None, apps: list[App] = None) -> None:
        super().__call__(args, apps)
        # Print if the called apps are a main or a sub-command.
        for x in apps:
            result = 'main' if x.is_main else 'sub-command'
            print(f'{x.name:10}: {result}.')


# Construct and call.
ExampleApp()()
```

The usage:

```shell
./argapp.py app1 app2 app3
# The output:
argapp.py : main.
app1      : sub-command.
app2      : sub-command.
app3      : sub-command.
```

### `App.is_sub`

Whether `App` is a sub-command.
 * Opposite to `App.is_main`.
 * Cannot be set.

Defaults:
1. `True`, if `App.app` is not `None`.
2. `False` otherwise.

#### Declaration

```python
@property
def is_sub(self) -> bool:
    ...
```

#### Example

```python
#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

from argapp import Arg, App


class ExampleApp(App):
    def __init__(self) -> None:
        super().__init__(name='argapp.py')
        app1 = App(app=self,
                   name='app1')
        app2 = App(app=app1,
                   name='app2')
        app3 = App(app=app2,
                   name='app3')

    def __call__(self, args: dict[Arg] = None, apps: list[App] = None) -> None:
        super().__call__(args, apps)
        # Print if the called apps are a main or a sub-command.
        for x in apps:
            result = 'sub-command' if x.is_sub else 'main'
            print(f'{x.name:10}: {result}.')


# Construct and call.
ExampleApp()()
```

The usage:

```shell
./argapp.py app1 app2 app3
# The output:
argapp.py : main.
app1      : sub-command.
app2      : sub-command.
app3      : sub-command.
```

### `App.args`

A list of `App`'s arguments (`Arg`).
 * Populated by constructing an `Arg` with `Arg.app` set to the `App` instance.
 * Must not be modified directly.

Each `Arg`:
 * Is used for the help message generation: `"usage"`, `"positional arguments"`, `"optional arguments"`.
 * Used as a key in the dictionary after the command line parsing.

There are two automatic arguments that are never on the list:
 * `-h, --help` - Display the help message and exit, always the first optional argument.
 * `CMD`        - A sub-command to run, always the last positional argument. Appears only if `App.apps` is not empty.

Defaults:
1. `[]`.

#### Declaration

```python
@property
def args(self) -> list[Arg]:
    ...
```

#### Example

```python
#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

from argapp import Arg, App


class ExampleApp(App):
    def __init__(self) -> None:
        super().__init__(name='argapp.py')
        self.arg_of = Arg(app=self,
                          help='Flag optional, count 0.',
                          count=0,
                          sopt='f',
                          lopt='flag')
        self.arg_oss = Arg(app=self,
                           help='Single-value optional, count 1.',
                           count=1,
                           sopt='s',
                           lopt='single')
        self.arg_osq = Arg(app=self,
                           help='Single-value optional, count "?".',
                           count='?',
                           sopt='q',
                           lopt='qmark')
        self.arg_omt = Arg(app=self,
                           help='Multi-value optional, count 2.',
                           count=2,
                           sopt='t',
                           lopt='two')
        self.arg_omp = Arg(app=self,
                           help='Multi-value optional, count "+".',
                           count='+',
                           sopt='p',
                           lopt='plus')
        self.arg_oma = Arg(app=self,
                           help='Multi-value optional, count "*".',
                           count='*',
                           sopt='a',
                           lopt='astra')
        self.arg_pss = Arg(app=self,
                           help='Single-value positional, count 1.',
                           count=1,
                           name='SINGLE')
        self.arg_psq = Arg(app=self,
                           help='Single-value positional, count "?".',
                           count='?',
                           name='QMARK')
        self.arg_pmt = Arg(app=self,
                           help='Multi-value positional, count 2.',
                           count=2,
                           name='TWO')
        self.arg_pmp = Arg(app=self,
                           help='Multi-value positional, count "+".',
                           count='+',
                           name='PLUS')
        self.arg_pma = Arg(app=self,
                           help='Multi-value positional, count "*".',
                           count='*',
                           name='ASTRA')

    def __call__(
        self,
        args: dict[Arg] = None,
        apps: list[App] = None,
    ) -> None:
        super().__call__(args, apps)
        # Print all App.args.
        for x in self.args:
            print(x.lopt or x.name)


# Construct and call.
ExampleApp()()
```

The help:

```shell
./argapp.py -h
# The output:
argapp.py SINGLE [QMARK] TWO TWO PLUS [PLUS...] [ASTRA...]

positional arguments:
  SINGLE    Single-value positional, count 1.
  QMARK     Single-value positional, count "?".
  TWO       Multi-value positional, count 2.
  PLUS      Multi-value positional, count "+".
  ASTRA     Multi-value positional, count "*".

optional arguments:
  -h, --help                   Show the help message and exit.
  -f, --flag                   Flag optional, count 0.
  -s, --single SINGLE          Single-value optional, count 1.
  -q, --qmark [QMARK]          Single-value optional, count "?".
  -t, --two TWO TWO            Multi-value optional, count 2.
  -p, --plus PLUS [PLUS...]    Multi-value optional, count "+".
  -a, --astra [ASTRA...]       Multi-value optional, count "*".
```

The usage:

```shell
# Supply dummy values for positionals.
./argapp.py 0 0 0 0 0
# The output:
flag
single
qmark
two
plus
astra
SINGLE
QMARK
TWO
PLUS
ASTRA
```

### `App.apps`

A list of `App`'s sub-commands (`App`).
 * Populated by constructing an `App` with `App.app` set to the instance.
 * Must not be modified directly.

Each `App`:
 * Is used for the help message generation.
 * Appears in its parent's help text for the `"CMD"` (see `App.args`).
 * Used as an item in the list after the command line parsing (if called).

Defaults:
1. `[]`.

#### Declaration

```python
@property
def apps(self) -> list[App]:
    ...
```

#### Example

```python
#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

from argapp import Arg, App


class ExampleApp(App):
    def __init__(self) -> None:
        super().__init__(name='argapp.py')
        # Create some Apps.
        for i in [1, 2, 3]:
            App(app=self,
                name=f'app{i}')

    def __call__(
        self,
        args: dict[Arg] = None,
        apps: list[App] = None,
    ) -> None:
        super().__call__(args, apps)
        # Print all App.apps, the sub-command does not matter.
        for x in self.apps:
            print(x.name)


# Construct and call.
ExampleApp()()
```

The help:

```shell
./argapp.py -h
# The output:
argapp.py CMD ...

positional arguments:
  CMD    A sub-command to run.
         Possible values:
          * app1
          * app2
          * app3

optional arguments:
  -h, --help     Show the help message and exit.
```

The usage:

```shell
# Supply dummy values for positionals.
../argapp.py app1
# The output:
app1
app2
app3
```

### `App.__init__`

Construct the `App` and:
 * Initialize the fields.
 * Add the instance to `app.apps`.

Parameters match the corresponding fields.

Exceptions:
1. `TypeError`, if the type of some parameter is invalid (see the corresponding field).
2. `ValueError`, if the value of some parameter is invalid (see the corresponding field).

#### Declaration

```python
def __init__(
    self,
    app: App | None = None,
    name: str | None = None,
    help: str | None = None,
    prolog: str | None = None,
    epilog: str | None = None,
) -> None:
    ...
```

#### Example

```python
#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

from argapp import Arg, App


class ExampleApp(App):
    def __init__(self) -> None:
        super().__init__(name='argapp.py')
        # App with only the required fields.
        App(app=self,
            name='one')
        # App with all fields.
        App(app=self,
            help='A sub-command help.',
            epilog='A sub-command prolog.',
            prolog='A sub-command epilog.',
            name='all')

    def __call__(
        self,
        args: dict[Arg] = None,
        apps: list[App] = None,
    ) -> None:
        super().__call__(args, apps)


# Construct and call.
ExampleApp()()
```

The help:

```shell
./argapp.py -h
# The output:
argapp.py CMD ...

positional arguments:
  CMD    A sub-command to run.
         Possible values:
          * one
          * all - A sub-command help.

optional arguments:
  -h, --help     Show the help message and exit.

# -------------------------------------------------

./argapp.py one -h
# The output:
argapp.py one

optional arguments:
  -h, --help     Show the help message and exit.

# -------------------------------------------------

./argapp.py all -h
# The output:
argapp.py all

A sub-command epilog.

optional arguments:
  -h, --help     Show the help message and exit.

A sub-command prolog.
```

### `App.__call__(list[str])`

An overload of `App.__call__` for the raw command line.
It should never be overridden, use the other overload's signature for overriding.

The functionality is as follows:
1. Parse the provided command line (`argv`) into `args` (`dict[Arg]`) and `apps` (`list[App]`).
2. If `"-h, --help"` is encountered, display the help message and exit with code 0.
3. If there are any issues with parsing, display the usage message, the error, and exit with non-zero code.
4. For each `App` in `apps`, call the other overload of `App.__call__` passing `args` and `apps` as the parameter values.
5. Exit with code 0 if there are no issues.
6. Exit with code 1 and print an error if there are any issues.

The help message structure is the same as in argparse, but there are specifics:
 * The usage shows only positional arguments.
 * All arguments are displayed in their respective sections in the order they were added.
   As for the automatic arguments:
   1. `"-h, --help"` is the very first argument.
   2. `"CMD"` is the very last argument, if present. Note that in the usage it appears as `"CMD ..."`.
 * Optional arguments are displayed as `"-a, --arg ARG"`, not `"-a ARG, --arg ARG"`.
 * Newlines, spaces, tabs in the individual help texts are retained.
 * All arguments are aligned section-wise. Their help texts are properly padded.
 * An argument and its help text are always on the same line, no matter how wide the argument is.

Parameters:
 * `argv` - A raw command line as `list[str]`. Effectively defaults to `sys.argv`, if `None`.
   The first item in the list must be the application name.

Exceptions:
 * `SystemExit`, regardless of success (code 0) or failure (code 1).
'''

#### Declaration

```python
def __call__(
    self,
    argv: list[str] = None,
) -> None:
    ...
```

#### Example

```python
#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

from argapp import Arg, App

# Provide a custom command line, even the default App handles that.
# For some other use cases, refer to App.args, App.apps.
App()(['my-fancy-name', '-h'])
```

The usage:

```shell
# It immediately calls help.
./argapp.py
# The output:
my-fancy-name

optional arguments:
  -h, --help     Show the help message and exit.
```

### `App.__call__(dict[Arg], list[App])`

An overload of `App.__call__` for the parsed command line. The default implementation does nothing.
It should be overridden, use this signature for overriding.

It is mandatory to call `super().__call__(args, apps)` in the body before accessing `args` or `apps`.

Parameters:
 * `args` - A dictionary containing each `Arg` and its value.
   The value is guaranteed to be set (can be `None`), so it is safe to use operator `[]`.
 * `apps` - A call stack of `App`.
   The first item is the main `App`, the other items are sub-commands.
   The left-to-right order is preserved. Consider `"git remote add"`:
   1. `apps[0].name` - `"git"`
   2. `apps[1].name` - `"remote"`
   3. `apps[2].name` - `"add"`

#### Declaration

```python
def __call__(
    self,
    args: dict[Arg] = None,
    apps: list[App] = None,
) -> None:
    ...
```

#### Example

```python
#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

from argapp import Arg, App


class ExampleApp(App):
    def __init__(self) -> None:
        super().__init__(name='argapp.py')
        # Add args.
        self.arg_of = Arg(app=self,
                          help='Flag optional, count 0.',
                          count=0,
                          sopt='f',
                          lopt='flag')
        self.arg_oss = Arg(app=self,
                           help='Single-value optional, count 1.',
                           count=1,
                           sopt='s',
                           lopt='single')
        self.arg_osq = Arg(app=self,
                           help='Single-value optional, count "?".',
                           count='?',
                           sopt='q',
                           lopt='qmark')
        self.arg_omt = Arg(app=self,
                           help='Multi-value optional, count 2.',
                           count=2,
                           sopt='t',
                           lopt='two')
        self.arg_omp = Arg(app=self,
                           help='Multi-value optional, count "+".',
                           count='+',
                           sopt='p',
                           lopt='plus')
        self.arg_oma = Arg(app=self,
                           help='Multi-value optional, count "*".',
                           count='*',
                           sopt='a',
                           lopt='astra')
        self.arg_pss = Arg(app=self,
                           help='Single-value positional, count 1.',
                           count=1,
                           name='SINGLE')
        self.arg_psq = Arg(app=self,
                           help='Single-value positional, count "?".',
                           count='?',
                           name='QMARK')
        self.arg_pmt = Arg(app=self,
                           help='Multi-value positional, count 2.',
                           count=2,
                           name='TWO')
        self.arg_pmp = Arg(app=self,
                           help='Multi-value positional, count "+".',
                           count='+',
                           name='PLUS')
        self.arg_pma = Arg(app=self,
                           help='Multi-value positional, count "*".',
                           count='*',
                           name='ASTRA')
        # Add apps.
        for i in [1, 2, 3]:
            App(app=self,
                name=f'app{i}')

    def __call__(
        self,
        args: dict[Arg] = None,
        apps: list[App] = None,
    ) -> None:
        super().__call__(args, apps)
        print('Args:')
        for x in self.args:
            print(f' * {x.lopt or x.name}')
        print('Apps:')
        for x in self.apps:
            print(f' * {x.name}')


# Construct and call.
ExampleApp()()
```

The help:

```shell
./argapp.py -h
# The output:
argapp.py SINGLE [QMARK] TWO TWO PLUS [PLUS...] [ASTRA...] CMD ...

positional arguments:
  SINGLE    Single-value positional, count 1.
  QMARK     Single-value positional, count "?".
  TWO       Multi-value positional, count 2.
  PLUS      Multi-value positional, count "+".
  ASTRA     Multi-value positional, count "*".
  CMD       A sub-command to run.
            Possible values:
             * app1
             * app2
             * app3

optional arguments:
  -h, --help                   Show the help message and exit.
  -f, --flag                   Flag optional, count 0.
  -s, --single SINGLE          Single-value optional, count 1.
  -q, --qmark [QMARK]          Single-value optional, count "?".
  -t, --two TWO TWO            Multi-value optional, count 2.
  -p, --plus PLUS [PLUS...]    Multi-value optional, count "+".
  -a, --astra [ASTRA...]       Multi-value optional, count "*".
```

The usage:

```shell
# Supply some dummy values, it does not change the output.
# The last argument is the sub-command.
./argapp.py 0 0 0 0 0 app1
# The output:
Args:
 * flag
 * single
 * qmark
 * two
 * plus
 * astra
 * SINGLE
 * QMARK
 * TWO
 * PLUS
 * ASTRA
Apps:
 * app1
 * app2
 * app3
```
