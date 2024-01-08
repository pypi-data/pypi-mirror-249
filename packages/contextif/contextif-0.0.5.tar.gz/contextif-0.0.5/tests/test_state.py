import io
from contextlib import redirect_stdout

import pytest

from contextif import state


def test_set_context_and_run_function():
    flag = False
    def function():
        nonlocal flag
        flag = True

    with state:
        state(function)

    assert flag


def test_not_set_context_and_run_function():
    flag = False
    def function():
        nonlocal flag
        flag = True

    state(function)

    assert not flag


def test_no_hide_exceptions():
    def function():
        raise ValueError

    with pytest.raises(ValueError):
        with state:
            state(function)


def test_builtin():
    with io.StringIO() as buffer, redirect_stdout(buffer):
        subglobals = globals().copy()
        subglobals.pop('state')
        exec('with state: state(print, "kek", end="")', {'print': print})
        assert buffer.getvalue() == 'kek'
