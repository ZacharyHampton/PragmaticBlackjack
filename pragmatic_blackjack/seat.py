from .websocket import Websocket
import requests
from datetime import datetime


class Seat:
    def __init__(
            self,
            websocket: Websocket,
            table_id: str,
            seat_number: int,
            session_id: str,
            user_id: str = None
    ):
        self._ws = websocket
        self.table_id = table_id
        self.seat_number = seat_number
        self.session_id = session_id
        self.user_id = user_id

    @property
    def ck(self):
        return str(int(datetime.now().timestamp()))

    def sit(self):
        self._ws.send_raw_message(
            "<command channel='table-{}' > <sitdown gameMode='blackjack_desktop' seatNum='{}'></sitdown></command>".format(
                self.table_id, self.seat_number))

    def leave(self):
        """
        Leaves table
        """

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,es-US;q=0.8,es;q=0.7,es-419;q=0.6',
            'dnt': '1',
            'origin': 'https://client.pragmaticplaylive.net',
            'priority': 'u=1, i',
            'referer': 'https://client.pragmaticplaylive.net/',
            'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        }
        params = {
            "JSESSIONID": self.session_id,
            "ck": self.ck,
            "game_mode": "blackjack_desktop",
            "s": self.seat_number,
            "table_id": self.table_id,
        }

        response = requests.get(
            'https://gs14.pragmaticplaylive.net/api/ui/blackjack/unseat',
            headers=headers,
            params=params
        )

        response.raise_for_status()

    def __del__(self):
        self.leave()

    def bet(self, bet_amount: int, game_id: int):
        self._ws.send_raw_message(
            "<command  channel='table-{}'><lpbet  gameMode='blackjack_desktop' gameId='{}' userId='{}' ck='{}'>"
            "<bet  seat='{}' amount='{}' betbehind='false' perfectpair='false' bj21plus3='false' mainbet='true' ck='{}'/></lpbet >".format(self.table_id, game_id, self.user_id, self.ck, self.seat_number, bet_amount, self.ck)
        )