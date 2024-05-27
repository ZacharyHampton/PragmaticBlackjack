import websockets
from websockets import Origin
import time
import asyncio


class _CustomPingWebSocket(websockets.WebSocketClientProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def ping(self, *args, **kwargs):
        await super().ping(*args, **kwargs)
        await super().send('<ping time={}></ping>'.format(int(time.time())))


class Websocket:
    def __init__(self, table_id: str, session_id: str):
        self._table_id = table_id
        self._session_id = session_id

        self.has_disconnected = False
        self.current_connection: websockets.WebSocketClientProtocol | None = None

    @property
    def uri(self):
        return "wss://gs4.pragmaticplaylive.net/game?JSESSIONID={}&tableId={}".format(
            self._session_id, self._table_id
        ) + "&reconnect=true" if self.has_disconnected else ""

    async def _handler(self):
        async for websocket in websockets.connect(
                self.uri,
                origin=Origin("https://client.pragmaticplaylive.net"),
                ping_interval=10,
                create_protocol=_CustomPingWebSocket
        ):
            self.current_connection = websocket

            try:
                async for message in websocket:
                    #: TODO: process message
                    print(message)

            except websockets.ConnectionClosed:
                self.has_disconnected = True
                continue

    def send_raw_message(self, message: str):
        asyncio.create_task(self.current_connection.send(message))