"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path
from typing import Optional

from .common import PATHABLE



def resolve_path(
    path: str | Path,
    replace: Optional[dict[str, str]] = None,
) -> Path:
    """
    Resolve the provided path and replace the magic keywords.

    Example
    -------
    >>> resolve_path('/foo/bar')
    PosixPath('/foo/bar')

    :param path: Complete or relative path for processing.
    :param replace: Optional string values to replace in path.
    :returns: New resolved filesystem path object instance.
    """

    path = str(path).strip()

    if replace is not None:
        for old, new in replace.items():
            path = path.replace(old, new)

    return Path(path).resolve()



def resolve_paths(
    paths: PATHABLE,
    replace: Optional[dict[str, str]] = None,
) -> tuple[Path, ...]:
    """
    Resolve the provided paths and replace the magic keywords.

    .. note::
       This will remove duplicative paths from the returned.

    Example
    -------
    >>> resolve_paths(['/foo/bar'])
    (PosixPath('/foo/bar'),)

    :param paths: Complete or relative paths for processing.
    :param replace: Optional string values to replace in path.
    :returns: New resolved filesystem path object instances.
    """

    returned: list[Path] = []

    if isinstance(paths, str | Path):
        paths = [paths]

    for path in paths:

        _path = resolve_path(
            str(path), replace)

        if _path in returned:
            continue

        returned.append(_path)

    return tuple(returned)
