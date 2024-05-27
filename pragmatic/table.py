from typing import Callable
from .event import Event
from .handler import HandlerBase, Handle
import websockets
import websocket


class Table:
    def __init__(
            self,
            table_id: str,
            session_id: str,
            handler: HandlerBase = None,
            handles: dict[Event, Handle] = None,
    ):
        self.table_id = table_id
        self.session_id = session_id

        self.handler = handler
        self.handles = handles or {}

        self._ws = websockets.Web

    def register(self, handler: HandlerBase) -> None:
        """
        Register a handler class to the table

        :param handler: Handler class to register
        :return: None
        """

        self.handler = handler

    def register_handle(self, event: Event, function: Callable[[Event | str], None], raw: bool = False) -> None:
        """
        Register an event to a function

        :param event: Event type to register
        :param function: Function to call when event is triggered
        :param raw: If True, the function will be called with the raw event data
        :return: None
        """

        self.handles[event] = Handle(function, raw)

    def connect(self):
        pass
