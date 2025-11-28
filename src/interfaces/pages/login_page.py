"""LoginPage - Web login (SRS V.1.b: 2-level password, 3 attempts)"""
import tkinter as tk
from tkinter import ttk
import time
from ..components.page import Page


class LoginPage(Page):
    """Login with UserID + 2 passwords. Lock after 3 failures."""
    
    def __init__(self, parent, web_interface):
        self._attempts, self._locked = 3, False
        self._lock_start_time = None
        self._countdown_job = None
        super().__init__(parent, web_interface)
    
    def _build_ui(self):
        c = ttk.Frame(self._frame)
        c.place(relx=0.5, rely=0.5, anchor='center')
        ttk.Label(c, text="SafeHome Login", font=('Arial', 24, 'bold')).pack(pady=20)
        
        f = ttk.LabelFrame(c, text="Credentials", padding=15)
        f.pack(padx=20, pady=10)
        
        ttk.Label(f, text="User ID:").grid(row=0, column=0, sticky='e', pady=5)
        self._user = tk.StringVar()
        ttk.Entry(f, textvariable=self._user, width=25).grid(row=0, column=1, pady=5)
        
        ttk.Label(f, text="Password 1:").grid(row=1, column=0, sticky='e', pady=5)
        self._pw1 = tk.StringVar()
        ttk.Entry(f, textvariable=self._pw1, show='*', width=25).grid(row=1, column=1, pady=5)
        
        ttk.Label(f, text="Password 2:").grid(row=2, column=0, sticky='e', pady=5)
        self._pw2 = tk.StringVar()
        e = ttk.Entry(f, textvariable=self._pw2, show='*', width=25)
        e.grid(row=2, column=1, pady=5)
        e.bind('<Return>', lambda x: self._login())
        
        self._btn = ttk.Button(f, text="Login", command=self._login, width=15)
        self._btn.grid(row=3, column=0, columnspan=2, pady=15)
        
        self._msg = ttk.Label(c, text="", foreground='red')
        self._msg.pack(pady=5)
        ttk.Label(c, text="Default: admin / password / password", foreground='gray').pack()
    
    def _login(self):
        if self._locked: return
        u, p1, p2 = self._user.get().strip(), self._pw1.get(), self._pw2.get()
        if not u or not p1 or not p2:
            self._msg.config(text="Fill all fields"); return
        
        res = self.send_to_system('login_web', user_id=u, password1=p1, password2=p2)
        if res.get('success'):
            self._user.set(''); self._pw1.set(''); self._pw2.set('')
            self._web_interface.set_context('user_id', u)
            self.navigate_to('major_function')
        else:
            self._attempts -= 1
            if self._attempts <= 0:
                self._lock()
            else:
                self._msg.config(text=f"Failed. {self._attempts} left")
    
    def _lock(self):
        """Lock the login and start countdown."""
        self._locked = True
        self._lock_start_time = time.time()
        self._btn.config(state='disabled')
        self._update_countdown()
    
    def _update_countdown(self):
        """Update the countdown display every second."""
        if not self._locked or self._lock_start_time is None:
            return
        
        elapsed = time.time() - self._lock_start_time
        remaining = max(0, int(60 - elapsed))
        
        if remaining > 0:
            self._msg.config(text=f"LOCKED - {remaining} seconds remaining")
            self._countdown_job = self._frame.after(1000, self._update_countdown)
        else:
            self._unlock()
    
    def _unlock(self):
        """Unlock the login."""
        if self._countdown_job:
            self._frame.after_cancel(self._countdown_job)
            self._countdown_job = None
        self._locked = False
        self._attempts = 3
        self._lock_start_time = None
        self._btn.config(state='normal')
        self._msg.config(text="Unlocked")
    
    def on_show(self):
        """Reset login state when page is shown."""
        if self._countdown_job:
            self._frame.after_cancel(self._countdown_job)
            self._countdown_job = None
        self._attempts = 3
        self._locked = False
        self._lock_start_time = None
        self._btn.config(state='normal')
        self._msg.config(text="")
