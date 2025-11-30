"""Modal dialog displaying currently selected sensors for zone editing/creation."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable, Iterable, Sequence

from ...utils import sensor_display_name


class SensorSelectionDialog(tk.Toplevel):
    def __init__(
        self,
        parent: tk.Tk,
        title: str,
        description: str,
        on_finish: Callable[[], None],
        on_cancel: Callable[[], None],
    ):
        super().__init__(parent)
        self._on_finish = on_finish
        self._on_cancel = on_cancel
        self.title(title)
        self.resizable(False, False)
        self.transient(parent)
        try:
            self.attributes("-topmost", True)
        except tk.TclError:
            pass

        container = ttk.Frame(self, padding=15)
        container.pack(fill="both", expand=True)

        self._desc_label = ttk.Label(container, text=description, wraplength=320, justify="left")
        self._desc_label.pack(fill="x", pady=(0, 10))

        self._listbox = tk.Listbox(container, height=10, width=42)
        self._listbox.pack(fill="both", expand=True)

        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill="x", pady=(12, 0))

        ttk.Button(btn_frame, text="Finish Selection", command=self._handle_finish).pack(
            side="left", padx=5
        )
        ttk.Button(btn_frame, text="Cancel", command=self._handle_cancel).pack(
            side="right", padx=5
        )

        self.protocol("WM_DELETE_WINDOW", self._handle_cancel)

    def update_selected(self, sensors: Sequence[str]):
        """Refresh the displayed sensor list."""
        self._listbox.delete(0, tk.END)
        if not sensors:
            self._listbox.insert(tk.END, "(No sensors selected)")
            return
        for sensor_id in sorted(sensors):
            self._listbox.insert(tk.END, sensor_display_name(sensor_id))

    def set_description(self, text: str):
        self._desc_label.config(text=text)

    def _handle_finish(self):
        if self._on_finish:
            self._on_finish()

    def _handle_cancel(self):
        if self._on_cancel:
            self._on_cancel()
        self.close()

    def close(self):
        try:
            self.grab_release()
        except tk.TclError:
            pass
        self.destroy()

