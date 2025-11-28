"""ViewLogPage - View intrusion logs (SRS V.2.j)

Displays log of security events:
- Timestamp
- Event type (INTRUSION, ARM, DISARM, PANIC, etc.)
- Details (sensor info, zone info)
"""
import tkinter as tk
from tkinter import ttk
from ..components.page import Page


class ViewLogPage(Page):
    """View intrusion and security event log."""
    
    def _build_ui(self) -> None:
        self._create_header("Security Event Log", back_page='security')
        
        # Main frame
        main = ttk.Frame(self._frame)
        main.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Log table
        log_frame = ttk.LabelFrame(main, text="Event Log", padding=10)
        log_frame.pack(fill='both', expand=True)
        
        # Treeview with columns
        columns = ('timestamp', 'event', 'detail')
        self._tree = ttk.Treeview(log_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        self._tree.heading('timestamp', text='Date/Time')
        self._tree.heading('event', text='Event Type')
        self._tree.heading('detail', text='Details')
        
        self._tree.column('timestamp', width=150, anchor='center')
        self._tree.column('event', width=120, anchor='center')
        self._tree.column('detail', width=350, anchor='w')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(log_frame, orient='vertical', command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)
        
        self._tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Button frame
        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill='x', pady=10)
        
        ttk.Button(btn_frame, text="Refresh", command=self._load, width=12).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Clear Log", command=self._clear_log, width=12).pack(side='left', padx=5)
        
        # Status
        self._status = ttk.Label(main, text="", font=('Arial', 9))
        self._status.pack()
    
    def _load(self) -> None:
        """Load log entries from system."""
        # Clear existing
        for item in self._tree.get_children():
            self._tree.delete(item)
        
        res = self.send_to_system('get_intrusion_log')
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
    
    def _clear_log(self) -> None:
        """Clear the displayed log (not from system)."""
        for item in self._tree.get_children():
            self._tree.delete(item)
        self._status.config(text="Log cleared from display")
    
    def on_show(self) -> None:
        """Called when page is shown."""
        self._load()
