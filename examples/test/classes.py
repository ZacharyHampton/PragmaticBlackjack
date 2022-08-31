from dataclasses import dataclass


@dataclass
class Hand:
    currentHandValue: int
    isSoft: bool
    isPair: bool


@dataclass
class Player:
    username: str
    isMe: bool
    bet: float
    currentHand: Hand | None = None


@dataclass
class Table:
    players: dict[int][Player] | None = None
    dealer: Player | None = None
