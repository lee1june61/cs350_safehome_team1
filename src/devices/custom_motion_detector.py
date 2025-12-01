"""Custom motion detector built on top of the TA virtual device."""

import random
import time

from ..virtual_devices.device_motion_detector import DeviceMotionDetector as BaseMotionDetector
from .custom_motion_detector_features import MotionDetectorSettingsMixin, MotionDetectorStatusMixin


class CustomMotionDetector(MotionDetectorSettingsMixin, MotionDetectorStatusMixin, BaseMotionDetector):
    """Detailed virtual motion detector with simulation helpers."""

    def __init__(self, location: str, sensor_id: int):
        super().__init__()
        self.sensor_id = sensor_id
        self._location = location
        self._triggered = False
        self._battery_level = 100.0
        self._last_trigger_time = 0
        self._detection_range = 5.0
        self._sensitivity = 0.5

    def read(self) -> bool:
        """Check if motion is detected."""
        if not self.armed:
            return False
        current_time = time.time()
        if current_time - self._last_trigger_time < 5:
            return self.detected
        if random.random() < (0.1 * self._sensitivity):
            self._triggered = True
            self._last_trigger_time = current_time
            self.intrude()
        else:
            self._triggered = False
            self.release()
        return self.detected

    def arm(self):
        super().arm()
        self._triggered = False

    def disarm(self):
        super().disarm()
        self._triggered = False

    def reset_trigger(self):
        """Reset triggered state."""
        self._triggered = False
        self.release()
        self._last_trigger_time = 0

    def force_trigger(self):
        """Force trigger for testing purposes."""
        if self.armed:
            self._triggered = True
            self._last_trigger_time = time.time()
            self.intrude()
