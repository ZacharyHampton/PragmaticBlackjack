from dataclasses import dataclass
from typing import Callable
from .event import Event


@dataclass
class Handle:
    function: Callable[[Event | str], None]
    raw: bool = False


class HandlerBase:
    def __init__(self, *args, **kwargs):
        pass
