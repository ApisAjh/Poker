"""Inline keyboards for lobby, modes, and in-game actions (i18n)."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from locales import t
from game.modes import GameMode


def lobby_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(t(lang, "btn_join"), callback_data="join"),
                InlineKeyboardButton(t(lang, "btn_leave"), callback_data="leave"),
            ],
            [
                InlineKeyboardButton(t(lang, "btn_players"), callback_data="players"),
                InlineKeyboardButton(t(lang, "btn_start"), callback_data="startgame"),
            ],
            [
                InlineKeyboardButton(t(lang, "btn_cancel"), callback_data="cancel"),
            ],
        ]
    )


def mode_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    t(lang, "mode_classic"), callback_data="mode:classic"
                ),
            ],
            [
                InlineKeyboardButton(
                    t(lang, "mode_private"), callback_data="mode:private"
                ),
            ],
        ]
    )


def game_keyboard(
    lang: str = "en",
    mode: GameMode | None = None,
    chat_id: int = 0,
    turn_label: str = "",  # kept for API compat; not shown on button
) -> InlineKeyboardMarkup:
    """Classic: action buttons. Private: UNO-style switch-inline button."""
    if mode == GameMode.PRIVATE:
        # Same pattern as UNO bots — short label, no player name in button
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        t(lang, "btn_open_hand"),
                        switch_inline_query_current_chat=f"hand {chat_id}",
                    ),
                ],
            ]
        )
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(t(lang, "btn_check"), callback_data="action:check"),
                InlineKeyboardButton(t(lang, "btn_call"), callback_data="action:call"),
            ],
            [
                InlineKeyboardButton(t(lang, "btn_raise"), callback_data="action:raise"),
                InlineKeyboardButton(t(lang, "btn_fold"), callback_data="action:fold"),
            ],
        ]
    )


def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    t("id", "btn_lang_id"), callback_data="lang:id"
                ),
            ],
            [
                InlineKeyboardButton(
                    t("en", "btn_lang_en"), callback_data="lang:en"
                ),
            ],
        ]
    )


def empty_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([])
