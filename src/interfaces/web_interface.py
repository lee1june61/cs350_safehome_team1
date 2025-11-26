"""
WebInterface - Interface between system and user (web browser)

SDS Design:
- Sends user command to the system (System)
- Receives message from the system (System)  
- Draws pages that are to be seen by the user (Page)
- Responds to button events from pages (Page)
- Passes information from system to page (Page)

IMPORTANT: WebInterface does NOT directly access System's internal components.
All requests go through System.handle_request() and System routes internally.
"""
import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .components.page import Page

from .pages.login_page import LoginPage
from .pages.major_function_page import MajorFunctionPage
from .pages.security_page import SecurityPage
from .pages.safety_zone_page import SafetyZonePage
from .pages.safehome_mode_page import SafeHomeModePage
from .pages.safehome_mode_configure_page import SafeHomeModeConfigurePage
from .pages.configure_system_setting_page import ConfigureSystemSettingPage
from .pages.phone_number_validation_page import PhoneNumberValidationPage
from .pages.surveillance_page import SurveillancePage
from .pages.camera_list_page import CameraListPage
from .pages.single_camera_view_page import SingleCameraViewPage
from .pages.thumbnail_view_page import ThumbnailViewPage
from .pages.view_log_page import ViewLogPage


class WebInterface(tk.Tk):
    """
    Web Interface - Main application window for web browser access.
    
    Responsibilities (from SDS CRC):
    - Respond to button events from pages
    - Draw pages that are to be seen by the user
    - Send message to System
    - Receive message from System
    - Pass information from System to Page
    
    NOTE: This class ONLY communicates with System.
    It does NOT directly access LoginManager, ConfigurationManager, etc.
    """
    
    PAGE_CLASSES = {
        'login': LoginPage,
        'major_function': MajorFunctionPage,
        'security': SecurityPage,
        'safety_zone': SafetyZonePage,
        'safehome_mode': SafeHomeModePage,
        'safehome_mode_configure': SafeHomeModeConfigurePage,
        'configure_system_setting': ConfigureSystemSettingPage,
        'phone_validation': PhoneNumberValidationPage,
        'surveillance': SurveillancePage,
        'camera_list': CameraListPage,
        'single_camera_view': SingleCameraViewPage,
        'thumbnail_view': ThumbnailViewPage,
        'view_log': ViewLogPage,
    }
    
    def __init__(self, system: 'System'):
        """
        Initialize WebInterface.
        
        Args:
            system: System instance - the ONLY component we communicate with
        """
        super().__init__()
        
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
            page_class = self.PAGE_CLASSES.get(page_name)
            if not page_class:
                print(f"Unknown page: {page_name}")
                return
            self._pages[page_name] = page_class(self._container, self)
        
        self._pages[page_name].show()
        self._current_page = page_name
    
    def get_current_page(self) -> Optional[str]:
        return self._current_page
    
    def send_message(self, command: str, **kwargs) -> Dict[str, Any]:
        """
        Send message/command to System and get response.
        
        WebInterface does NOT know about System's internal structure.
        All routing is handled by System.handle_request().
        """
        if not self._system:
            return {'success': False, 'message': 'System not connected'}
        
        return self._system.handle_request(source='web', command=command, **kwargs)
    
    def set_context(self, key: str, value: Any) -> None:
        self._context[key] = value
    
    def get_context(self, key: str, default: Any = None) -> Any:
        return self._context.get(key, default)
    
    def clear_context(self) -> None:
        self._context.clear()


def run_web_interface(system: 'System') -> None:
    """Run the web interface application."""
    app = WebInterface(system)
    app.mainloop()
