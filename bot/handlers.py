"""Command and callback handlers for the Poker bot."""

from __future__ import annotations

import logging
import time
from typing import Dict, Optional

from telegram import Update, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from game.poker import PokerGame, GameState, PlayerAction
from bot.keyboards import lobby_keyboard, game_keyboard, empty_keyboard

logger = logging.getLogger(__name__)

# In-memory store – one game per chat_id
games: Dict[int, PokerGame] = {}


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _get_game(chat_id: int) -> Optional[PokerGame]:
    return games.get(chat_id)


def _is_group(update: Update) -> bool:
    chat = update.effective_chat
    return chat is not None and chat.type in ("group", "supergroup")


async def _answer_callback(
    update: Update, text: str = "", show_alert: bool = False
) -> None:
    query = update.callback_query
    if query:
        await query.answer(text=text, show_alert=show_alert)


async def _edit_or_reply(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    text: str,
    reply_markup: Optional[InlineKeyboardMarkup] = None,
    message_id: Optional[int] = None,
) -> Optional[int]:
    """Edit existing main message or send a new one. Returns message_id."""
    chat_id = update.effective_chat.id  # type: ignore
    try:
        if message_id is not None:
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup,
            )
            return message_id
        # fallback – new message
        msg = await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
        )
        return msg.message_id
    except Exception as e:
        logger.warning("edit/send failed: %s", e)
        try:
            msg = await context.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup,
            )
            return msg.message_id
        except Exception as e2:
            logger.error("send also failed: %s", e2)
            return None


# ------------------------------------------------------------------
# Commands
# ------------------------------------------------------------------

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    text = (
        "🃏 <b>Telegram Poker Bot</b>\n\n"
        "Play Texas Hold'em directly in your group!\n\n"
        "Commands:\n"
        "/poker – Create a new room\n"
        "/join – Join current room\n"
        "/leave – Leave room\n"
        "/players – List players\n"
        "/startgame – Start the game (host)\n"
        "/cancel – Cancel room (host)\n"
        "/help – Show this help\n\n"
        "Add me to a group and type /poker to begin."
    )
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await cmd_start(update, context)


async def cmd_poker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.effective_user:
        return
    if not _is_group(update):
        await update.message.reply_text(
            "❌ This bot only works in groups. Add me to a group and try again."
        )
        return

    chat_id = update.effective_chat.id  # type: ignore
    user = update.effective_user

    existing = _get_game(chat_id)
    if existing and existing.state != GameState.FINISHED:
        await update.message.reply_text(
            "⚠️ A game is already active in this group. "
            "Finish or cancel it first."
        )
        return

    game = PokerGame(
        chat_id=chat_id,
        host_id=user.id,
        host_name=user.full_name or user.username or str(user.id),
    )
    games[chat_id] = game

    text = game.render_room()
    msg = await update.message.reply_text(
        text, parse_mode=ParseMode.HTML, reply_markup=lobby_keyboard()
    )
    game.message_id = msg.message_id


