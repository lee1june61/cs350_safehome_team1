"""
Password helpers for SafeHomeCamera.
"""

from __future__ import annotations

from typing import Optional

from ...utils.exceptions import CameraPasswordError
from .safehome_camera_base import SafeHomeCameraBase


class SafeHomeCameraPasswordMixin(SafeHomeCameraBase):
    """Set and read camera passwords."""

    def set_password(self, password: str) -> bool:
        with self._lock:
            if not password:
                raise CameraPasswordError("Password cannot be empty")
            self.password = password
            self._has_password = True
            return True

    def get_password(self) -> Optional[str]:
        with self._lock:
            return self.password

    def has_password(self) -> bool:
        with self._lock:
            return self._has_password

    def clear_password(self) -> bool:
        with self._lock:
            self.password = None
            self._has_password = False
            return True

    def delete_password(self) -> bool:
        """SDS alias used by legacy components."""
        return self.clear_password()
