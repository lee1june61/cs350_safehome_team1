import tkinter as tk
from tkinter import ttk
from typing import Tuple

def create_alarm_monitoring_section(parent_frame: ttk.Frame) -> Tuple[tk.StringVar, tk.StringVar]:
    """
    Creates the UI section for alarm and monitoring settings.

    Args:
        parent_frame: The parent ttk.Frame to pack this section into.

    Returns:
        A tuple containing tk.StringVars for (delay_time, monitor_phone).
    """
    alarm_frame = ttk.LabelFrame(parent_frame, text="Alarm & Monitoring Settings", padding=10)
    alarm_frame.pack(fill='x', pady=5)
    
    delay_time = tk.StringVar(value='5')
    monitor_phone = tk.StringVar()
    
    ttk.Label(alarm_frame, text="Alarm Delay Time (minutes):").grid(row=0, column=0, sticky='e', padx=5, pady=2)
    delay_entry = ttk.Entry(alarm_frame, textvariable=delay_time, width=10)
    delay_entry.grid(row=0, column=1, sticky='w', pady=2)
    ttk.Label(alarm_frame, text="(Minimum 5 minutes)", font=('Arial', 8)).grid(row=0, column=2, sticky='w', padx=5)
    
    ttk.Label(alarm_frame, text="Monitoring Service Phone:").grid(row=1, column=0, sticky='e', padx=5, pady=2)
    ttk.Entry(alarm_frame, textvariable=monitor_phone, width=20).grid(row=1, column=1, sticky='w', pady=2)
    
    return delay_time, monitor_phone
