from functools import cache as cache_decorator
from typing import Callable, Dict, Optional

from tpify.core.response import TPResponse
from tpify.core.status_code import TPStatus, TPStatusCustom

_DEFAULT_ERROR_CODE = TPStatus.ProcessingError


def tpify(exception_type_map: Optional[Dict[Exception, TPStatus]] = None) -> Callable:
    def tpify_function(func: Callable) -> Callable:
        def tpified_function(*args, **kwargs) -> TPResponse:
            try:
                result = func(*args, **kwargs)
                if (
                    isinstance(result, tuple)
                    and isinstance(
                        result[0],
                        (
                            TPStatus,
                            TPStatusCustom,
                        ),
                    )
                    and len(result) >= 2
                ):
                    if len(result) > 2:
                        return TPResponse(result[0], result[1:])
                    return TPResponse(result[0], result[1])
                return TPResponse(
                    TPStatus.OK,
                    result,
                )
            except Exception as e:
                return TPResponse(
                    (exception_type_map or dict()).get(type(e), _DEFAULT_ERROR_CODE),
                    e,
                )

        return tpified_function

    return tpify_function


def tpify_function(
    func: Callable,
    exception_type_map: Optional[Dict[Exception, TPStatus]] = None,
):
    return tpify(exception_type_map=exception_type_map)(func)
