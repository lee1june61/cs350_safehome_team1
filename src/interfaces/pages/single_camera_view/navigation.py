"""Back navigation helpers for SingleCameraViewPage."""
from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from tkinter import ttk
    from .single_camera_view_page import SingleCameraViewPage


class BackNavigation:
    """Keep the back button wired to the most recent origin page."""

    def __init__(self, page: "SingleCameraViewPage", default_target: str = "camera_list"):
        self._page = page
        self._default_target = default_target
        self._button: Optional["ttk.Button"] = None

    def register_button(self, button: Optional["ttk.Button"]) -> None:
        self._button = button
        self.apply()

    def apply(self) -> None:
        target = self._page._web_interface.get_context(
            "camera_back_page", self._default_target
        ) or self._default_target
        if self._button:
            self._button.configure(
                command=lambda dest=target: self._page.navigate_to(dest)
            )




