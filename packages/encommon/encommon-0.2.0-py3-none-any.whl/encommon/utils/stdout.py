"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from re import compile
from re import sub as re_sub
from sys import stdout
from typing import Any
from typing import Literal

from .common import JOINABLE



ANSICODE = compile(
    r'\x1b\[[^A-Za-z]*[A-Za-z]')



def print_ansi(
    string: str = '',
    method: Literal['stdout', 'print'] = 'stdout',
    output: bool = True,
) -> str:
    """
    Print the ANSI colorized string to the standard output.

    Example
    -------
    >>> print_ansi('<c91>ERROR<c0>')
    '\\x1b[0;91mERROR\\x1b[0;0m'

    :param string: String processed using inline directives.
    :param method: Which method for standard output is used.
    :param output: Whether or not hte output should be print.
    :returns: ANSI colorized string using inline directives.
    """  # noqa: D301 LIT102

    string = make_ansi(string)

    if output is True:
        if method == 'stdout':
            stdout.write(f'{string}\n')
        else:
            print(string)  # noqa: T201

    return string



def make_ansi(
    string: str,
) -> str:
    """
    Parse the string and replace directives with ANSI codes.

    Example
    -------
    >>> make_ansi('<c91>ERROR<c0>')
    '\\x1b[0;91mERROR\\x1b[0;0m'

    :param string: String containing directives to replace.
    :returns: Provided string with the directives replaced.
    """  # noqa: D301 LIT102

    pattern = r'\<c([\d\;]+)\>'
    replace = r'\033[0;\1m'

    return re_sub(pattern, replace, string)



def kvpair_ansi(
    key: str,
    value: Any,  # noqa: ANN401
) -> str:
    """
    Process and colorize keys and values for standard output.

    Example
    -------
    >>> kvpair_ansi('k', 'v')
    '\\x1b[0;90mk\\x1b[0;37m="\\x1b[0;0m...

    :param key: String value to use for the key name portion.
    :param value: String value to use for the value portion.
    :returns: ANSI colorized string using inline directives.
    """  # noqa: D301 LIT102

    if isinstance(value, JOINABLE):  # type: ignore
        value = ','.join([
            str(x) for x in value])

    elif not isinstance(value, str):
        value = str(value)

    return make_ansi(
        f'<c90>{key}<c37>="<c0>'
        f'{value}<c37>"<c0>')



def strip_ansi(
    string: str,
) -> str:
    """
    Return the provided string with the ANSI codes removed.

    Example
    -------
    >>> strip_ansi('\\x1b[0;91mERROR\\x1b[0;0m')
    'ERROR'

    :param string: String which contains ANSI codes to strip.
    :returns: Provided string with the ANSI codes removed.
    """  # noqa: D301 LIT102

    return re_sub(ANSICODE, '', string)
