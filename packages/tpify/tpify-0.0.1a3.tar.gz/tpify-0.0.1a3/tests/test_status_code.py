from typing import Iterable

import pytest

from tpify import TPResponse, tp, tpify, tpify_function
from tpify.core.extendability import append_statuses_tp
from tpify.core.status_code import TPStatusCustom
from tpify.core.wrapper import _DEFAULT_ERROR_CODE


class TestStatusCodes:
    @pytest.mark.parametrize(
        "new_codes, ",
        [("NewStatus",), ("A", "B", "C", "D")],
    )
    def test_append_statuses(_, new_codes: Iterable):
        new_statuses = append_statuses_tp(new_codes).content
        assert len(new_statuses) == len(new_codes) + len(tp)
        for new_code in new_codes:
            assert isinstance(
                getattr(new_statuses, new_code),
                (
                    tp,
                    TPStatusCustom,
                ),
            )

    @pytest.mark.parametrize(
        "new_codes,return_code,should_error",
        [
            (
                ("A", "B", "C", "D"),
                "D",
                False,
            ),
            (
                ("A", "B", "C", "D"),
                "AA",
                True,
            ),
            (
                ("A", "B", "C", "D"),
                "OK",
                False,
            ),
        ],
    )
    def test_append_status_returning(
        _, new_codes: Iterable, return_code: str, should_error: bool
    ):
        new_statuses_raw: TPResponse = append_statuses_tp(new_codes)
        assert new_statuses_raw.status_code == tp.OK
        new_statuses = new_statuses_raw.content
        assert new_statuses_raw.status_code == new_statuses["OK"]

        @tpify()
        def return_new_code_tp(return_code: str) -> TPResponse:
            return (new_statuses[return_code], return_code)

        resp = return_new_code_tp(return_code=return_code)
        if not should_error:
            assert resp.status_code == new_statuses[return_code]
            assert resp.content == return_code
        else:
            assert resp.status_code == _DEFAULT_ERROR_CODE

    @pytest.mark.parametrize(
        "new_codes,expected_status",
        [
            (("OK", "OK", "OK", "OK"), tp.InputError),
            (
                (
                    "New",
                    "New",
                ),
                tp.InputError,
            ),
            (([1, 2],), tp.InputError),
            ((12,), tp.InputError),
            (12, tp.InputError),
        ],
    )
    def test_append_status_overload(_, new_codes: Iterable, expected_status: tp):
        new_statuses_raw: TPResponse = append_statuses_tp(new_codes)
        assert new_statuses_raw.status_code == expected_status
