"""
WebInterface - Interface between system and user (web browser)
SDS: Sends commands to System, receives responses, draws pages.
"""
import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Optional, TYPE_CHECKING

from .page_registry import PAGE_CLASSES

if TYPE_CHECKING:
    from src.core.system import System
    from .components.page import Page


class WebInterface(tk.Toplevel):
    """Web Interface - Main application window for web browser access."""

    def __init__(self, system: 'System', master=None):
        super().__init__(master)
        self._system = system
        self._pages: Dict[str, 'Page'] = {}
        self._current_page: Optional[str] = None
        self._context: Dict[str, Any] = {}
        self._setup_window()
        self._create_container()
        self.show_page('login')

    def _setup_window(self):
        self.title("SafeHome Web Interface")
        # Extra width prevents right-side panels (e.g., Safety Zones) from clipping
        self.geometry("1040x720")
        self.minsize(960, 620)

    def _create_container(self):
        self._container = ttk.Frame(self)
        self._container.pack(fill='both', expand=True)

    def show_page(self, page_name: str):
        """Show a page by name."""
        # Clear context only when going back to login (logout)
        if page_name == 'login':
            self.clear_context()

        # Hide any currently visible page before showing the next one.
        for page in self._pages.values():
            if page.is_visible:
                page.hide()

        if page_name not in self._pages:
            page_class = PAGE_CLASSES.get(page_name)
            if not page_class:
                print(f"[WebInterface] Unknown page: {page_name}")
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

    def set_context(self, key: str, value: Any):
        """Store context value for sharing between pages."""
        self._context[key] = value

    def get_context(self, key: str, default: Any = None) -> Any:
        """Get context value."""
        return self._context.get(key, default)

    def clear_context(self):
        """Clear all context (on logout)."""
        self._context.clear()

    def clear_security_verification(self):
        """Clear only security verification (when leaving security section)."""
        self._context.pop('security_verified', None)


def run_web_interface(system: 'System', master=None) -> WebInterface:
    """Factory function to create web interface."""
    return WebInterface(system, master)
