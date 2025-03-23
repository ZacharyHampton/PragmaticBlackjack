from typing import Callable, Type
from .event import Event, _get_event_type, _get_event_name, Switch
from .handler import HandlerBase
from .websocket import Websocket
from .seat import Seat
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
            handles: dict[Type[Event], list[Callable]] = None,
    ):
        self.table_id = table_id
        self.session_id = session_id

        self.handles = handles or {}

        if handler:
            self._process_base_class_handles(handler)

        self._event_loop = asyncio.get_event_loop()
        self._ws = Websocket(table_id, session_id)

    def _process_base_class_handles(self, handler_class: HandlerBase):
        for handle in handler_class.__mapping__:
            self.register_handle(handle, getattr(handler_class, handler_class.__mapping__[handle]))

    def register(self, handler: HandlerBase) -> None:
        """
        Register a handler class to the table

        :param handler: Handler class to register
        :return: None
        """

        self._process_base_class_handles(handler)

    def register_handle(self, event: Type[Event], function: Callable) -> None:
        """
        Register an event to a function

        :param event: Event type to register
        :param function: Function to call when event is triggered
        :return: None
        """

        if self.handles.get(event):
            self.handles[event].append(event)
        else:
            self.handles[event] = [function]

    def handle_switch(self, event: Switch):
        self.disconnect()

        self._ws = Websocket(self.table_id, self.session_id, event.game_server)
        return self.connect()

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

        handles = self.handles.get(event_type)
        if handles:
            for handle in handles:
                details = inspect.signature(handle)
                argument_count = len(details.parameters)
                event = event_type.from_raw(message)

                if isinstance(event, Switch):
                    return self.handle_switch(event)

                if argument_count == 0:  #: Function has no arguments, therefore useless
                    self.handles.pop(type(event))
                elif argument_count == 1:
                    handle(event)
                else:
                    handle(event, message)

    def connect(self):
        asyncio.run(self._websocket_handler())

    def disconnect(self):
        self._ws.disconnect()

    def sit(self, seat_number: int) -> Seat:
        seat = Seat(self._ws, self.table_id, seat_number, self.session_id)
        seat.sit()

        return seat

    def handle(self, event: Type[Event]):
        """
        Table.handle decorator, used to register events to functions

        :param event:
        :return:
        """

        def wrapper(func):
            self.register_handle(event, func)
            return func

        return wrapper

    def handle_all(self, function: Callable):
        """
        Table.handle_all decorator, used to register all events to a function

        :param function:
        :return:
        """

        for event in Event.__subclasses__():
            self.register_handle(event, function)

