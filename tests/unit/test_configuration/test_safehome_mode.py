"""Unit tests for SafeHomeMode class."""

import unittest
from src.configuration.safehome_mode import SafeHomeMode
from src.configuration.exceptions import ValidationError


class TestSafeHomeMode(unittest.TestCase):
    """Test SafeHomeMode sensor configuration class."""

    def test_mode_creation_basic(self):
        """Test basic mode creation."""
        mode = SafeHomeMode(mode_id=1, mode_name="HOME")
        
        self.assertEqual(mode.mode_id, 1)
        self.assertEqual(mode.mode_name, "HOME")
        self.assertEqual(mode.sensor_ids, [])
        self.assertTrue(mode.is_active)
        self.assertEqual(mode.description, "")

    def test_mode_creation_with_sensors(self):
        """Test mode creation with sensor list."""
        mode = SafeHomeMode(
            mode_id=2,
            mode_name="AWAY",
            sensor_ids=[1, 2, 3],
            is_active=True,
            description="All sensors active",
        )
        
        self.assertEqual(mode.sensor_ids, [1, 2, 3])
        self.assertEqual(mode.description, "All sensors active")

    def test_add_sensor(self):
        """Test adding sensor to mode."""
        mode = SafeHomeMode(mode_id=1, mode_name="HOME")
        
        result = mode.add_sensor(10)
        self.assertTrue(result)
        self.assertIn(10, mode.sensor_ids)

    def test_add_duplicate_sensor(self):
        """Test that adding duplicate sensor returns False."""
        mode = SafeHomeMode(mode_id=1, mode_name="HOME", sensor_ids=[10])
        
        result = mode.add_sensor(10)
        self.assertFalse(result)
        self.assertEqual(mode.sensor_ids.count(10), 1)

    def test_add_multiple_sensors(self):
        """Test adding multiple sensors."""
        mode = SafeHomeMode(mode_id=1, mode_name="HOME")
        
        mode.add_sensor(1)
        mode.add_sensor(2)
        mode.add_sensor(3)
        
        self.assertEqual(len(mode.sensor_ids), 3)
        self.assertEqual(mode.sensor_ids, [1, 2, 3])

    def test_remove_sensor(self):
        """Test removing sensor from mode."""
        mode = SafeHomeMode(mode_id=1, mode_name="HOME", sensor_ids=[1, 2, 3])
        
        result = mode.remove_sensor(2)
        self.assertTrue(result)
        self.assertNotIn(2, mode.sensor_ids)
        self.assertEqual(mode.sensor_ids, [1, 3])

    def test_remove_nonexistent_sensor(self):
        """Test that removing nonexistent sensor returns False."""
        mode = SafeHomeMode(mode_id=1, mode_name="HOME", sensor_ids=[1, 2])
        
        result = mode.remove_sensor(99)
        self.assertFalse(result)
        self.assertEqual(mode.sensor_ids, [1, 2])

    def test_clear_sensors(self):
        """Test clearing all sensors from mode."""
        mode = SafeHomeMode(mode_id=1, mode_name="HOME", sensor_ids=[1, 2, 3, 4])
        
        mode.clear_sensors()
        self.assertEqual(mode.sensor_ids, [])
        self.assertEqual(mode.get_sensor_count(), 0)

    def test_has_sensor(self):
        """Test checking if mode has specific sensor."""
        mode = SafeHomeMode(mode_id=1, mode_name="HOME", sensor_ids=[5, 10, 15])
        
        self.assertTrue(mode.has_sensor(10))
        self.assertFalse(mode.has_sensor(20))

    def test_get_sensor_count(self):
        """Test getting sensor count."""
        mode = SafeHomeMode(mode_id=1, mode_name="HOME")
        self.assertEqual(mode.get_sensor_count(), 0)
        
        mode.add_sensor(1)
        mode.add_sensor(2)
        self.assertEqual(mode.get_sensor_count(), 2)

    def test_validate_valid_mode(self):
        """Test validation of valid mode."""
        mode = SafeHomeMode(mode_id=1, mode_name="HOME")
        self.assertTrue(mode.validate())

    def test_validate_empty_name(self):
        """Test validation fails for empty mode name."""
        mode = SafeHomeMode(mode_id=1, mode_name="")
        
        with self.assertRaises(ValidationError) as cm:
            mode.validate()
        self.assertIn("Mode name", str(cm.exception))

    def test_validate_negative_id(self):
        """Test validation fails for negative mode ID."""
        mode = SafeHomeMode(mode_id=-1, mode_name="HOME")
        
        with self.assertRaises(ValidationError) as cm:
            mode.validate()
        self.assertIn("Mode ID", str(cm.exception))

    def test_to_dict(self):
        """Test serialization to dictionary."""
        mode = SafeHomeMode(
            mode_id=3,
            mode_name="OVERNIGHT",
            sensor_ids=[1, 2, 3],
            is_active=True,
            description="Night mode",
        )
        
        data = mode.to_dict()
        
        self.assertIsInstance(data, dict)
        self.assertEqual(data["mode_id"], 3)
        self.assertEqual(data["mode_name"], "OVERNIGHT")
        self.assertEqual(data["sensor_ids"], [1, 2, 3])
        self.assertTrue(data["is_active"])
        self.assertEqual(data["description"], "Night mode")

    def test_from_dict(self):
        """Test deserialization from dictionary."""
        data = {
            "mode_id": 4,
            "mode_name": "EXTENDED",
            "sensor_ids": [10, 20, 30],
            "is_active": False,
            "description": "Long absence",
        }
        
        mode = SafeHomeMode.from_dict(data)
        
        self.assertEqual(mode.mode_id, 4)
        self.assertEqual(mode.mode_name, "EXTENDED")
        self.assertEqual(mode.sensor_ids, [10, 20, 30])
        self.assertFalse(mode.is_active)
        self.assertEqual(mode.description, "Long absence")

    def test_from_dict_with_json_string_sensors(self):
        """Test deserialization when sensor_ids is JSON string."""
        data = {
            "mode_id": 1,
            "mode_name": "HOME",
            "sensor_ids": "[1, 2, 3]",  # JSON string
        }
        
        mode = SafeHomeMode.from_dict(data)
        self.assertEqual(mode.sensor_ids, [1, 2, 3])

    def test_from_dict_empty_sensor_string(self):
        """Test deserialization with empty sensor string."""
        data = {
            "mode_id": 1,
            "mode_name": "HOME",
            "sensor_ids": "",
        }
        
        mode = SafeHomeMode.from_dict(data)
        self.assertEqual(mode.sensor_ids, [])

    def test_from_dict_default_values(self):
        """Test deserialization with missing optional fields."""
        data = {
            "mode_id": 1,
            "mode_name": "HOME",
        }
        
        mode = SafeHomeMode.from_dict(data)
        self.assertEqual(mode.sensor_ids, [])
        self.assertTrue(mode.is_active)
        self.assertEqual(mode.description, "")

    def test_roundtrip_serialization(self):
        """Test that serialization and deserialization preserve data."""
        original = SafeHomeMode(
            mode_id=2,
            mode_name="AWAY",
            sensor_ids=[5, 10, 15, 20],
            is_active=True,
            description="All zones armed",
        )
        
        data = original.to_dict()
        restored = SafeHomeMode.from_dict(data)
        
        self.assertEqual(restored.mode_id, original.mode_id)
        self.assertEqual(restored.mode_name, original.mode_name)
        self.assertEqual(restored.sensor_ids, original.sensor_ids)
        self.assertEqual(restored.is_active, original.is_active)
        self.assertEqual(restored.description, original.description)

    def test_mode_types(self):
        """Test creating different mode types."""
        modes = ["HOME", "AWAY", "OVERNIGHT", "EXTENDED", "GUEST"]
        
        for idx, name in enumerate(modes, start=1):
            mode = SafeHomeMode(mode_id=idx, mode_name=name)
            self.assertEqual(mode.mode_name, name)
            self.assertEqual(mode.mode_id, idx)

    def test_is_active_flag(self):
        """Test is_active flag functionality."""
        mode = SafeHomeMode(mode_id=1, mode_name="HOME", is_active=True)
        self.assertTrue(mode.is_active)
        
        mode.is_active = False
        self.assertFalse(mode.is_active)


if __name__ == "__main__":
    unittest.main()

