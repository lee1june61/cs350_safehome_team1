"""
WebInterface - Interface between system and user (web browser)

SDS Design:
- Sends user command to the system (System)
- Receives message from the system (System)  
- Draws pages that are to be seen by the user (Page)
- Responds to button events from pages (Page)
- Passes information from system to page (Page)
"""
import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Optional, TYPE_CHECKING

from .page_registry import PAGE_CLASSES

if TYPE_CHECKING:
    from .components.page import Page


class WebInterface(tk.Toplevel):
    """
    Web Interface - Main application window for web browser access.
    
    Uses tk.Toplevel so it can run alongside ControlPanel.
    NOTE: This class ONLY communicates with System.
    """
    
    PAGE_CLASSES = PAGE_CLASSES  # For backward compatibility
    
    def __init__(self, system: 'System', master=None):
        super().__init__(master)
        self._system = system
        self._pages: Dict[str, 'Page'] = {}
        self._current_page: Optional[str] = None
        self._context: Dict[str, Any] = {}
        
        self._setup_window()
        self._create_container()
        self.show_page('login')
    
    def _setup_window(self) -> None:
        self.title("SafeHome Web Interface")
        self.geometry("900x700")
        self.minsize(800, 600)
    
    def _create_container(self) -> None:
        self._container = ttk.Frame(self)
        self._container.pack(fill='both', expand=True)
    
    def show_page(self, page_name: str) -> None:
        """Show a page by name."""
        if self._current_page and self._current_page in self._pages:
            self._pages[self._current_page].hide()
        
        if page_name not in self._pages:
            page_class = PAGE_CLASSES.get(page_name)
            if not page_class:
                print(f"Unknown page: {page_name}")
                return
            self._pages[page_name] = page_class(self._container, self)
        
        self._pages[page_name].show()
        self._current_page = page_name
    
    def get_current_page(self) -> Optional[str]:
        return self._current_page
    
    def send_message(self, command: str, **kwargs) -> Dict[str, Any]:
        """Send message/command to System and get response."""
        if not self._system:
            return {'success': False, 'message': 'System not connected'}
        return self._system.handle_request(source='web', command=command, **kwargs)
    
    def set_context(self, key: str, value: Any) -> None:
        self._context[key] = value
    
    def get_context(self, key: str, default: Any = None) -> Any:
        return self._context.get(key, default)
    
    def clear_context(self) -> None:
        self._context.clear()


def run_web_interface(system: 'System', master=None) -> WebInterface:
    """Create and return web interface instance."""
    return WebInterface(system, master)
