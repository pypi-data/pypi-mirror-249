"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import PosixPath

from ..paths import resolve_path
from ..paths import resolve_paths



def test_resolve_path() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    path = resolve_path(
        path='/foo/bar',
        replace={'bar': 'foo'})

    assert path == (
        PosixPath('/foo/foo'))



def test_resolve_paths() -> None:
    """
    Perform various tests associated with relevant routines.
    """


    paths = resolve_paths(
        paths='/foo/bar',
        replace={'bar': 'foo'})

    assert list(paths) == [
        PosixPath('/foo/foo')]


    paths = resolve_paths(
        paths=['/foo/bar', '/bar/foo'],
        replace={'bar': 'foo'})

    assert list(paths) == [
        PosixPath('/foo/foo')]
