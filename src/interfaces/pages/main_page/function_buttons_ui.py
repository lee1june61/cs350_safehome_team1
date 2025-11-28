import tkinter as tk
from typing import Callable, List

def _create_function_button(
    parent: tk.Frame,
    text: str,
    description: str,
    command: Callable[[], None],
    bg_color: str,
) -> tk.Frame:
    """Create a function button with description."""
    button_frame = tk.Frame(parent, bg="#ffffff")

    button = tk.Button(
        button_frame,
        text=text,
        font=("Arial", 11, "bold"),
        bg=bg_color,
        fg="#ffffff",
        relief=tk.RAISED,
        borderwidth=3,
        command=command,
        cursor="hand2",
        height=2,
    )
    button.pack(fill=tk.X)

    tk.Label(
        button_frame,
        text=description,
        font=("Arial", 8),
        fg="#7f8c8d",
        bg="#ffffff",
        justify=tk.CENTER,
    ).pack(pady=(3, 0))

    return button_frame

def create_function_buttons_section(
    parent_frame: tk.Widget,
    on_security: Callable[[], None],
    on_surveillance: Callable[[], None],
    on_settings: Callable[[], None],
) -> tk.Frame:
    """
    Creates the function buttons section for the control panel.

    Args:
        parent_frame: The parent widget.
        on_security: Callback for the security button.
        on_surveillance: Callback for the surveillance button.
        on_settings: Callback for the settings button.

    Returns:
        The frame containing the function buttons.
    """
    functions_frame = tk.LabelFrame(
        parent_frame,
        text="Main Functions",
        font=("Arial", 11, "bold"),
        bg="#ffffff",
        relief=tk.RIDGE,
        borderwidth=2,
    )
    functions_frame.pack(fill=tk.X, pady=(0, 15))

    _create_function_button(
        functions_frame,
        "🔒 Security",
        "Configure security\nand safety zones",
        on_security,
        "#3498db",
    ).pack(pady=8, padx=10, fill=tk.X)

    _create_function_button(
        functions_frame,
        "📹 Surveillance",
        "View cameras",
        on_surveillance,
        "#9b59b6",
    ).pack(pady=8, padx=10, fill=tk.X)

    _create_function_button(
        functions_frame,
        "⚙️ Settings",
        "System settings",
        on_settings,
        "#95a5a6",
    ).pack(pady=8, padx=10, fill=tk.X)
    
    return functions_frame
