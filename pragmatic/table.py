from typing import Callable, Type, Optional
from .event import Event, _get_event
from .handler import HandlerBase
from .websocket import Websocket
import websockets
import asyncio
from .exceptions import PragmaticSessionInvalid, PragmaticDuplicateSession


class Table:
    def __init__(
            self,
            table_id: str,
            session_id: str,
            handler: HandlerBase = None,
            handles: dict[Type[Event], Callable] = None,
    ):
        self.table_id = table_id
        self.session_id = session_id

        self.handler = handler
        self.handles = handles or {}

        self._event_loop = asyncio.new_event_loop()
        self._ws = Websocket(table_id, session_id)
        self.connect()

    def register(self, handler: HandlerBase) -> None:
        """
        Register a handler class to the table

        :param handler: Handler class to register
        :return: None
        """

        self.handler = handler

    def register_handle(self, event: Type[Event], function: Callable) -> None:
        """
        Register an event to a function

        :param event: Event type to register
        :param function: Function to call when event is triggered
        :param raw: If True, the function will be called with the raw event data
        :return: None
        """

        self.handles[event] = function

    async def _websocket_handler(self):
        print("Connecting to websocket")

        async for websocket in self._ws.get_connection():
            self._ws.current_connection = websocket

            try:
                async for message in websocket:
                    if message == "Connection Exception":
                        raise PragmaticSessionInvalid("Session is invalid.")

                    if "duplicated_connection" in message:
                        raise PragmaticDuplicateSession("Two sessions are active.")

                    await self._handle_message(message)

            except websockets.ConnectionClosed:
                self.has_previously_disconnected = True
                continue

    async def _handle_message(self, message: str):
        event = _get_event(message)

        handle = self.handles.get(type(event))
        if handle:
            handle(event, message)

    def connect(self):
        self._event_loop.create_task(self._websocket_handler())
        self._event_loop.run_forever()

        while not self._ws.connected:
            pass

