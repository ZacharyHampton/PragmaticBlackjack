import websocket
import requests
from dataclasses import dataclass
from datetime import datetime

"""
bjSocket$
GameConstants
"""


@dataclass
class Response:
    success: bool
    message: str | None = None


class PragmaticActions:
    def __init__(self, tableId: str, sessionId: str):
        self.tableId = tableId
        self._sessionId = sessionId
        self.headers = {
            'authority': 'gs7.pragmaticplaylive.net',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'origin': 'https://client.pragmaticplaylive.net',
            'pragma': 'no-cache',
            'referer': 'https://client.pragmaticplaylive.net/',
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        }

    @staticmethod
    def getTimeString():
        return str(int(datetime.now().timestamp()))

    def _get_base_params(self):
        return {
            'table_id': self.tableId,
            'JSESSIONID': self._sessionId,
            'ck': self.getTimeString(),
            'game_mode': 'blackjack_desktop',
        }

    @staticmethod
    def _getDecisionUrl(isPreDecision: bool):
        return 'https://gs7.pragmaticplaylive.net/api/ui/blackjack/predecision' if isPreDecision else 'https://gs7.pragmaticplaylive.net/api/ui/blackjack/decision'

    def sitDown(self, seatNumber: int) -> Response:
        # return self.ws.send(
        #             "<command channel='table-{}'> <sitdown gameMode='blackjack' seatNum='{}'></sitdown></command>".format(
        #                 self.tableId, seatNumber))

        params = self._get_base_params() | {
            'seat': '{}'.format(seatNumber),
        }

        response = requests.get('https://gs7.pragmaticplaylive.net/api/ui/blackjack/sitdown', params=params,
                                headers=self.headers)

        # todo: check response
        return Response(success=True)

    def unseat(self, seatNumber: int) -> Response:
        params = self._get_base_params() | {
            's': '{}'.format(seatNumber),
        }

        response = requests.get('https://gs7.pragmaticplaylive.net/api/ui/blackjack/unseat', params=params,
                                headers=self.headers)

        # todo: check response
        return Response(success=True)

    def placeBet(self, seatNumber: int, gameId: int, betAmount: int) -> Response:
        params = self._get_base_params()

        response = requests.post('https://gs7.pragmaticplaylive.net/api/ui/blackjack/placebet', params=params,
                                 headers=self.headers,
                                 json={
                                     {
                                         "tableId": self.tableId,
                                         "gameId": gameId,
                                         "ck": int(self.getTimeString()),
                                         "bets": [
                                             {
                                                 "seat": seatNumber,
                                                 "mainBet": True,
                                                 "betAmount": betAmount
                                             }
                                         ],
                                         "gameMode": "blackjack_desktop"
                                     }
                                 })

        # todo: check response
        return Response(success=True)

    def hit(self, seatNumber: int, gameId: int, isPreDecision: bool) -> Response:
        params = self._get_base_params()

        response = requests.post(self._getDecisionUrl(isPreDecision=isPreDecision), params=params,
                                 headers=self.headers,
                                 json={
                                     "tableId": self.tableId,
                                     "gameId": gameId,
                                     "seat": seatNumber,
                                     "dec": "hit",
                                     "ck": int(self.getTimeString()),
                                     "gameMode": "blackjack_desktop"
                                 })

        # todo: check response
        return Response(success=True)

    def stand(self, seatNumber: int, gameId: int, isPreDecision: bool) -> Response:
        params = self._get_base_params()

        response = requests.post(self._getDecisionUrl(isPreDecision=isPreDecision), params=params,
                                 headers=self.headers,
                                 json={
                                     "tableId": self.tableId,
                                     "gameId": gameId,
                                     "seat": seatNumber,
                                     "dec": "stand",
                                     "ck": int(self.getTimeString()),
                                     "gameMode": "blackjack_desktop"
                                 })

        # todo: check response
        return Response(success=True)

    def double_down(self, seatNumber: int, gameId: int, isPreDecision: bool) -> Response:
        params = self._get_base_params()

        response = requests.post(self._getDecisionUrl(isPreDecision=isPreDecision), params=params,
                                 headers=self.headers,
                                 json={
                                     "tableId": self.tableId,
                                     "gameId": gameId,
                                     "seat": seatNumber,
                                     "dec": "double",
                                     "ck": int(self.getTimeString()),
                                     "gameMode": "blackjack_desktop"
                                 })

        # todo: check response
        return Response(success=True)

    def split(self, seatNumber: int, gameId: int, isPreDecision: bool) -> Response:
        params = self._get_base_params()

        response = requests.post(self._getDecisionUrl(isPreDecision=isPreDecision), params=params,
                                 headers=self.headers,
                                 json={
                                     "tableId": self.tableId,
                                     "gameId": gameId,
                                     "seat": seatNumber,
                                     "dec": "split",
                                     "ck": int(self.getTimeString()),
                                     "gameMode": "blackjack_desktop"
                                 })

        # todo: check response
        return Response(success=True)
