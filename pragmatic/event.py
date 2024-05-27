from dataclasses import dataclass
import xmltodict
import re


@dataclass
class Event:
    @staticmethod
    def _xml_to_json(data: str) -> dict:
        return xmltodict.parse(data)

    @classmethod
    def from_raw(cls, data: str) -> "Event": ...


@dataclass
class Table(Event):
    """
    Creates a new table or opens an existing table

    XML Example: <table newTable="false" openTime="" seq="1">BJ36.1</table>
    """

    new_table: bool
    open_time: str

    @classmethod
    def from_raw(cls, data: str) -> "Table":
        data = cls._xml_to_json(data)

        return cls(
            new_table=data["@newTable"] == "true",
            open_time=data["@openTime"],
        )


@dataclass
class Seat(Event):
    """
    Seat event
    XML Example: <seat casino_id="ppcds00000003709" country_code="CA" screen_name="itsazert" user_id="ppc1716788013363" casino_name="PP Rare Stake" num="2" event="sit" table_id="bj321mstakebj321" enrollment_date="2024-05-27" currency_code="CAD" sidebets="false" seq="3">11d74766-f84f-4168-8ff5-285cf614da8d 11d74766-f84f-4168-8ff5-285cf614da8d</seat>
    XML Example: <seat seats_taken="6" user_id="ppc1643442204078" idle="true" num="5" event="stand" table_id="bj361mstakebj361" type="timeout" seq="7067"></seat>
    """

    casino_id: str
    country_code: str
    screen_name: str
    user_id: str
    casino_name: str
    num: int
    event: str
    table_id: str
    enrollment_date: str
    currency_code: str
    sidebets: bool
    seats_taken: int | None = None
    idle: bool | None = None
    type: str | None = None

    @classmethod
    def from_raw(cls, data: str) -> "Seat":
        data = cls._xml_to_json(data)

        return cls(
            casino_id=data["@casino_id"],
            country_code=data["@country_code"],
            screen_name=data["@screen_name"],
            user_id=data["@user_id"],
            casino_name=data["@casino_name"],
            num=int(data["@num"]),
            event=data["@event"],
            table_id=data["@table_id"],
            enrollment_date=data["@enrollment_date"],
            currency_code=data["@currency_code"],
            sidebets=data["@sidebets"] == "true",
            seats_taken=int(data["@seats_taken"]) if "@seats_taken" in data else None,
            idle=data["@idle"] == "true" if "@idle" in data else None,
            type=data["@type"] if "@type" in data else None,
        )


@dataclass
class Pong(Event):
    """
    Pong event
    XML Example: <pong channel="" time="1716790886214" seq="1109"></pong>
    """

    time: str

    @classmethod
    def from_raw(cls, data: str) -> "Pong":
        data = cls._xml_to_json(data)

        return cls(
            time=data["@time"],
        )


@dataclass
class Card(Event):
    """
    Dealt to player's seat number with score value -- seat="-1" for dealer

    XML Example: <card seat="2" sc="9D2" score="9" game="4694781004" resulttime="Mon May 27 06:06:56 UTC 2024" initial="true" hand="0" seq="27">20</card>
    """

    seat: int
    sc: str
    score: int
    game: int
    result_time: str
    initial: bool
    hand: int

    @classmethod
    def from_raw(cls, data: str) -> "Card":
        data = cls._xml_to_json(data)

        return cls(
            seat=int(data["@seat"]),
            sc=data["@sc"],
            score=int(data["@score"]),
            game=int(data["@game"]),
            result_time=data["@resulttime"],
            initial=data["@initial"] == "true",
            hand=int(data["@hand"]),
        )


@dataclass
class PreDecision(Event):
    """
    Event asks each player before initial player's turn

    XML Example: <predecision seat="1" game="4694781004" code="102" action="playerCall" hand="0" seq="50">Decision: Hit</predecision>
    """

    seat: int
    game: int
    code: int
    action: str
    hand: int
    decision: str

    @classmethod
    def from_raw(cls, data: str) -> "PreDecision":
        data = cls._xml_to_json(data)

        return cls(
            seat=int(data["@seat"]),
            game=int(data["@game"]),
            code=int(data["@code"]),
            action=data["@action"],
            hand=int(data["@hand"]),
            decision=data["#text"],
        )


