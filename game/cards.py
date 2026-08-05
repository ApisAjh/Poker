"""Card and Deck representation for Texas Hold'em."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List


SUITS = ("♠", "♥", "♦", "♣")
RANKS = ("2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A")
RANK_VALUES = {r: i for i, r in enumerate(RANKS, start=2)}


@dataclass(frozen=True, order=True)
class Card:
    rank: str
    suit: str

    def __post_init__(self) -> None:
        if self.rank not in RANK_VALUES:
            raise ValueError(f"Invalid rank: {self.rank}")
        if self.suit not in SUITS:
            raise ValueError(f"Invalid suit: {self.suit}")

    @property
    def value(self) -> int:
        return RANK_VALUES[self.rank]

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    def display(self) -> str:
        """Pretty display with rank + suit symbol."""
        return f"{self.rank}{self.suit}"


class Deck:
    """Standard 52-card deck."""

    def __init__(self) -> None:
        self.cards: List[Card] = [
            Card(rank, suit) for suit in SUITS for rank in RANKS
        ]
        self.shuffle()

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def deal(self, n: int = 1) -> List[Card]:
        if n > len(self.cards):
            raise ValueError("Not enough cards left in deck")
        dealt = self.cards[:n]
        self.cards = self.cards[n:]
        return dealt

    def deal_one(self) -> Card:
        return self.deal(1)[0]

    def remaining(self) -> int:
        return len(self.cards)
