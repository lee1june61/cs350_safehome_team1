"""DeviceControlPanelAbstract - Control Panel GUI from TA (virtual_device_v4)"""

import tkinter as tk
from abc import ABC, abstractmethod
from .control_panel_ui_layout import (
    create_zone_panel,
    create_status_panel,
    create_text_display,
    create_led_panel,
)
from .control_panel_buttons import create_button_panel
from .control_panel_buttons_base import ControlPanelButtonCallbacks


class DeviceControlPanelAbstract(ControlPanelButtonCallbacks, tk.Toplevel, ABC):
    """Abstract Control Panel GUI."""

    def __init__(self, master=None):
        tk.Toplevel.__init__(self, master=master)
        self.title("Control Panel")
        self.geometry("505x300")
        self.resizable(False, False)
        self.short_message1 = ""
        self.short_message2 = ""
        x_start, y_start, x_w1, x_w2, x_w3, y_h1, y_h2 = 15, 15, 100, 40, 80, 90, 70
        self.display_number = create_zone_panel(
            self, x_start, y_start, x_w1, x_w2, y_h1
        )
        self.display_away, self.display_stay, self.display_not_ready = (
            create_status_panel(self, x_start, x_w1, x_w2, x_w3, y_start, y_h1)
        )
        self.display_text = create_text_display(
            self, x_start, y_start, y_h1, x_w1, x_w2, x_w3, y_h2
        )
        self._update_display_text()
        callbacks = {
            "button1": self.button1,
            "button2": self.button2,
            "button3": self.button3,
            "button4": self.button4,
            "button5": self.button5,
            "button6": self.button6,
            "button7": self.button7,
            "button8": self.button8,
            "button9": self.button9,
            "button_star": self.button_star,
            "button0": self.button0,
            "button_sharp": self.button_sharp,
        }
        create_button_panel(self, callbacks)
        self.led_armed, self.led_power = create_led_panel(
            self, x_start, y_start, y_h1, y_h2
        )

    def _update_display_text(self):
        self.display_text.config(state="normal")
        self.display_text.delete("1.0", tk.END)
        self.display_text.insert(
            "1.0", f"\n{self.short_message1}\n{self.short_message2}"
        )
        self.display_text.config(state="disabled")

    def set_security_zone_number(self, num: int):
        self.display_number.config(text=str(num))

    def set_display_away(self, on: bool):
        self.display_away.config(fg="black" if on else "light gray")

    def set_display_stay(self, on: bool):
        self.display_stay.config(fg="black" if on else "light gray")

    def set_display_not_ready(self, on: bool):
        self.display_not_ready.config(fg="black" if on else "light gray")

    def set_display_short_message1(self, message: str):
        self.short_message1 = message
        self._update_display_text()

    def set_display_short_message2(self, message: str):
        self.short_message2 = message
        self._update_display_text()

    def set_armed_led(self, on: bool):
        self.led_armed.config(bg="red" if on else "light gray")

    def set_powered_led(self, on: bool):
        self.led_power.config(bg="green" if on else "light gray")
