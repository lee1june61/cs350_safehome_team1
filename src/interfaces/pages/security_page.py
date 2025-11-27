"""SecurityPage - Security function menu (SRS GUI)"""
import tkinter as tk
from tkinter import ttk
from ..components.page import Page


class SecurityPage(Page):
    """Security page - SRS Section II 'Security Function'"""
    
    def _build_ui(self) -> None:
        # Header
        self._create_header("Security Function", back_page='major_function')
        
        # Phone/Address validation (SRS requires this)
        validation_frame = ttk.LabelFrame(self._frame, text="Identity Confirmation", padding=15)
        validation_frame.pack(fill='x', padx=30, pady=10)
        
        ttk.Label(validation_frame, text="Enter phone number or address:").pack(anchor='w')
        
        input_frame = ttk.Frame(validation_frame)
        input_frame.pack(fill='x', pady=5)
        
        self._validation_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self._validation_var, width=40).pack(side='left', padx=(0, 10))
        ttk.Button(input_frame, text="Verify", command=self._verify).pack(side='left')
        
        self._validation_status = ttk.Label(validation_frame, text="")
        self._validation_status.pack(anchor='w', pady=5)
        
        # Function buttons (disabled until verified)
        self._buttons_frame = ttk.Frame(self._frame)
        self._buttons_frame.pack(expand=True, fill='both', padx=30, pady=20)
        
        self._buttons_frame.columnconfigure(0, weight=1)
        self._buttons_frame.rowconfigure((0, 1, 2, 3), weight=1)
        
        # Safety Zone button
        self._btn_zone = tk.Button(
            self._buttons_frame, text="Safety Zone", font=('Arial', 16),
            bg='#607D8B', fg='white', state='disabled',
            command=lambda: self.navigate_to('safety_zone'), height=2
        )
        self._btn_zone.grid(row=0, column=0, sticky='nsew', padx=20, pady=10)
        
        # Security Mode button (Set SafeHome Mode)
        self._btn_mode = tk.Button(
            self._buttons_frame, text="Set SafeHome Mode", font=('Arial', 16),
            bg='#607D8B', fg='white', state='disabled',
            command=lambda: self.navigate_to('safehome_mode'), height=2
        )
        self._btn_mode.grid(row=1, column=0, sticky='nsew', padx=20, pady=10)
        
        # View Intrusion Log button
        self._btn_log = tk.Button(
            self._buttons_frame, text="View Intrusion Log", font=('Arial', 16),
            bg='#607D8B', fg='white', state='disabled',
            command=lambda: self.navigate_to('view_log'), height=2
        )
        self._btn_log.grid(row=2, column=0, sticky='nsew', padx=20, pady=10)
        
        # Redefine Security Modes button
        self._btn_redefine = tk.Button(
            self._buttons_frame, text="Redefine Security Modes", font=('Arial', 16),
            bg='#607D8B', fg='white', state='disabled',
            command=lambda: self.navigate_to('safehome_mode_configure'), height=2
        )
        self._btn_redefine.grid(row=3, column=0, sticky='nsew', padx=20, pady=10)
    
    def _verify(self) -> None:
        """Verify phone/address - enables buttons"""
        value = self._validation_var.get().strip()
        if value:
            self._validation_status.config(text="✓ Verified", foreground='green')
            self._enable_buttons()
        else:
            self._validation_status.config(text="Please enter phone or address", foreground='red')
    
    def _enable_buttons(self) -> None:
        for btn in [self._btn_zone, self._btn_mode, self._btn_log, self._btn_redefine]:
            btn.config(state='normal', bg='#2196F3')
    
    def on_show(self) -> None:
        # Reset verification
        self._validation_var.set('')
        self._validation_status.config(text='')
        for btn in [self._btn_zone, self._btn_mode, self._btn_log, self._btn_redefine]:
            btn.config(state='disabled', bg='#607D8B')
