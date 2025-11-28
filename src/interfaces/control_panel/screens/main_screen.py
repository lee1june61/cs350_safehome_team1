"""Main screen for Control Panel - BUTTONS ONLY (NO FLOOR PLAN).

Following SRS requirements:
- Control Panel is for LOCAL access only
- Simple button interface (Home/Away/Panic/Code)
- 4-digit password authentication
- Status display (text only)

Reference: SRS Section V.1.a (Log onto system through control panel)
"""
import tkinter as tk
from tkinter import messagebox
from typing import Callable, Optional
from .main_screen_ui.header import create_header
from .main_screen_ui.status_display import create_status_display
from .main_screen_ui.control_buttons import create_control_buttons
from .main_screen_ui.status_bar import create_status_bar


class MainScreen:
    """Main control panel screen with buttons only."""

    def __init__(
        self,
        parent: tk.Widget,
        username: str,
        on_home: Callable[[], None],
        on_away: Callable[[], None],
        on_code: Callable[[], None],
        on_panic: Callable[[], None],
        on_logout: Callable[[], None],
    ):
        self.parent = parent
        self.username = username
        self.on_home = on_home
        self.on_away = on_away
        self.on_code = on_code
        self.on_panic = on_panic
        self.on_logout = on_logout

        self.status_label: Optional[tk.Label] = None
        self.system_status_label: Optional[tk.Label] = None
        self.status_indicator: Optional[tk.Label] = None

    def build(self) -> tk.Frame:
        frame = tk.Frame(self.parent, bg="#ffffff")

        create_header(frame, self.username)

        content = tk.Frame(frame, bg="#ffffff")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        _, self.status_indicator, self.system_status_label = \
            create_status_display(content)

        create_control_buttons(
            content, self.on_home, self.on_away,
            self.on_code, self.on_panic)

        _, self.status_label = create_status_bar(frame, self.on_logout)

        return frame

    def update_system_status(self, armed: bool) -> None:
        if armed:
            self.status_indicator.config(text="🔴", fg="#e74c3c")
            self.system_status_label.config(text="ARMED", fg="#e74c3c")
        else:
            self.status_indicator.config(text="🟢", fg="#27ae60")
            self.system_status_label.config(text="DISARMED", fg="#27ae60")

    def update_status(self, message: str) -> None:
        if self.status_label:
            self.status_label.config(text=message)

    def show_message(self, title: str, message: str, msg_type: str = "info"):
        if msg_type == "info":
            messagebox.showinfo(title, message)
        elif msg_type == "warning":
            messagebox.showwarning(title, message)
        elif msg_type == "error":
            messagebox.showerror(title, message)
