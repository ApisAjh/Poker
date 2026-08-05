"""i18n helper – Bahasa Indonesia & English."""

from __future__ import annotations

from typing import Any, Dict, Optional

from locales import en, id as id_locale

# user_id -> "id" | "en"  (in-memory preference)
user_languages: Dict[int, str] = {}

TEXTS: Dict[str, Dict[str, str]] = {
    "id": id_locale.TEXTS,
    "en": en.TEXTS,
}

DEFAULT_LANG = "en"


def resolve_lang(
    user_id: Optional[int] = None,
    language_code: Optional[str] = None,
) -> str:
    """
    Priority:
    1. Explicit preference stored in RAM
    2. Telegram language_code == "id" → Indonesian
    3. Otherwise → English
    """
    if user_id is not None and user_id in user_languages:
        return user_languages[user_id]
    if language_code and language_code.lower().startswith("id"):
        return "id"
    return DEFAULT_LANG


def set_lang(user_id: int, lang: str) -> None:
    if lang not in ("id", "en"):
        lang = DEFAULT_LANG
    user_languages[user_id] = lang


def t(
    lang: str,
    key: str,
    **kwargs: Any,
) -> str:
    """Translate key for given language, with optional format kwargs."""
    bundle = TEXTS.get(lang) or TEXTS[DEFAULT_LANG]
    text = bundle.get(key) or TEXTS[DEFAULT_LANG].get(key) or key
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, ValueError):
            return text
    return text
