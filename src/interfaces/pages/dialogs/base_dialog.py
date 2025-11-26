"""BaseDialog - Base class for all dialogs"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any


class BaseDialog(tk.Toplevel):
    """Base class for all dialog windows"""
    
    def __init__(self, parent: tk.Widget, title: str, width: int = 400, height: int = 300):
        super().__init__(parent)
        
        self.result: Any = None
        
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Center on parent
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() - width) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - height) // 2
        self.geometry(f"+{x}+{y}")
    
    def show(self) -> Any:
        self.wait_window()
        return self.result
    
    def _on_ok(self) -> None:
        self.result = True
        self.destroy()
    
    def _on_cancel(self) -> None:
        self.result = False
        self.destroy()
    
    def _show_error(self, message: str) -> None:
        messagebox.showerror("Error", message, parent=self)
    
    def _show_info(self, message: str) -> None:
        messagebox.showinfo("Info", message, parent=self)
