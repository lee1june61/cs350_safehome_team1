"""ViewLogPage - Intrusion log viewer"""
import tkinter as tk
from tkinter import ttk
from ..components.page import Page


class ViewLogPage(Page):
    """Intrusion log viewer page"""
    
    def _build_ui(self) -> None:
        header = self._create_header("Intrusion Logs", back_page='security')
        ttk.Button(header, text="Refresh", command=self._load, width=10).pack(side='right')
        
        # Log table
        table_frame = ttk.Frame(self._frame)
        table_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        columns = ('datetime', 'type', 'description')
        self._tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        self._tree.heading('datetime', text='Date/Time')
        self._tree.heading('type', text='Type')
        self._tree.heading('description', text='Description')
        
        self._tree.column('datetime', width=150)
        self._tree.column('type', width=100)
        self._tree.column('description', width=350)
        
        v_scroll = ttk.Scrollbar(table_frame, orient='vertical', command=self._tree.yview)
        h_scroll = ttk.Scrollbar(table_frame, orient='horizontal', command=self._tree.xview)
        self._tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        self._tree.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        self._summary = ttk.Label(self._frame, text="Total logs: -", font=('Arial', 9))
        self._summary.pack(pady=(0, 10))
    
    def _load(self) -> None:
        for item in self._tree.get_children():
            self._tree.delete(item)
        
        response = self.send_to_system('get_intrusion_logs', limit=100)
        
        if response.get('success'):
            logs = response.get('data', [])
            for log in logs:
                self._tree.insert('', tk.END, values=(
                    log.get('datetime', ''),
                    log.get('type', ''),
                    log.get('description', '')
                ))
            self._summary.config(text=f"Total logs: {len(logs)}")
        else:
            self._summary.config(text="Failed to load logs")
    
    def on_show(self) -> None:
        self._load()
