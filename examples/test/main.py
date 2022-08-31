from pragmatic.controller import PragmaticController
import asyncio
import os
from dotenv import load_dotenv
import halves
from classes import Table, Player, Hand

load_dotenv()
SESSIONID = os.getenv('SESSIONID')
TABLEID = os.getenv('TABLEID')

GameTable = Table()
CardCounter = halves.GameState(decks=7, bank_roll=100.00)
AllowGame = False
SeatNumber = 1


# <betsopen> = open for bets
# <seat> = describes the seat (who is on it) (check for open seats)
#: <card> = describes dealt cards
#: split case on decision: <decisioninc seat="2" score="4" game="1850564704" cansplit="true" dealerscore="10" id="by7mco374logcksp9vcsjixbybnew2fg" time="14" candouble="true" preautostand="false" userid="ppc1661951196580" hand="0" seq="710"></decisioninc>
#: <pre_decisioninc seat="2" score="4" game="1850564704" cansplit="true" candouble="true" hand="0" seq="664"></pre_decisioninc>
#: dealer seat is -1

async def handler(game: PragmaticController, data: dict):
    if not AllowGame:
        pass

    if data.get('dealer'):
        print(data)  #: debug line

    if data.get('seat'):
        if data['seat']['@event'] == "sit":
            GameTable.players[int(data['seat']['@num'])] = Player(
                username=data['seat']['@screen_name'],
                isMe=False,
                bet=0.00,
                currentHand=Hand(
                    currentHandValue=0,
                    isSoft=False,
                    isPair=False,
                )
            )
        elif data['seat']['@event'] == "stand":
            del GameTable.players[int(data['seat']['@num'])]

    if data.get('card'):
        soft = False
        score = 0

        if "/" in data['card']['@score']:
            soft = True
            score = int(data['card']['@score'].split('/')[0])

        hand = GameTable.players[int(data['card']['@seat'])].currentHand
        hand.isSoft = soft
        hand.currentHandValue = score





async def main():
    game = PragmaticController(SESSIONID, TABLEID, handler=handler)
    await game.connect()
    while True:
        input("Press enter on every shuffle.")
        CardCounter.shuffle()
        global AllowGame
        AllowGame = True


if __name__ == '__main__':
    asyncio.new_event_loop().run_until_complete(main())
