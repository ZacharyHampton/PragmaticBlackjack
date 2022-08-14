from pragmatic.controller import PragmaticController
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
SESSIONID = os.getenv('SESSIONID')


# <betsopen> = open for bets
# <seat> = describes the seat (who is on it) (check for open seats)
#: <card> = describes dealt cards


async def handler(data: dict):
    print(data)


async def main():
    game = PragmaticController(SESSIONID, 'sbjsbim6hsbj2421', handler=handler)
    await game.connect()
    input('Press Enter to exit...')


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
