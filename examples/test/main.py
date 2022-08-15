from pragmatic.controller import PragmaticController
import asyncio
import os
from dotenv import load_dotenv
import websocket

load_dotenv()
SESSIONID = os.getenv('SESSIONID')
TABLEID = os.getenv('TABLEID')
CARDSPLAYED = 0

# <betsopen> = open for bets
# <seat> = describes the seat (who is on it) (check for open seats)
#: <card> = describes dealt cards


async def handler(game: PragmaticController, data: dict):
    global CARDSPLAYED
    if data.get('card'):
        if data['card']['@initial'] == 'false':
            CARDSPLAYED += 1
            print("Cards played:", CARDSPLAYED, data)
    # print(data)


async def main():
    game = PragmaticController(SESSIONID, TABLEID, handler=handler)
    await game.connect()
    input('Press Enter to exit...')


if __name__ == '__main__':
    asyncio.new_event_loop().run_until_complete(main())
