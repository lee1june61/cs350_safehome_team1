import tkinter as tk

def create_floor_plan_legend_section(parent_frame: tk.Widget) -> tk.Frame:
    """
    Creates the legend section for the floor plan.

    Args:
        parent_frame: The parent widget.

    Returns:
        The frame containing the legend.
    """
    legend_frame = tk.Frame(parent_frame, bg="#ecf0f1", height=35)
    legend_frame.pack(fill=tk.X, padx=5, pady=5)
    legend_frame.pack_propagate(False)

    tk.Label(
        legend_frame,
        text=(
            "Legend: 🔴 Armed  🟢 Disarmed  |  "
            "🔴 Red: Window Sensor  🔵 Blue: Door Sensor / Motion Sensor  🟣 Purple: Camera"
        ),
        font=("Arial", 9),
        bg="#ecf0f1",
    ).pack(pady=7)
    
    return legend_frame
