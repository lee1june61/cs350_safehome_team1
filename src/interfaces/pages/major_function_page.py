"""MajorFunctionPage - Main menu with 3 big buttons (SRS GUI)"""
import tkinter as tk
from tkinter import ttk
from ..components.page import Page


class MajorFunctionPage(Page):
    """Main function page - SRS Section II 'SafeHome MainFunctions'"""
    
    def _build_ui(self) -> None:
        header = ttk.Frame(self._frame)
        header.pack(fill='x', padx=20, pady=20)
        ttk.Label(header, text="SafeHome", font=('Arial', 24, 'bold')).pack(side='left')
        
        sf = ttk.Frame(header)
        sf.pack(side='right')
        self._armed_label = ttk.Label(sf, text="● DISARMED", foreground='green')
        self._armed_label.pack(side='right', padx=10)
        ttk.Button(sf, text="Logout", command=self._logout).pack(side='right')
        
        content = ttk.Frame(self._frame)
        content.pack(expand=True, fill='both', padx=50, pady=30)
        content.columnconfigure(0, weight=1)
        content.rowconfigure((0, 1, 2), weight=1)
        
        buttons = [
            ("Security Function", '#2196F3', 'security'),
            ("Surveillance Function", '#4CAF50', 'surveillance'),
            ("Configure System Setting", '#FF9800', 'configure_system_setting'),
        ]
        for i, (txt, color, page) in enumerate(buttons):
            b = tk.Button(content, text=txt, font=('Arial', 18, 'bold'), bg=color, fg='white',
                         height=3, command=lambda p=page: self.navigate_to(p))
            b.grid(row=i, column=0, sticky='nsew', padx=20, pady=15)
    
    def _logout(self) -> None:
        self.send_to_system('logout')
        self.navigate_to('login')
    
    def on_show(self) -> None:
        res = self.send_to_system('get_status')
        if res.get('success'):
            d = res.get('data', {})
            if d.get('armed'):
                self._armed_label.config(text=f"● ARMED ({d.get('mode')})", foreground='red')
            else:
                self._armed_label.config(text="● DISARMED", foreground='green')
