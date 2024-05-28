from .event import *


class HandlerBase:
    __mapping__ = {
        Subscribe: "handle_subscribe",
        Seat: "handle_seat",
        Game: "handle_game",
        TableEvent: "handle_table_event",
        Card: "handle_card",
        PreDecision: "handle_pre_decision",
        DecisionInc: "handle_decision_inc",
        Decision: "handle_decision",
        Pong: "handle_pong",
        PreDecisionInc: "handle_pre_decision_inc",
        VoipCC: "handle_voip_cc",
        Dealer: "handle_dealer",
        StartGame: "handle_start_game",
        BetsOpen: "handle_bets_open",
        BetsClosingSoon: "handle_bets_closing_soon",
        BetsClosed: "handle_bets_closed",
        PreBet: "handle_pre_bet",
        Score: "handle_score",
        Bet: "handle_bet",
        Bj21Plus3: "handle_bj_21plus3",
        PerfectPairs: "handle_perfect_pairs",
        BetResult: "handle_bet_result",
        HandResult: "handle_hand_result",
        Wins: "handle_wins",
        BjGameEnd: "handle_bj_game_end",
        StartGameError: "handle_start_game_error",
        StartDealing: "handle_start_dealing",
        Timer: "handle_timer",
        NotInsured: "handle_not_insured",
        MainBetCount: "handle_main_bet_count",
        CardInc: "handle_card_inc",
        CurrentShoe: "handle_current_shoe",
        InsuredBb: "handle_insured_bb",
        Insured: "handle_insured",
        OfferOver: "handle_offer_over",
        DuplicatedConnection: "handle_duplicated_connection",
        CloseConnection: "handle_close_connection",
        Logout: "handle_logout",
        BetStats: "handle_bet_stats",
        Command: "handle_command",
    }

    def __init__(self, *args, **kwargs):
        pass

    def handle_subscribe(self, event: Subscribe, raw: str = None): ...
    def handle_seat(self, event: Seat, raw: str = None): ...
    def handle_game(self, event: Game, raw: str = None): ...
    def handle_table_event(self, event: TableEvent, raw: str = None): ...
    def handle_card(self, event: Card, raw: str = None): ...
    def handle_pre_decision(self, event: PreDecision, raw: str = None): ...
    def handle_decision_inc(self, event: DecisionInc, raw: str = None): ...
    def handle_decision(self, event: Decision, raw: str = None): ...
    def handle_pong(self, event: Pong, raw: str = None): ...
    def handle_pre_decision_inc(self, event: PreDecisionInc, raw: str = None): ...
    def handle_voip_cc(self, event: VoipCC, raw: str = None): ...
    def handle_dealer(self, event: Dealer, raw: str = None): ...
    def handle_start_game(self, event: StartGame, raw: str = None): ...
    def handle_bets_open(self, event: BetsOpen, raw: str = None): ...
    def handle_bets_closing_soon(self, event: BetsClosingSoon, raw: str = None): ...
    def handle_bets_closed(self, event: BetsClosed, raw: str = None): ...
    def handle_pre_bet(self, event: PreBet, raw: str = None): ...
    def handle_score(self, event: Score, raw: str = None): ...
    def handle_bet(self, event: Bet, raw: str = None): ...
    def handle_bj_21plus3(self, event: Bj21Plus3, raw: str = None): ...
    def handle_perfect_pairs(self, event: PerfectPairs, raw: str = None): ...
    def handle_bet_result(self, event: BetResult, raw: str = None): ...
    def handle_hand_result(self, event: HandResult, raw: str = None): ...
    def handle_wins(self, event: Wins, raw: str = None): ...
    def handle_bj_game_end(self, event: BjGameEnd, raw: str = None): ...
    def handle_start_game_error(self, event: StartGameError, raw: str = None): ...
    def handle_start_dealing(self, event: StartDealing, raw: str = None): ...
    def handle_timer(self, event: Timer, raw: str = None): ...
    def handle_not_insured(self, event: NotInsured, raw: str = None): ...
    def handle_main_bet_count(self, event: MainBetCount, raw: str = None): ...
    def handle_card_inc(self, event: CardInc, raw: str = None): ...
    def handle_current_shoe(self, event: CurrentShoe, raw: str = None): ...
    def handle_insured_bb(self, event: InsuredBb, raw: str = None): ...
    def handle_insured(self, event: Insured, raw: str = None): ...
    def handle_offer_over(self, event: OfferOver, raw: str = None): ...
    def handle_duplicated_connection(self, event: DuplicatedConnection, raw: str = None): ...
    def handle_close_connection(self, event: CloseConnection, raw: str = None): ...
    def handle_logout(self, event: Logout, raw: str = None): ...
    def handle_bet_stats(self, event: BetStats, raw: str = None): ...
    def handle_command(self, event: Command, raw: str = None): ...



