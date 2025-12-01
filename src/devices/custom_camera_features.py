"""Feature mixins for custom camera."""

from __future__ import annotations


class CameraPasswordMixin:
    """Password management for cameras."""

    _password: str | None
    _enabled: bool

    def set_password(self, password: str):
        self._password = password

    def get_password(self) -> str | None:
        return self._password

    def clear_password(self):
        self._password = None

    def has_password(self) -> bool:
        return self._password is not None

    def verify_password(self, password: str) -> bool:
        if self._password is None:
            return True
        return self._password == password


class CameraStateMixin:
    """State management for cameras."""

    _enabled: bool
    _location: str

    def set_location(self, location: str):
        self._location = location

    def get_location(self) -> str:
        return self._location

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    def is_enabled(self) -> bool:
        return self._enabled

    def get_status(self) -> dict:
        return {
            "id": f"C{self.camera_id}",
            "location": self._location,
            "enabled": self._enabled,
            "password": self.has_password(),
            "pan": self.pan,
            "zoom": self.zoom,
        }


class CameraTiltMixin:
    """Tilt control for cameras."""

    tilt: int
    _enabled: bool
    _lock: object

    def tilt_up(self) -> bool:
        with self._lock:
            if not self._enabled or self.tilt >= 5:
                return False
            self.tilt += 1
            return True

    def tilt_down(self) -> bool:
        with self._lock:
            if not self._enabled or self.tilt <= -5:
                return False
            self.tilt -= 1
            return True

