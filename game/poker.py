"""Core Texas Hold'em game logic – fully in-memory."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Set

from .cards import Card, Deck
from .evaluator import HandRank, HandScore, compare_hands, evaluate_hand


class GameState(Enum):
    WAITING = auto()
    PREFLOP = auto()
    FLOP = auto()
    TURN = auto()
    RIVER = auto()
    SHOWDOWN = auto()
    FINISHED = auto()


class PlayerAction(Enum):
    CHECK = "check"
    CALL = "call"
    RAISE = "raise"
    FOLD = "fold"


@dataclass
class Player:
    user_id: int
    name: str
    hole_cards: List[Card] = field(default_factory=list)
    folded: bool = False
    is_all_in: bool = False  # kept for future extension, not used with chips
    last_action: Optional[PlayerAction] = None

    @property
    def is_active(self) -> bool:
        return not self.folded


@dataclass
class PokerGame:
    """
    One active game per Telegram group chat.
    No chips / betting amounts – simplified action-only Hold'em
    (Check / Call / Raise / Fold) suitable for casual group play.
    """

    chat_id: int
    host_id: int
    host_name: str
    players: Dict[int, Player] = field(default_factory=dict)
    state: GameState = GameState.WAITING
    deck: Optional[Deck] = None
    community: List[Card] = field(default_factory=list)
    current_turn_index: int = 0
    dealer_index: int = 0
    acted_this_street: Set[int] = field(default_factory=set)
    raised_this_street: bool = False
    turn_deadline: float = 0.0  # unix timestamp
    message_id: Optional[int] = None  # main status message to edit
    turn_seconds: int = 20
    min_players: int = 2
    max_players: int = 6

    def __post_init__(self) -> None:
        if self.host_id not in self.players:
            self.players[self.host_id] = Player(
                user_id=self.host_id, name=self.host_name
            )

    # ------------------------------------------------------------------
    # Lobby helpers
    # ------------------------------------------------------------------

    @property
    def player_list(self) -> List[Player]:
        return list(self.players.values())

    @property
    def active_players(self) -> List[Player]:
        return [p for p in self.player_list if p.is_active]

    @property
    def player_count(self) -> int:
        return len(self.players)

    def add_player(self, user_id: int, name: str) -> str:
        if self.state != GameState.WAITING:
            return "Game already started."
        if user_id in self.players:
            return "You already joined."
        if self.player_count >= self.max_players:
            return f"Room full (max {self.max_players})."
        self.players[user_id] = Player(user_id=user_id, name=name)
        return "ok"

    def remove_player(self, user_id: int) -> str:
        if self.state != GameState.WAITING:
            return "Cannot leave after game started."
        if user_id not in self.players:
            return "You are not in this room."
        del self.players[user_id]
        if user_id == self.host_id:
            return "host_left"
        return "ok"

    def can_start(self) -> bool:
        return (
            self.state == GameState.WAITING
            and self.min_players <= self.player_count <= self.max_players
        )

    # ------------------------------------------------------------------
    # Game flow
    # ------------------------------------------------------------------

    def start(self) -> None:
        if not self.can_start():
            raise RuntimeError("Cannot start game")
        self.deck = Deck()
        self.community = []
        self.state = GameState.PREFLOP
        self.dealer_index = 0
        self.current_turn_index = 0
        self._deal_hole_cards()
        self._reset_street()
        self._set_turn_deadline()

    def _deal_hole_cards(self) -> None:
        assert self.deck is not None
        for p in self.player_list:
            p.hole_cards = self.deck.deal(2)
            p.folded = False
            p.last_action = None

    def _reset_street(self) -> None:
        self.acted_this_street = set()
        self.raised_this_street = False
        for p in self.player_list:
            p.last_action = None

    def _set_turn_deadline(self) -> None:
        self.turn_deadline = time.time() + self.turn_seconds

    def _ordered_ids(self) -> List[int]:
        """Stable seat order (insertion order of dict)."""
        return list(self.players.keys())

    def current_player(self) -> Optional[Player]:
        if self.state in (GameState.SHOWDOWN, GameState.FINISHED):
            return None
        ids = self._ordered_ids()
        if not ids:
            return None
        n = len(ids)
        for _ in range(n):
            uid = ids[self.current_turn_index % n]
            p = self.players[uid]
            if p.is_active:
                return p
            self.current_turn_index = (self.current_turn_index + 1) % n
        return None

    def is_player_turn(self, user_id: int) -> bool:
        cur = self.current_player()
        return cur is not None and cur.user_id == user_id

    def apply_action(self, user_id: int, action: PlayerAction) -> str:
        """Apply player action. Returns status message or 'ok'."""
        if self.state in (GameState.WAITING, GameState.SHOWDOWN, GameState.FINISHED):
            return "Game is not in progress."
        if not self.is_player_turn(user_id):
            return "not_your_turn"
        player = self.players[user_id]
        if player.folded:
            return "You already folded."

        if action == PlayerAction.FOLD:
            player.folded = True
            player.last_action = PlayerAction.FOLD
        elif action == PlayerAction.CHECK:
            if self.raised_this_street:
                return "Cannot check – there is a raise. Call or fold."
            player.last_action = PlayerAction.CHECK
        elif action == PlayerAction.CALL:
            player.last_action = PlayerAction.CALL
        elif action == PlayerAction.RAISE:
            self.raised_this_street = True
            player.last_action = PlayerAction.RAISE
            # After a raise everyone else must respond again
            self.acted_this_street = {user_id}
        else:
            return "Unknown action."

        self.acted_this_street.add(user_id)
        self._advance_turn()
        return "ok"

    def auto_action_on_timeout(self) -> Optional[PlayerAction]:
        """Called when turn timer expires. Returns the action taken."""
        cur = self.current_player()
        if cur is None:
            return None
        if self.raised_this_street:
            action = PlayerAction.FOLD
        else:
            action = PlayerAction.CHECK
        self.apply_action(cur.user_id, action)
        return action

    def _advance_turn(self) -> None:
        active = self.active_players
        if len(active) <= 1:
            self._go_to_showdown()
            return

        # Street complete when every still-active player has acted
        active_ids = {p.user_id for p in active}
        if active_ids <= self.acted_this_street:
            self._next_street()
            return

        # Move pointer to next seat; current_player() skips folded
        ids = self._ordered_ids()
        self.current_turn_index = (self.current_turn_index + 1) % len(ids)
        self._set_turn_deadline()

    def _next_street(self) -> None:
        assert self.deck is not None
        if self.state == GameState.PREFLOP:
            self.community.extend(self.deck.deal(3))
            self.state = GameState.FLOP
        elif self.state == GameState.FLOP:
            self.community.append(self.deck.deal_one())
            self.state = GameState.TURN
        elif self.state == GameState.TURN:
            self.community.append(self.deck.deal_one())
            self.state = GameState.RIVER
        elif self.state == GameState.RIVER:
            self._go_to_showdown()
            return
        self._reset_street()
        # First active player after dealer
        self.current_turn_index = 0
        # Ensure pointer lands on an active player
        _ = self.current_player()
        self._set_turn_deadline()

    def _go_to_showdown(self) -> None:
        self.state = GameState.SHOWDOWN

    def get_winners(self) -> List[Player]:
        active = self.active_players
        if len(active) == 1:
            return active
        hands = [(p.user_id, p.hole_cards) for p in active]
        winner_ids = compare_hands(hands, self.community)
        return [self.players[uid] for uid in winner_ids]

    def get_hand_score(self, player: Player) -> HandScore:
        return evaluate_hand(player.hole_cards, self.community)

    def finish(self) -> None:
        self.state = GameState.FINISHED

    # ------------------------------------------------------------------
    # Rendering helpers (pure data – no Telegram objects)
    # ------------------------------------------------------------------

    def render_room(self) -> str:
        lines = ["🎮 <b>Poker Room</b>", ""]
        if self.state == GameState.WAITING:
            lines.append(f"<b>Host</b>\n👤 {self.host_name}")
            lines.append("")
            lines.append("<b>Players</b>")
            for p in self.player_list:
                lines.append(f"👤 {p.name}")
            lines.append("")
            if self.player_count < self.min_players:
                lines.append(
                    f"<b>Status</b>\nWaiting Player... "
                    f"({self.player_count}/{self.min_players})"
                )
            else:
                lines.append(
                    f"<b>Status</b>\nWaiting Host to start "
                    f"({self.player_count}/{self.max_players})"
                )
        return "\n".join(lines)

    def render_game(self) -> str:
        lines = ["🃏 <b>Texas Hold'em</b>", ""]
        lines.append("<b>Players</b>")
        for p in self.player_list:
            cards = "🂠🂠" if not p.folded else "❌ Folded"
            marker = " ⬅️" if self.is_player_turn(p.user_id) else ""
            lines.append(f"👤 {p.name}   {cards}{marker}")
        lines.append("")
        lines.append("<b>Community Cards</b>")
        if not self.community:
            lines.append("🂠 🂠 🂠 🂠 🂠")
        else:
            shown = " ".join(c.display() for c in self.community)
            hidden = " 🂠" * (5 - len(self.community))
            lines.append(shown + hidden)
        lines.append("")
        cur = self.current_player()
        if cur and self.state not in (GameState.SHOWDOWN, GameState.FINISHED):
            remaining = max(0, int(self.turn_deadline - time.time()))
            lines.append(f"<b>Current Turn</b>\n👤 {cur.name} ({remaining}s)")
        lines.append("")
        lines.append(f"<b>Street</b>: {self.state.name.title()}")
        return "\n".join(lines)

    def render_showdown(self) -> str:
        lines = ["🏁 <b>SHOWDOWN</b>", ""]
        for p in self.player_list:
            if p.folded:
                lines.append(f"👤 {p.name}\n❌ Folded")
            else:
                cards = " ".join(c.display() for c in p.hole_cards)
                score = self.get_hand_score(p)
                lines.append(
                    f"👤 {p.name}\n{cards}\n→ {score.rank.label}"
                )
            lines.append("")
        lines.append("<b>Community</b>")
        lines.append(" ".join(c.display() for c in self.community))
        lines.append("")

        winners = self.get_winners()
        if len(winners) == 1:
            w = winners[0]
            score = self.get_hand_score(w)
            lines.append("🏆 <b>Winner</b>")
            lines.append(f"👤 {w.name}")
            lines.append(f"<b>Combination</b>\n{score.rank.label}")
            lines.append("")
            lines.append("🎉 Congratulations!")
        else:
            lines.append("🤝 <b>Split Pot</b>")
            for w in winners:
                score = self.get_hand_score(w)
                lines.append(f"👤 {w.name} – {score.rank.label}")
            lines.append("")
            lines.append("🎉 Congratulations!")
        return "\n".join(lines)
