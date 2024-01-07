from typing import Iterable

from tpify.core.response import TPResponse
from tpify.core.status_code import TPStatus, TPStatusCustom
from tpify.core.wrapper import tpify


@tpify(exception_type_map={TypeError: TPStatus.InputError})
def append_statuses_tp(statuses: Iterable[str]) -> TPStatusCustom:
    return TPStatusCustom(
        "TPStatusCustom", [status.name for status in TPStatus] + list(statuses)
    )