@dataclass
class DecisionInc(Event):
    """
    Event asked directly to player during their turn validating split/double

    XML Example: <decisioninc seat="4" score="16" game="4695117904" cansplit="true" dealerscore="10" id="c2sktf5jijg9nxatwrjkz7q8gnwx9208" time="14" candouble="true" preautostand="false" userid="ppc1707004956891" hand="0" seq="3483"></decisioninc>
    """

    seat: int
    score: int
    game: int
    can_split: bool
    dealer_score: int
    id: str
    time: int
    can_double: bool
    pre_auto_stand: bool
    user_id: str
    hand: int

    @classmethod
    def from_raw(cls, data: str) -> "DecisionInc":
        data = cls._xml_to_json(data)

        return cls(
            seat=int(data["@seat"]),
            score=int(data["@score"]),
            game=int(data["@game"]),
            can_split=data["@cansplit"] == "true",
            dealer_score=int(data["@dealerscore"]),
            id=data["@id"],
            time=int(data["@time"]),
            can_double=data["@candouble"] == "true",
            pre_auto_stand=data["@preautostand"] == "true",
            user_id=data["@userid"],
            hand=int(data["@hand"]),
        )


@dataclass
class PreDecisionInc(Event):
    """
    Event before start of initial player's turn validating split/double for each player

    XML Example: <pre_decisioninc seat="0" score="8/18" game="4694789204" cansplit="false" candouble="true" hand="0" seq="152"></pre_decisioninc>
    """

    seat: int
    score: str
    game: int
    can_split: bool
    can_double: bool
    hand: int

    @classmethod
    def from_raw(cls, data: str) -> "PreDecisionInc":
        data = cls._xml_to_json(data)

        return cls(
            seat=int(data["@seat"]),
            score=data["@score"],
            game=int(data["@game"]),
            can_split=data["@cansplit"] == "true",
            can_double=data["@candouble"] == "true",
            hand=int(data["@hand"]),
        )


@dataclass
class Decision(Event):
    """
    Event directed at current player's turn

    XML Example: <decision seat="1" game="4695108804" code="107" action="playerCall" hand="0" seq="3417">Decision: Double down</decision>
    """

    seat: int
    game: int
    code: int
    action: str
    hand: int
    decision: str

    @classmethod
    def from_raw(cls, data: str) -> "Decision":
        data = cls._xml_to_json(data)

        return cls(
            seat=int(data["@seat"]),
            game=int(data["@game"]),
            code=int(data["@code"]),
            action=data["@action"],
            hand=int(data["@hand"]),
            decision=data["#text"],
        )


@dataclass
class VoipCC(Event):
    """
    Dealer red card from shoe

    XML Example: <voip_cc table="bj361mstakebj361" seq="3970"></voip_cc>
    """

    table: str

    @classmethod
    def from_raw(cls, data: str) -> "VoipCC":
        data = cls._xml_to_json(data)

        return cls(
            table=data["@table"],
        )


@dataclass
class Dealer(Event):
    """
    Event called after dealer scans ID card

    XML Example: <dealer id="8buotd89xl95ll40" seq="4746">Atley</dealer>
    """

    id: str
    name: str

    @classmethod
    def from_raw(cls, data: str) -> "Dealer":
        data = cls._xml_to_json(data)

        return cls(
            id=data["@id"],
            name=data["#text"],
        )


@dataclass
class Game(Event):
    """
    Game event

    XML Example: <game id="4695270804" dealNow="false" seq="4918">07:13:13</game>
    """

    id: int
    deal_now: bool

    @classmethod
    def from_raw(cls, data: str) -> "Game":
        data = cls._xml_to_json(data)

        return cls(
            id=int(data["@id"]),
            deal_now=data["@dealNow"] == "true",
        )


@dataclass
class StartGame(Event):
    """
    Event to start new game

    XML Example: <startGame seat="2" tableId="bj361mstakebj361" dealNow="false" userId="ppc1715133812263" seq="4917"></startGame>
    """

    seat: int
    table_id: str
    deal_now: bool
    user_id: str

    @classmethod
    def from_raw(cls, data: str) -> "StartGame":
        data = cls._xml_to_json(data)

        return cls(
            seat=int(data["@seat"]),
            table_id=data["@tableId"],
            deal_now=data["@dealNow"] == "true",
            user_id=data["@userId"],
        )


