"""
DeviceSensorTester - Base class for sensor devices from TA
"""
from abc import ABC, abstractmethod


class DeviceSensorTester(ABC):
    """Abstract base class for sensor devices with testing capability."""
    
    # Class-level sensor tracking
    head_windoor_sensor = None
    head_motion_detector = None
    id_sequence_windoor = 0
    id_sequence_motion = 0
    
    def __init__(self):
        self.next_sensor = None
        self.sensor_id = 0
    
    @abstractmethod
    def intrude(self):
        """Simulate intrusion/detection."""
        pass
    
    @abstractmethod
    def release(self):
        """Release intrusion/detection state."""
        pass
