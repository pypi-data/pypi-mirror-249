![logo](https://raw.githubusercontent.com/pomponchik/contextif/develop/docs/assets/logo_3.svg)

[![Downloads](https://static.pepy.tech/badge/contextif/month)](https://pepy.tech/project/contextif)
[![Downloads](https://static.pepy.tech/badge/contextif)](https://pepy.tech/project/contextif)
[![codecov](https://codecov.io/gh/pomponchik/contextif/graph/badge.svg?token=krgDghlvu7)](https://codecov.io/gh/pomponchik/contextif)
[![Hits-of-Code](https://hitsofcode.com/github/pomponchik/contextif?branch=main)](https://hitsofcode.com/github/pomponchik/contextif/view?branch=main)
[![Test-Package](https://github.com/pomponchik/contextif/actions/workflows/tests_and_coverage.yml/badge.svg)](https://github.com/pomponchik/contextif/actions/workflows/tests_and_coverage.yml)
[![Python versions](https://img.shields.io/pypi/pyversions/contextif.svg)](https://pypi.python.org/pypi/contextif)
[![PyPI version](https://badge.fury.io/py/contextif.svg)](https://badge.fury.io/py/contextif)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# contextif: run the function only in a specific context

Sometimes we may need to run a function only if it happens in a strictly defined context. In this case, we can use this mini library.

Install it:

```bash
pip install contextif
```

And use:

```python
from contextif import state

with state:
    state(print, 'hello,', 'world!')  # It will be printed.

state(print, "it's me, Mario!")  # It won't.
```

Using `state` as a function, you can pass another function and arguments to it there. It will be called only if it happens in a context created also using `state`. The function will not be called out of context.

For convenience, after the first import of `state`, this variable becomes builtin and you can access it in other modules of your program without importing.
