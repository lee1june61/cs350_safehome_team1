"""
Page - Base class for all UI pages

SDS Design:
- Superclass of classes that represent various pages shown to the homeowner
- Each page has a unique id and draws its own UI page
- Collaborates with: FloorPlan, DeviceIcon, Button, Label, Textbox

NOTE: Pages communicate with System ONLY through WebInterface.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod
from typing import Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..web_interface import WebInterface


class Page(ABC):
    """
    Abstract base class for all pages in SafeHome UI.
    
    All system communication goes through WebInterface.send_message().
    """
    
    _id_counter = 0
    
    def __init__(self, parent: tk.Widget, web_interface: 'WebInterface'):
        self._page_id = Page._generate_id()
        self._parent = parent
        self._web_interface = web_interface
        self._frame: Optional[tk.Frame] = None
        self._is_visible = False
    
    @classmethod
    def _generate_id(cls) -> int:
        cls._id_counter += 1
        return cls._id_counter
    
    @property
    def page_id(self) -> int:
        return self._page_id
    
    @property
    def is_visible(self) -> bool:
        return self._is_visible
    
    def get_frame(self) -> tk.Frame:
        if self._frame is None:
            self._frame = ttk.Frame(self._parent)
            self._build_ui()
        return self._frame
    
    @abstractmethod
    def _build_ui(self) -> None:
        """Build the UI components. Must be implemented by subclasses."""
        pass
    
    def show(self) -> None:
        frame = self.get_frame()
        frame.pack(fill=tk.BOTH, expand=True)
        self._is_visible = True
        self.on_show()
    
    def hide(self) -> None:
        if self._frame:
            self._frame.pack_forget()
        self._is_visible = False
        self.on_hide()
    
    def on_show(self) -> None:
        """Called when page becomes visible."""
        pass
    
    def on_hide(self) -> None:
        """Called when page is hidden."""
        pass
    
    def refresh(self) -> None:
        """Refresh page content."""
        pass
    
    def send_to_system(self, command: str, **kwargs) -> Any:
        """Send command to System via WebInterface."""
        return self._web_interface.send_message(command, **kwargs)
    
    def navigate_to(self, page_name: str) -> None:
        """Navigate to another page."""
        self._web_interface.show_page(page_name)
    
    def _create_header(self, title: str, back_page: Optional[str] = None) -> ttk.Frame:
        """Create standard page header"""
        header = ttk.Frame(self._frame)
        header.pack(fill='x', padx=20, pady=20)
        
        if back_page:
            ttk.Button(header, text="← Back", 
                      command=lambda: self.navigate_to(back_page), 
                      width=10).pack(side='left')
        
        ttk.Label(header, text=title, 
                 font=('Arial', 20, 'bold')).pack(side='left', padx=20 if back_page else 0)
        return header
    
    def _create_entry(self, parent=None, show=None, width=20):
        """Create entry with StringVar"""
        parent = parent or self._frame
        var = tk.StringVar()
        entry = ttk.Entry(parent, textvariable=var, show=show, width=width)
        return entry, var
    
    def _show_message(self, title: str, message: str, msg_type: str = 'info') -> None:
        if msg_type == 'info':
            messagebox.showinfo(title, message)
        elif msg_type == 'error':
            messagebox.showerror(title, message)
        elif msg_type == 'warning':
            messagebox.showwarning(title, message)
    
    def _ask_confirm(self, title: str, message: str) -> bool:
        return messagebox.askyesno(title, message)
