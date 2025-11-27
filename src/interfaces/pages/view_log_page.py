"""ViewLogPage - View intrusion logs (SRS GUI)"""
import tkinter as tk
from tkinter import ttk
from ..components.page import Page


class ViewLogPage(Page):
    """View intrusion log - SRS 'View intrusion log'"""
    
    def _build_ui(self) -> None:
        # Header
        self._create_header("Intrusion Log", back_page='security')
        
        # Log list
        list_frame = ttk.LabelFrame(self._frame, text="Event Log", padding=10)
        list_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Treeview for logs
        columns = ('timestamp', 'event', 'zone')
        self._tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        self._tree.heading('timestamp', text='Timestamp')
        self._tree.heading('event', text='Event')
        self._tree.heading('zone', text='Zone')
        
        self._tree.column('timestamp', width=180)
        self._tree.column('event', width=250)
        self._tree.column('zone', width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)
        
        self._tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Refresh button
        btn_frame = ttk.Frame(self._frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Refresh", command=self._load_logs, width=15).pack()
    
    def _load_logs(self) -> None:
        # Clear existing
        for item in self._tree.get_children():
            self._tree.delete(item)
        
        # Load from system
        response = self.send_to_system('get_intrusion_log')
        if response.get('success'):
            logs = response.get('data', [])
            for log in logs:
                self._tree.insert('', 'end', values=(
                    log.get('timestamp', '-'),
                    log.get('event', '-'),
                    log.get('zone', '-')
                ))
    
    def on_show(self) -> None:
        self._load_logs()
