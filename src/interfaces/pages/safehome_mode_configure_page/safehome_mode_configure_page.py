"""SafeHomeModeConfigurePage - Redefine security modes (SRS V.2.i)"""
import tkinter as tk
from tkinter import ttk
from ...components.page import Page
from .left_panel import create_left_panel
from .right_panel import create_right_panel
from .mode_config_manager import ModeConfigManager


class SafeHomeModeConfigurePage(Page):
    """Configure which sensors are active in each SafeHome mode."""

    def _build_ui(self):
        self._create_header("Configure Security Modes", back_page='security')

        content = ttk.Frame(self._frame)
        content.pack(expand=True, fill='both', padx=15, pady=10)
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=2)

        # Create left panel (floor plan)
        self._floorplan, self._sel_info = create_left_panel(
            content, self._on_sensor_click)

        # Mode variable
        self._mode_var = tk.StringVar(value='HOME')

        # Create right panel (mode selection and controls)
        self._mode_desc, self._sensor_list = create_right_panel(
            content,
            self._mode_var,
            load_mode_callback=self._load_mode,
            save_mode_callback=self._save_mode,
            reset_mode_callback=self._reset_mode,
            select_all_callback=self._select_all,
            clear_all_callback=self._clear_all,
        )

        # Initialize manager
        self._manager = ModeConfigManager(
            self, self._floorplan, self._sel_info,
            self._mode_var, self._mode_desc, self._sensor_list)

    def _on_sensor_click(self, dev_id: str, dev_type: str):
        self._manager.on_sensor_click(dev_id, dev_type)

    def _load_mode(self):
        self._manager.load_mode()

    def _save_mode(self):
        self._manager.save_mode()

    def _reset_mode(self):
        self._manager.reset_mode()

    def _select_all(self):
        self._manager.select_all()

    def _clear_all(self):
        self._manager.clear_all()

    def on_show(self):
        self._manager.on_show()
