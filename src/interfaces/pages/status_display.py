"""
StatusDisplay - Status display logic for major function page

Single Responsibility: Handle status display updates.
"""
from typing import Dict, Any


class StatusDisplayMixin:
    """Mixin providing status display handlers"""
    
    def _update_header_status(self, armed: bool) -> None:
        """Update header status indicator"""
        if armed:
            self._status_label.config(text="● ARMED", foreground='red')
        else:
            self._status_label.config(text="● DISARMED", foreground='green')
    
    def _update_status_panel(self, data: Dict[str, Any]) -> None:
        """Update status panel labels"""
        armed = data.get('armed', False)
        mode = data.get('mode')
        alarm = data.get('alarm_active', False)
        
        self._armed_label.config(text=f"Armed: {'Yes' if armed else 'No'}")
        self._mode_label.config(text=f"Mode: {mode or 'None'}")
        self._alarm_label.config(
            text=f"Alarm: {'ACTIVE' if alarm else 'Silent'}",
            foreground='red' if alarm else 'black'
        )
        
        active = data.get('active_sensors', 0)
        total = data.get('sensor_count', 0)
        self._sensor_label.config(text=f"Sensors: {active}/{total}")
        
        enabled = data.get('enabled_cameras', 0)
        cam_total = data.get('camera_count', 0)
        self._camera_label.config(text=f"Cameras: {enabled}/{cam_total}")
