"""SecurityPage - Security menu with identity verification (SRS V.2)"""
import tkinter as tk
from tkinter import ttk
from ...components.page import Page


class SecurityPage(Page):
    """Security functions - requires phone/address verification first."""
    
    def _build_ui(self):
        self._create_header("Security Function", back_page='major_function')
        
        # Verification frame
        vf = ttk.LabelFrame(self._frame, text="Identity Confirmation", padding=10)
        vf.pack(fill='x', padx=30, pady=10)
        
        ttk.Label(vf, text="Phone or Address:").pack(side='left')
        self._val = tk.StringVar()
        self._entry = ttk.Entry(vf, textvariable=self._val, width=30)
        self._entry.pack(side='left', padx=5)
        self._verify_btn = ttk.Button(vf, text="Verify", command=self._verify)
        self._verify_btn.pack(side='left')
        self._status = ttk.Label(vf, text="")
        self._status.pack(side='left', padx=10)
        
        # Buttons (disabled until verified)
        bf = ttk.Frame(self._frame)
        bf.pack(expand=True, fill='both', padx=30, pady=10)
        bf.columnconfigure(0, weight=1)
        
        self._btns = []
        items = [("Safety Zone", 'safety_zone'), ("Set SafeHome Mode", 'safehome_mode'),
                 ("View Intrusion Log", 'view_log'), ("Redefine Security Modes", 'safehome_mode_configure')]
        for i, (txt, page) in enumerate(items):
            b = tk.Button(bf, text=txt, font=('Arial', 14), bg='#607D8B', fg='white',
                         height=2, state='disabled', command=lambda p=page: self.navigate_to(p))
            b.grid(row=i, column=0, sticky='ew', pady=8, padx=20)
            self._btns.append(b)
    
    def _verify(self):
        val = self._val.get().strip()
        res = self.send_to_system('verify_identity', value=val)
        if res.get('success'):
            self._set_verified(True)
        else:
            self._status.config(text="Invalid", foreground='red')
    
    def _set_verified(self, verified: bool):
        """Update UI based on verification state."""
        self._web_interface.set_context('security_verified', verified)
        if verified:
            self._status.config(text="✓ Verified", foreground='green')
            self._entry.config(state='disabled')
            self._verify_btn.config(state='disabled')
            for b in self._btns:
                b.config(state='normal', bg='#2196F3')
        else:
            self._status.config(text="")
            self._entry.config(state='normal')
            self._verify_btn.config(state='normal')
            for b in self._btns:
                b.config(state='disabled', bg='#607D8B')
    
    def on_show(self):
        """Check if already verified in this session."""
        if self._web_interface.get_context('security_verified'):
            self._set_verified(True)
        else:
            self._val.set('')
            self._set_verified(False)

