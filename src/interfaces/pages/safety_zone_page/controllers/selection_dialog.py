"""Dialog controller for sensor selection."""

from __future__ import annotations

from typing import Optional, Callable, TYPE_CHECKING

from ..sensor_selection_dialog import SensorSelectionDialog

if TYPE_CHECKING:  # pragma: no cover
    from ...components.page import Page


class SelectionDialogController:
    """Opens and updates the sensor selection dialog."""

    def __init__(self, page: "Page"):
        self._page = page
        self._dialog: Optional[SensorSelectionDialog] = None

    def open(self, title: str, description: str, on_finish: Callable, on_cancel: Callable, selected: list[str]):
        parent = self._page.get_frame().winfo_toplevel()
        self.close()
        self._dialog = SensorSelectionDialog(
            parent=parent,
            title=title,
            description=description,
            on_finish=on_finish,
            on_cancel=on_cancel,
        )
        self._dialog.update_selected(selected)

    def update(self, selected: list[str]):
        if self._dialog:
            self._dialog.update_selected(selected)

    def close(self):
        if self._dialog:
            self._dialog.close()
            self._dialog = None





