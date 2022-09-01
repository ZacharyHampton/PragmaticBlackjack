from pragmatic.controller import PragmaticController
import asyncio
import os
from dotenv import load_dotenv
import halves
from classes import Table, Player, Hand
from basic_strategy import basic_strategy

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

            if int(data['seat']['@num']) == SeatNumber:
                GameTable.players[int(data['seat']['@num'])].isMe = True

        elif data['seat']['@event'] == "stand":
            del GameTable.players[int(data['seat']['@num'])]

    if data.get('card'):
        soft = False
        score = 0
        CardCounter.add_card(data['card']['@sc'][0])
        if "/" in data['card']['@score']:
            soft = True
            score = int(data['card']['@score'].split('/')[1])

        hand = GameTable.players[int(data['card']['@seat'])].currentHand
        hand.isSoft = soft
        hand.currentHandValue = score
        GameTable.players[int(data['card']['@seat'])].currentHand = hand

    if data.get('pre_decisioninc') or data.get('decisioninc'):
        prefix = 'pre_decisioninc' if data.get('pre_decisioninc') else 'decisioninc'
        is_pre_decision = prefix == 'pre_decisioninc'

        if SeatNumber == int(data['pre_decisioninc']['@seat']):
            decision = basic_strategy(player_val=GameTable.players[SeatNumber].currentHand.currentHandValue,
                                      dealer_val=GameTable.dealer.currentHand.currentHandValue,
                                      soft=GameTable.players[SeatNumber].currentHand.isSoft,
                                      pair=data[prefix]['@cansplit'] != "false"
                                      )
            match decision:
                case "stand":
                    game.actions.stand(seatNumber=SeatNumber, gameId=0, isPreDecision=is_pre_decision)
                case "hit":
                    game.actions.hit(seatNumber=SeatNumber, gameId=0, isPreDecision=is_pre_decision)
                case "double":
                    game.actions.double_down(seatNumber=SeatNumber, gameId=0, isPreDecision=is_pre_decision)
                case "split":
                    game.actions.split(seatNumber=SeatNumber, gameId=0, isPreDecision=is_pre_decision)


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