@dataclass
class BetsOpen(Event):
    """
    Event opens bets for 12 seconds

    XML Example: <betsopen game="4695270804" table="bj361mstakebj361" seq="4920"></betsopen>
    """

    game: int
    table: str

    @classmethod
    def from_raw(cls, data: str) -> "BetsOpen":
        data = cls._xml_to_json(data)

        return cls(
            game=int(data["@game"]),
            table=data["@table"],
        )


@dataclass
class BetsClosingSoon(Event):
    """
    Event runs approximately 6 seconds after BetsOpen event

    XML Example: <betsclosingsoon game="4695270804" table="bj361mstakebj361" seq="4922"></betsclosingsoon>
    """

    game: int
    table: str

    @classmethod
    def from_raw(cls, data: str) -> "BetsClosingSoon":
        data = cls._xml_to_json(data)

        return cls(
            game=int(data["@game"]),
            table=data["@table"],
        )


@dataclass
class BetsClosed(Event):
    """
    Timer to bet ended; no longer accepting bets

    XML Example: <betsclosed game="4695270804" table="bj361mstakebj361" seq="4923"></betsclosed>
    """

    game: int
    table: str

    @classmethod
    def from_raw(cls, data: str) -> "BetsClosed":
        data = cls._xml_to_json(data)

        return cls(
            game=int(data["@game"]),
            table=data["@table"],
        )


@dataclass
class PreBet(Event):
    """
    Initial bet placed by player

    XML Example: <preBet seat="2" hand="0" seq="6207"></preBet>
    """
    seat: int
    hand: int

    @classmethod
    def from_raw(cls, data: str) -> "PreBet":
        data = cls._xml_to_json(data)

        return cls(
            seat=int(data["@seat"]),
            hand=int(data["@hand"]),
        )


@dataclass
class Score(Event):
    """
    Score event

    XML Example: <score seat="2" game="4695368704" hand="0" seq="6208">10</score>
    """
    seat: int
    game: int
    hand: int
    score: int

    @classmethod
    def from_raw(cls, data: str) -> "Score":
        data = cls._xml_to_json(data)

        return cls(
            seat=int(data["@seat"]),
            game=int(data["@game"]),
            hand=int(data["@hand"]),
            score=int(data["#text"]),
        )


@dataclass
class Bet(Event):
    """
    Bet event -- Includes amount of bet placed by player

    XML Example: <bet gameId="4695368704" userId="ppc1716788013363" seat="2" hand="0" seq="6209">10</bet>
    """
    game_id: int
    user_id: str
    seat: int
    hand: int
    bet: int

    @classmethod
    def from_raw(cls, data: str) -> "Bet":
        data = cls._xml_to_json(data)

        return cls(
            game_id=int(data["@gameId"]),
            user_id=data["@userId"],
            seat=int(data["@seat"]),
            hand=int(data["@hand"]),
            bet=int(data["#text"]),
        )


@dataclass
class Bj21Plus3(Event):
    """
    Event plays for 21+3 side bet -- Outcome either Win or Lose

    XML Example: <bj21plus3 seat="5" result="4" game="4695368704" hand="2" seq="6212">Lose</bj21plus3>
    """
    seat: int
    result: int
    game: int
    hand: int

    @classmethod
    def from_raw(cls, data: str) -> "Bj21Plus3":
        data = cls._xml_to_json(data)

        return cls(
            seat=int(data["@seat"]),
            result=int(data["@result"]),
            game=int(data["@game"]),
            hand=int(data["@hand"]),
        )


@dataclass
class PerfectPairs(Event):
    """
    Event plays for perfect pair side bet -- Outcome either Win or Lose

    XML Example: <perfectpairs seat="5" result="4" game="4695368704" hand="3" seq="6213">Lose</perfectpairs>
    """
    seat: int
    result: int
    game: int
    hand: int

    @classmethod
    def from_raw(cls, data: str) -> "PerfectPairs":
        data = cls._xml_to_json(data)

        return cls(
            seat=int(data["@seat"]),
            result=int(data["@result"]),
            game=int(data["@game"]),
            hand=int(data["@hand"]),
        )


@dataclass
class BetResult(Event):
    """
    Event signifies round outcome for player -- Results can be: Win, Lose, Push, Blackjack, Bust

    XML Example: <betresult seat="2" game="4695368704" seq="6266"><handresult result="3" hand="0" >Win</handresult></betresult>
    """
    seat: int
    game: int
    hand_result: str

    @classmethod
    def from_raw(cls, data: str) -> "BetResult":
        data = cls._xml_to_json(data)

        return cls(
            seat=int(data["@seat"]),
            game=int(data["@game"]),
            hand_result=data["handresult"]["#text"],
        )


