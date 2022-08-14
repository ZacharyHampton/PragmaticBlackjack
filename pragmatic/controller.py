import websocket
import time
import asyncio
import xmltodict
import pragmatic.exceptions


class PragmaticController:
    def __init__(self, sessionId: str, tableId: str, handler=None):
        self.sessionId = sessionId
        self.tableId = tableId
        self.handler = handler
        self.ws: websocket.WebSocket = websocket.WebSocket()
        self._event_loop = asyncio.get_event_loop()

    async def _handle_data(self):
        while self.ws.connected:
            data = self.ws.recv()
            if self.handler:
                if data:
                    if data == "Connection Exception":
                        raise pragmatic.exceptions.PragmaticSessionInvalid("Connection Exception")

                    if "duplicated_connection" in data:
                        raise pragmatic.exceptions.PragmaticDuplicateSession("Two sessions are active.")

                    await self.handler(self, xmltodict.parse(data))

    async def _ping(self):
        while self.ws.connected:
            time.sleep(10)
            self.ws.send('<ping time={}></ping>'.format(int(time.time())))

    async def connect(self):
        self.ws.connect('wss://gs7.pragmaticplaylive.net/game?JSESSIONID={}&tableId={}'.format(self.sessionId, self.tableId), origin='https://client.pragmaticplaylive.net')

        self._event_loop.create_task(self._handle_data())
        self._event_loop.create_task(self._ping())
        self._event_loop.run_forever()
