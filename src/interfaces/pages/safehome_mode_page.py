"""SafeHomeModePage - Mode selection (SRS V.2.b Step 5-8)"""
import tkinter as tk
from tkinter import ttk, messagebox
from ..components.page import Page


class SafeHomeModePage(Page):
    """Set SafeHome mode: HOME, AWAY, OVERNIGHT, EXTENDED."""
    
    MODE_BUTTONS = [
        ("HOME", "Home - perimeter sensors only"),
        ("AWAY", "Away - full security"),
        ("OVERNIGHT", "Overnight travel mode"),
        ("EXTENDED", "Extended travel mode"),
    ]
    
    def _build_ui(self):
        self._create_header("Set SafeHome Mode", back_page='security')
        
        sf = ttk.LabelFrame(self._frame, text="Current Status", padding=10)
        sf.pack(fill='x', padx=30, pady=10)
        self._status = ttk.Label(sf, text="", font=('Arial', 12))
        self._status.pack()
        
        mf = ttk.LabelFrame(self._frame, text="Choose a SafeHome Status", padding=15)
        mf.pack(fill='both', expand=True, padx=30, pady=10)

        for mode, desc in self.MODE_BUTTONS:
            btn = ttk.Button(
                mf,
                text=f"{mode}",
                width=18,
                command=lambda m=mode: self._apply_mode(m),
            )
            btn.pack(pady=3)
            ttk.Label(mf, text=desc, foreground="#666").pack(pady=(0, 5))

        quick = ttk.LabelFrame(self._frame, text="Quick Actions", padding=10)
        quick.pack(fill="x", padx=30, pady=(0, 15))
        ttk.Button(
            quick, text="Arm All System", command=self._arm_all, width=18
        ).pack(side="left", padx=5)
        ttk.Button(
            quick, text="Disarm All System", command=self._disarm_all, width=18
        ).pack(side="left", padx=5)
    
    def _update(self):
        res = self.send_to_system('get_status')
        if res.get('success'):
            d = res.get('data', {})
            if d.get('armed'):
                mode = d.get('mode', '').upper() or 'ARMED'
                self._status.config(text=f"● ARMED - {mode}", foreground='red')
            else:
                self._status.config(text="● DISARMED", foreground='green')
    
    def _apply_mode(self, mode: str):
        res = self.send_to_system('arm_system', mode=mode)
        if res.get('success'):
            messagebox.showinfo("Success", f"System armed in {mode} mode.")
        else:
            messagebox.showerror("Set Mode", res.get('message', 'Failed to change mode'))
        self._update()
    
    def _arm_all(self):
        res = self.send_to_system('arm_system', mode='AWAY')
        if not res.get('success'):
            messagebox.showerror("Arm All", res.get('message', 'Failed to arm system'))
        else:
            messagebox.showinfo("Arm All", "System armed (AWAY).")
        self._update()
    
    def _disarm_all(self):
        res = self.send_to_system('disarm_system')
        if res.get('success'):
            messagebox.showinfo("Disarm", "System disarmed.")
        else:
            messagebox.showerror("Disarm", res.get('message', 'Failed to disarm'))
        self._update()
    
    def on_show(self): self._update()
