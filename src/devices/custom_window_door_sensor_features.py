"""Feature mixins for custom window/door sensor."""

from __future__ import annotations


class WinDoorSensorStatusMixin:
    """Status helpers for window/door sensor."""

    sensor_id: int
    _location: str
    _subtype: str
    _battery_level: float
    armed: bool
    opened: bool

    def get_location(self) -> str:
        return self._location

    def get_type(self) -> str:
        return f"{self._subtype}_sensor"

    def get_sensor_id(self) -> int:
        return self.sensor_id

    def get_subtype(self) -> str:
        return self._subtype

    def get_battery_level(self) -> int:
        if self.armed and self._battery_level > 0:
            self._battery_level -= 0.005
        return max(0, int(self._battery_level))

    def is_open(self) -> bool:
        return self.opened

    def is_closed(self) -> bool:
        return not self.opened

    def can_arm(self) -> bool:
        return not self.opened

    def get_status(self) -> dict:
        return {
            "id": f"S{self.sensor_id}",
            "type": self.get_type(),
            "subtype": self._subtype,
            "location": self._location,
            "armed": self.armed,
            "is_open": self.opened,
            "triggered": self.read(),
            "battery": self.get_battery_level(),
            "can_arm": self.can_arm(),
        }

    def __repr__(self):
        status = "ARMED" if self.armed else "DISARMED"
        state = "OPEN" if self.opened else "CLOSED"
        trigger = " [TRIGGERED]" if self.read() else ""
        return (
            f"CustomWinDoorSensor(id={self.sensor_id}, type={self._subtype}, "
            f"location='{self._location}', state={state}, status={status}{trigger})"
        )

