"""Interactive multi-page tutorial system."""

from __future__ import annotations

from typing import Dict, List, Optional, Set

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from locales import t

# Ordered page keys for Previous / Next navigation
PAGE_ORDER: List[str] = [
    "basics",
    "flow",
    "examples",
    "buttons",
    "ranking",
    "tips",
    "faq",
]

# In-memory: users who have seen the first-time welcome
seen_welcome: Set[int] = set()


def mark_welcome_seen(user_id: int) -> None:
    seen_welcome.add(user_id)


def has_seen_welcome(user_id: int) -> bool:
    return user_id in seen_welcome


def page_index(page: str) -> int:
    try:
        return PAGE_ORDER.index(page)
    except ValueError:
        return 0


def prev_page(page: str) -> Optional[str]:
    i = page_index(page)
    return PAGE_ORDER[i - 1] if i > 0 else None


def next_page(page: str) -> Optional[str]:
    i = page_index(page)
    return PAGE_ORDER[i + 1] if i < len(PAGE_ORDER) - 1 else None


def menu_text(lang: str) -> str:
    return t(lang, "tut_menu")


def page_text(lang: str, page: str) -> str:
    key = f"tut_{page}"
    return t(lang, key)


def menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(t(lang, "tut_btn_basics"), callback_data="tut:basics")],
        [InlineKeyboardButton(t(lang, "tut_btn_flow"), callback_data="tut:flow")],
        [InlineKeyboardButton(t(lang, "tut_btn_examples"), callback_data="tut:examples")],
        [InlineKeyboardButton(t(lang, "tut_btn_ranking"), callback_data="tut:ranking")],
        [InlineKeyboardButton(t(lang, "tut_btn_buttons"), callback_data="tut:buttons")],
        [InlineKeyboardButton(t(lang, "tut_btn_tips"), callback_data="tut:tips")],
        [InlineKeyboardButton(t(lang, "tut_btn_faq"), callback_data="tut:faq")],
        [InlineKeyboardButton(t(lang, "tut_btn_lang"), callback_data="tut:lang")],
    ]
    return InlineKeyboardMarkup(rows)


def nav_keyboard(lang: str, page: str) -> InlineKeyboardMarkup:
    """Previous / Home / Next for a content page."""
    row: List[InlineKeyboardButton] = []
    p = prev_page(page)
    n = next_page(page)
    if p:
        row.append(
            InlineKeyboardButton(t(lang, "tut_btn_prev"), callback_data=f"tut:{p}")
        )
    row.append(
        InlineKeyboardButton(t(lang, "tut_btn_home"), callback_data="tut:menu")
    )
    if n:
        row.append(
            InlineKeyboardButton(t(lang, "tut_btn_next"), callback_data=f"tut:{n}")
        )
    return InlineKeyboardMarkup([row])


def welcome_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    t(lang, "welcome_btn_tutorial"), callback_data="tut:menu"
                ),
            ],
            [
                InlineKeyboardButton(
                    t(lang, "welcome_btn_skip"), callback_data="welcome:skip"
                ),
            ],
        ]
    )


def welcome_text(lang: str) -> str:
    return t(lang, "welcome_first")
