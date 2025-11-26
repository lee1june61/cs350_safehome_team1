"""MajorFunctionPage - Main function selection screen"""
import tkinter as tk
from tkinter import ttk
from ..components.page import Page


class MajorFunctionPage(Page):
    """Main page showing major functions and system status"""
    
    def _build_ui(self) -> None:
        header = ttk.Frame(self._frame)
        header.pack(fill='x', padx=20, pady=20)
        
        ttk.Label(header, text="SafeHome", font=('Arial', 24, 'bold')).pack(side='left')
        
        self._status_label = ttk.Label(header, text="● DISARMED", 
                                       font=('Arial', 12), foreground='green')
        self._status_label.pack(side='right')
        
        content = ttk.Frame(self._frame)
        content.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Status display
        left = ttk.LabelFrame(content, text="System Status", padding=15)
        left.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        self._armed_label = ttk.Label(left, text="Armed: No")
        self._armed_label.pack(anchor='w')
        self._mode_label = ttk.Label(left, text="Mode: None")
        self._mode_label.pack(anchor='w')
        self._alarm_label = ttk.Label(left, text="Alarm: Silent")
        self._alarm_label.pack(anchor='w')
        ttk.Separator(left).pack(fill='x', pady=10)
        self._sensor_label = ttk.Label(left, text="Sensors: -")
        self._sensor_label.pack(anchor='w')
        self._camera_label = ttk.Label(left, text="Cameras: -")
        self._camera_label.pack(anchor='w')
        
        # Function buttons
        right = ttk.Frame(content)
        right.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        for frame_name, buttons in [
            ("Security", [("Security Management", 'security')]),
            ("Surveillance", [("Camera Management", 'surveillance')]),
            ("Configuration", [("System Settings", 'configure_system_setting')]),
        ]:
            f = ttk.LabelFrame(right, text=frame_name, padding=10)
            f.pack(fill='x', pady=(0, 10))
            for text, page in buttons:
                ttk.Button(f, text=text, command=lambda p=page: self.navigate_to(p),
                          width=25).pack(pady=5)
        
        ttk.Separator(right).pack(fill='x', pady=10)
        ttk.Button(right, text="Logout", command=self._logout, width=25).pack(pady=5)
    
    def _logout(self) -> None:
        self.send_to_system('logout')
        self.navigate_to('login')
    
    def on_show(self) -> None:
        self.refresh()
    
    def refresh(self) -> None:
        response = self.send_to_system('get_status')
        if response.get('success'):
            data = response.get('data', {})
            armed = data.get('armed', False)
            
            if armed:
                self._status_label.config(text="● ARMED", foreground='red')
                self._armed_label.config(text="Armed: Yes")
            else:
                self._status_label.config(text="● DISARMED", foreground='green')
                self._armed_label.config(text="Armed: No")
            
            self._mode_label.config(text=f"Mode: {data.get('mode') or 'None'}")
            alarm = data.get('alarm_active', False)
            self._alarm_label.config(text=f"Alarm: {'ACTIVE' if alarm else 'Silent'}",
                                    foreground='red' if alarm else 'black')
            self._sensor_label.config(
                text=f"Sensors: {data.get('active_sensors', 0)}/{data.get('sensor_count', 0)}")
            self._camera_label.config(
                text=f"Cameras: {data.get('enabled_cameras', 0)}/{data.get('camera_count', 0)}")
