from contextvars import ContextVar
from typing import List, Optional


flags: ContextVar[Optional[List[bool]]] = ContextVar('flags', default=None)
