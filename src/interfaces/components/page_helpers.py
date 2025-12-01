"""PageHelpers - Helper methods for UI pages"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Tuple, Optional


class PageHelpersMixin:
    """Mixin providing common UI helper methods"""
    
    def _create_header(self, title: str, back_page: Optional[str] = None) -> ttk.Frame:
        header = ttk.Frame(self._frame)
        header.pack(fill='x', padx=20, pady=20)
        back_btn = None
        if back_page:
            back_btn = ttk.Button(header, text="← Back", command=lambda: self.navigate_to(back_page), width=10)
            back_btn.pack(side='left')
        ttk.Label(header, text=title, font=('Arial', 20, 'bold')).pack(side='left', padx=20 if back_page else 0)
        header.back_button = back_btn
        return header
    
    def _create_entry(self, parent=None, show=None, width=20) -> Tuple[ttk.Entry, tk.StringVar]:
        parent = parent or self._frame
        var = tk.StringVar()
        return ttk.Entry(parent, textvariable=var, show=show, width=width), var
    
    def _show_message(self, title: str, message: str, msg_type: str = 'info') -> None:
        getattr(messagebox, f'show{msg_type}' if msg_type != 'info' else 'showinfo')(title, message)
    
    def _ask_confirm(self, title: str, message: str) -> bool:
        return messagebox.askyesno(title, message)
