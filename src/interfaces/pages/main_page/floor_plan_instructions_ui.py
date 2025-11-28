import tkinter as tk

def create_floor_plan_instructions_section(parent_frame: tk.Widget) -> tk.Label:
    """
    Creates the instructions section for the floor plan.

    Args:
        parent_frame: The parent widget.

    Returns:
        The tk.Label widget for the instructions.
    """
    instructions = tk.Label(
        parent_frame,
        text="Click on device icons to view details or control them",
        font=("Arial", 9, "italic"),
        bg="#ffffff",
        fg="#7f8c8d",
    )
    instructions.pack(pady=5)
    return instructions
