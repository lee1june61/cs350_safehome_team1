"""MajorFunctionPage - Main menu with 3 big buttons (SRS GUI)"""
import tkinter as tk
from tkinter import ttk
from ..components.page import Page


class MajorFunctionPage(Page):
    """Main function page - SRS Section II 'SafeHome MainFunctions'"""
    
    def _build_ui(self) -> None:
        # Header with status
        header = ttk.Frame(self._frame)
        header.pack(fill='x', padx=20, pady=20)
        
        ttk.Label(header, text="SafeHome", font=('Arial', 24, 'bold')).pack(side='left')
        
        # Status indicators on right
        status_frame = ttk.Frame(header)
        status_frame.pack(side='right')
        
        self._armed_label = ttk.Label(status_frame, text="● DISARMED", foreground='green')
        self._armed_label.pack(side='right', padx=10)
        
        ttk.Button(status_frame, text="Logout", command=self._logout).pack(side='right')
        
        # Main content - 3 big buttons
        content = ttk.Frame(self._frame)
        content.pack(expand=True, fill='both', padx=50, pady=30)
        
        # Configure grid
        content.columnconfigure(0, weight=1)
        content.rowconfigure((0, 1, 2), weight=1)
        
        # Security Function button
        btn_security = tk.Button(
            content, text="Security Function", font=('Arial', 18, 'bold'),
            bg='#2196F3', fg='white', activebackground='#1976D2',
            command=lambda: self.navigate_to('security'), height=3
        )
        btn_security.grid(row=0, column=0, sticky='nsew', padx=20, pady=15)
        
        # Surveillance Function button  
        btn_surveillance = tk.Button(
            content, text="Surveillance Function", font=('Arial', 18, 'bold'),
            bg='#4CAF50', fg='white', activebackground='#388E3C',
            command=lambda: self.navigate_to('surveillance'), height=3
        )
        btn_surveillance.grid(row=1, column=0, sticky='nsew', padx=20, pady=15)
        
        # Configure System Setting button
        btn_config = tk.Button(
            content, text="Configure System Setting", font=('Arial', 18, 'bold'),
            bg='#FF9800', fg='white', activebackground='#F57C00',
            command=lambda: self.navigate_to('configure_system_setting'), height=3
        )
        btn_config.grid(row=2, column=0, sticky='nsew', padx=20, pady=15)
    
    def _logout(self) -> None:
        self.send_to_system('logout')
        self.navigate_to('login')
    
    def on_show(self) -> None:
        self._update_status()
    
    def _update_status(self) -> None:
        response = self.send_to_system('get_status')
        if response.get('success'):
            data = response.get('data', {})
            armed = data.get('armed', False)
            mode = data.get('mode', 'DISARMED')
            
            if armed:
                self._armed_label.config(text=f"● ARMED ({mode})", foreground='red')
            else:
                self._armed_label.config(text="● DISARMED", foreground='green')
