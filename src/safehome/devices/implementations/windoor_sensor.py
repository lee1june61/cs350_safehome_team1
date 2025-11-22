"""Window/Door sensor device implementation for SafeHome system.

Integrated from virtual_device_v3/device/device_windoor_sensor.py
Removed DeviceSensorTester dependency for clean integration.
"""

from ..interfaces.sensor import InterfaceSensor


class DeviceWinDoorSensor(InterfaceSensor):
    """Window/Door sensor device."""
    
    # Class-level ID counter
    _id_counter = 0
    
    def __init__(self, sensor_id=None):
        """Initialize window/door sensor.
        
        Args:
            sensor_id: Optional sensor ID. If not provided, auto-increments.
        """
        super().__init__()
        
        # Assign unique ID
        if sensor_id is None:
            DeviceWinDoorSensor._id_counter += 1
            self.sensor_id = DeviceWinDoorSensor._id_counter
        else:
            self.sensor_id = sensor_id
        
        # Initialize state
        self.opened = False
        self.armed = False
    
    def intrude(self):
        """Simulate opening the window/door."""
        self.opened = True
    
    def release(self):
        """Simulate closing the window/door."""
        self.opened = False
    
    def get_id(self):
        """Get the sensor ID."""
        return self.sensor_id
    
    def read(self):
        """Read the sensor state.
        
        Returns:
            bool: True if armed and door/window is open, False otherwise.
        """
        if self.armed:
            return self.opened
        return False
    
    def arm(self):
        """Enable the sensor."""
        self.armed = True
    
    def disarm(self):
        """Disable the sensor."""
        self.armed = False
    
    def test_armed_state(self):
        """Test if the sensor is enabled.
        
        Returns:
            bool: True if armed, False otherwise.
        """
        return self.armed
