"""LoginPage - Login screen for web interface"""
import tkinter as tk
from tkinter import ttk
from ..components.page import Page


class LoginPage(Page):
    """Login page for web interface authentication"""
    
    def _build_ui(self) -> None:
        center = ttk.Frame(self._frame)
        center.place(relx=0.5, rely=0.5, anchor='center')
        
        ttk.Label(center, text="SafeHome", font=('Arial', 28, 'bold')).pack(pady=(0, 5))
        ttk.Label(center, text="Web Interface", font=('Arial', 14)).pack(pady=(0, 30))
        
        form = ttk.LabelFrame(center, text="Login", padding=20)
        form.pack()
        
        ttk.Label(form, text="User ID:").grid(row=0, column=0, sticky='w', pady=5)
        self._user_entry, self._user_var = self._create_entry(form, width=25)
        self._user_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(form, text="Password 1 (8 chars):").grid(row=1, column=0, sticky='w', pady=5)
        self._pw1_entry, self._pw1_var = self._create_entry(form, show='*', width=25)
        self._pw1_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(form, text="Password 2 (8 chars):").grid(row=2, column=0, sticky='w', pady=5)
        self._pw2_entry, self._pw2_var = self._create_entry(form, show='*', width=25)
        self._pw2_entry.grid(row=2, column=1, pady=5, padx=(10, 0))
        
        ttk.Button(form, text="Login", command=self._handle_login, 
                  width=20).grid(row=3, column=0, columnspan=2, pady=(20, 0))
        
        self._status = ttk.Label(center, text="", foreground='red')
        self._status.pack(pady=(15, 0))
        
        ttk.Label(center, text="Default: admin / password / password",
                 font=('Arial', 9, 'italic'), foreground='gray').pack(pady=(10, 0))
        
        self._pw2_entry.bind('<Return>', lambda e: self._handle_login())
    
    def _handle_login(self) -> None:
        user = self._user_var.get()
        pw1, pw2 = self._pw1_var.get(), self._pw2_var.get()
        
        if not user:
            self._status.config(text="User ID required")
            return
        if len(pw1) != 8 or len(pw2) != 8:
            self._status.config(text="Passwords must be 8 characters")
            return
        
        response = self.send_to_system('login_web', user_id=user, password1=pw1, password2=pw2)
        
        if response.get('success'):
            self._clear_form()
            self.navigate_to('major_function')
        else:
            self._status.config(text=response.get('message', 'Login failed'))
            if response.get('attempts_remaining', 1) == 0:
                self._disable_form()
    
    def _clear_form(self) -> None:
        self._user_var.set('')
        self._pw1_var.set('')
        self._pw2_var.set('')
        self._status.config(text='')
    
    def _disable_form(self) -> None:
        for e in [self._user_entry, self._pw1_entry, self._pw2_entry]:
            e.config(state='disabled')
        self._frame.after(60000, self._enable_form)
    
    def _enable_form(self) -> None:
        for e in [self._user_entry, self._pw1_entry, self._pw2_entry]:
            e.config(state='normal')
        self._status.config(text='Unlocked')
    
    def on_show(self) -> None:
        self._user_entry.focus_set()
