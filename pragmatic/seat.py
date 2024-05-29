from .websocket import Websocket


class Seat:
    def __init__(
            self,
            websocket: Websocket,
            table_id: str,
            seat_number: int
    ):
        self._ws = websocket
        self.table_id = table_id
        self.seat_number = seat_number

    def sit(self):
        self._ws.send_raw_message("<command channel='table-{}' > <sitdown gameMode='blackjack_desktop' seatNum='{}'></sitdown></command>".format(self.table_id, self.seat_number))

