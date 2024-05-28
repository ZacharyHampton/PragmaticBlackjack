from typing import Callable, Type
from .event import Event, _get_event_type, _get_event_name
from .handler import HandlerBase
from .websocket import Websocket
import websockets
import asyncio
from .exceptions import PragmaticSessionInvalid, PragmaticDuplicateSession
import inspect


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

        self._event_loop = asyncio.get_event_loop()
        self._ws = Websocket(table_id, session_id)

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
        :return: None
        """

        self.handles[event] = function

    async def _websocket_handler(self):
        async for websocket in self._ws.get_connection():
            self._ws.current_connection = websocket

            try:
                async for message in websocket:
                    if message == "Connection Exception":
                        raise PragmaticSessionInvalid("Session is invalid.")

                    if "duplicated_connection" in message:
                        raise PragmaticDuplicateSession("Two sessions are active.")

                    await asyncio.create_task(self._handle_message(message))

            except websockets.ConnectionClosed:
                self.has_previously_disconnected = True
                continue

    async def _handle_message(self, message: str):
        event_type = _get_event_type(_get_event_name(message))

        handle = self.handles.get(event_type)
        if handle:
            argument_count = len(inspect.signature(handle).parameters)
            event = event_type.from_raw(message)

            if argument_count == 0:
                self.handles.pop(type(event))
            elif argument_count == 1:
                handle(event)
            else:
                handle(event, message)

    def connect(self):
        self._event_loop.run_until_complete(self._websocket_handler())

    def sit(self, seat_number: int):
        self._ws.send_raw_message("<command channel='table-{}' > <sitdown gameMode='blackjack_desktop' seatNum='{}'></sitdown></command>".format(self.table_id, seat_number))

