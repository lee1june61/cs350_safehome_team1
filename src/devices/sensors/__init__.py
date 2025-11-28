"""Sensor devices package."""

from .motion_sensor import CustomMotionDetector as DeviceMotionDetector
from .window_door_sensor import CustomWinDoorSensor as DeviceWinDoorSensor

__all__ = ["DeviceMotionDetector", "DeviceWinDoorSensor"]
