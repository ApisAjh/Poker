"""Pure-Python Texas Hold'em hand evaluator (best 5 of 7 cards)."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from enum import IntEnum
from itertools import combinations
from typing import List, Sequence, Tuple

from .cards import Card, RANK_VALUES


class HandRank(IntEnum):
    HIGH_CARD = 0
    PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8
    ROYAL_FLUSH = 9

    @property
    def label(self) -> str:
        return {
            HandRank.HIGH_CARD: "High Card",
            HandRank.PAIR: "Pair",
            HandRank.TWO_PAIR: "Two Pair",
            HandRank.THREE_OF_A_KIND: "Three of a Kind",
            HandRank.STRAIGHT: "Straight",
            HandRank.FLUSH: "Flush",
            HandRank.FULL_HOUSE: "Full House",
            HandRank.FOUR_OF_A_KIND: "Four of a Kind",
            HandRank.STRAIGHT_FLUSH: "Straight Flush",
            HandRank.ROYAL_FLUSH: "Royal Flush",
        }[self]


@dataclass(frozen=True, order=True)
class HandScore:
    """Comparable hand score. Higher is better."""

    rank: HandRank
    tiebreakers: Tuple[int, ...]  # descending strength values

    def __str__(self) -> str:
        return f"{self.rank.label} {self.tiebreakers}"


def _is_straight(values: Sequence[int]) -> bool:
    """Check if sorted unique values form a straight (handles wheel A-2-3-4-5)."""
    vals = sorted(set(values), reverse=True)
    if len(vals) < 5:
        return False
    # normal straight
    for i in range(len(vals) - 4):
        window = vals[i : i + 5]
        if window[0] - window[4] == 4:
            return True
    # wheel: A,5,4,3,2
    if set(vals) >= {14, 5, 4, 3, 2}:
        return True
    return False


def _straight_high(values: Sequence[int]) -> int:
    """Return the highest card of the straight (5 for wheel)."""
    vals = sorted(set(values), reverse=True)
    for i in range(len(vals) - 4):
        window = vals[i : i + 5]
        if window[0] - window[4] == 4:
            return window[0]
    if set(vals) >= {14, 5, 4, 3, 2}:
        return 5
    return 0


def _evaluate_five(cards: Sequence[Card]) -> HandScore:
    """Evaluate exactly 5 cards."""
    values = sorted((c.value for c in cards), reverse=True)
    suits = [c.suit for c in cards]
    counts = Counter(values)
    is_flush = len(set(suits)) == 1
    is_straight = _is_straight(values)

    # multiplicities sorted by (count desc, value desc)
    mult = sorted(counts.items(), key=lambda x: (x[1], x[0]), reverse=True)
    ranks_by_count = [v for v, _ in mult]

    if is_straight and is_flush:
        high = _straight_high(values)
        if high == 14:
            return HandScore(HandRank.ROYAL_FLUSH, (14,))
        return HandScore(HandRank.STRAIGHT_FLUSH, (high,))

    if mult[0][1] == 4:
        four = mult[0][0]
        kicker = max(v for v in values if v != four)
        return HandScore(HandRank.FOUR_OF_A_KIND, (four, kicker))

    if mult[0][1] == 3 and mult[1][1] == 2:
        return HandScore(HandRank.FULL_HOUSE, (mult[0][0], mult[1][0]))

    if is_flush:
        return HandScore(HandRank.FLUSH, tuple(values))

    if is_straight:
        return HandScore(HandRank.STRAIGHT, (_straight_high(values),))

    if mult[0][1] == 3:
        three = mult[0][0]
        kickers = sorted((v for v in values if v != three), reverse=True)
        return HandScore(HandRank.THREE_OF_A_KIND, (three, *kickers))

    if mult[0][1] == 2 and mult[1][1] == 2:
        high_pair, low_pair = sorted(
            (mult[0][0], mult[1][0]), reverse=True
        )
        kicker = max(v for v in values if v not in (high_pair, low_pair))
        return HandScore(HandRank.TWO_PAIR, (high_pair, low_pair, kicker))

    if mult[0][1] == 2:
        pair = mult[0][0]
        kickers = sorted((v for v in values if v != pair), reverse=True)
        return HandScore(HandRank.PAIR, (pair, *kickers))

    return HandScore(HandRank.HIGH_CARD, tuple(values))


def evaluate_hand(hole: Sequence[Card], board: Sequence[Card]) -> HandScore:
    """
    Evaluate best 5-card hand from hole (2) + board (0-5).
    Returns HandScore comparable with > / < / ==.
    """
    all_cards = list(hole) + list(board)
    if len(all_cards) < 5:
        # Pre-flop / incomplete – rank by high cards only (for completeness)
        values = sorted((c.value for c in all_cards), reverse=True)
        return HandScore(HandRank.HIGH_CARD, tuple(values))

    best: HandScore | None = None
    for combo in combinations(all_cards, 5):
        score = _evaluate_five(combo)
        if best is None or score > best:
            best = score
    assert best is not None
    return best


def compare_hands(
    hands: List[Tuple[int, Sequence[Card]]], board: Sequence[Card]
) -> List[int]:
    """
    hands: list of (player_id, hole_cards)
    Returns list of winner player_ids (can be multiple on true tie).
    """
    scored = [
        (pid, evaluate_hand(hole, board)) for pid, hole in hands
    ]
    best_score = max(s for _, s in scored)
    return [pid for pid, s in scored if s == best_score]
