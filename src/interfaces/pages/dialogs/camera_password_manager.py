import tkinter as tk
from tkinter import messagebox
from typing import Dict, Any, Optional

class CameraPasswordManager:
    """
    Manages the logic for setting and deleting camera passwords.
    """
    def __init__(self, dialog_instance: Any, web_interface: Any, camera: Dict, mode: str):
        self._dialog = dialog_instance
        self._web_interface = web_interface
        self._camera = camera
        self._mode = mode

        # StringVars will be passed from the dialog UI
        self._old_var: Optional[tk.StringVar] = None
        self._new_var: Optional[tk.StringVar] = None
        self._confirm_var: Optional[tk.StringVar] = None
        self._pw_var: Optional[tk.StringVar] = None

    def set_string_vars(self, old_var: Optional[tk.StringVar], new_var: Optional[tk.StringVar], confirm_var: Optional[tk.StringVar], pw_var: Optional[tk.StringVar]):
        self._old_var = old_var
        self._new_var = new_var
        self._confirm_var = confirm_var
        self._pw_var = pw_var

    def handle_set_password(self) -> None:
        if not self._new_var or not self._confirm_var:
            self._dialog._show_error("Password fields not initialized.")
            return

        old_pw = self._old_var.get() if self._old_var else None
        new_pw = self._new_var.get()
        confirm = self._confirm_var.get()
        
        if len(new_pw) < 4:
            self._dialog._show_error("Password must be at least 4 characters")
            return
        if new_pw != confirm:
            self._dialog._show_error("Passwords do not match")
            return
        
        response = self._web_interface.send_message('set_camera_password',
                                                    camera_id=self._camera['id'],
                                                    old_password=old_pw,
                                                    new_password=new_pw)
        
        if response.get('success'):
            self._dialog._show_info("Password set successfully")
            self._dialog._on_ok()
        else:
            self._dialog._show_error(response.get('message', 'Failed'))

    def handle_delete_password(self) -> None:
        if not self._pw_var:
            self._dialog._show_error("Password field not initialized.")
            return

        password = self._pw_var.get()
        if not password:
            self._dialog._show_error("Enter current password")
            return
        
        response = self._web_interface.send_message('delete_camera_password',
                                                    camera_id=self._camera['id'],
                                                    password=password)
        
        if response.get('success'):
            self._dialog._show_info("Password deleted")
            self._dialog._on_ok()
        else:
            self._dialog._show_error(response.get('message', 'Failed'))
