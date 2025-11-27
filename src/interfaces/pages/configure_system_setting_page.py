"""ConfigureSystemSettingPage - System settings configuration (SRS V.1.c)

SRS V.1.c specifies:
- Two web passwords and reconfirmation fields
- Master password and reconfirmation field  
- Guest password and reconfirmation field (can be empty)
- Delay time for alarm event (minimum 5 minutes)
- Phone number for panic/monitoring service
"""
import tkinter as tk
from tkinter import ttk, messagebox
from ..components.page import Page


class ConfigureSystemSettingPage(Page):
    """Configure all system settings including passwords, delay time, and phone."""
    
    def _build_ui(self):
        self._create_header("System Settings", back_page='major_function')
        
        # Main container with scrollable frame if needed
        main = ttk.Frame(self._frame)
        main.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Web Password Section
        web_frame = ttk.LabelFrame(main, text="Web Login Passwords (8+ chars)", padding=10)
        web_frame.pack(fill='x', pady=5)
        
        self._web_pw1 = tk.StringVar()
        self._web_pw1_confirm = tk.StringVar()
        self._web_pw2 = tk.StringVar()
        self._web_pw2_confirm = tk.StringVar()
        
        ttk.Label(web_frame, text="Password 1:").grid(row=0, column=0, sticky='e', padx=5, pady=2)
        ttk.Entry(web_frame, textvariable=self._web_pw1, show='*', width=20).grid(row=0, column=1, pady=2)
        ttk.Label(web_frame, text="Confirm:").grid(row=0, column=2, sticky='e', padx=5)
        ttk.Entry(web_frame, textvariable=self._web_pw1_confirm, show='*', width=20).grid(row=0, column=3, pady=2)
        
        ttk.Label(web_frame, text="Password 2:").grid(row=1, column=0, sticky='e', padx=5, pady=2)
        ttk.Entry(web_frame, textvariable=self._web_pw2, show='*', width=20).grid(row=1, column=1, pady=2)
        ttk.Label(web_frame, text="Confirm:").grid(row=1, column=2, sticky='e', padx=5)
        ttk.Entry(web_frame, textvariable=self._web_pw2_confirm, show='*', width=20).grid(row=1, column=3, pady=2)
        
        # Control Panel Password Section
        panel_frame = ttk.LabelFrame(main, text="Control Panel Passwords (4 digits)", padding=10)
        panel_frame.pack(fill='x', pady=5)
        
        self._master_pw = tk.StringVar()
        self._master_pw_confirm = tk.StringVar()
        self._guest_pw = tk.StringVar()
        self._guest_pw_confirm = tk.StringVar()
        
        ttk.Label(panel_frame, text="Master Password:").grid(row=0, column=0, sticky='e', padx=5, pady=2)
        ttk.Entry(panel_frame, textvariable=self._master_pw, show='*', width=15).grid(row=0, column=1, pady=2)
        ttk.Label(panel_frame, text="Confirm:").grid(row=0, column=2, sticky='e', padx=5)
        ttk.Entry(panel_frame, textvariable=self._master_pw_confirm, show='*', width=15).grid(row=0, column=3, pady=2)
        
        ttk.Label(panel_frame, text="Guest Password:").grid(row=1, column=0, sticky='e', padx=5, pady=2)
        ttk.Entry(panel_frame, textvariable=self._guest_pw, show='*', width=15).grid(row=1, column=1, pady=2)
        ttk.Label(panel_frame, text="Confirm:").grid(row=1, column=2, sticky='e', padx=5)
        ttk.Entry(panel_frame, textvariable=self._guest_pw_confirm, show='*', width=15).grid(row=1, column=3, pady=2)
        ttk.Label(panel_frame, text="(Guest password can be empty)", font=('Arial', 8)).grid(row=2, column=0, columnspan=4)
        
        # Alarm & Monitoring Section
        alarm_frame = ttk.LabelFrame(main, text="Alarm & Monitoring Settings", padding=10)
        alarm_frame.pack(fill='x', pady=5)
        
        self._delay_time = tk.StringVar(value='5')
        self._monitor_phone = tk.StringVar()
        
        ttk.Label(alarm_frame, text="Alarm Delay Time (minutes):").grid(row=0, column=0, sticky='e', padx=5, pady=2)
        delay_entry = ttk.Entry(alarm_frame, textvariable=self._delay_time, width=10)
        delay_entry.grid(row=0, column=1, sticky='w', pady=2)
        ttk.Label(alarm_frame, text="(Minimum 5 minutes)", font=('Arial', 8)).grid(row=0, column=2, sticky='w', padx=5)
        
        ttk.Label(alarm_frame, text="Monitoring Service Phone:").grid(row=1, column=0, sticky='e', padx=5, pady=2)
        ttk.Entry(alarm_frame, textvariable=self._monitor_phone, width=20).grid(row=1, column=1, sticky='w', pady=2)
        
        # Buttons
        btn_frame = ttk.Frame(main)
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="Save All Settings", command=self._save_all, width=20).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Reset to Defaults", command=self._reset_defaults, width=20).pack(side='left', padx=5)
        
        # Status message
        self._status = ttk.Label(main, text="", font=('Arial', 10))
        self._status.pack(pady=5)

    def _validate_inputs(self) -> tuple:
        """Validate all inputs. Returns (success, error_message)."""
        errors = []
        
        # Web passwords
        if self._web_pw1.get():
            if len(self._web_pw1.get()) < 8:
                errors.append("Web Password 1 must be at least 8 characters")
            elif self._web_pw1.get() != self._web_pw1_confirm.get():
                errors.append("Web Password 1 confirmation doesn't match")
        
        if self._web_pw2.get():
            if len(self._web_pw2.get()) < 8:
                errors.append("Web Password 2 must be at least 8 characters")
            elif self._web_pw2.get() != self._web_pw2_confirm.get():
                errors.append("Web Password 2 confirmation doesn't match")
        
        # Master password
        if self._master_pw.get():
            if not self._master_pw.get().isdigit() or len(self._master_pw.get()) != 4:
                errors.append("Master password must be exactly 4 digits")
            elif self._master_pw.get() != self._master_pw_confirm.get():
                errors.append("Master password confirmation doesn't match")
        
        # Guest password (optional)
        if self._guest_pw.get():
            if not self._guest_pw.get().isdigit() or len(self._guest_pw.get()) != 4:
                errors.append("Guest password must be exactly 4 digits")
            elif self._guest_pw.get() != self._guest_pw_confirm.get():
                errors.append("Guest password confirmation doesn't match")
        
        # Delay time
        try:
            delay = int(self._delay_time.get())
            if delay < 5:
                errors.append("Delay time must be at least 5 minutes")
        except ValueError:
            errors.append("Delay time must be a number")
        
        # Phone number
        if not self._monitor_phone.get().strip():
            errors.append("Monitoring service phone number is required")
        
        if errors:
            return False, "\n".join(errors)
        return True, ""

    def _save_all(self):
        """Save all settings to system."""
        valid, error = self._validate_inputs()
        if not valid:
            self._status.config(text=error, foreground='red')
            messagebox.showerror("Validation Error", error)
            return
        
        # Build settings dictionary
        settings = {
            'delay_time': int(self._delay_time.get()),
            'monitor_phone': self._monitor_phone.get().strip()
        }
        
        # Add passwords if provided
        if self._web_pw1.get():
            settings['web_password1'] = self._web_pw1.get()
        if self._web_pw2.get():
            settings['web_password2'] = self._web_pw2.get()
        if self._master_pw.get():
            settings['master_password'] = self._master_pw.get()
        if self._guest_pw.get():
            settings['guest_password'] = self._guest_pw.get()
        
        # Send to system
        res = self.send_to_system('configure_system_settings', **settings)
        
        if res.get('success'):
            self._status.config(text="Settings saved successfully", foreground='green')
            messagebox.showinfo("Success", "All settings have been saved")
            # Clear password fields after save
            self._clear_password_fields()
        else:
            self._status.config(text="Failed to save settings", foreground='red')
            messagebox.showerror("Error", res.get('message', 'Failed to save settings'))

    def _clear_password_fields(self):
        """Clear all password entry fields."""
        for var in [self._web_pw1, self._web_pw1_confirm, self._web_pw2, self._web_pw2_confirm,
                    self._master_pw, self._master_pw_confirm, self._guest_pw, self._guest_pw_confirm]:
            var.set('')

    def _reset_defaults(self):
        """Reset to default values."""
        if messagebox.askyesno("Confirm", "Reset all settings to defaults?"):
            self._delay_time.set('5')
            self._monitor_phone.set('911')
            self._clear_password_fields()
            self._status.config(text="Reset to defaults (not saved yet)", foreground='orange')

    def on_show(self):
        """Load current settings when page is shown."""
        res = self.send_to_system('get_system_settings')
        if res.get('success'):
            data = res.get('data', {})
            self._delay_time.set(str(data.get('delay_time', 5)))
            self._monitor_phone.set(data.get('monitor_phone', ''))
        self._clear_password_fields()
        self._status.config(text="")
