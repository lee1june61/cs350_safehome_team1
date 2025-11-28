"""UI builder for camera list page."""
import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING
from ...components.floor_plan import FloorPlan

if TYPE_CHECKING:
    from .camera_list_page import CameraListPage


class CameraListUIBuilder:
    """Builds the UI for camera list page."""

    def __init__(self, page: "CameraListPage"):
        self._page = page

    def build(self):
        self._page._create_header("Pick a Camera", back_page="surveillance")
        content = ttk.Frame(self._page._frame)
        content.pack(expand=True, fill="both", padx=20, pady=10)
        content.columnconfigure(0, weight=2)
        content.columnconfigure(1, weight=1)

        self._build_left_panel(content)
        self._build_right_panel(content)

    def _build_left_panel(self, parent):
        left = ttk.LabelFrame(parent, text="Click camera on map", padding=5)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self._page._floorplan = FloorPlan(left, 380, 300)
        self._page._floorplan.set_on_click(self._page._on_map_click)
        self._page._floorplan.create().pack()

    def _build_right_panel(self, parent):
        right = ttk.Frame(parent)
        right.grid(row=0, column=1, sticky="nsew")

        lf = ttk.LabelFrame(right, text="Cameras", padding=5)
        lf.pack(fill="both", expand=True)
        self._page._list = tk.Listbox(lf, font=("Arial", 10), height=10)
        self._page._list.pack(fill="both", expand=True)
        self._page._list.bind("<<ListboxSelect>>", self._page._on_select)

        info = ttk.LabelFrame(right, text="Info", padding=5)
        info.pack(fill="x", pady=5)
        self._page._info = ttk.Label(info, text="Select a camera")
        self._page._info.pack()

        self._page._btn = ttk.Button(right, text="View Camera", command=self._page._view, state="disabled")
        self._page._btn.pack(pady=10)

