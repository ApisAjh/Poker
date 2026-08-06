"""Core Texas Hold'em game logic – fully in-memory."""

from __future__ import annotations

import html
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Set

from .cards import Card, Deck
from .evaluator import HandRank, HandScore, compare_hands, evaluate_hand
from .modes import GameMode


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
    username: Optional[str] = None  # Telegram @username (no @)
    hole_cards: List[Card] = field(default_factory=list)
    folded: bool = False
    is_all_in: bool = False  # kept for future extension, not used with chips
    last_action: Optional[PlayerAction] = None

    @property
    def is_active(self) -> bool:
        return not self.folded

    @property
    def mention(self) -> str:
        """Plain display: Name (@username). HTML-escaped for safe ParseMode.HTML."""
        name = html.escape(self.name or "Player")
        if self.username:
            # UNO-style: Name (@username) — no tg:// links (avoids 404 Not found)
            return f"{name} (@{html.escape(self.username)})"
        return name

    @property
    def short_name(self) -> str:
        """Short label for buttons (no HTML)."""
        if self.username:
            return f"@{self.username}"
        return (self.name or "Player")[:20]


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
    lang: str = "en"  # display language for shared room/game messages
    mode: Optional[GameMode] = None  # chosen when room is created
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
    turn_seconds: int = 60
    min_players: int = 2
    max_players: int = 6

    def __post_init__(self) -> None:
        if self.host_id not in self.players:
            self.players[self.host_id] = Player(
                user_id=self.host_id, name=self.host_name
            )  # username set later if provided

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

    def add_player(self, user_id: int, name: str, username: Optional[str] = None) -> str:
        if self.state != GameState.WAITING:
            return "game_started_already"
        if user_id in self.players:
            return "already_joined"
        if self.player_count >= self.max_players:
            return "room_full"
        self.players[user_id] = Player(user_id=user_id, name=name, username=username)
        return "ok"

    def remove_player(self, user_id: int) -> str:
        if self.state != GameState.WAITING:
            return "cannot_leave_started"
        if user_id not in self.players:
            return "not_in_room"
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

    def uses_turn_timer(self) -> bool:
        """Soft turn timer only for Classic mode."""
        return self.mode is None or self.mode.value == "classic"

    def _set_turn_deadline(self) -> None:
        if self.uses_turn_timer():
            self.turn_deadline = time.time() + self.turn_seconds
        else:
            self.turn_deadline = 0.0  # no soft timer (Private)

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
            return "not_in_progress"
        if not self.is_player_turn(user_id):
            return "not_your_turn"
        player = self.players[user_id]
        if player.folded:
            return "already_folded"

        if action == PlayerAction.FOLD:
            player.folded = True
            player.last_action = PlayerAction.FOLD
        elif action == PlayerAction.CHECK:
            if self.raised_this_street:
                return "cannot_check"
            player.last_action = PlayerAction.CHECK
        elif action == PlayerAction.CALL:
            player.last_action = PlayerAction.CALL
        elif action == PlayerAction.RAISE:
            self.raised_this_street = True
            player.last_action = PlayerAction.RAISE
            # After a raise everyone else must respond again
            self.acted_this_street = {user_id}
        else:
            return "unknown_action"

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

    def _street_key(self) -> str:
        return {
            GameState.WAITING: "street_waiting",
            GameState.PREFLOP: "street_preflop",
            GameState.FLOP: "street_flop",
            GameState.TURN: "street_turn",
            GameState.RIVER: "street_river",
            GameState.SHOWDOWN: "street_showdown",
            GameState.FINISHED: "street_finished",
        }.get(self.state, "street_waiting")

    @staticmethod
    def _rank_key(rank: HandRank) -> str:
        return {
            HandRank.HIGH_CARD: "hand_rank_high_card",
            HandRank.PAIR: "hand_rank_pair",
            HandRank.TWO_PAIR: "hand_rank_two_pair",
            HandRank.THREE_OF_A_KIND: "hand_rank_three",
            HandRank.STRAIGHT: "hand_rank_straight",
            HandRank.FLUSH: "hand_rank_flush",
            HandRank.FULL_HOUSE: "hand_rank_full_house",
            HandRank.FOUR_OF_A_KIND: "hand_rank_four",
            HandRank.STRAIGHT_FLUSH: "hand_rank_straight_flush",
            HandRank.ROYAL_FLUSH: "hand_rank_royal",
        }.get(rank, "hand_rank_high_card")

    def render_room(self, lang: str = "en") -> str:
        from locales import t

        lines = [t(lang, "room_title"), ""]
        if self.state == GameState.WAITING:
            lines.append(t(lang, "room_host", host=self.host_name))
            lines.append("")
            lines.append(t(lang, "room_players"))
            for p in self.player_list:
                lines.append(f"👤 {p.mention}")
            lines.append("")
            if self.player_count < self.min_players:
                lines.append(
                    t(
                        lang,
                        "room_status_waiting",
                        count=self.player_count,
                        min=self.min_players,
                    )
                )
            else:
                lines.append(
                    t(
                        lang,
                        "room_status_ready",
                        count=self.player_count,
                        max=self.max_players,
                    )
                )
        return "\n".join(lines)

    def render_game(self, lang: str = "en") -> str:
        from locales import t

        lines = [t(lang, "game_title"), ""]
        lines.append(t(lang, "label_players"))
        for p in self.player_list:
            cards = "🂠🂠" if not p.folded else t(lang, "folded")
            marker = " ⬅️" if self.is_player_turn(p.user_id) else ""
            lines.append(f"👤 {p.mention}   {cards}{marker}")
        lines.append("")
        lines.append(t(lang, "label_community"))
        if not self.community:
            lines.append("🂠 🂠 🂠 🂠 🂠")
        else:
            shown = " ".join(c.display() for c in self.community)
            hidden = " 🂠" * (5 - len(self.community))
            lines.append(shown + hidden)
        lines.append("")
        cur = self.current_player()
        if cur and self.state not in (GameState.SHOWDOWN, GameState.FINISHED):
            if self.uses_turn_timer():
                remaining = max(0, int(self.turn_deadline - time.time()))
                lines.append(
                    t(lang, "label_turn", name=cur.mention, seconds=remaining)
                )
            else:
                # Private / no-timer: UNO-style "Next player"
                lines.append(
                    t(lang, "label_next_player", name=cur.mention)
                )
        lines.append("")
        lines.append(
            t(lang, "label_street", street=t(lang, self._street_key()))
        )
        if self.mode and self.mode.value == "private":
            lines.append("")
            lines.append(t(lang, "private_turn_hint"))
        if self.mode:
            lines.append("")
            lines.append(t(lang, self.mode.label_key))
        return "\n".join(lines)

    def render_showdown(self, lang: str = "en") -> str:
        from locales import t

        lines = [t(lang, "showdown_title"), ""]
        for p in self.player_list:
            if p.folded:
                lines.append(f"👤 {p.name}\n{t(lang, 'folded')}")
            else:
                cards = " ".join(c.display() for c in p.hole_cards)
                score = self.get_hand_score(p)
                rank_label = t(lang, self._rank_key(score.rank))
                lines.append(f"👤 {p.name}\n{cards}\n→ {rank_label}")
            lines.append("")
        lines.append(t(lang, "label_community_short"))
        lines.append(" ".join(c.display() for c in self.community))
        lines.append("")

        winners = self.get_winners()
        if len(winners) == 1:
            w = winners[0]
            score = self.get_hand_score(w)
            rank_label = t(lang, self._rank_key(score.rank))
            lines.append(t(lang, "winner_title"))
            lines.append(f"👤 {w.name}")
            lines.append(t(lang, "combination", combination=rank_label))
            lines.append("")
            lines.append(t(lang, "congrats"))
        else:
            lines.append(t(lang, "split_pot"))
            for w in winners:
                score = self.get_hand_score(w)
                rank_label = t(lang, self._rank_key(score.rank))
                lines.append(f"👤 {w.name} – {rank_label}")
            lines.append("")
            lines.append(t(lang, "congrats"))
        return "\n".join(lines)
