"""SecurityPage - Security menu with identity verification (SRS V.2)"""
import tkinter as tk
from tkinter import ttk
from ...components.page import Page


class SecurityPage(Page):
    """Security functions - requires phone/address verification first."""
    
    def _build_ui(self):
        self._create_header("Security Function", back_page='major_function')
        self._lock_after_id = None
        self._lock_message = ""
        self._lock_seconds = 0
        
        # Verification frame
        vf = ttk.LabelFrame(self._frame, text="Identity Confirmation", padding=10)
        vf.pack(fill='x', padx=30, pady=10)
        
        ttk.Label(vf, text="Monitoring Phone:").pack(side='left')
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
            message = res.get('message', "Invalid")
            if res.get('locked'):
                seconds = res.get('seconds_remaining') or res.get('lock_duration')
                self._set_locked_state(message, seconds)
            else:
                self._status.config(text=message, foreground='red')
    
    def _set_verified(self, verified: bool):
        """Update UI based on verification state."""
        self._clear_lock_timer()
        self._web_interface.set_context('security_verified', verified)
        if verified:
            self._status.config(text="✓ Verified", foreground='green')
            self._entry.config(state='disabled')
            self._verify_btn.config(state='disabled')
            for b in self._btns:
                b.config(state='normal', bg='#2196F3')
        else:
            self._status.config(text="Enter registered phone number", foreground='#555')
            self._entry.config(state='normal')
            self._verify_btn.config(state='normal')
            for b in self._btns:
                b.config(state='disabled', bg='#607D8B')
    
    def _set_locked_state(self, message: str, seconds: int | None):
        self._lock_message = message or "Verification locked"
        self._lock_seconds = max(int(seconds or 0), 0)
        self._update_lock_status()
        self._entry.config(state='disabled')
        self._verify_btn.config(state='disabled')
        self._clear_lock_timer()
        if self._lock_seconds > 0:
            self._schedule_lock_tick()
        else:
            self._unlock_verification()

    def _update_lock_status(self):
        if self._lock_seconds and self._lock_seconds > 0:
            self._status.config(
                text=f"{self._lock_message} ({self._lock_seconds}s)",
                foreground='red',
            )
        else:
            self._status.config(text=self._lock_message, foreground='red')

    def _schedule_lock_tick(self):
        self._update_lock_status()
        if self._lock_seconds <= 0:
            self._unlock_verification()
            return
        self._lock_seconds -= 1
        self._lock_after_id = self._frame.after(1000, self._schedule_lock_tick)
    
    def _unlock_verification(self):
        self._lock_after_id = None
        if not self._web_interface.get_context('security_verified'):
            self._entry.config(state='normal')
            self._verify_btn.config(state='normal')
            self._status.config(text="Enter registered phone number", foreground='#555')
        self._lock_seconds = 0
    
    def _clear_lock_timer(self):
        if getattr(self, '_lock_after_id', None):
            self._frame.after_cancel(self._lock_after_id)
            self._lock_after_id = None
    
    def on_show(self):
        """Check if already verified in this session."""
        self._clear_lock_timer()
        if self._web_interface.get_context('security_verified'):
            self._set_verified(True)
        else:
            self._val.set('')
            self._set_verified(False)


