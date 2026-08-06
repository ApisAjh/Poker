"""Telegram Inline Mode – private hole cards (UNO-style).

Only the querying user sees their cards in the inline popup.
Choosing an action posts a clean line to the group (no cards).
"""

from __future__ import annotations

import logging
from typing import Dict, Optional
from uuid import uuid4

from telegram import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    Update,
)
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from game.modes import GameMode
from game.poker import GameState, PlayerAction, PokerGame
from locales import resolve_lang, t

logger = logging.getLogger(__name__)

_games_ref: Optional[Dict[int, PokerGame]] = None

# Hidden marker for action payload (stripped from group after processing)
_ACT_PREFIX = "§P§"


def bind_games(games: Dict[int, PokerGame]) -> None:
    global _games_ref
    _games_ref = games


def _find_user_game(user_id: int, chat_hint: Optional[int] = None) -> Optional[PokerGame]:
    if not _games_ref:
        return None
    if chat_hint is not None:
        g = _games_ref.get(chat_hint)
        if (
            g
            and g.mode == GameMode.PRIVATE
            and user_id in g.players
            and g.state not in (GameState.WAITING, GameState.FINISHED, GameState.SHOWDOWN)
        ):
            return g
    for g in _games_ref.values():
        if (
            g.mode == GameMode.PRIVATE
            and user_id in g.players
            and g.state not in (GameState.WAITING, GameState.FINISHED, GameState.SHOWDOWN)
        ):
            return g
    return None


async def inline_query_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
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

    def _empty(title: str) -> list:
        return [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=title,
                input_message_content=InputTextMessageContent(title),
            )
        ]

    if not game:
        await iq.answer(
            _empty(t(lang, "inline_not_in_game")), cache_time=0, is_personal=True
        )
        return

    if game.state in (GameState.SHOWDOWN, GameState.FINISHED):
        await iq.answer(
            _empty(t(lang, "inline_game_over")), cache_time=0, is_personal=True
        )
        return

    player = game.players.get(user.id)
    if not player or player.folded:
        await iq.answer(
            _empty(t(lang, "inline_not_in_game")), cache_time=0, is_personal=True
        )
        return

    cards_str = "  ".join(c.display() for c in player.hole_cards)
    is_turn = game.is_player_turn(user.id)

    results = []

    # Cards visible only inside this user's inline panel
    results.append(
        InlineQueryResultArticle(
            id=f"view-{uuid4().hex[:8]}",
            title=f"🃏  {cards_str}",
            description=t(lang, "inline_title_cards", cards=cards_str),
            input_message_content=InputTextMessageContent(
                t(lang, "private_turn_hint")
                if is_turn
                else t(lang, "inline_not_your_turn")
            ),
        )
    )

    actions = [
        ("check", "✅ Check", "inline_desc_check"),
        ("call", "📞 Call", "inline_desc_call"),
        ("raise", "⬆ Raise", "inline_desc_raise"),
        ("fold", "❌ Fold", "inline_desc_fold"),
    ]

    for act, label, desc_key in actions:
        if not is_turn:
            results.append(
                InlineQueryResultArticle(
                    id=f"{act}-{uuid4().hex[:8]}",
                    title=f"{label}  🔒",
                    description=t(lang, "inline_not_your_turn"),
                    input_message_content=InputTextMessageContent(
                        t(lang, "inline_not_your_turn")
                    ),
                )
            )
            continue

        visible = t(
            lang, "inline_action_posted", player=player.mention, action=label
        )
        payload = f"{_ACT_PREFIX}{game.chat_id}|{user.id}|{act}"
        message_text = f"{visible}\n{payload}"

        results.append(
            InlineQueryResultArticle(
                id=f"{act}-{uuid4().hex[:8]}",
                title=f"{label}   ·   {cards_str}",
                description=t(lang, desc_key),
                input_message_content=InputTextMessageContent(
                    message_text,
                    parse_mode=ParseMode.HTML,
                ),
            )
        )

    await iq.answer(results, cache_time=0, is_personal=True)


async def process_private_action_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    if not update.message or not update.message.text or not update.effective_user:
        return
    text = update.message.text
    if _ACT_PREFIX not in text:
        return

    try:
        payload = text.split(_ACT_PREFIX, 1)[1].strip().split()[0]
        chat_id_s, user_id_s, action_str = payload.split("|", 2)
        chat_id = int(chat_id_s)
        user_id = int(user_id_s)
    except (IndexError, ValueError):
        return

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

    try:
        action = PlayerAction(action_str)
    except ValueError:
        return

    result = game.apply_action(user_id, action)
    lang = resolve_lang(user_id, update.effective_user.language_code)
    player = game.players.get(user_id)
    name = player.mention if player else str(user_id)
    label = {
        "check": "✅ Check",
        "call": "📞 Call",
        "raise": "⬆ Raise",
        "fold": "❌ Fold",
    }.get(action_str, action_str)

    try:
        await update.message.delete()
    except Exception:
        pass

    if result != "ok":
        try:
            await context.bot.send_message(chat_id=chat_id, text=t(lang, result))
        except Exception:
            pass
        return

    try:
        await context.bot.send_message(
            chat_id=chat_id,
            text=t(lang, "inline_action_posted", player=name, action=label),
            parse_mode=ParseMode.HTML,
        )
    except Exception:
        logger.exception("post private action failed")

    from bot.handlers import _refresh_game_view_bot

    await _refresh_game_view_bot(context.bot, game)
