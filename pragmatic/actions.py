import websocket
import requests


"""
bjSocket$
GameConstants
"""


class PragmaticActions:
    def __init__(self, ws: websocket.WebSocket, tableId: str):
        self.ws = ws
        self.tableId = tableId
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

    def sitDown(self, seatNumber: int):
        # return self.ws.send(
        #             "<command channel='table-{}'> <sitdown gameMode='blackjack' seatNum='{}'></sitdown></command>".format(
        #                 self.tableId, seatNumber))

        params = {
            'seat': '0',
            'table_id': 'bas2sgk7ph2ybj17',
            'JSESSIONID': 'sessionid',
            'ck': '1660608699230',
            'game_mode': 'blackjack_desktop',
        }

        response = requests.get('https://gs7.pragmaticplaylive.net/api/ui/blackjack/sitdown', params=params,
                                headers=self.headers)

    def placeBet(self):
        pass
