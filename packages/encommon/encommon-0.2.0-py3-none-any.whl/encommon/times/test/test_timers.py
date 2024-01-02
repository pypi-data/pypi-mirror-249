"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from time import sleep

from pytest import raises

from ..timers import Timers



def test_Timers() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    timers = Timers({'one': 1})

    attrs = list(timers.__dict__)

    assert attrs == [
        '_Timers__timing',
        '_Timers__caches']


    assert repr(timers).startswith(
        '<encommon.times.timers.Timers')
    assert isinstance(hash(timers), int)
    assert str(timers).startswith(
        '<encommon.times.timers.Timers')


    assert timers.timing == {'one': 1}

    assert not timers.ready('one')
    sleep(1.1)
    assert timers.ready('one')


    timers.create('two', 2, 0)

    assert timers.ready('two')
    assert not timers.ready('two')



def test_Timers_raises() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    timers = Timers({'one': 1})


    with raises(ValueError) as reason:
        timers.ready('dne')

    assert str(reason.value) == 'unique'


    with raises(ValueError) as reason:
        timers.update('dne')

    assert str(reason.value) == 'unique'


    with raises(ValueError) as reason:
        timers.create('one', 1)

    assert str(reason.value) == 'unique'
