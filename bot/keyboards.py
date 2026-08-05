"""Inline keyboards for lobby and in-game actions."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def lobby_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("➕ Join", callback_data="join"),
                InlineKeyboardButton("➖ Leave", callback_data="leave"),
            ],
            [
                InlineKeyboardButton("👥 Players", callback_data="players"),
                InlineKeyboardButton("▶ Start Game", callback_data="startgame"),
            ],
            [
                InlineKeyboardButton("❌ Cancel", callback_data="cancel"),
            ],
        ]
    )


def game_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅ Check", callback_data="action:check"),
                InlineKeyboardButton("📞 Call", callback_data="action:call"),
            ],
            [
                InlineKeyboardButton("⬆ Raise", callback_data="action:raise"),
                InlineKeyboardButton("❌ Fold", callback_data="action:fold"),
            ],
        ]
    )


def empty_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([])
