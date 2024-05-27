from typing import Callable
from .event import Event
from .handler import HandlerBase


class Table:
    def __init__(
            self,
            table_id: str,
            session_id: str,
            handler: HandlerBase = None,
            handles: list = None,
    ):
        self.table_id = table_id
        self.session_id = session_id

    def register(self, handler: HandlerBase):
        pass

    def register_handle(self, event: Event, function: Callable[[Event], None]):
        pass

    def connect(self):
        pass
