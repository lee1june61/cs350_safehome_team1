"""Alarm lifecycle helpers."""

from __future__ import annotations

from typing import Dict, Optional

from ..logging.system_logger import SystemLogger


class AlarmService:
    def __init__(self, logger: SystemLogger, delay_time: int, monitor_phone: str):
        self._logger = logger
        self._delay_time = delay_time
        self._monitor_phone = monitor_phone
        self._state = "OFF"

    # ------------------------------------------------------------------ #
    def turn_on(self):
        self._state = "READY"

    def turn_off(self):
        self._state = "OFF"

    def panic(self):
        self._state = "ALARM"
        self._logger.add_event("PANIC", f"Emergency call to {self._monitor_phone}")
        return {"success": True, "message": f"Calling {self._monitor_phone}"}

    def trigger(self, sensor_info: str, zone_info: str, user: Optional[str]) -> Dict:
        self._state = "ALARM"
        self._logger.add_event(
            "INTRUSION",
            f"Sensor: {sensor_info}, Zone: {zone_info}",
            user=user,
        )
        return {
            "success": True,
            "alarm": True,
            "sensor": sensor_info,
            "zone": zone_info,
            "delay_time": self._delay_time,
            "monitor_phone": self._monitor_phone,
        }

    def clear(self):
        self._state = "READY"
        return {"success": True}

    def status_payload(self):
        return {
            "state": self._state,
            "alarm_active": self._state == "ALARM",
        }

    def get_alarm_status(self, latest_log) -> Dict:
        is_alarm = self._state == "ALARM"
        sensor_id = "Unknown"
        zone_name = "Unknown"
        alarm_type = "INTRUSION"

        if is_alarm and latest_log:
            log = latest_log[0]
            if log.event_type == "INTRUSION":
                detail = log.description or ""
                if "Sensor:" in detail and "Zone:" in detail:
                    parts = detail.split("Zone:")
                    if len(parts) == 2:
                        zone_name = parts[1].strip()
                        sensor_part = parts[0].replace("Sensor:", "").strip()
                        if "(" in sensor_part:
                            sensor_id = sensor_part.split("(")[0].strip()

        return {
            "success": True,
            "data": {
                "alarm_active": is_alarm,
                "sensor_id": sensor_id,
                "zone_name": zone_name,
                "alarm_type": alarm_type,
            },
        }

    def update_from_settings(self, delay_time: int, monitor_phone: str):
        self._delay_time = delay_time
        self._monitor_phone = monitor_phone

    @property
    def state(self) -> str:
        return self._state


