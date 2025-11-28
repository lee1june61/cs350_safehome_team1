import tkinter as tk
from tkinter import ttk
from typing import Any

class LogManager:
    """
    Manages loading and displaying security event logs.
    """
    def __init__(self, page_instance: Any, treeview: ttk.Treeview, status_label: ttk.Label):
        self._page = page_instance
        self._tree = treeview
        self._status = status_label

    def load_log_entries(self) -> None:
        """Load log entries from system."""
        # Clear existing
        for item in self._tree.get_children():
            self._tree.delete(item)
        
        res = self._page.send_to_system('get_intrusion_log')
        if res.get('success'):
            logs = res.get('data', [])
            for log in logs:
                # Color code by event type
                event = log.get('event', '-')
                tag = 'normal'
                if event in ('INTRUSION', 'PANIC'):
                    tag = 'alert'
                elif event in ('ARM', 'ARM_ZONE'):
                    tag = 'armed'
                elif event in ('DISARM', 'DISARM_ZONE'):
                    tag = 'disarmed'
                
                self._tree.insert('', 'end', values=(
                    log.get('timestamp', '-'),
                    event,
                    log.get('detail', '-')
                ), tags=(tag,))
            
            # Configure tag colors
            self._tree.tag_configure('alert', foreground='red')
            self._tree.tag_configure('armed', foreground='green')
            self._tree.tag_configure('disarmed', foreground='gray')
            
            self._status.config(text=f"Showing {len(logs)} entries")
        else:
            self._status.config(text="Failed to load log")

    def clear_log_display(self) -> None:
        """Clear the displayed log (not from system)."""
        for item in self._tree.get_children():
            self._tree.delete(item)
        self._status.config(text="Log cleared from display")
