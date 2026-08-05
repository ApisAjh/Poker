"""Telegram Inline Mode – private hole cards for Poker Private mode."""

from __future__ import annotations

import logging
from typing import Dict, Optional
from uuid import uuid4

from telegram import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    Update,
)
from telegram.ext import ContextTypes

from game.modes import GameMode
from game.poker import GameState, PlayerAction, PokerGame
from locales import resolve_lang, t

logger = logging.getLogger(__name__)

# Filled by handlers module to avoid circular import
_games_ref: Optional[Dict[int, PokerGame]] = None


def bind_games(games: Dict[int, PokerGame]) -> None:
    global _games_ref
    _games_ref = games


def _find_user_game(user_id: int, chat_hint: Optional[int] = None) -> Optional[PokerGame]:
    if not _games_ref:
        return None
    if chat_hint is not None:
        g = _games_ref.get(chat_hint)
        if g and user_id in g.players and g.state not in (
            GameState.WAITING,
            GameState.FINISHED,
        ):
            return g
    for g in _games_ref.values():
        if user_id in g.players and g.state not in (
            GameState.WAITING,
            GameState.FINISHED,
            GameState.SHOWDOWN,
        ):
            if g.mode == GameMode.PRIVATE:
                return g
    return None


async def inline_query_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    User opened @Bot via switch_inline_query_current_chat.
    Query may contain: "hand <chat_id>"
    Returns personal hole cards + action options (only for that user).
    """
    iq = update.inline_query
    if not iq or not iq.from_user:
        return

    user = iq.from_user
    lang = resolve_lang(user.id, user.language_code)
    query = (iq.query or "").strip()

    chat_hint: Optional[int] = None
    parts = query.split()
    if len(parts) >= 2 and parts[0].lower() == "hand":
        try:
            chat_hint = int(parts[1])
        except ValueError:
            chat_hint = None

    game = _find_user_game(user.id, chat_hint)

    if not game:
        await iq.answer(
            [
                InlineQueryResultArticle(
                    id=str(uuid4()),
                    title=t(lang, "inline_not_in_game"),
                    input_message_content=InputTextMessageContent(
                        t(lang, "inline_not_in_game")
                    ),
                )
            ],
            cache_time=1,
            is_personal=True,
        )
        return

    if game.state in (GameState.SHOWDOWN, GameState.FINISHED):
        await iq.answer(
            [
                InlineQueryResultArticle(
                    id=str(uuid4()),
                    title=t(lang, "inline_game_over"),
                    input_message_content=InputTextMessageContent(
                        t(lang, "inline_game_over")
                    ),
                )
            ],
            cache_time=1,
            is_personal=True,
        )
        return

    player = game.players.get(user.id)
    if not player or player.folded:
        await iq.answer(
            [
                InlineQueryResultArticle(
                    id=str(uuid4()),
                    title=t(lang, "inline_not_in_game"),
                    input_message_content=InputTextMessageContent(
                        t(lang, "inline_not_in_game")
                    ),
                )
            ],
            cache_time=1,
            is_personal=True,
        )
        return

    cards_str = " ".join(c.display() for c in player.hole_cards)
    title = t(lang, "inline_title_cards", cards=cards_str)

    # Only allow actions on the player's turn
    is_turn = game.is_player_turn(user.id)

    results = []
    actions = [
        ("check", "✅ Check", "inline_desc_check"),
        ("call", "📞 Call", "inline_desc_call"),
        ("raise", "⬆ Raise", "inline_desc_raise"),
        ("fold", "❌ Fold", "inline_desc_fold"),
    ]

    for act, label, desc_key in actions:
        # Payload encoded in message text for ChosenInlineResult / message filter
        payload = f"POKERACT|{game.chat_id}|{user.id}|{act}"
        body = (
            t(lang, "inline_action_posted", player=player.mention, action=label)
            if is_turn
            else t(lang, "inline_not_your_turn")
        )
        # Always attach payload in a way we can parse; use invisible-ish suffix
        message_text = f"{body}\n`{payload}`" if is_turn else body

        results.append(
            InlineQueryResultArticle(
                id=f"{act}-{uuid4().hex[:8]}",
                title=f"{label}  ·  {cards_str}" if is_turn else f"{label} 🔒",
                description=t(lang, desc_key) if is_turn else t(lang, "inline_not_your_turn"),
                input_message_content=InputTextMessageContent(
                    message_text,
                    parse_mode="Markdown",
                ),
            )
        )

    # Header-only result so user always sees cards even if not their turn
    results.insert(
        0,
        InlineQueryResultArticle(
            id=f"view-{uuid4().hex[:8]}",
            title=title,
            description="🔒 Only you can see this",
            input_message_content=InputTextMessageContent(
                t(lang, "private_turn_hint") if is_turn else t(lang, "inline_not_your_turn")
            ),
        ),
    )

    await iq.answer(results, cache_time=1, is_personal=True)


async def process_private_action_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    When a private-mode player selects an inline action, Telegram posts a
    message containing POKERACT|chat|user|action. Process it and clean up.
    """
    if not update.message or not update.message.text or not update.effective_user:
        return
    text = update.message.text
    if "POKERACT|" not in text:
        return

    # Extract payload
    try:
        payload = text.split("POKERACT|", 1)[1].split()[0].strip("`")
        parts = payload.split("|")
        chat_id = int(parts[0])
        user_id = int(parts[1])
        action_str = parts[2]
    except (IndexError, ValueError):
        return

    # Security: only the sender may apply their own action
    if update.effective_user.id != user_id:
        try:
            await update.message.delete()
        except Exception:
            pass
        return

    if not _games_ref:
        return
    game = _games_ref.get(chat_id)
    if not game or game.mode != GameMode.PRIVATE:
        return

    from bot.handlers import _refresh_game_view  # late import

    try:
        action = PlayerAction(action_str)
    except ValueError:
        return

    result = game.apply_action(user_id, action)
    lang = resolve_lang(user_id, update.effective_user.language_code)

    # Delete the payload message to keep chat clean, then post clean action line
    try:
        await update.message.delete()
    except Exception:
        pass

    if result != "ok":
        try:
            await context.bot.send_message(
                chat_id=chat_id, text=t(lang, result)
            )
        except Exception:
            pass
        return

    player = game.players.get(user_id)
    name = player.name if player else str(user_id)
    label = {
        "check": "✅ Check",
        "call": "📞 Call",
        "raise": "⬆ Raise",
        "fold": "❌ Fold",
    }.get(action_str, action_str)

    try:
        await context.bot.send_message(
            chat_id=chat_id,
            text=t(lang, "inline_action_posted", player=(player.mention if player else name), action=label),
            parse_mode="HTML",
        )
    except Exception:
        pass

    # Build a minimal update-like refresh via bot
    from bot.handlers import _refresh_game_view_bot

    await _refresh_game_view_bot(context.bot, game)
