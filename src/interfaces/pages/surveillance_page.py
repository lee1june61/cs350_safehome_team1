"""SurveillancePage - Surveillance function main screen"""
import tkinter as tk
from tkinter import ttk
from ..components.page import Page


class SurveillancePage(Page):
    """Surveillance main page"""
    
    def _build_ui(self) -> None:
        self._create_header("Surveillance", back_page='major_function')
        
        content = ttk.Frame(self._frame)
        content.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Status display
        left = ttk.LabelFrame(content, text="Camera Status", padding=15)
        left.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        self._total = ttk.Label(left, text="Total Cameras: -")
        self._total.pack(anchor='w', pady=2)
        self._enabled = ttk.Label(left, text="Enabled: -")
        self._enabled.pack(anchor='w', pady=2)
        self._disabled = ttk.Label(left, text="Disabled: -")
        self._disabled.pack(anchor='w', pady=2)
        self._protected = ttk.Label(left, text="Password Protected: -")
        self._protected.pack(anchor='w', pady=2)
        
        ttk.Separator(left).pack(fill='x', pady=15)
        
        btn_frame = ttk.Frame(left)
        btn_frame.pack()
        ttk.Button(btn_frame, text="Enable All", command=self._enable_all, 
                  width=12).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Disable All", command=self._disable_all, 
                  width=12).pack(side='left', padx=5)
        
        # Navigation
        right = ttk.Frame(content)
        right.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        view_frame = ttk.LabelFrame(right, text="View Cameras", padding=10)
        view_frame.pack(fill='x', pady=(0, 10))
        ttk.Button(view_frame, text="Pick a Camera", 
                  command=lambda: self.navigate_to('camera_list'), width=25).pack(pady=5)
        ttk.Button(view_frame, text="All Cameras (Thumbnails)", 
                  command=lambda: self.navigate_to('thumbnail_view'), width=25).pack(pady=5)
    
    def _enable_all(self) -> None:
        response = self.send_to_system('enable_all_cameras')
        if response.get('success'):
            self._show_message("Success", "All cameras enabled")
            self.refresh()
        else:
            self._show_message("Error", response.get('message', 'Failed'), 'error')
    
    def _disable_all(self) -> None:
        if not self._ask_confirm("Confirm", "Disable all cameras?"):
            return
        response = self.send_to_system('disable_all_cameras')
        if response.get('success'):
            self._show_message("Success", "All cameras disabled")
            self.refresh()
        else:
            self._show_message("Error", response.get('message', 'Failed'), 'error')
    
    def on_show(self) -> None:
        self.refresh()
    
    def refresh(self) -> None:
        response = self.send_to_system('get_cameras')
        if response.get('success'):
            cameras = response.get('data', [])
            total = len(cameras)
            enabled = sum(1 for c in cameras if c.get('enabled'))
            protected = sum(1 for c in cameras if c.get('has_password'))
            
            self._total.config(text=f"Total Cameras: {total}")
            self._enabled.config(text=f"Enabled: {enabled}")
            self._disabled.config(text=f"Disabled: {total - enabled}")
            self._protected.config(text=f"Password Protected: {protected}")
