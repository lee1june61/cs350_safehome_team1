"""SecurityPage - Security function main screen"""
import tkinter as tk
from tkinter import ttk
from ..components.page import Page


class SecurityPage(Page):
    """Security management page"""
    
    def _build_ui(self) -> None:
        self._create_header("Security", back_page='major_function')
        
        content = ttk.Frame(self._frame)
        content.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Arm/Disarm controls
        left = ttk.LabelFrame(content, text="Arm/Disarm", padding=15)
        left.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        self._status_label = ttk.Label(left, text="Status: DISARMED", 
                                       font=('Arial', 14, 'bold'), foreground='green')
        self._status_label.pack(pady=(0, 20))
        
        ttk.Label(left, text="Select Mode:").pack(anchor='w')
        self._mode_var = tk.StringVar(value='HOME')
        for mode in ['HOME', 'AWAY', 'NIGHT', 'EXTENDED', 'GUEST']:
            ttk.Radiobutton(left, text=mode, variable=self._mode_var, 
                           value=mode).pack(anchor='w', pady=2)
        
        btn_frame = ttk.Frame(left)
        btn_frame.pack(pady=20)
        self._arm_btn = ttk.Button(btn_frame, text="ARM", command=self._arm, width=12)
        self._arm_btn.pack(side='left', padx=5)
        self._disarm_btn = ttk.Button(btn_frame, text="DISARM", command=self._disarm, 
                                      width=12, state='disabled')
        self._disarm_btn.pack(side='left', padx=5)
        
        ttk.Separator(left).pack(fill='x', pady=15)
        ttk.Button(left, text="🚨 PANIC", command=self._panic, width=20).pack()
        
        # Navigation
        right = ttk.Frame(content)
        right.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        for frame_name, buttons in [
            ("Safety Zones", [("Manage Safety Zones", 'safety_zone')]),
            ("SafeHome Modes", [("Set Mode", 'safehome_mode'), 
                               ("Configure Modes", 'safehome_mode_configure')]),
            ("Logs", [("View Intrusion Logs", 'view_log')]),
        ]:
            f = ttk.LabelFrame(right, text=frame_name, padding=10)
            f.pack(fill='x', pady=(0, 10))
            for text, page in buttons:
                ttk.Button(f, text=text, command=lambda p=page: self.navigate_to(p),
                          width=25).pack(pady=3)
    
    def _arm(self) -> None:
        response = self.send_to_system('arm_system', mode=self._mode_var.get())
        if response.get('success'):
            self._show_message("Success", f"System armed: {self._mode_var.get()}")
            self.refresh()
        else:
            self._show_message("Error", response.get('message', 'Failed'), 'error')
    
    def _disarm(self) -> None:
        response = self.send_to_system('disarm_system')
        if response.get('success'):
            self._show_message("Success", "System disarmed")
            self.refresh()
        else:
            self._show_message("Error", response.get('message', 'Failed'), 'error')
    
    def _panic(self) -> None:
        if not self._ask_confirm("Panic", "Trigger alarm and call monitoring?"):
            return
        response = self.send_to_system('panic')
        if response.get('success'):
            self._show_message("Alert", "Panic triggered. Monitoring called.")
        else:
            self._show_message("Error", response.get('message', 'Failed'), 'error')
    
    def on_show(self) -> None:
        self.refresh()
    
    def refresh(self) -> None:
        response = self.send_to_system('get_status')
        if response.get('success'):
            armed = response.get('data', {}).get('armed', False)
            mode = response.get('data', {}).get('mode', 'None')
            
            if armed:
                self._status_label.config(text=f"Status: ARMED ({mode})", foreground='red')
                self._arm_btn.config(state='disabled')
                self._disarm_btn.config(state='normal')
            else:
                self._status_label.config(text="Status: DISARMED", foreground='green')
                self._arm_btn.config(state='normal')
                self._disarm_btn.config(state='disabled')
