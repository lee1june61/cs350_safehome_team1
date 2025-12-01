import tkinter as tk
from tkinter import messagebox, ttk
from typing import Any, Callable

def reset_to_defaults(
    page_instance: Any,
    delay_time_var: tk.StringVar,
    monitor_phone_var: tk.StringVar,
    status_label: ttk.Label,
    clear_password_fields_func: Callable[[], None]
) -> None:
    """
    Handles resetting all system settings to default values.
    """
    if messagebox.askyesno("Confirm", "Reset all settings to defaults?"):
        delay_time_var.set('5')
        monitor_phone_var.set('911')
        clear_password_fields_func()
        status_label.config(text="Reset to defaults (not saved yet)", foreground='orange')