@dataclass
class HandResult(Event):
    """
    result integer corresponds with outcome: 2=Blackjack, 3=Win, 4=Lose, 5=Push, 6=Bust

    XML Example: <handresult seat="3" result="2" game="4695368704" hand="0" seq="6269">Blackjack</handresult>
    """
    seat: int
    result: int
    game: int
    hand: int

    @classmethod
    def from_raw(cls, data: str) -> "HandResult":
        data = cls._xml_to_json(data)

        return cls(
            seat=int(data["@seat"]),
            result=int(data["@result"]),
            game=int(data["@game"]),
            hand=int(data["@hand"]),
        )


@dataclass
class Wins(Event):
    """
    Amount of wins each player has accumulated for each round they win in a row (appears as a medal next to username)

    XML Example: <wins gameId="4695368704" seat6="0" seat5="0" seat0="0" tableId="bj361mstakebj361" seat4="0" seat3="1" seat2="1" seat1="0" seq="6277"></wins>
    """
    game_id: int
    table_id: str
    seats: list[int]

    @classmethod
    def from_raw(cls, data: str) -> "Wins":
        data = cls._xml_to_json(data)

        return cls(
            game_id=int(data["@gameId"]),
            table_id=data["@tableId"],
            seats=[int(data[f"seat{i}"]) for i in range(7)],
        )


@dataclass
class BjGameEnd(Event):
    """
    Event signifies end of current round

    XML Example: <bjGameEnd id="4695368704" seq="6276"></bjGameEnd>
    """
    id: int

    @classmethod
    def from_raw(cls, data: str) -> "BjGameEnd":
        data = cls._xml_to_json(data)

        return cls(
            id=int(data["@id"]),
        )


@dataclass
class StartGameError(Event):
    """
    StartGameError event

    #XML Example: <startGameError code="bj361mstakebj361" seatNum="6" desc="ppc1706782600787" seq="6284"></startGameError>
    """
    code: str
    seat_num: int
    desc: str

    @classmethod
    def from_raw(cls, data: str) -> "StartGameError":
        data = cls._xml_to_json(data)

        return cls(
            code=data["@code"],
            seat_num=int(data["@seatNum"]),
            desc=data["@desc"],
        )


@dataclass
class StartDealing(Event):
    """
    Dealer will start dealing cards to table

    XML Example: <startDealing game="4695377904" table="bj361mstakebj361" seq="6291"></startDealing>
    """
    game: int
    table: str

    @classmethod
    def from_raw(cls, data: str) -> "StartDealing":
        data = cls._xml_to_json(data)

        return cls(
            game=int(data["@game"]),
            table=data["@table"],
        )


@dataclass
class Timer(Event):
    """
    Timer event

    XML Example: <timer dns="false" id="4695383504" seq="6357">12</timer>
    """
    dns: bool
    id: int
    time: int

    @classmethod
    def from_raw(cls, data: str) -> "Timer":
        data = cls._xml_to_json(data)

        return cls(
            dns=data["@dns"] == "true",
            id=int(data["@id"]),
            time=int(data["#text"]),
        )


@dataclass
class NotInsured(Event):
    """
    Checks if player is insured

    XML Example: <notinsured seat="1" auto="false" hand="0" seq="3724"></notinsured>
    """
    seat: int
    auto: bool
    hand: int

    @classmethod
    def from_raw(cls, data: str) -> "NotInsured":
        data = cls._xml_to_json(data)

        return cls(
            seat=int(data["@seat"]),
            auto=data["@auto"] == "true",
            hand=int(data["@hand"]),
        )


@dataclass
class MainBetCount(Event):
    """
    MainBetCount event

    XML Example: <mainBetCount gameId="4695432804" mainBetCount="6" seq="6891"></mainBetCount>
    """
    game_id: int
    main_bet_count: int

    @classmethod
    def from_raw(cls, data: str) -> "MainBetCount":
        data = cls._xml_to_json(data)

        return cls(
            game_id=int(data["@gameId"]),
            main_bet_count=int(data["@mainBetCount"]),
        )


