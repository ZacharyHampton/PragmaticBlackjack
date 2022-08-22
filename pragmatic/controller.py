import websocket
import time
import asyncio
import xmltodict
import pragmatic.exceptions
from pragmatic.actions import PragmaticActions


class PragmaticController:
    def __init__(self, sessionId: str, tableId: str, handler=None):
        self._sessionId = sessionId
        self.tableId = tableId
        self._handler = handler
        self._ws: websocket.WebSocket = websocket.WebSocket()
        self._event_loop = asyncio.get_event_loop()
        self.actions = PragmaticActions(self._ws, self.tableId)

    async def _handle_data(self):
        while self._ws.connected:
            try:
                data = self._ws.recv()
            except websocket.WebSocketConnectionClosedException:
                print('Disconnected, reconnecting...')
                await self.connect(reconnect=True)
                return await self._handle_data()

            if self._handler:
                if data:
                    if data == "Connection Exception":
                        raise pragmatic.exceptions.PragmaticSessionInvalid("Connection Exception")

                    if "duplicated_connection" in data:
                        raise pragmatic.exceptions.PragmaticDuplicateSession("Two sessions are active.")

                    await self._handler(self, xmltodict.parse(data))

    async def _ping(self):
        while True:
            while self._ws.connected:
                time.sleep(10)
                self._ws.send('<ping time={}></ping>'.format(int(time.time())))

    async def connect(self, reconnect=False):
        if reconnect is False:
            self._ws.connect(
                'wss://gs7.pragmaticplaylive.net/game?JSESSIONID={}&tableId={}'.format(self._sessionId, self.tableId),
                origin='https://client.pragmaticplaylive.net')

            if self._ws.connected:
                print('Connected.')

            self._event_loop.create_task(self._handle_data())
            self._event_loop.create_task(self._ping())
            self._event_loop.run_forever()
        else:
            self._ws.connect(
                'wss://gs7.pragmaticplaylive.net/game?JSESSIONID={}&tableId={}&reconnect=true'.format(self._sessionId,
                                                                                                      self.tableId),
                origin='https://client.pragmaticplaylive.net')

        if self._ws.connected:
            print('Connected.')
