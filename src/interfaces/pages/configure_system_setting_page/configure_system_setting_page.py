"""ConfigureSystemSettingPage - System settings configuration (SRS V.1.c)"""
import tkinter as tk
from tkinter import ttk, messagebox
from ...components.page import Page
from .web_password_ui import create_web_password_section
from .control_panel_password_ui import create_control_panel_password_section
from .alarm_monitoring_ui import create_alarm_monitoring_section
from .setting_buttons_ui import create_buttons_section
from .system_settings_validator import SystemSettingsValidator
from .settings_saver import save_all_settings


class ConfigureSystemSettingPage(Page):
    """Configure system settings including passwords, delay, phone."""

    def _build_ui(self):
        self._create_header("System Settings", back_page='major_function')

        main = ttk.Frame(self._frame)
        main.pack(fill='both', expand=True, padx=20, pady=10)

        # Web password section
        (self._web_pw1_current, self._web_pw1, self._web_pw1_confirm,
         self._web_pw2_current, self._web_pw2, self._web_pw2_confirm) = \
            create_web_password_section(main)

        # Control panel password section
        (self._master_pw_current, self._master_pw, self._master_pw_confirm,
         self._guest_pw_current, self._guest_pw, self._guest_pw_confirm) = \
            create_control_panel_password_section(main)

        # Alarm & monitoring section
        self._delay_time, self._monitor_phone = \
            create_alarm_monitoring_section(main)

        # Buttons and status
        self._status = create_buttons_section(
            main, self._save_all, self._reset_defaults)

        self._validator = SystemSettingsValidator()

    def _save_all(self):
        save_all_settings(
            self,
            self._web_pw1_current, self._web_pw1, self._web_pw1_confirm,
            self._web_pw2_current, self._web_pw2, self._web_pw2_confirm,
            self._master_pw_current, self._master_pw, self._master_pw_confirm,
            self._guest_pw_current, self._guest_pw, self._guest_pw_confirm,
            self._delay_time, self._monitor_phone,
            self._status, self._clear_password_fields, self._validator
        )

    def _clear_password_fields(self):
        for var in [self._web_pw1_current, self._web_pw1, self._web_pw1_confirm,
                    self._web_pw2_current, self._web_pw2, self._web_pw2_confirm,
                    self._master_pw_current, self._master_pw, self._master_pw_confirm,
                    self._guest_pw_current, self._guest_pw, self._guest_pw_confirm]:
            var.set('')

    def _reset_defaults(self):
        if not messagebox.askyesno("Confirm", "Reset all settings to defaults?"):
            return
        res = self.send_to_system('reset_system_settings')
        if res.get('success'):
            data = res.get('data', {})
            self._delay_time.set(str(data.get('delay_time', 5)))
            self._monitor_phone.set(data.get('monitor_phone', ''))
            self._clear_password_fields()
            self._status.config(
                text="Defaults restored (including control panel PINs)",
                foreground='green'
            )
            messagebox.showinfo(
                "Reset Complete",
                "Settings and control panel passwords have been restored to defaults.\n"
                "Master: 1234, Guest: 5678"
            )
        else:
            message = res.get('message', 'Failed to reset settings')
            self._status.config(text=message, foreground='red')
            messagebox.showerror("Error", message)

    def on_show(self):
        res = self.send_to_system('get_system_settings')
        if res.get('success'):
            data = res.get('data', {})
            self._delay_time.set(str(data.get('delay_time', 5)))
            self._monitor_phone.set(data.get('monitor_phone', ''))
        self._clear_password_fields()
        self._status.config(text="")

