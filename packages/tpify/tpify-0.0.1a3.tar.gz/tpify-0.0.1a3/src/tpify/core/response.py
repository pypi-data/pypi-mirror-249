from collections import namedtuple

from tpify.core.status_code import TPStatus as tp

TPResponse = namedtuple(
    "TPResponse", ["status_code", "content"], defaults=[tp.Unknown, None]
)
