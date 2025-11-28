"""
Control Panel component for the Main Page.
"""
import tkinter as tk
from typing import Callable

from .system_status_ui import create_system_status_section
from .function_buttons_ui import create_function_buttons_section


def create_control_panel(
    parent: tk.Widget,
    on_security: Callable[[], None],
    on_surveillance: Callable[[], None],
    on_settings: Callable[[], None],
) -> (tk.Frame, tk.Label):
    """Create the control panel with function buttons.

    Args:
        parent: The parent widget.
        on_security: Callback for the security button.
        on_surveillance: Callback for the surveillance button.
        on_settings: Callback for the settings button.

    Returns:
        A tuple containing the control panel frame and the system mode label.
    """
    panel = tk.Frame(parent, bg="#ffffff", width=250)
    panel.pack_propagate(False)

    _, system_mode_label = create_system_status_section(panel)

    create_function_buttons_section(
        panel, on_security, on_surveillance, on_settings
    )

    return panel, system_mode_label

