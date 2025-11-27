"""LoginPage - SRS GUI based login screen"""
import tkinter as tk
from tkinter import ttk
from ..components.page import Page


class LoginPage(Page):
    """Login page - SRS Section II GUI"""
    
    def _build_ui(self) -> None:
        # Center container
        center = ttk.Frame(self._frame)
        center.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title
        ttk.Label(center, text="SafeHome", font=('Arial', 32, 'bold')).pack(pady=10)
        ttk.Label(center, text="Security System", font=('Arial', 14)).pack(pady=(0, 30))
        
        # Login form
        form = ttk.LabelFrame(center, text="Login", padding=20)
        form.pack(padx=20, pady=10)
        
        # User ID
        ttk.Label(form, text="User ID:").grid(row=0, column=0, sticky='e', pady=8)
        self._user_var = tk.StringVar()
        self._user_entry = ttk.Entry(form, textvariable=self._user_var, width=30)
        self._user_entry.grid(row=0, column=1, padx=10, pady=8)
        
        # Password 1 (8 characters)
        ttk.Label(form, text="Password 1:").grid(row=1, column=0, sticky='e', pady=8)
        self._pw1_var = tk.StringVar()
        self._pw1_entry = ttk.Entry(form, textvariable=self._pw1_var, show='*', width=30)
        self._pw1_entry.grid(row=1, column=1, padx=10, pady=8)
        
        # Password 2 (8 characters)  
        ttk.Label(form, text="Password 2:").grid(row=2, column=0, sticky='e', pady=8)
        self._pw2_var = tk.StringVar()
        self._pw2_entry = ttk.Entry(form, textvariable=self._pw2_var, show='*', width=30)
        self._pw2_entry.grid(row=2, column=1, padx=10, pady=8)
        
        # Login button
        ttk.Button(form, text="Login", command=self._login, width=20).grid(
            row=3, column=0, columnspan=2, pady=20)
        
        # Status message
        self._status = ttk.Label(center, text="", foreground='red')
        self._status.pack(pady=10)
        
        # Help text
        ttk.Label(center, text="Default: admin / password / password",
                 foreground='gray').pack(pady=5)
        
        # Bind Enter key
        self._pw2_entry.bind('<Return>', lambda e: self._login())
    
    def _login(self) -> None:
        user = self._user_var.get().strip()
        pw1 = self._pw1_var.get()
        pw2 = self._pw2_var.get()
        
        if not user:
            self._status.config(text="Please enter User ID")
            return
        
        if len(pw1) < 1 or len(pw2) < 1:
            self._status.config(text="Please enter both passwords")
            return
        
        # Send login request
        response = self.send_to_system('login_web', 
                                       user_id=user, password1=pw1, password2=pw2)
        
        if response.get('success'):
            self._clear()
            self.navigate_to('major_function')
        else:
            self._status.config(text=response.get('message', 'Login failed'))
    
    def _clear(self) -> None:
        self._user_var.set('')
        self._pw1_var.set('')
        self._pw2_var.set('')
        self._status.config(text='')
    
    def on_show(self) -> None:
        self._user_entry.focus_set()
