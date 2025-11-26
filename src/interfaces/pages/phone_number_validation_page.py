"""PhoneNumberValidationPage - Phone/Address verification"""
import tkinter as tk
from tkinter import ttk
from ..components.page import Page


class PhoneNumberValidationPage(Page):
    """Identity verification page for security function access"""
    
    def _build_ui(self) -> None:
        center = ttk.Frame(self._frame)
        center.place(relx=0.5, rely=0.5, anchor='center')
        
        ttk.Label(center, text="Identity Verification", 
                 font=('Arial', 18, 'bold')).pack(pady=(0, 20))
        ttk.Label(center, text="Enter your address or phone number:",
                 font=('Arial', 11)).pack(pady=(0, 15))
        
        input_frame = ttk.Frame(center)
        input_frame.pack(pady=(0, 20))
        ttk.Label(input_frame, text="Address/Phone:").pack(side='left')
        self._input_entry, self._input_var = self._create_entry(input_frame, width=30)
        self._input_entry.pack(side='left', padx=(10, 0))
        
        btn_frame = ttk.Frame(center)
        btn_frame.pack()
        ttk.Button(btn_frame, text="Verify", command=self._verify, width=12).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Cancel", 
                  command=lambda: self.navigate_to('major_function'), width=12).pack(side='left', padx=5)
        
        self._status = ttk.Label(center, text="", foreground='red')
        self._status.pack(pady=(15, 0))
        
        self._input_entry.bind('<Return>', lambda e: self._verify())
    
    def _verify(self) -> None:
        value = self._input_var.get().strip()
        if not value:
            self._status.config(text="Please enter address or phone number")
            return
        
        response = self.send_to_system('verify_identity', value=value)
        if response.get('success'):
            target = self._web_interface.get_context('verification_target', 'security')
            self._web_interface.set_context('verified', True)
            self.navigate_to(target)
        else:
            remaining = response.get('attempts_remaining', 0)
            if remaining == 0:
                self._status.config(text="System locked")
                self._input_entry.config(state='disabled')
            else:
                self._status.config(text=f"Invalid. {remaining} attempts remaining")
    
    def on_show(self) -> None:
        self._input_var.set('')
        self._status.config(text='')
        self._input_entry.config(state='normal')
        self._input_entry.focus_set()
