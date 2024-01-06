# File generated from our OpenAPI spec by Stainless.

import builtins
import datetime

from .._models import BaseModel

__all__ = ["NamePropertiesCommonConflictsResponse"]


class NamePropertiesCommonConflictsResponse(BaseModel):
    bool: builtins.bool

    bool_2: builtins.bool
    """
    In certain languages the type declaration for this prop can shadow the `bool`
    property declaration.
    """

    date: datetime.date
    """This shadows the stdlib `datetime.date` type in Python & causes type errors."""

    date_2: datetime.date
    """
    In certain languages the type declaration for this prop can shadow the `date`
    property declaration.
    """

    float: builtins.float

    float_2: builtins.float
    """
    In certain languages the type declaration for this prop can shadow the `float`
    property declaration.
    """

    int: builtins.int

    int_2: builtins.int
    """
    In certain languages the type declaration for this prop can shadow the `int`
    property declaration.
    """
