"""
LoginPage - Web login (SRS V.1.b: 2-level password, 3 attempts)
Refactored to coordinate UI components and a logic manager.
"""
import tkinter as tk
from tkinter import ttk
from src.interfaces.components.page import Page
from .login_form import create_login_form
from .messages import create_message_display
from .login_manager import LoginManager


class LoginPage(Page):
    """Login with UserID + 2 passwords. Lock after 3 failures."""
    
    def __init__(self, parent, web_interface):
        # Initialize string variables for form inputs
        self._user = tk.StringVar()
        self._pw1 = tk.StringVar()
        self._pw2 = tk.StringVar()
        
        super().__init__(parent, web_interface)
    
    def _build_ui(self):
        c = ttk.Frame(self._frame)
        c.place(relx=0.5, rely=0.5, anchor='center')
        ttk.Label(c, text="SafeHome Login", font=('Arial', 24, 'bold')).pack(pady=20)
        
        # Create form and message display
        login_btn = create_login_form(c, self._login, self._user, self._pw1, self._pw2)
        status_msg, _ = create_message_display(c)
        
        # Initialize LoginManager
        self._manager = LoginManager(self, self._user, self._pw1, self._pw2, login_btn, status_msg)
    
    # Delegate login action to manager
    def _login(self):
        self._manager.login()
    
    def on_show(self):
        # Delegate on_show to manager
        self._manager.on_show()
        # Clear input fields
        self._user.set('')
        self._pw1.set('')
        self._pw2.set('')
