import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any, Callable

def save_all_settings(
    page_instance: Any, # Use Any to avoid circular import with Page
    web_pw1_current: tk.StringVar, web_pw1: tk.StringVar, web_pw1_confirm: tk.StringVar,
    web_pw2_current: tk.StringVar, web_pw2: tk.StringVar, web_pw2_confirm: tk.StringVar,
    master_pw_current: tk.StringVar, master_pw: tk.StringVar, master_pw_confirm: tk.StringVar,
    guest_pw_current: tk.StringVar, guest_pw: tk.StringVar, guest_pw_confirm: tk.StringVar,
    delay_time: tk.StringVar, monitor_phone: tk.StringVar,
    status_label: ttk.Label,
    clear_password_fields_func: Callable[[], None],
    validator: Any # SystemSettingsValidator instance
) -> None:
    """
    Handles saving all system settings.
    """
    valid, error = validator.validate(
        web_pw1_current, web_pw1, web_pw1_confirm,
        web_pw2_current, web_pw2, web_pw2_confirm,
        master_pw_current, master_pw, master_pw_confirm,
        guest_pw_current, guest_pw, guest_pw_confirm,
        delay_time, monitor_phone
    )
    if not valid:
        status_label.config(text=error, foreground='red')
        messagebox.showerror("Validation Error", error)
        return
    
    # Build settings dictionary
    settings = {
        'delay_time': int(delay_time.get()),
        'monitor_phone': monitor_phone.get().strip()
    }
    
    # Add passwords if provided
    if web_pw1.get():
        settings['web_password1'] = web_pw1.get()
    if web_pw2.get():
        settings['web_password2'] = web_pw2.get()
    if master_pw.get():
        settings['master_password'] = master_pw.get()
    if guest_pw.get():
        settings['guest_password'] = guest_pw.get()
    
    # Send to system
    res = page_instance.send_to_system('configure_system_settings', **settings)
    
    if res.get('success'):
        status_label.config(text="Settings saved successfully", foreground='green')
        messagebox.showinfo("Success", "All settings have been saved")
        # Clear password fields after save
        clear_password_fields_func()
    else:
        message = res.get('message', 'Failed to save settings')
        status_label.config(text=message, foreground='red')
        messagebox.showerror("Error", message)
