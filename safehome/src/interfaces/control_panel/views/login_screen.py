"""Login screen view."""

import tkinter as tk
from .base_screen import BaseScreen
from ..config.ui_config import UIConfig
from ..utils.ui_helpers import create_keypad


class LoginScreen(BaseScreen):
    """Login screen for password entry.

    Following LoginInterface and LoginManager from SDS.
    """

    def __init__(self, parent: tk.Widget, on_submit, on_keypad_press):
        """Initialize login screen.

        Args:
            parent: Parent widget
            on_submit: Callback for login submission
            on_keypad_press: Callback for keypad button press
        """
        super().__init__(parent)
        self.on_submit = on_submit
        self.on_keypad_press = on_keypad_press
        self.password_var = tk.StringVar()

    def build(self) -> tk.Frame:
        """Build login screen."""
        frame = tk.Frame(self.parent, bg=UIConfig.COLOR_WHITE)

        # Header
        header = tk.Frame(frame, bg=UIConfig.COLOR_PRIMARY, height=100)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="SafeHome Security System",
            font=UIConfig.FONT_SUBTITLE,
            fg=UIConfig.COLOR_WHITE,
            bg=UIConfig.COLOR_PRIMARY,
        ).pack(pady=15)

        # Login form
        login_frame = tk.Frame(frame, bg=UIConfig.COLOR_WHITE)
        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Title
        tk.Label(
            login_frame,
            text="Enter Password (4 digits)",
            font=("Arial", 16),
            bg=UIConfig.COLOR_WHITE,
        ).pack(pady=20)

        # Password display
        tk.Entry(
            login_frame,
            textvariable=self.password_var,
            font=UIConfig.FONT_PASSWORD,
            justify="center",
            show="●",
            width=10,
            state="readonly",
        ).pack(pady=10)

        # Keypad
        keypad = create_keypad(login_frame, self._handle_keypad_press)
        keypad.pack(pady=20)

        return frame

    def _handle_keypad_press(self, key: str):
        """Handle keypad button press.

        Args:
            key: Key that was pressed
        """
        if key == "C":
            self.clear_password()
        elif key == "✓":
            self.on_submit(self.password_var.get())
        else:
            self.on_keypad_press(key)
            if len(self.password_var.get()) < UIConfig.PASSWORD_LENGTH:
                self.password_var.set(self.password_var.get() + key)

    def clear_password(self):
        """Clear password field."""
        self.password_var.set("")

    def get_password(self) -> str:
        """Get entered password."""
        return self.password_var.get()
