"""Enable/disable security action buttons."""

from __future__ import annotations

from typing import Sequence
from tkinter import Button


class ActionButtonController:
    """Applies consistent styling when enabling/disabling buttons."""

    def __init__(self, buttons: Sequence[Button]):
        self._buttons = list(buttons)

    def set_enabled(self, enabled: bool):
        bg = "#2196F3" if enabled else "#607D8B"
        state = "normal" if enabled else "disabled"
        for button in self._buttons:
            button.config(state=state, bg=bg)




