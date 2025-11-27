"""ConfigureSystemSettingPage - System settings (SRS GUI)"""
import tkinter as tk
from tkinter import ttk, messagebox
from ..components.page import Page


class ConfigureSystemSettingPage(Page):
    """Configure system settings - SRS 'Configure system setting'"""
    
    def _build_ui(self) -> None:
        # Header
        self._create_header("Configure System Settings", back_page='major_function')
        
        # Form
        form_frame = ttk.LabelFrame(self._frame, text="System Settings", padding=20)
        form_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Web Password 1
        ttk.Label(form_frame, text="Web Password 1:").grid(row=0, column=0, sticky='e', pady=10)
        self._web_pw1_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self._web_pw1_var, show='*', width=30).grid(
            row=0, column=1, padx=10, pady=10)
        
        # Web Password 1 Confirm
        ttk.Label(form_frame, text="Confirm Password 1:").grid(row=1, column=0, sticky='e', pady=10)
        self._web_pw1_confirm_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self._web_pw1_confirm_var, show='*', width=30).grid(
            row=1, column=1, padx=10, pady=10)
        
        # Web Password 2
        ttk.Label(form_frame, text="Web Password 2:").grid(row=2, column=0, sticky='e', pady=10)
        self._web_pw2_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self._web_pw2_var, show='*', width=30).grid(
            row=2, column=1, padx=10, pady=10)
        
        # Web Password 2 Confirm
        ttk.Label(form_frame, text="Confirm Password 2:").grid(row=3, column=0, sticky='e', pady=10)
        self._web_pw2_confirm_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self._web_pw2_confirm_var, show='*', width=30).grid(
            row=3, column=1, padx=10, pady=10)
        
        ttk.Separator(form_frame, orient='horizontal').grid(row=4, column=0, columnspan=2, 
                                                           sticky='ew', pady=15)
        
        # Master Password
        ttk.Label(form_frame, text="Master Password (4 digits):").grid(row=5, column=0, sticky='e', pady=10)
        self._master_pw_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self._master_pw_var, show='*', width=30).grid(
            row=5, column=1, padx=10, pady=10)
        
        # Guest Password
        ttk.Label(form_frame, text="Guest Password (4 digits):").grid(row=6, column=0, sticky='e', pady=10)
        self._guest_pw_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self._guest_pw_var, show='*', width=30).grid(
            row=6, column=1, padx=10, pady=10)
        
        ttk.Separator(form_frame, orient='horizontal').grid(row=7, column=0, columnspan=2, 
                                                           sticky='ew', pady=15)
        
        # Delay Time
        ttk.Label(form_frame, text="Delay Time (minutes):").grid(row=8, column=0, sticky='e', pady=10)
        self._delay_var = tk.StringVar(value='5')
        ttk.Entry(form_frame, textvariable=self._delay_var, width=30).grid(
            row=8, column=1, padx=10, pady=10)
        
        # Phone Number
        ttk.Label(form_frame, text="Phone Number (panic):").grid(row=9, column=0, sticky='e', pady=10)
        self._phone_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self._phone_var, width=30).grid(
            row=9, column=1, padx=10, pady=10)
        
        # Submit button
        btn_frame = ttk.Frame(self._frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Save Settings", command=self._save, width=20).pack()
        
        # Status
        self._status = ttk.Label(self._frame, text="")
        self._status.pack()
    
    def _load_settings(self) -> None:
        response = self.send_to_system('get_system_settings')
        if response.get('success'):
            data = response.get('data', {})
            self._delay_var.set(str(data.get('delay_time', 5)))
            self._phone_var.set(data.get('phone', ''))
    
    def _save(self) -> None:
        # Validate
        pw1 = self._web_pw1_var.get()
        pw1_confirm = self._web_pw1_confirm_var.get()
        pw2 = self._web_pw2_var.get()
        pw2_confirm = self._web_pw2_confirm_var.get()
        
        if pw1 and pw1 != pw1_confirm:
            self._status.config(text="Password 1 mismatch", foreground='red')
            return
        
        if pw2 and pw2 != pw2_confirm:
            self._status.config(text="Password 2 mismatch", foreground='red')
            return
        
        try:
            delay = int(self._delay_var.get())
            if delay < 5:
                self._status.config(text="Delay must be at least 5 minutes", foreground='red')
                return
        except ValueError:
            self._status.config(text="Invalid delay time", foreground='red')
            return
        
        phone = self._phone_var.get()
        if not phone:
            self._status.config(text="Phone number required", foreground='red')
            return
        
        # Save
        settings = {
            'delay_time': delay,
            'phone': phone,
        }
        
        response = self.send_to_system('configure_system_settings', settings=settings)
        if response.get('success'):
            messagebox.showinfo("Success", "Settings saved")
            self._status.config(text="Settings saved", foreground='green')
        else:
            self._status.config(text="Failed to save", foreground='red')
    
    def on_show(self) -> None:
        self._load_settings()
