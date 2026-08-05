"""Command and callback handlers for the Poker bot (i18n)."""

from __future__ import annotations

import logging
import time
from typing import Dict, Optional

from telegram import Update, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from game.poker import PokerGame, GameState, PlayerAction
from game.modes import GameMode
from bot.keyboards import (
    lobby_keyboard,
    game_keyboard,
    language_keyboard,
    empty_keyboard,
    mode_keyboard,
)
from bot.tutorial import (
    PAGE_ORDER,
    has_seen_welcome,
    mark_welcome_seen,
    menu_keyboard,
    menu_text,
    nav_keyboard,
    page_text,
    welcome_keyboard,
    welcome_text,
)
from locales import t, resolve_lang, set_lang
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


def _lang(update: Update) -> str:
    user = update.effective_user
    if not user:
        return "en"
    return resolve_lang(user.id, user.language_code)


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
    lang = _lang(update)
    text = t(lang, "start") + t(lang, "help_menu_hint")
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Open interactive tutorial menu."""
    if not update.message:
        return
    lang = _lang(update)
    await update.message.reply_text(
        menu_text(lang),
        parse_mode=ParseMode.HTML,
        reply_markup=menu_keyboard(lang),
    )


async def cmd_tutorial(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await cmd_help(update, context)


async def cmd_rules(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await cmd_help(update, context)


async def cmd_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    lang = _lang(update)
    await update.message.reply_text(
        t(lang, "language_title"),
        parse_mode=ParseMode.HTML,
        reply_markup=language_keyboard(),
    )



async def _show_mode_select(
    update: Update, context: ContextTypes.DEFAULT_TYPE, lang: str
) -> None:
    """Ask host to pick Classic or Private before creating the room."""
    text = t(lang, "mode_select_title")
    if update.message:
        await update.message.reply_text(
            text, parse_mode=ParseMode.HTML, reply_markup=mode_keyboard(lang)
        )
    elif update.callback_query:
        try:
            await update.callback_query.edit_message_text(
                text, parse_mode=ParseMode.HTML, reply_markup=mode_keyboard(lang)
            )
        except Exception:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,  # type: ignore
                text=text,
                parse_mode=ParseMode.HTML,
                reply_markup=mode_keyboard(lang),
            )


async def _create_poker_room(
    update: Update, context: ContextTypes.DEFAULT_TYPE, lang: str, mode: GameMode
) -> None:
    """Actually create the room (shared by /poker and welcome skip)."""
    if not update.effective_user or not update.effective_chat:
        return
    chat_id = update.effective_chat.id
    user = update.effective_user

    existing = _get_game(chat_id)
    if existing and existing.state != GameState.FINISHED:
        if update.callback_query:
            await _answer_callback(
                update, t(lang, "game_already_active"), show_alert=True
            )
        elif update.message:
            await update.message.reply_text(t(lang, "game_already_active"))
        return

    game = PokerGame(
        chat_id=chat_id,
        host_id=user.id,
        host_name=user.full_name or user.username or str(user.id),
        lang=lang,
        mode=mode,
    )
    if user.username and game.host_id in game.players:
        game.players[game.host_id].username = user.username
    games[chat_id] = game

    text = game.render_room(lang)
    msg = await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=lobby_keyboard(lang),
    )
    game.message_id = msg.message_id


    if update.callback_query:
        try:
            await update.callback_query.edit_message_reply_markup(
                reply_markup=empty_keyboard()
            )
        except Exception:
            pass


async def cmd_poker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.effective_user:
        return
    lang = _lang(update)
    if not _is_group(update):
        await update.message.reply_text(t(lang, "group_only"))
        return

    chat_id = update.effective_chat.id  # type: ignore
    user = update.effective_user

    existing = _get_game(chat_id)
    if existing and existing.state != GameState.FINISHED:
        await update.message.reply_text(t(lang, "game_already_active"))
        return

    # First-time welcome with tutorial option
    if not has_seen_welcome(user.id):
        await update.message.reply_text(
            welcome_text(lang),
            parse_mode=ParseMode.HTML,
            reply_markup=welcome_keyboard(lang),
        )
        return

    await _show_mode_select(update, context, lang)


async def cmd_join(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.effective_user:
        return
    lang = _lang(update)
    if not _is_group(update):
        return
    chat_id = update.effective_chat.id  # type: ignore
    user = update.effective_user
    game = _get_game(chat_id)
    if not game or game.state == GameState.FINISHED:
        await update.message.reply_text(t(lang, "no_active_room"))
        return
    result = game.add_player(
        user.id, user.full_name or user.username or str(user.id), user.username
    )
    if result == "ok":
        await update.message.reply_text(
            t(lang, "joined", player=user.full_name or user.username or str(user.id))
        )
        text = game.render_room(game.lang)
        await _edit_or_reply(
            update, context, text, lobby_keyboard(game.lang), game.message_id
        )
        return
    if result == "room_full":
        await update.message.reply_text(
            t(lang, "room_full", max=game.max_players)
        )
    else:
        await update.message.reply_text(t(lang, result))


async def cmd_leave(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.effective_user:
        return
    lang = _lang(update)
    if not _is_group(update):
        return
    chat_id = update.effective_chat.id  # type: ignore
    user = update.effective_user
    game = _get_game(chat_id)
    if not game or game.state == GameState.FINISHED:
        await update.message.reply_text(t(lang, "no_room"))
        return
    result = game.remove_player(user.id)
    if result == "host_left":
        games.pop(chat_id, None)
        await update.message.reply_text(
            t(lang, "host_left"), reply_markup=empty_keyboard()
        )
        return
    if result == "ok":
        if game.player_count == 0:
            games.pop(chat_id, None)
            await update.message.reply_text(t(lang, "room_empty"))
            return
        await update.message.reply_text(t(lang, "left"))
        text = game.render_room(game.lang)
        await _edit_or_reply(
            update, context, text, lobby_keyboard(game.lang), game.message_id
        )
        return
    await update.message.reply_text(t(lang, result))


async def cmd_players(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    lang = _lang(update)
    if not _is_group(update):
        return
    chat_id = update.effective_chat.id  # type: ignore
    game = _get_game(chat_id)
    if not game or game.state == GameState.FINISHED:
        await update.message.reply_text(t(lang, "no_room"))
        return
    names = "\n".join(f"👤 {p.name}" for p in game.player_list)
    await update.message.reply_text(
        t(lang, "players_list", count=game.player_count, names=names),
        parse_mode=ParseMode.HTML,
    )


async def cmd_startgame(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    if not update.message or not update.effective_user:
        return
    lang = _lang(update)
    if not _is_group(update):
        return
    chat_id = update.effective_chat.id  # type: ignore
    user = update.effective_user
    game = _get_game(chat_id)
    if not game or game.state == GameState.FINISHED:
        await update.message.reply_text(t(lang, "no_active_room"))
        return
    if user.id != game.host_id:
        await update.message.reply_text(t(lang, "only_host_start"))
        return
    if not game.can_start():
        await update.message.reply_text(
            t(lang, "need_players", min=game.min_players, count=game.player_count)
        )
        return
    game.start()
    await update.message.reply_text(t(lang, "game_started"))
    text = game.render_game(game.lang)
    mid = await _edit_or_reply(
        update, context, text, game_keyboard(game.lang, game.mode, game.chat_id, (game.current_player().mention if game.current_player() else '')), game.message_id
    )
    if mid:
        game.message_id = mid


async def cmd_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.effective_user:
        return
    lang = _lang(update)
    if not _is_group(update):
        return
    chat_id = update.effective_chat.id  # type: ignore
    user = update.effective_user
    game = _get_game(chat_id)
    if not game or game.state == GameState.FINISHED:
        await update.message.reply_text(t(lang, "no_room"))
        return
    if user.id != game.host_id:
        await update.message.reply_text(t(lang, "only_host_cancel"))
        return
    games.pop(chat_id, None)
    await update.message.reply_text(
        t(lang, "room_cancelled"), reply_markup=empty_keyboard()
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
    lang = _lang(update)
    game = _get_game(chat_id)

    # ----- Language selection -----
    if data.startswith("lang:"):
        new_lang = data.split(":", 1)[1]
        if new_lang not in ("id", "en"):
            new_lang = "en"
        set_lang(user.id, new_lang)
        key = "language_set_id" if new_lang == "id" else "language_set_en"
        await _answer_callback(update)
        try:
            await query.edit_message_text(
                t(new_lang, key), parse_mode=ParseMode.HTML
            )
        except Exception:
            pass
        return


    # ----- Mode selection -----
    if data.startswith("mode:"):
        mode_str = data.split(":", 1)[1]
        if mode_str not in ("classic", "private"):
            await _answer_callback(update, t(lang, "unknown_button"))
            return
        mode = GameMode.CLASSIC if mode_str == "classic" else GameMode.PRIVATE
        mark_welcome_seen(user.id)
        await _answer_callback(update)
        if not _is_group(update):
            await _answer_callback(update, t(lang, "group_only"), show_alert=True)
            return
        await _create_poker_room(update, context, lang, mode)
        return

    # ----- First-time welcome: Skip → create room -----
    if data == "welcome:skip":
        mark_welcome_seen(user.id)
        await _answer_callback(update)
        if not _is_group(update):
            await _answer_callback(update, t(lang, "group_only"), show_alert=True)
            return
        try:
            await query.edit_message_text(
                t(lang, "mode_select_title"),
                parse_mode=ParseMode.HTML,
                reply_markup=mode_keyboard(lang),
            )
        except Exception:
            await context.bot.send_message(
                chat_id=chat_id,
                text=t(lang, "mode_select_title"),
                parse_mode=ParseMode.HTML,
                reply_markup=mode_keyboard(lang),
            )
        return

    # ----- Tutorial navigation -----
    if data.startswith("tut:"):
        page = data.split(":", 1)[1]
        await _answer_callback(update)
        mark_welcome_seen(user.id)

        if page == "lang":
            try:
                await query.edit_message_text(
                    t(lang, "language_title"),
                    parse_mode=ParseMode.HTML,
                    reply_markup=language_keyboard(),
                )
            except Exception:
                pass
            return

        if page == "menu":
            try:
                await query.edit_message_text(
                    menu_text(lang),
                    parse_mode=ParseMode.HTML,
                    reply_markup=menu_keyboard(lang),
                )
            except Exception:
                pass
            return

        if page in PAGE_ORDER:
            try:
                await query.edit_message_text(
                    page_text(lang, page),
                    parse_mode=ParseMode.HTML,
                    reply_markup=nav_keyboard(lang, page),
                )
            except Exception:
                pass
            return

        await _answer_callback(update, t(lang, "unknown_button"))
        return

    # ----- Lobby actions -----
    if data == "join":
        if not game or game.state != GameState.WAITING:
            await _answer_callback(update, t(lang, "no_open_room"), show_alert=True)
            return
        result = game.add_player(
            user.id, user.full_name or user.username or str(user.id), user.username
        )
        if result != "ok":
            if result == "room_full":
                msg = t(lang, "room_full", max=game.max_players)
            else:
                msg = t(lang, result)
            await _answer_callback(update, msg, show_alert=True)
            return
        await _answer_callback(update, t(lang, "joined_short"))
        text = game.render_room(game.lang)
        await _edit_or_reply(
            update, context, text, lobby_keyboard(game.lang), game.message_id
        )
        return

    if data == "leave":
        if not game or game.state != GameState.WAITING:
            await _answer_callback(update, t(lang, "no_open_room"), show_alert=True)
            return
        result = game.remove_player(user.id)
        if result == "host_left":
            games.pop(chat_id, None)
            await _answer_callback(update, t(lang, "host_left"))
            await _edit_or_reply(
                update,
                context,
                t(lang, "host_left"),
                empty_keyboard(),
                game.message_id,
            )
            return
        if result != "ok":
            await _answer_callback(update, t(lang, result), show_alert=True)
            return
        await _answer_callback(update, t(lang, "left_short"))
        if game.player_count == 0:
            games.pop(chat_id, None)
            await _edit_or_reply(
                update,
                context,
                t(lang, "room_empty"),
                empty_keyboard(),
                game.message_id,
            )
            return
        text = game.render_room(game.lang)
        await _edit_or_reply(
            update, context, text, lobby_keyboard(game.lang), game.message_id
        )
        return

    if data == "players":
        if not game:
            await _answer_callback(update, t(lang, "no_room"), show_alert=True)
            return
        names = ", ".join(p.name for p in game.player_list) or "–"
        await _answer_callback(
            update,
            t(lang, "players_popup", count=game.player_count, names=names),
            show_alert=True,
        )
        return

    if data == "startgame":
        if not game or game.state != GameState.WAITING:
            await _answer_callback(update, t(lang, "no_open_room"), show_alert=True)
            return
        if user.id != game.host_id:
            await _answer_callback(
                update, t(lang, "only_host_short"), show_alert=True
            )
            return
        if not game.can_start():
            await _answer_callback(
                update,
                t(lang, "need_players_short", min=game.min_players),
                show_alert=True,
            )
            return
            game.start()
        await _answer_callback(update, t(lang, "started_short"))
        text = game.render_game(game.lang)
        mid = await _edit_or_reply(
            update, context, text, game_keyboard(game.lang, game.mode, game.chat_id, (game.current_player().mention if game.current_player() else '')), game.message_id
        )
        if mid:
            game.message_id = mid
            return

    if data == "cancel":
        if not game:
            await _answer_callback(update, t(lang, "no_room"), show_alert=True)
            return
        if user.id != game.host_id:
            await _answer_callback(
                update, t(lang, "only_host_cancel_short"), show_alert=True
            )
            return
            games.pop(chat_id, None)
        await _answer_callback(update, t(lang, "cancelled_short"))
        await _edit_or_reply(
            update,
            context,
            t(lang, "room_cancelled"),
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
            await _answer_callback(
                update, t(lang, "no_active_game"), show_alert=True
            )
            return

        if game.uses_turn_timer() and game.turn_deadline and time.time() > game.turn_deadline:
            auto = game.auto_action_on_timeout()
            action_name = auto.value if auto else "?"
            await _answer_callback(
                update, t(lang, "time_expired", action=action_name)
            )
            await _refresh_game_view(update, context, game)
            return

        action_str = data.split(":", 1)[1]
        try:
            action = PlayerAction(action_str)
        except ValueError:
            await _answer_callback(
                update, t(lang, "invalid_action"), show_alert=True
            )
            return

        result = game.apply_action(user.id, action)
        if result != "ok":
            await _answer_callback(update, t(lang, result), show_alert=True)
            return

        await _answer_callback(
            update, t(lang, "action_ok", action=action.value.title())
        )
        await _refresh_game_view(update, context, game)
        return

    await _answer_callback(update, t(lang, "unknown_button"))


# ------------------------------------------------------------------

async def _refresh_game_view_bot(bot, game: PokerGame) -> None:
    """Refresh board using Bot only (used by private-mode inline actions)."""
    lang = game.lang
    chat_id = game.chat_id
    try:
        if game.state == GameState.SHOWDOWN:
            text = game.render_showdown(lang)
            if game.message_id:
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=game.message_id,
                    text=text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=empty_keyboard(),
                )
            game.finish()
            games.pop(chat_id, None)
            return

        if len(game.active_players) <= 1:
            game._go_to_showdown()
            await _refresh_game_view_bot(bot, game)
            return

        text = game.render_game(lang)
        if game.message_id:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=game.message_id,
                text=text,
                parse_mode=ParseMode.HTML,
                reply_markup=game_keyboard(lang, game.mode, game.chat_id, (game.current_player().mention if game.current_player() else '')),
            )
    except Exception:
        logger.exception("refresh bot view failed chat=%s", chat_id)


async def _refresh_game_view(
    update: Update, context: ContextTypes.DEFAULT_TYPE, game: PokerGame
) -> None:
    """Update main message after an action / street change / showdown."""
    lang = game.lang
    if game.state == GameState.SHOWDOWN:
        text = game.render_showdown(lang)
        mid = await _edit_or_reply(
            update, context, text, empty_keyboard(), game.message_id
        )
        if mid:
            game.message_id = mid
            game.finish()
        games.pop(game.chat_id, None)
        return

    text = game.render_game(lang)
    mid = await _edit_or_reply(
        update, context, text, game_keyboard(lang, game.mode, game.chat_id, (game.current_player().mention if game.current_player() else '')), game.message_id
    )
    if mid:
        game.message_id = mid

    if len(game.active_players) <= 1 and game.state not in (
        GameState.SHOWDOWN,
        GameState.FINISHED,
    ):
        game._go_to_showdown()
        await _refresh_game_view(update, context, game)
        return

