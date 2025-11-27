"""
Page - Base class for all UI pages

Single Responsibility: Abstract page lifecycle and navigation.
"""
import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod
from typing import Optional, Any, TYPE_CHECKING

from .page_helpers import PageHelpersMixin

if TYPE_CHECKING:
    from ..web_interface import WebInterface


class Page(PageHelpersMixin, ABC):
    """
    Abstract base class for all pages in SafeHome UI.
    
    All system communication goes through WebInterface.send_message().
    """
    
    _id_counter = 0
    
    def __init__(self, parent: tk.Widget, web_interface: 'WebInterface'):
        self._page_id = self._generate_id()
        self._parent = parent
        self._web_interface = web_interface
        self._frame: Optional[tk.Frame] = None
        self._is_visible = False
    
    @classmethod
    def _generate_id(cls) -> int:
        """Generate unique page ID"""
        cls._id_counter += 1
        return cls._id_counter
    
    @property
    def page_id(self) -> int:
        return self._page_id
    
    @property
    def is_visible(self) -> bool:
        return self._is_visible
    
    def get_frame(self) -> tk.Frame:
        """Get or create the page frame"""
        if self._frame is None:
            self._frame = ttk.Frame(self._parent)
            self._build_ui()
        return self._frame
    
    @abstractmethod
    def _build_ui(self) -> None:
        """Build UI components. Must be implemented by subclasses."""
        pass
    
    def show(self) -> None:
        """Show the page"""
        frame = self.get_frame()
        frame.pack(fill=tk.BOTH, expand=True)
        self._is_visible = True
        self.on_show()
    
    def hide(self) -> None:
        """Hide the page"""
        if self._frame:
            self._frame.pack_forget()
        self._is_visible = False
        self.on_hide()
    
    def on_show(self) -> None:
        """Called when page becomes visible"""
        pass
    
    def on_hide(self) -> None:
        """Called when page is hidden"""
        pass
    
    def refresh(self) -> None:
        """Refresh page content"""
        pass
    
    def send_to_system(self, command: str, **kwargs) -> Any:
        """Send command to System via WebInterface"""
        return self._web_interface.send_message(command, **kwargs)
    
    def navigate_to(self, page_name: str) -> None:
        """Navigate to another page"""
        self._web_interface.show_page(page_name)
