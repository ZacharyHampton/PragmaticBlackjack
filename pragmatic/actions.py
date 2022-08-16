import websocket

"""
bjSocket$
GameConstants
"""


class PragmaticActions:
    def __init__(self, ws: websocket.WebSocket, tableId: str):
        self.ws = ws
        self.tableId = tableId

    def sitDown(self, seatNumber: int):
        # return self.ws.send(
        #             "<command channel='table-{}'> <sitdown gameMode='blackjack' seatNum='{}'></sitdown></command>".format(
        #                 self.tableId, seatNumber))
        pass

    def placeBet(self):
        pass
