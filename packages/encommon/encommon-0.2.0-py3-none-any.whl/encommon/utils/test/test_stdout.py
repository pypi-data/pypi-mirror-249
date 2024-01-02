"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from _pytest.capture import CaptureFixture

from ..stdout import kvpair_ansi
from ..stdout import make_ansi
from ..stdout import print_ansi
from ..stdout import strip_ansi



def test_print_ansi(
    capsys: CaptureFixture[str],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param capsys: pytest object for capturing print message.
    """

    print_ansi('<c91>test<c0>', 'print')

    output = capsys.readouterr().out

    assert strip_ansi(output) == 'test\n'



def test_make_ansi() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    output = make_ansi('<c31>test<c0>')

    assert output == (
        '\x1b[0;31mtest\x1b[0;0m')



def test_kvpair_ansi() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    output = kvpair_ansi('key', 'value')

    assert output == (
        '\x1b[0;90mkey\x1b[0;37m="\x1b'
        '[0;0mvalue\x1b[0;37m"\x1b[0;0m')

    output = kvpair_ansi('key', [1, 2])

    assert output == (
        '\x1b[0;90mkey\x1b[0;37m="\x1b'
        '[0;0m1,2\x1b[0;37m"\x1b[0;0m')

    output = kvpair_ansi('key', None)

    assert output == (
        '\x1b[0;90mkey\x1b[0;37m="\x1b'
        '[0;0mNone\x1b[0;37m"\x1b[0;0m')



def test_strip_ansi() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    output = '\x1b[0;31mtest\x1b[0;0m'

    assert strip_ansi(output) == 'test'