async def cmd_join(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.effective_user:
        return
    if not _is_group(update):
        return
    chat_id = update.effective_chat.id  # type: ignore
    user = update.effective_user
    game = _get_game(chat_id)
    if not game or game.state == GameState.FINISHED:
        await update.message.reply_text("No active room. Use /poker first.")
        return
    result = game.add_player(
        user.id, user.full_name or user.username or str(user.id)
    )
    if result != "ok":
        await update.message.reply_text(f"⚠️ {result}")
        return
    text = game.render_room()
    await _edit_or_reply(
        update, context, text, lobby_keyboard(), game.message_id
    )


async def cmd_leave(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.effective_user:
        return
    if not _is_group(update):
        return
    chat_id = update.effective_chat.id  # type: ignore
    user = update.effective_user
    game = _get_game(chat_id)
    if not game or game.state == GameState.FINISHED:
        await update.message.reply_text("No active room.")
        return
    result = game.remove_player(user.id)
    if result == "host_left":
        games.pop(chat_id, None)
        await update.message.reply_text(
            "🏠 Host left. Room cancelled.",
            reply_markup=empty_keyboard(),
        )
        return
    if result != "ok":
        await update.message.reply_text(f"⚠️ {result}")
        return
    if game.player_count == 0:
        games.pop(chat_id, None)
        await update.message.reply_text("Room empty – closed.")
        return
    text = game.render_room()
    await _edit_or_reply(
        update, context, text, lobby_keyboard(), game.message_id
    )


async def cmd_players(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    if not _is_group(update):
        return
    chat_id = update.effective_chat.id  # type: ignore
    game = _get_game(chat_id)
    if not game or game.state == GameState.FINISHED:
        await update.message.reply_text("No active room.")
        return
    names = "\n".join(f"👤 {p.name}" for p in game.player_list)
    await update.message.reply_text(
        f"<b>Players ({game.player_count})</b>\n{names}",
        parse_mode=ParseMode.HTML,
    )


async def cmd_startgame(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    if not update.message or not update.effective_user:
        return
    if not _is_group(update):
        return
    chat_id = update.effective_chat.id  # type: ignore
    user = update.effective_user
    game = _get_game(chat_id)
    if not game or game.state == GameState.FINISHED:
        await update.message.reply_text("No active room. Use /poker first.")
        return
    if user.id != game.host_id:
        await update.message.reply_text("Only the host can start the game.")
        return
    if not game.can_start():
        await update.message.reply_text(
            f"Need at least {game.min_players} players "
            f"(currently {game.player_count})."
        )
        return
    game.start()
    text = game.render_game()
    mid = await _edit_or_reply(
        update, context, text, game_keyboard(), game.message_id
    )
    if mid:
        game.message_id = mid


async def cmd_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.effective_user:
        return
    if not _is_group(update):
        return
    chat_id = update.effective_chat.id  # type: ignore
    user = update.effective_user
    game = _get_game(chat_id)
    if not game or game.state == GameState.FINISHED:
        await update.message.reply_text("No active room.")
        return
    if user.id != game.host_id:
        await update.message.reply_text("Only the host can cancel.")
        return
    games.pop(chat_id, None)
    await update.message.reply_text(
        "❌ Room cancelled.", reply_markup=empty_keyboard()
    )


# ------------------------------------------------------------------
# Callback queries (inline buttons)
# ------------------------------------------------------------------

async def callback_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query
    if not query or not update.effective_user or not update.effective_chat:
        return

    data = query.data or ""
    chat_id = update.effective_chat.id
    user = update.effective_user
    game = _get_game(chat_id)

    # ----- Lobby actions -----
    if data == "join":
        if not game or game.state != GameState.WAITING:
            await _answer_callback(update, "No open room.", show_alert=True)
            return
        result = game.add_player(
            user.id, user.full_name or user.username or str(user.id)
        )
        if result != "ok":
            await _answer_callback(update, result, show_alert=True)
            return
        await _answer_callback(update, "Joined!")
        text = game.render_room()
        await _edit_or_reply(
            update, context, text, lobby_keyboard(), game.message_id
        )
        return

    if data == "leave":
        if not game or game.state != GameState.WAITING:
            await _answer_callback(update, "No open room.", show_alert=True)
            return
        result = game.remove_player(user.id)
        if result == "host_left":
            games.pop(chat_id, None)
            await _answer_callback(update, "Host left – room closed.")
            await _edit_or_reply(
                update,
                context,
                "🏠 Host left. Room cancelled.",
                empty_keyboard(),
                game.message_id,
            )
            return
        if result != "ok":
            await _answer_callback(update, result, show_alert=True)
            return
        await _answer_callback(update, "Left.")
        if game.player_count == 0:
            games.pop(chat_id, None)
            await _edit_or_reply(
                update,
                context,
                "Room empty – closed.",
                empty_keyboard(),
                game.message_id,
            )
            return
        text = game.render_room()
        await _edit_or_reply(
            update, context, text, lobby_keyboard(), game.message_id
        )
        return

    if data == "players":
        if not game:
            await _answer_callback(update, "No room.", show_alert=True)
            return
        names = ", ".join(p.name for p in game.player_list) or "–"
        await _answer_callback(
            update, f"Players ({game.player_count}): {names}", show_alert=True
        )
        return

    if data == "startgame":
        if not game or game.state != GameState.WAITING:
            await _answer_callback(update, "No open room.", show_alert=True)
            return
        if user.id != game.host_id:
            await _answer_callback(
                update, "Only host can start.", show_alert=True
            )
            return
        if not game.can_start():
            await _answer_callback(
                update,
                f"Need ≥{game.min_players} players.",
                show_alert=True,
            )
            return
        game.start()
        await _answer_callback(update, "Game started!")
        text = game.render_game()
        mid = await _edit_or_reply(
            update, context, text, game_keyboard(), game.message_id
        )
        if mid:
            game.message_id = mid
        return

    if data == "cancel":
        if not game:
            await _answer_callback(update, "No room.", show_alert=True)
            return
        if user.id != game.host_id:
            await _answer_callback(
                update, "Only host can cancel.", show_alert=True
            )
            return
        games.pop(chat_id, None)
        await _answer_callback(update, "Cancelled.")
        await _edit_or_reply(
            update,
            context,
            "❌ Room cancelled.",
            empty_keyboard(),
            game.message_id if game else None,
        )
        return

    # ----- In-game actions -----
    if data.startswith("action:"):
        if not game or game.state in (
            GameState.WAITING,
            GameState.SHOWDOWN,
            GameState.FINISHED,
        ):
            await _answer_callback(update, "No active game.", show_alert=True)
            return

        # Timeout check before accepting action
        if time.time() > game.turn_deadline:
            auto = game.auto_action_on_timeout()
            await _answer_callback(
                update, f"Time expired – auto {auto.value if auto else '?'}"
            )
            await _refresh_game_view(update, context, game)
            return

        action_str = data.split(":", 1)[1]
        try:
            action = PlayerAction(action_str)
        except ValueError:
            await _answer_callback(update, "Invalid action.", show_alert=True)
            return

        result = game.apply_action(user.id, action)
        if result == "not_your_turn":
            await _answer_callback(update, "Bukan giliranmu.", show_alert=True)
            return
        if result != "ok":
            await _answer_callback(update, result, show_alert=True)
            return

        await _answer_callback(update, f"{action.value.title()}!")
        await _refresh_game_view(update, context, game)
        return

    await _answer_callback(update, "Unknown button.")


async def _refresh_game_view(
    update: Update, context: ContextTypes.DEFAULT_TYPE, game: PokerGame
) -> None:
    """Update main message after an action / street change / showdown."""
    if game.state == GameState.SHOWDOWN:
        text = game.render_showdown()
        mid = await _edit_or_reply(
            update, context, text, empty_keyboard(), game.message_id
        )
        if mid:
            game.message_id = mid
        # Clean up after showdown
        game.finish()
        games.pop(game.chat_id, None)
        return

    # Still playing
    text = game.render_game()
    mid = await _edit_or_reply(
        update, context, text, game_keyboard(), game.message_id
    )
    if mid:
        game.message_id = mid

    # Auto-win if only one left
    if len(game.active_players) <= 1 and game.state not in (
        GameState.SHOWDOWN,
        GameState.FINISHED,
    ):
        game._go_to_showdown()
        await _refresh_game_view(update, context, game)
