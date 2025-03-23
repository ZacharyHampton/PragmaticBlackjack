import websockets
from websockets import Origin
import time
import asyncio


class _CustomPingWebSocket(websockets.WebSocketClientProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def ping(self, *args, **kwargs):
        await super().send('<ping time={}></ping>'.format(int(time.time())))

        return super().ping(*args, **kwargs)


class Websocket:
    def __init__(self, table_id: str, session_id: str, game_server: str = "gs14"):
        self._table_id = table_id
        self._session_id = session_id
        self.game_server = game_server

        self.has_previously_disconnected = False
        self.current_connection: websockets.WebSocketClientProtocol | None = None

    @property
    def uri(self):
        return "wss://{}.pragmaticplaylive.net/game?JSESSIONID={}&tableId={}".format(
            self.game_server, self._session_id, self._table_id
        ) + ("&reconnect=true" if self.has_previously_disconnected else "")

    @property
    def connected(self):
        return self.current_connection is not None and self.current_connection.open

    def get_connection(self):
        return websockets.connect(
                self.uri,
                origin=Origin("https://client.pragmaticplaylive.net"),
                ping_interval=10,
                create_protocol=_CustomPingWebSocket
        )

    def send_raw_message(self, message: str):
        asyncio.create_task(self.current_connection.send(message))

    def disconnect(self):
        if self.current_connection:
            asyncio.create_task(self.current_connection.close())
