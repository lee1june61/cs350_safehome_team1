"""SafeHomeModePage - Security mode selection (SRS GUI)"""
import tkinter as tk
from tkinter import ttk, messagebox
from ..components.page import Page


class SafeHomeModePage(Page):
    """SafeHome Mode page - SRS Section II 'Security Function - Security Mode'"""
    
    MODES = [
        ('HOME', 'Home - Partial security while at home'),
        ('AWAY', 'Away - Full security when leaving'),
        ('OVERNIGHT', 'Overnight Travel - Extended away mode'),
        ('EXTENDED', 'Extended Travel - Long-term away mode'),
    ]
    
    def _build_ui(self) -> None:
        # Header
        self._create_header("Set SafeHome Mode", back_page='security')
        
        # Current status
        status_frame = ttk.LabelFrame(self._frame, text="Current Status", padding=15)
        status_frame.pack(fill='x', padx=30, pady=15)
        
        self._status_label = ttk.Label(status_frame, text="Loading...", font=('Arial', 14))
        self._status_label.pack()
        
        # Mode selection
        mode_frame = ttk.LabelFrame(self._frame, text="Select Security Mode", padding=20)
        mode_frame.pack(fill='both', expand=True, padx=30, pady=10)
        
        self._mode_var = tk.StringVar(value='')
        
        for mode, description in self.MODES:
            frame = ttk.Frame(mode_frame)
            frame.pack(fill='x', pady=8)
            
            rb = ttk.Radiobutton(frame, text=mode, variable=self._mode_var, 
                                value=mode, style='TRadiobutton')
            rb.pack(side='left')
            
            ttk.Label(frame, text=f"  - {description}", foreground='gray').pack(side='left')
        
        # Quick actions
        quick_frame = ttk.Frame(mode_frame)
        quick_frame.pack(fill='x', pady=20)
        
        ttk.Button(quick_frame, text="Arm All", command=self._arm_all, 
                  width=15).pack(side='left', padx=10)
        ttk.Button(quick_frame, text="Disarm All", command=self._disarm_all,
                  width=15).pack(side='left', padx=10)
        
        # Apply button
        btn_frame = ttk.Frame(self._frame)
        btn_frame.pack(fill='x', padx=30, pady=20)
        
        ttk.Button(btn_frame, text="Apply Mode", command=self._apply_mode,
                  width=20).pack(pady=10)
    
    def _update_status(self) -> None:
        response = self.send_to_system('get_status')
        if response.get('success'):
            data = response.get('data', {})
            armed = data.get('armed', False)
            mode = data.get('mode', 'DISARMED')
            
            if armed:
                self._status_label.config(text=f"● System ARMED - Mode: {mode}", 
                                         foreground='red')
                self._mode_var.set(mode)
            else:
                self._status_label.config(text="● System DISARMED", foreground='green')
                self._mode_var.set('')
    
    def _apply_mode(self) -> None:
        mode = self._mode_var.get()
        if not mode:
            messagebox.showwarning("Warning", "Please select a mode")
            return
        
        response = self.send_to_system('arm_system', mode=mode)
        if response.get('success'):
            messagebox.showinfo("Success", f"System armed in {mode} mode")
            self._update_status()
        else:
            messagebox.showerror("Error", response.get('message', 'Failed to arm system'))
    
    def _arm_all(self) -> None:
        response = self.send_to_system('arm_system', mode='AWAY')
        if response.get('success'):
            messagebox.showinfo("Success", "System fully armed")
            self._update_status()
    
    def _disarm_all(self) -> None:
        response = self.send_to_system('disarm_system')
        if response.get('success'):
            messagebox.showinfo("Success", "System disarmed")
            self._update_status()
    
    def on_show(self) -> None:
        self._update_status()
