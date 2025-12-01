"""Control panel UI layout builder."""

import tkinter as tk


def create_zone_panel(parent, x_start, y_start, x_w1, x_w2, y_h1):
    """Create security zone panel."""
    zone_frame = tk.Frame(parent, bd=0, relief='flat', bg='white')
    zone_frame.place(x=x_start, y=y_start, width=(x_w1 + x_w2), height=y_h1)
    tk.Label(zone_frame, text="Security Zone", justify='center',
             bg='white', fg='black', font=('Arial', 10, 'bold')).place(x=0, y=0, width=x_w1, height=y_h1)
    display_number = tk.Label(zone_frame, text="1", justify='center',
                              bg='white', fg='black', font=('Arial', 24, 'bold'))
    display_number.place(x=x_w1, y=0, width=x_w2, height=y_h1)
    return display_number


def create_status_panel(parent, x_start, x_w1, x_w2, x_w3, y_start, y_h1):
    """Create status displays."""
    status_frame = tk.Frame(parent, bg='white')
    status_frame.place(x=x_start + x_w1 + x_w2, y=y_start, width=x_w3, height=y_h1)
    display_away = tk.Label(status_frame, text="away", bg='white', fg='light gray')
    display_away.pack(fill='both', expand=True)
    display_stay = tk.Label(status_frame, text="stay", bg='white', fg='light gray')
    display_stay.pack(fill='both', expand=True)
    display_not_ready = tk.Label(status_frame, text="not ready", bg='white', fg='light gray')
    display_not_ready.pack(fill='both', expand=True)
    return display_away, display_stay, display_not_ready


def create_text_display(parent, x_start, y_start, y_h1, x_w1, x_w2, x_w3, y_h2):
    """Create text display area."""
    display_text = tk.Text(parent, height=3, width=27, bg='white', fg='black',
                           font=('Courier', 10), state='disabled', wrap='word',
                           bd=0, relief='flat', highlightthickness=0)
    text_width = x_w1 + x_w2 + x_w3
    text_height = max(40, y_h2 - 10)
    display_text.place(x=x_start, y=y_start + y_h1, width=text_width, height=text_height)
    display_text.lower()
    return display_text


def create_led_panel(parent, x_start, y_start, y_h1, y_h2):
    """Create LED panel."""
    led_frame = tk.Frame(parent)
    led_frame.place(x=30, y=y_start + y_h1 + y_h2, width=230, height=70)
    tk.Label(led_frame, text="armed").grid(row=0, column=0)
    tk.Label(led_frame, text="").grid(row=0, column=1)
    tk.Label(led_frame, text="power").grid(row=0, column=2)
    led_armed = tk.Label(led_frame, bg='light gray', width=8, height=1, bd=2, relief='groove')
    led_armed.grid(row=1, column=0)
    tk.Label(led_frame, text="").grid(row=1, column=1)
    led_power = tk.Label(led_frame, bg='light gray', width=8, height=1, bd=2, relief='groove')
    led_power.grid(row=1, column=2)
    return led_armed, led_power

