"""LoginPage - Web login (SRS V.1.b: 2-level password, 3 attempts)"""
import tkinter as tk
from tkinter import ttk
from ..components.page import Page


class LoginPage(Page):
    """Login with UserID + 2 passwords. Lock after 3 failures."""
    
    def __init__(self, parent, web_interface):
        self._attempts, self._locked = 3, False
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
                self._locked = True
                self._btn.config(state='disabled')
                self._msg.config(text="LOCKED - wait 60s")
                self._frame.after(60000, self._unlock)
            else:
                self._msg.config(text=f"Failed. {self._attempts} left")
    
    def _unlock(self):
        self._locked, self._attempts = False, 3
        self._btn.config(state='normal')
        self._msg.config(text="Unlocked")
    
    def on_show(self):
        self._attempts, self._locked = 3, False
        self._btn.config(state='normal')
        self._msg.config(text="")
