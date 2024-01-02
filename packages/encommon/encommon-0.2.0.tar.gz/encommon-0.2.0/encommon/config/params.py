"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Optional

from pydantic import BaseModel

from .common import LOGLEVELS
from ..crypts.params import CryptsParams



class ConfigParams(BaseModel, extra='forbid'):
    """
    Process and validate the common configuration parameters.

    :param data: Keyword arguments passed to Pydantic model.
    """

    paths: Optional[list[str]] = None



class LoggerParams(BaseModel, extra='forbid'):
    """
    Process and validate the common configuration parameters.

    :param data: Keyword arguments passed to Pydantic model.
    """

    stdo_level: Optional[LOGLEVELS] = None
    file_level: Optional[LOGLEVELS] = None
    file_path: Optional[str] = None



class Params(BaseModel, extra='forbid'):
    """
    Process and validate the common configuration parameters.

    :param data: Keyword arguments passed to Pydantic model.
    """

    enconfig: Optional[ConfigParams] = None
    enlogger: Optional[LoggerParams] = None
    encrypts: Optional[CryptsParams] = None
