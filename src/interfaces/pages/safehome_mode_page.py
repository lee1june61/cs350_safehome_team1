"""SafeHomeModePage - Mode selection (SRS V.2.b Step 5-8)"""
import tkinter as tk
from tkinter import ttk, messagebox
from ..components.page import Page


class SafeHomeModePage(Page):
    """Set SafeHome mode: HOME, AWAY, OVERNIGHT, EXTENDED."""
    
    MODES = [
        ('HOME', 'Partial security while at home'),
        ('AWAY', 'Full security when leaving'),
        ('OVERNIGHT', 'Overnight travel mode'),
        ('EXTENDED', 'Extended travel mode'),
    ]
    
    def _build_ui(self):
        self._create_header("Set SafeHome Mode", back_page='security')
        
        sf = ttk.LabelFrame(self._frame, text="Current Status", padding=10)
        sf.pack(fill='x', padx=30, pady=10)
        self._status = ttk.Label(sf, text="", font=('Arial', 12))
        self._status.pack()
        
        mf = ttk.LabelFrame(self._frame, text="Select Mode", padding=15)
        mf.pack(fill='both', expand=True, padx=30, pady=10)
        
        self._mode = tk.StringVar()
        for m, desc in self.MODES:
            f = ttk.Frame(mf)
            f.pack(fill='x', pady=5)
            ttk.Radiobutton(f, text=m, variable=self._mode, value=m).pack(side='left')
            ttk.Label(f, text=f" - {desc}", foreground='gray').pack(side='left')
        
        qf = ttk.Frame(mf)
        qf.pack(pady=15)
        ttk.Button(qf, text="Arm All", command=self._arm_all, width=12).pack(side='left', padx=5)
        ttk.Button(qf, text="Disarm All", command=self._disarm_all, width=12).pack(side='left', padx=5)
        
        ttk.Button(self._frame, text="Apply Mode", command=self._apply, width=15).pack(pady=15)
    
    def _update(self):
        res = self.send_to_system('get_status')
        if res.get('success'):
            d = res.get('data', {})
            if d.get('armed'):
                self._status.config(text=f"● ARMED - {d.get('mode')}", foreground='red')
                self._mode.set(d.get('mode', ''))
            else:
                self._status.config(text="● DISARMED", foreground='green')
    
    def _apply(self):
        m = self._mode.get()
        if not m: messagebox.showwarning("", "Select a mode"); return
        res = self.send_to_system('arm_system', mode=m)
        if res.get('success'): messagebox.showinfo("", f"Armed: {m}")
        self._update()
    
    def _arm_all(self):
        self.send_to_system('arm_system', mode='AWAY')
        self._update()
    
    def _disarm_all(self):
        self.send_to_system('disarm_system')
        self._update()
    
    def on_show(self): self._update()
