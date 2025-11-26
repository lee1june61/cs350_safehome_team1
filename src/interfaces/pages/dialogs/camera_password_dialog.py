"""CameraPasswordDialog - Set/Delete camera password dialog"""
import tkinter as tk
from tkinter import ttk
from typing import Dict
from .base_dialog import BaseDialog


class CameraPasswordDialog(BaseDialog):
    """Dialog for setting or deleting camera password"""
    
    def __init__(self, parent: tk.Widget, web_interface, camera: Dict, mode: str = 'set'):
        title = 'Set Camera Password' if mode == 'set' else 'Delete Camera Password'
        height = 280 if mode == 'set' else 180
        super().__init__(parent, title, 380, height)
        
        self._web_interface = web_interface
        self._camera = camera
        self._mode = mode
        
        self._build_ui()
    
    def _build_ui(self) -> None:
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text=f"Camera: {self._camera['name']}", 
                 font=('Arial', 11, 'bold')).pack(pady=(0, 15))
        
        if self._mode == 'set':
            if self._camera.get('has_password'):
                ttk.Label(frame, text="Current Password:").pack(anchor='w')
                self._old_var = tk.StringVar()
                ttk.Entry(frame, textvariable=self._old_var, show='*', width=30).pack(pady=(5, 10))
            else:
                self._old_var = None
            
            ttk.Label(frame, text="New Password (min 4 chars):").pack(anchor='w')
            self._new_var = tk.StringVar()
            ttk.Entry(frame, textvariable=self._new_var, show='*', width=30).pack(pady=(5, 10))
            
            ttk.Label(frame, text="Confirm Password:").pack(anchor='w')
            self._confirm_var = tk.StringVar()
            ttk.Entry(frame, textvariable=self._confirm_var, show='*', width=30).pack(pady=(5, 15))
            
            btn_frame = ttk.Frame(frame)
            btn_frame.pack()
            ttk.Button(btn_frame, text="Set", command=self._set, width=12).pack(side='left', padx=5)
            ttk.Button(btn_frame, text="Cancel", command=self._on_cancel, width=12).pack(side='left', padx=5)
        else:
            ttk.Label(frame, text="Enter current password to delete:").pack(anchor='w')
            self._pw_var = tk.StringVar()
            ttk.Entry(frame, textvariable=self._pw_var, show='*', width=30).pack(pady=(5, 15))
            
            btn_frame = ttk.Frame(frame)
            btn_frame.pack()
            ttk.Button(btn_frame, text="Delete", command=self._delete, width=12).pack(side='left', padx=5)
            ttk.Button(btn_frame, text="Cancel", command=self._on_cancel, width=12).pack(side='left', padx=5)
    
    def _set(self) -> None:
        old_pw = self._old_var.get() if self._old_var else None
        new_pw = self._new_var.get()
        confirm = self._confirm_var.get()
        
        if len(new_pw) < 4:
            return self._show_error("Password must be at least 4 characters")
        if new_pw != confirm:
            return self._show_error("Passwords do not match")
        
        response = self._web_interface.send_message('set_camera_password',
                                                    camera_id=self._camera['id'],
                                                    old_password=old_pw,
                                                    new_password=new_pw)
        
        if response.get('success'):
            self._show_info("Password set successfully")
            self._on_ok()
        else:
            self._show_error(response.get('message', 'Failed'))
    
    def _delete(self) -> None:
        password = self._pw_var.get()
        if not password:
            return self._show_error("Enter current password")
        
        response = self._web_interface.send_message('delete_camera_password',
                                                    camera_id=self._camera['id'],
                                                    password=password)
        
        if response.get('success'):
            self._show_info("Password deleted")
            self._on_ok()
        else:
            self._show_error(response.get('message', 'Failed'))