@dataclass
class CardInc(Event):
    """
    CardInc event

    XML Example: <cardinc seat="1" game="4695418404" initial="true" splitinitial="false" hand="0" seq="6831"></cardinc>
    """
    seat: int
    game: int
    initial: bool
    split_initial: bool
    hand: int

    @classmethod
    def from_raw(cls, data: str) -> "CardInc":
        data = cls._xml_to_json(data)

        return cls(
            seat=int(data["@seat"]),
            game=int(data["@game"]),
            initial=data["@initial"] == "true",
            split_initial=data["@splitinitial"] == "true",
            hand=int(data["@hand"]),
        )


@dataclass
class CurrentShoe(Event):
    """
    Event signifies shoe change after current round ends

    XML Example: <currentShoe cc="0" code="blue" changeShoe="true" seq="7199"></currentShoe>
    """
    cc: int
    code: str
    change_shoe: bool

    @classmethod
    def from_raw(cls, data: str) -> "CurrentShoe":
        data = cls._xml_to_json(data)

        return cls(
            cc=int(data["@cc"]),
            code=data["@code"],
            change_shoe=data["@changeShoe"] == "true",
        )


@dataclass
class InsuredBb(Event):
    """
    InsuredBb event

    XML Example: <insured_bb seat="6" hand="" seq="7709"></insured_bb>
    """
    seat: int
    hand: str

    @classmethod
    def from_raw(cls, data: str) -> "InsuredBb":
        data = cls._xml_to_json(data)

        return cls(
            seat=int(data["@seat"]),
            hand=data["@hand"],
        )


@dataclass
class Insured(Event):
    """
    Event for insurance

    XML Example: <insured seat="6" auto="false" betbehind="false" hand="0" seq="7710"></insured>
    """
    seat: int
    auto: bool
    bet_behind: bool
    hand: int

    @classmethod
    def from_raw(cls, data: str) -> "Insured":
        data = cls._xml_to_json(data)

        return cls(
            seat=int(data["@seat"]),
            auto=data["@auto"] == "true",
            bet_behind=data["@betbehind"] == "true",
            hand=int(data["@hand"]),
        )


@dataclass
class OfferOver(Event):
    """
    Event signifies insurance offer ends

    XML Example: <offerOver id="4695524404" seq="7716"></offerOver>
    """
    id: int

    @classmethod
    def from_raw(cls, data: str) -> "OfferOver":
        data = cls._xml_to_json(data)

        return cls(
            id=int(data["@id"]),
        )


@dataclass
class Subscribe(Event):
    """
    Subscribe event

    XML Example: <subscribe channel="table-bj361mstakebj361" table="bj361mstakebj361" status="success" seq="49"></subscribe>
    """
    channel: str
    table: str
    status: str

    @classmethod
    def from_raw(cls, data: str) -> "Subscribe":
        data = cls._xml_to_json(data)

        return cls(
            channel=data["@channel"],
            table=data["@table"],
            status=data["@status"],
        )


_mapping = {
    "seat": Seat,
    "pong": Pong,
    "card": Card,
    "predecision": PreDecision,
    "decisioninc": DecisionInc,
    "predecisioninc": PreDecisionInc,
    "decision": Decision,
    "voip_cc": VoipCC,
    "dealer": Dealer,
    "game": Game,
    "startgame": StartGame,
    "betsopen": BetsOpen,
    "betsclosingsoon": BetsClosingSoon,
    "betsclosed": BetsClosed,
    "prebet": PreBet,
    "score": Score,
    "bet": Bet,
    "bj21plus3": Bj21Plus3,
    "perfectpairs": PerfectPairs,
    "betresult": BetResult,
    "handresult": HandResult,
    "wins": Wins,
    "bjgameend": BjGameEnd,
    "startgameerror": StartGameError,
    "startdealing": StartDealing,
    "timer": Timer,
    "notinsured": NotInsured,
    "mainbetcount": MainBetCount,
    "cardinc": CardInc,
    "currentshoe": CurrentShoe,
    "insuredbb": InsuredBb,
    "insured": Insured,
    "offerover": OfferOver,
}


def _get_event(message: str) -> Event:
    if event_name := re.findall(r"<(.*?) ", message):
        event_type = event_name[0]
    else:
        raise ValueError("Invalid message: No event type found.", message)

    if event_type not in _mapping:
        raise NotImplementedError(f"Event type {event_type} is not implemented.")

    event = _mapping[event_type]
    return event.from_raw(message)
