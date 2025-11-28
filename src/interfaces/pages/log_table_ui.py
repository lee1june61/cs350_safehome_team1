import tkinter as tk
from tkinter import ttk
from typing import Tuple

def create_log_table_section(parent_frame: ttk.Frame) -> ttk.Treeview:
    """
    Creates the UI section for displaying the event log in a Treeview.

    Args:
        parent_frame: The parent ttk.Frame to pack this section into.

    Returns:
        The ttk.Treeview widget for the log.
    """
    log_frame = ttk.LabelFrame(parent_frame, text="Event Log", padding=10)
    log_frame.pack(fill='both', expand=True)
    
    columns = ('timestamp', 'event', 'detail')
    tree = ttk.Treeview(log_frame, columns=columns, show='headings', height=15)
    
    tree.heading('timestamp', text='Date/Time')
    tree.heading('event', text='Event Type')
    tree.heading('detail', text='Details')
    
    tree.column('timestamp', width=150, anchor='center')
    tree.column('event', width=120, anchor='center')
    tree.column('detail', width=350, anchor='w')
    
    scrollbar = ttk.Scrollbar(log_frame, orient='vertical', command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
    
    return tree
