"""Game mode definitions."""

from __future__ import annotations

from enum import Enum, auto


class GameMode(Enum):
    CLASSIC = "classic"  # actions in group, cards hidden as 🂠🂠
    PRIVATE = "private"  # hole cards only via Inline Mode

    @property
    def label_key(self) -> str:
        return {
            GameMode.CLASSIC: "mode_classic",
            GameMode.PRIVATE: "mode_private",
        }[self]
