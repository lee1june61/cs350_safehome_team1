"""
LoginManager - A helper class to manage login logic for the LoginPage.
"""
import tkinter as tk
from tkinter import ttk
from typing import Callable
import time

class LoginManager:
    def __init__(self, page, user_var: tk.StringVar, pw1_var: tk.StringVar, pw2_var: tk.StringVar,
                 login_btn: ttk.Button, status_msg: ttk.Label):
        self.page = page
        self._user_var = user_var
        self._pw1_var = pw1_var
        self._pw2_var = pw2_var
        self._login_btn = login_btn
        self._status_msg = status_msg
        
        self._attempts = 3
        self._locked = False
        self._lock_start_time = None
        self._countdown_job = None
    
    def login(self):
        if self._locked:
            return
            
        u, p1, p2 = self._user_var.get().strip(), self._pw1_var.get(), self._pw2_var.get()
        if not u or not p1 or not p2:
            self._status_msg.config(text="Fill all fields")
            return
        
        res = self.page.send_to_system('login_web', user_id=u, password1=p1, password2=p2)
        if res.get('success'):
            self._user_var.set('')
            self._pw1_var.set('')
            self._pw2_var.set('')
            self.page._web_interface.set_context('user_id', u)
            self.page.navigate_to('major_function')
        else:
            self._attempts -= 1
            if self._attempts <= 0:
                self._lock()
            else:
                self._status_msg.config(text=f"Failed. {self._attempts} left")
    
    def _lock(self):
        """Lock the login and start countdown."""
        self._locked = True
        self._lock_start_time = time.time()
        self._login_btn.config(state='disabled')
        self._update_countdown()
    
    def _update_countdown(self):
        """Update the countdown display every second."""
        if not self._locked or self._lock_start_time is None:
            return
        
        elapsed = time.time() - self._lock_start_time
        remaining = max(0, int(60 - elapsed))
        
        if remaining > 0:
            self._status_msg.config(text=f"LOCKED - {remaining} seconds remaining")
            self._countdown_job = self.page._frame.after(1000, self._update_countdown)
        else:
            self._unlock()
    
    def _unlock(self):
        """Unlock the login."""
        if self._countdown_job:
            self.page._frame.after_cancel(self._countdown_job)
            self._countdown_job = None
        self._locked = False
        self._attempts = 3
        self._lock_start_time = None
        self._login_btn.config(state='normal')
        self._status_msg.config(text="Unlocked")
    
    def on_show(self):
        """Reset login state when page is shown."""
        if self._countdown_job:
            self.page._frame.after_cancel(self._countdown_job)
            self._countdown_job = None
        self._attempts = 3
        self._locked = False
        self._lock_start_time = None
        self._login_btn.config(state='normal')
        self._status_msg.config(text="")
