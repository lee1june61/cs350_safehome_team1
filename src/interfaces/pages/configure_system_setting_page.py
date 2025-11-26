"""ConfigureSystemSettingPage - System settings configuration"""
import tkinter as tk
from tkinter import ttk
from ..components.page import Page


class ConfigureSystemSettingPage(Page):
    """Page for system settings configuration"""
    
    def _build_ui(self) -> None:
        self._create_header("System Settings", back_page='major_function')
        
        # Scrollable form
        canvas = tk.Canvas(self._frame)
        scrollbar = ttk.Scrollbar(self._frame, orient='vertical', command=canvas.yview)
        form = ttk.Frame(canvas)
        form.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=form, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side='left', fill='both', expand=True, padx=20)
        scrollbar.pack(side='right', fill='y')
        
        self._fields = {}
        row = 0
        
        # Delay time
        ttk.Label(form, text="Delay Time (minutes):").grid(row=row, column=0, sticky='w', pady=5)
        self._fields['delay_time'] = tk.StringVar()
        ttk.Entry(form, textvariable=self._fields['delay_time'], width=25).grid(
            row=row, column=1, pady=5, padx=(10, 0))
        row += 1
        
        ttk.Separator(form).grid(row=row, column=0, columnspan=2, sticky='ew', pady=10)
        row += 1
        
        # Passwords
        for key, label in [
            ('master_password', 'Master Password (4 digits):'),
            ('master_confirm', 'Confirm Master:'),
            ('guest_password', 'Guest Password (optional):'),
            ('guest_confirm', 'Confirm Guest:'),
            ('web_password1', 'Web Password 1 (8 chars):'),
            ('web1_confirm', 'Confirm Web 1:'),
            ('web_password2', 'Web Password 2 (8 chars):'),
            ('web2_confirm', 'Confirm Web 2:'),
        ]:
            ttk.Label(form, text=label).grid(row=row, column=0, sticky='w', pady=3)
            self._fields[key] = tk.StringVar()
            ttk.Entry(form, textvariable=self._fields[key], show='*', width=25).grid(
                row=row, column=1, pady=3, padx=(10, 0))
            row += 1
        
        ttk.Separator(form).grid(row=row, column=0, columnspan=2, sticky='ew', pady=10)
        row += 1
        
        # Phone number
        ttk.Label(form, text="Phone Number:").grid(row=row, column=0, sticky='w', pady=5)
        self._fields['phone_number'] = tk.StringVar()
        ttk.Entry(form, textvariable=self._fields['phone_number'], width=25).grid(
            row=row, column=1, pady=5, padx=(10, 0))
        row += 1
        
        ttk.Button(form, text="Save Settings", command=self._save, 
                  width=20).grid(row=row, column=0, columnspan=2, pady=20)
    
    def _save(self) -> None:
        try:
            delay = int(self._fields['delay_time'].get()) if self._fields['delay_time'].get() else None
        except ValueError:
            return self._show_message("Error", "Invalid delay time", 'error')
        
        params = {k: v.get() or None for k, v in self._fields.items()}
        params['delay_time'] = delay
        
        response = self.send_to_system('configure_system_settings', **params)
        if response.get('success'):
            self._show_message("Success", "Settings saved")
        else:
            self._show_message("Error", response.get('message', 'Failed'), 'error')
    
    def on_show(self) -> None:
        response = self.send_to_system('get_system_settings')
        if response.get('success'):
            data = response.get('data', {})
            self._fields['delay_time'].set(str(data.get('delay_time', 5)))
            self._fields['phone_number'].set(data.get('phone_number', ''))
