"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from datetime import timedelta

from pytest import mark
from pytest import raises

from ..common import utcdatetime
from ..parse import duration
from ..parse import parse_time
from ..parse import shift_time
from ..parse import since_time
from ..parse import string_time



def test_parse_time() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    utcnow = utcdatetime()
    delta = timedelta(seconds=1)


    dtime = parse_time(
        '1/1/1970 6:00am')

    assert dtime.year == 1970
    assert dtime.month == 1
    assert dtime.day == 1
    assert dtime.hour == 6


    dtime = parse_time(
        '12/31/1969 6:00pm',
        tzname='US/Central')

    assert dtime.year == 1970
    assert dtime.month == 1
    assert dtime.day == 1
    assert dtime.hour == 0


    dtime = parse_time(0)
    assert dtime.year == 1970

    dtime = parse_time('0')
    assert dtime.year == 1970


    dtime = parse_time('max')

    assert dtime.year == 9999
    assert dtime.month == 12
    assert dtime.day == 31
    assert dtime.hour == 23

    dtime = parse_time('min')

    assert dtime.year == 1
    assert dtime.month == 1
    assert dtime.day == 1
    assert dtime.hour == 0


    dtime = parse_time('now')
    assert dtime - utcnow <= delta

    dtime = parse_time(None)
    assert dtime - utcnow <= delta

    dtime = parse_time('None')
    assert dtime - utcnow <= delta


    dtime = parse_time('+1y')
    assert dtime - utcnow > delta


    assert parse_time(dtime) == dtime



def test_parse_time_raises() -> None:
    """
    Perform various tests associated with relevant routines.
    """


    with raises(ValueError) as reason:
        parse_time(0, tzname='foo/bar')

    assert str(reason.value) == 'tzname'


    with raises(ValueError) as reason:
        parse_time(parse_time)  # type: ignore

    assert str(reason.value) == 'source'



@mark.parametrize(
    'notate,expect',
    [('+1y', (1981, 1, 1)),
     ('-1y', (1979, 1, 1)),
     ('+1y@s', (1981, 1, 1)),
     ('-1y@s', (1979, 1, 1)),
     ('+1y@s+1h', (1981, 1, 1, 1)),
     ('-1y@s-1h', (1978, 12, 31, 23)),
     ('+1mon', (1980, 2, 1)),
     ('-1mon', (1979, 12, 1)),
     ('+1mon@m', (1980, 2, 1)),
     ('-1mon@m', (1979, 12, 1)),
     ('+1mon@m+1mon', (1980, 3, 1)),
     ('-1mon@m-1mon', (1979, 11, 1)),
     ('+1w', (1980, 1, 8)),
     ('-1w', (1979, 12, 25)),
     ('+1w@h', (1980, 1, 8)),
     ('-1w@h', (1979, 12, 25)),
     ('+1w@h+1w', (1980, 1, 15)),
     ('-1w@h-1w', (1979, 12, 18)),
     ('+1d', (1980, 1, 2)),
     ('-1d', (1979, 12, 31)),
     ('+1d@d', (1980, 1, 2)),
     ('-1d@d', (1979, 12, 31)),
     ('+1d@d+30d', (1980, 2, 1)),
     ('-1d@d-30d', (1979, 12, 1))])
def test_shift_time(
    notate: str,
    expect: tuple[int, ...],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param notate: Syntax compatable using snaptime library.
    :param expect: Expected output from the testing routine.
    """

    anchor = utcdatetime(1980, 1, 1)

    parsed = shift_time(notate, anchor)

    assert parsed == utcdatetime(*expect)



def test_string_time() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    expect = utcdatetime(1980, 1, 1)


    strings = [
        '1980-01-01T00:00:00Z',
        '1980-01-01T00:00:00',
        '1980-01-01 00:00:00 +0000',
        '1980-01-01 00:00:00']

    for string in strings:
        assert string_time(string) == expect


    parsed = string_time(
        '1980_01_01',
        formats=['%Y', '%Y_%m_%d'])

    assert parsed == expect

    parsed = string_time(
        '1980_01_01',
        formats='%Y_%m_%d')

    assert parsed == expect

    parsed = string_time(
        '1979-12-31 18:00:00',
        tzname='US/Central')

    assert parsed == expect



def test_since_time() -> None:
    """
    Perform various tests associated with relevant routines.
    """


    dtime = shift_time('-1s')

    assert since_time(dtime) >= 1
    assert since_time(dtime) < 2


    dtime = shift_time('+1s')

    assert since_time(dtime) > 0
    assert since_time(dtime) < 2



def test_duration() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    second = 60
    hour = second * 60
    day = hour * 24
    week = day * 7
    month = day * 30
    quarter = day * 90
    year = day * 365


    expects = {

        year: ('1y', '1 year'),
        year + 1: ('1y', '1 year'),
        year - 1: (
            '12mon4d23h59m',
            '12 months, 4 days'),

        quarter: ('3mon', '3 months'),
        quarter + 1: ('3mon', '3 months'),
        quarter - 1: (
            '2mon4w1d23h59m',
            '2 months, 4 weeks'),

        month: ('1mon', '1 month'),
        month + 1: ('1mon', '1 month'),
        month - 1: (
            '4w1d23h59m',
            '4 weeks, 1 day'),

        week: ('1w', '1 week'),
        week + 1: ('1w', '1 week'),
        week - 1: (
            '6d23h59m',
            '6 days, 23 hours'),

        day: ('1d', '1 day'),
        day + 1: ('1d', '1 day'),
        day - 1: (
            '23h59m',
            '23 hours, 59 minutes'),

        hour: ('1h', '1 hour'),
        hour + 1: ('1h', '1 hour'),
        hour - 1: ('59m', '59 minutes'),

        second: ('1m', '1 minute'),
        second + 1: ('1m', '1 minute'),
        second - 1: ('59s', 'just now')}


    for source, expect in expects.items():

        durated = duration(
            seconds=source,
            compact=True)

        assert durated == expect[0]

        durated = duration(
            seconds=source,
            compact=False,
            maximum=2)

        assert durated == expect[1]
