"""Control panel button layout builder."""

import tkinter as tk
from tkinter import Button


def create_button_panel(parent, callbacks):
    """Create button panel with all buttons."""
    button_frame = tk.Frame(parent)
    button_frame.place(x=300, y=6, width=240, height=300)
    
    # Row 0: Labels (match legacy hardware markings)
    tk.Label(button_frame, text="     on").grid(row=0, column=0)
    tk.Label(button_frame, text="").grid(row=0, column=1)
    tk.Label(button_frame, text="    off").grid(row=0, column=2)
    tk.Label(button_frame, text="").grid(row=0, column=3)
    tk.Label(button_frame, text="  reset").grid(row=0, column=4)
    
    # Row 1: 1, 2, 3
    Button(button_frame, text="1", bg='white', command=callbacks['button1'], width=3).grid(row=1, column=0)
    tk.Label(button_frame, text="").grid(row=1, column=1)
    Button(button_frame, text="2", bg='white', command=callbacks['button2'], width=3).grid(row=1, column=2)
    tk.Label(button_frame, text="").grid(row=1, column=3)
    Button(button_frame, text="3", bg='white', command=callbacks['button3'], width=3).grid(row=1, column=4)
    
    # Row 2: Spacer row
    for i in range(5):
        tk.Label(button_frame, text="").grid(row=2, column=i)
    
    # Row 3: 4, 5, 6
    Button(button_frame, text="4", bg='white', command=callbacks['button4'], width=3).grid(row=3, column=0)
    tk.Label(button_frame, text="").grid(row=3, column=1)
    Button(button_frame, text="5", bg='white', command=callbacks['button5'], width=3).grid(row=3, column=2)
    tk.Label(button_frame, text="").grid(row=3, column=3)
    Button(button_frame, text="6", bg='white', command=callbacks['button6'], width=3).grid(row=3, column=4)
    
    # Row 4: Labels
    tk.Label(button_frame, text="  away").grid(row=4, column=0)
    tk.Label(button_frame, text="").grid(row=4, column=1)
    tk.Label(button_frame, text="   stay").grid(row=4, column=2)
    tk.Label(button_frame, text="").grid(row=4, column=3)
    tk.Label(button_frame, text="  code").grid(row=4, column=4)
    
    # Row 5: 7, 8, 9
    Button(button_frame, text="7", bg='white', command=callbacks['button7'], width=3).grid(row=5, column=0)
    tk.Label(button_frame, text="").grid(row=5, column=1)
    Button(button_frame, text="8", bg='white', command=callbacks['button8'], width=3).grid(row=5, column=2)
    tk.Label(button_frame, text="").grid(row=5, column=3)
    Button(button_frame, text="9", bg='white', command=callbacks['button9'], width=3).grid(row=5, column=4)
    
    # Row 6: Empty
    for i in range(5):
        tk.Label(button_frame, text="").grid(row=6, column=i)
    
    # Row 7: *, 0, #
    Button(button_frame, text="*", bg='white', command=callbacks['button_star'], width=3).grid(row=7, column=0)
    tk.Label(button_frame, text="").grid(row=7, column=1)
    Button(button_frame, text="0", bg='white', command=callbacks['button0'], width=3).grid(row=7, column=2)
    tk.Label(button_frame, text="").grid(row=7, column=3)
    Button(button_frame, text="#", bg='white', command=callbacks['button_sharp'], width=3).grid(row=7, column=4)
    
    # Row 8: Panic labels
    tk.Label(button_frame, text="(panic)").grid(row=8, column=0)
    tk.Label(button_frame, text="").grid(row=8, column=1)
    tk.Label(button_frame, text="").grid(row=8, column=2)
    tk.Label(button_frame, text="").grid(row=8, column=3)
    tk.Label(button_frame, text="(panic)").grid(row=8, column=4)
    
    return button_frame

