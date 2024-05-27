import websockets
from websockets import Origin
import time


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
            try:
                async for message in websocket:
                    print(message)

            except websockets.ConnectionClosed:
                self.has_disconnected = True
                continue
