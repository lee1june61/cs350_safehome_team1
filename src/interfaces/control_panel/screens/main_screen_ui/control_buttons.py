import tkinter as tk
from typing import Callable
from .button import create_styled_button # Import the shared button creator

def create_control_buttons(
    parent: tk.Frame,
    on_home: Callable[[], None],
    on_away: Callable[[], None],
    on_code: Callable[[], None],
    on_panic: Callable[[], None],
) -> tk.Frame:
    """Create control buttons panel.
    Following SRS: Control Panel has HOME, AWAY, CODE, PANIC buttons
    """
    buttons_frame = tk.LabelFrame(
        parent,
        text="Control Buttons",
        font=("Arial", 14, "bold"),
        bg="#ffffff",
        relief=tk.RIDGE,
        borderwidth=2,
    )
    buttons_frame.pack(fill=tk.BOTH, expand=True)

    button_container = tk.Frame(buttons_frame, bg="#ffffff")
    button_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    row1 = tk.Frame(button_container, bg="#ffffff")
    row1.pack(pady=10)

    create_styled_button(
        row1,
        "🏠 HOME",
        on_home,
        "#27ae60",
    ).pack(side=tk.LEFT, padx=10)

    create_styled_button(
        row1,
        "🚗 AWAY",
        on_away,
        "#f39c12",
    ).pack(side=tk.LEFT, padx=10)

    row2 = tk.Frame(button_container, bg="#ffffff")
    row2.pack(pady=10)

    create_styled_button(
        row2,
        "🔐 CODE",
        on_code,
        "#3498db",
    ).pack(side=tk.LEFT, padx=10)

    create_styled_button(
        row2,
        "🚨 PANIC",
        on_panic,
        "#e74c3c",
    ).pack(side=tk.LEFT, padx=10)

    instructions = tk.Label(
        button_container,
        text=(
            "HOME: Disarm system | AWAY: Arm system\n"
            "CODE: Change password | PANIC: Emergency call"
        ),
        font=("Arial", 9),
        bg="#ffffff",
        fg="#7f8c8d",
        justify=tk.CENTER,
    )
    instructions.pack(pady=20)
    return buttons_frame
