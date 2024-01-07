from enum import IntEnum
from typing import Iterable


class TPStatus(IntEnum):
    Unknown = 1
    OK = 2
    Continue = 3
    InputError = 4
    ProcessingError = 5
    Created = 6
    Read = 7
    Updated = 8
    Deleted = 9


class TPStatusCustom(IntEnum):
    pass
