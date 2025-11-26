"""SafeHomeModePage - Set current SafeHome mode"""
import tkinter as tk
from tkinter import ttk
from ..components.page import Page


class SafeHomeModePage(Page):
    """Page for setting current SafeHome mode"""
    
    MODES = ['HOME', 'AWAY', 'NIGHT', 'EXTENDED', 'GUEST']
    
    def _build_ui(self) -> None:
        self._create_header("Set SafeHome Mode", back_page='security')
        
        status_frame = ttk.LabelFrame(self._frame, text="Current Status", padding=15)
        status_frame.pack(fill='x', padx=20, pady=(0, 20))
        self._status_label = ttk.Label(status_frame, text="Loading...", font=('Arial', 12))
        self._status_label.pack()
        
        mode_frame = ttk.LabelFrame(self._frame, text="Select Mode", padding=15)
        mode_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        self._mode_var = tk.StringVar()
        for mode in self.MODES:
            ttk.Radiobutton(mode_frame, text=mode, variable=self._mode_var, 
                           value=mode).pack(anchor='w', pady=5)
        
        btn_frame = ttk.Frame(self._frame)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Arm All", command=lambda: self._set(True), 
                  width=15).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Disarm All", command=lambda: self._set(False), 
                  width=15).pack(side='left', padx=5)
    
    def _set(self, arm: bool) -> None:
        if arm:
            mode = self._mode_var.get()
            if not mode:
                return self._show_message("Info", "Select a mode", 'warning')
            response = self.send_to_system('arm_system', mode=mode)
            if response.get('success'):
                self._show_message("Success", f"Armed in {mode} mode")
                self.refresh()
            else:
                self._show_message("Error", response.get('message', 'Failed'), 'error')
        else:
            response = self.send_to_system('disarm_system')
            if response.get('success'):
                self._show_message("Success", "System disarmed")
                self.refresh()
            else:
                self._show_message("Error", response.get('message', 'Failed'), 'error')
    
    def on_show(self) -> None:
        self.refresh()
    
    def refresh(self) -> None:
        response = self.send_to_system('get_status')
        if response.get('success'):
            data = response.get('data', {})
            armed = data.get('armed', False)
            mode = data.get('mode', 'None')
            self._status_label.config(text=f"Armed: {mode}" if armed else "Disarmed")
            if armed and mode:
                self._mode_var.set(mode)
