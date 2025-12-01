"""Fallback drawing routines when floorplan image is unavailable."""

import tkinter as tk


def draw_fallback_layout(canvas: tk.Canvas, width: int, height: int) -> None:
    """Render a simple layout when no floorplan image exists."""
    canvas.create_rectangle(
        10, 10, width * 0.42, height * 0.45, fill="#fafafa", outline="#555", width=2
    )
    canvas.create_text(
        width * 0.22, height * 0.25, text="DR", font=("Arial", 16, "italic"), fill="#888"
    )

    canvas.create_rectangle(
        10,
        height * 0.45,
        width * 0.42,
        height - 10,
        fill="#fafafa",
        outline="#555",
        width=2,
    )
    canvas.create_text(
        width * 0.22, height * 0.72, text="KIT", font=("Arial", 16, "italic"), fill="#888"
    )

    canvas.create_rectangle(
        width * 0.5,
        10,
        width - 10,
        height - 10,
        fill="#fafafa",
        outline="#555",
        width=2,
    )
    canvas.create_text(
        width * 0.75, height * 0.5, text="LR", font=("Arial", 16, "italic"), fill="#888"
    )

    canvas.create_rectangle(
        width * 0.42,
        height * 0.3,
        width * 0.5,
        height * 0.7,
        fill="#e8e8e8",
        outline="#777",
    )
