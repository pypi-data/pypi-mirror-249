import pytest

from tpify import TPResponse, tp, tpify, tpify_function
from tpify.core.wrapper import _DEFAULT_ERROR_CODE


def double_number(n: int) -> int:
    return n * 2


class TestCoreFunction:
    @pytest.mark.parametrize("n", [2])
    def test_double_number_pie_syntax(_, n):
        @tpify()
        def double_number_decorator_tp(n: int):
            return double_number(n)

        resp = double_number_decorator_tp(n)
        assert isinstance(resp, tuple)
        assert isinstance(resp, TPResponse)
        assert resp.content == double_number(n)
        assert resp.status_code == tp.OK

    @pytest.mark.parametrize("n", [2])
    def test_double_number_named_function(_, n):
        double_tp = tpify_function(double_number)
        resp = double_tp(n)
        assert isinstance(resp, tuple)
        assert isinstance(resp, TPResponse)
        assert resp.content == double_number(n)
        assert resp.status_code == tp.OK

    @pytest.mark.parametrize("n", [2])
    def test_correct_tuple_vals(_, n):
        @tpify()
        def double_number_decorator_tp(n: int):
            return (
                tp.OK,
                n * 2,
            )

        resp = double_number_decorator_tp(n)
        assert isinstance(resp, tuple)
        assert isinstance(resp, TPResponse)
        assert resp.content == double_number(n)
        assert resp.status_code == tp.OK

    @pytest.mark.parametrize("n", [2])
    def test_too_many_tuple_vals(_, n):
        @tpify()
        def double_number_decorator_tp(n: int):
            return (tp.OK, n * 2, n, double_number_decorator_tp)

        resp = double_number_decorator_tp(n)
        assert isinstance(resp, tuple)
        assert isinstance(resp, TPResponse)
        assert resp.content == (
            double_number(n),
            n,
            double_number_decorator_tp,
        )
        assert resp.status_code == tp.OK

    @pytest.mark.parametrize("n", [2])
    def test_non_tp_tuple(_, n):
        @tpify()
        def double_number_decorator_tp(n: int):
            return (2, n * 2, n, double_number_decorator_tp)

        resp = double_number_decorator_tp(n)
        assert isinstance(resp, tuple)
        assert isinstance(resp, TPResponse)
        assert resp.content == (2, 4, 2, double_number_decorator_tp)


class TestExceptions:
    exception_type_map = {
        ValueError: tp.InputError,
        RuntimeError: tp.ProcessingError,
    }

    def test_raise_exception_default(_):
        @tpify()
        def raise_exception_tp() -> TPResponse:
            raise Exception("This could be any exception in a function")

        resp = raise_exception_tp()
        assert resp.status_code == tp.ProcessingError
        assert isinstance(resp.content, Exception)

    def test_raise_exception_status(_):
        @tpify()
        def raise_exception_tp():
            return (tp.InputError, ValueError("You're not allowed to do that"))

        resp = raise_exception_tp()
        assert resp.status_code == tp.InputError
        assert isinstance(resp.content, ValueError)

    @pytest.mark.parametrize(
        "error,tp_status",
        [
            (ValueError("This is a ValueError"), tp.InputError),
            (RuntimeError, tp.ProcessingError),
            (IndentationError, tp.InputError),
        ],
    )
    def test_raise_exception_status(self, error: Exception, tp_status: tp):
        @tpify(exception_type_map=self.exception_type_map)
        def raise_exception_tp():
            raise error

        resp = raise_exception_tp()
        if type(resp.content) in self.exception_type_map:
            assert resp.status_code == tp_status
        else:
            assert resp.status_code == _DEFAULT_ERROR_CODE
