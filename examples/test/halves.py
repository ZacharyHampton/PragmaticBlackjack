class GameState:
    """
    Tracks the state of a blackjack game.
    """
    def __init__(self, decks: int, bank_roll: float, risk=1):
        """
        Initializes the game state.

        :param decks: The number of decks currently in the shoe.
        :param bank_roll: Total amount of money that you are willing to bet.
        :param risk: An integer, by default 1 with a max of 3, that will determine how large your bet unit is
        (1%, 2%, 3%)
        """
        if risk <= 1:
            self.risk = 1
        elif 1 < risk <= 2:
            self.risk = 2
        else:
            self.risk = 3
        self.bank_roll = bank_roll
        self.bet_unit = bank_roll * risk/100
        self.decks = decks
        self.running_count = 0
        self.true_count = 0
        self.cards = {"A": -1, "K": -1, "Q": -1, "J": -1, "10": -1, "9": -0.5,
                      "8": 0, "7": 0.5, "6": 1, "5": 1.5, "4": 1, "3": 1, "2": 0.5}

        # Keeps track of the number of cards taken out of the shoe so the deck estimate can be updated as
        # cards are counted
        self.card_count = 0
        self.shoe_size = 7

    def get_bet(self) -> float:
        if self.true_count <= 0:
            return 0.00
        elif self.true_count > 6:
            return self.bet_unit * 6.00
        else:
            return round((self.bet_unit * self.true_count), 2)

    def add_card(self, card: str):
        """
        Adds and then subsequently counts a card into the game state.

        :param card: A card (A, K, 1, 2, 3, ect...) as a string
        """
        self.running_count += self.cards[card]
        self.card_count += 1
        if self.card_count == 52:
            self.decks -= 1
            self.card_count = 0
            if self.decks == 0:
                self.decks = 1

        self.true_count = self.running_count / (self.decks - self.card_count / 52)

    def shuffle(self):
        """
        Resets the game state after a shuffle.
        """
        self.running_count = 0
        self.true_count = 0
        self.decks = self.shoe_size
        self.card_count = 0
