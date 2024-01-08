import builtins
from contextvars import ContextVar
from typing import Callable, List, Optional, Type, Any
from typing_extensions import Literal
from threading import Lock
from types import TracebackType

from contextif.variable import flags


class ContextState:
    def __init__(self, variable: ContextVar[Optional[List[bool]]] = flags, builtin: bool = True) -> None:
        self.flags = variable
        self.lock = Lock()
        if builtin:
            builtins.state = self  # type: ignore[attr-defined]

    def __call__(self, some_callable: Callable[[], Any], *args: Any, **kwargs: Any) -> Any:
        if self.flags.get():
            return some_callable(*args, **kwargs)

    def __enter__(self) -> None:
        with self.lock:
            if self.flags.get() is None:
                self.flags.set([])

            self.flags.get().append(True)  # type: ignore[union-attr]

    def __exit__(self, exception_type: Optional[Type[Exception]], exception_value: Optional[Exception], traceback: Optional[TracebackType]) -> Literal[False]:
        with self.lock:
            self.flags.get().pop()  # type: ignore[union-attr]
            return False


state = ContextState()
