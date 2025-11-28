import tkinter as tk
from typing import List, Tuple

class SystemSettingsValidator:
    """
    Handles validation logic for system settings input fields.
    """
    def validate(self, 
                 web_pw1: tk.StringVar, web_pw1_confirm: tk.StringVar,
                 web_pw2: tk.StringVar, web_pw2_confirm: tk.StringVar,

                 master_pw: tk.StringVar, master_pw_confirm: tk.StringVar,
                 guest_pw: tk.StringVar, guest_pw_confirm: tk.StringVar,

                 delay_time: tk.StringVar, monitor_phone: tk.StringVar) -> Tuple[bool, str]:
        
        errors: List[str] = []
        
        # Web passwords
        if web_pw1.get():
            if len(web_pw1.get()) < 8:
                errors.append("Web Password 1 must be at least 8 characters")
            elif web_pw1.get() != web_pw1_confirm.get():
                errors.append("Web Password 1 confirmation doesn't match")
        
        if web_pw2.get():
            if len(web_pw2.get()) < 8:
                errors.append("Web Password 2 must be at least 8 characters")
            elif web_pw2.get() != web_pw2_confirm.get():
                errors.append("Web Password 2 confirmation doesn't match")
        
        # Master password
        if master_pw.get():
            if not master_pw.get().isdigit() or len(master_pw.get()) != 4:
                errors.append("Master password must be exactly 4 digits")
            elif master_pw.get() != master_pw_confirm.get():
                errors.append("Master password confirmation doesn't match")
        
        # Guest password (optional)
        if guest_pw.get():
            if not guest_pw.get().isdigit() or len(guest_pw.get()) != 4:
                errors.append("Guest password must be exactly 4 digits")
            elif guest_pw.get() != guest_pw_confirm.get():
                errors.append("Guest password confirmation doesn't match")
        
        # Delay time
        try:
            delay = int(delay_time.get())
            if delay < 5:
                errors.append("Delay time must be at least 5 minutes")
        except ValueError:
            errors.append("Delay time must be a number")
        
        # Phone number
        if not monitor_phone.get().strip():
            errors.append("Monitoring service phone number is required")
        
        if errors:
            return False, "\n".join(errors)
        return True, ""
