"""Unit tests for SafetyZone class."""

import unittest
from src.configuration.safety_zone import SafetyZone
from src.configuration.exceptions import ValidationError


class TestSafetyZone(unittest.TestCase):
    """Test SafetyZone logical grouping class."""

    def test_zone_creation_basic(self):
        """Test basic zone creation."""
        zone = SafetyZone(zone_id=1, zone_name="First Floor")

        self.assertEqual(zone.zone_id, 1)
        self.assertEqual(zone.zone_name, "First Floor")
        self.assertEqual(zone.sensor_ids, [])
        self.assertFalse(zone.is_armed)
        self.assertEqual(zone.description, "")

    def test_zone_creation_with_sensors(self):
        """Test zone creation with sensor list."""
        zone = SafetyZone(
            zone_id=2,
            zone_name="Perimeter",
            sensor_ids=[1, 2, 3],
            is_armed=True,
            description="Outer sensors",
        )

        self.assertEqual(zone.sensor_ids, [1, 2, 3])
        self.assertTrue(zone.is_armed)
        self.assertEqual(zone.description, "Outer sensors")

    def test_add_sensor(self):
        """Test adding sensor to zone."""
        zone = SafetyZone(zone_id=1, zone_name="Living Room")

        result = zone.add_sensor(10)
        self.assertTrue(result)
        self.assertIn(10, zone.sensor_ids)

    def test_add_duplicate_sensor(self):
        """Test that adding duplicate sensor returns False."""
        zone = SafetyZone(zone_id=1, zone_name="Kitchen", sensor_ids=[5])

        result = zone.add_sensor(5)
        self.assertFalse(result)
        self.assertEqual(zone.sensor_ids.count(5), 1)

    def test_add_multiple_sensors(self):
        """Test adding multiple sensors."""
        zone = SafetyZone(zone_id=1, zone_name="Bedroom")

        zone.add_sensor(1)
        zone.add_sensor(2)
        zone.add_sensor(3)

        self.assertEqual(len(zone.sensor_ids), 3)
        self.assertEqual(zone.sensor_ids, [1, 2, 3])

    def test_remove_sensor(self):
        """Test removing sensor from zone."""
        zone = SafetyZone(zone_id=1, zone_name="Garage", sensor_ids=[10, 20, 30])

        result = zone.remove_sensor(20)
        self.assertTrue(result)
        self.assertNotIn(20, zone.sensor_ids)
        self.assertEqual(zone.sensor_ids, [10, 30])

    def test_remove_nonexistent_sensor(self):
        """Test that removing nonexistent sensor returns False."""
        zone = SafetyZone(zone_id=1, zone_name="Basement", sensor_ids=[1, 2])

        result = zone.remove_sensor(99)
        self.assertFalse(result)
        self.assertEqual(zone.sensor_ids, [1, 2])

    def test_clear_sensors(self):
        """Test clearing all sensors from zone."""
        zone = SafetyZone(zone_id=1, zone_name="Office", sensor_ids=[5, 10, 15])

        zone.clear_sensors()
        self.assertEqual(zone.sensor_ids, [])
        self.assertEqual(zone.get_sensor_count(), 0)

    def test_has_sensor(self):
        """Test checking if zone has specific sensor."""
        zone = SafetyZone(zone_id=1, zone_name="Hallway", sensor_ids=[7, 14, 21])

        self.assertTrue(zone.has_sensor(14))
        self.assertFalse(zone.has_sensor(28))

    def test_get_sensor_count(self):
        """Test getting sensor count."""
        zone = SafetyZone(zone_id=1, zone_name="Attic")
        self.assertEqual(zone.get_sensor_count(), 0)

        zone.add_sensor(1)
        zone.add_sensor(2)
        self.assertEqual(zone.get_sensor_count(), 2)

    def test_arm_zone(self):
        """Test arming zone."""
        zone = SafetyZone(zone_id=1, zone_name="Windows")

        self.assertFalse(zone.is_armed)
        zone.arm()
        self.assertTrue(zone.is_armed)

    def test_disarm_zone(self):
        """Test disarming zone."""
        zone = SafetyZone(zone_id=1, zone_name="Doors", is_armed=True)

        self.assertTrue(zone.is_armed)
        zone.disarm()
        self.assertFalse(zone.is_armed)

    def test_arm_disarm_toggle(self):
        """Test toggling armed status."""
        zone = SafetyZone(zone_id=1, zone_name="Patio")

        zone.arm()
        self.assertTrue(zone.is_armed)

        zone.disarm()
        self.assertFalse(zone.is_armed)

        zone.arm()
        self.assertTrue(zone.is_armed)

    def test_validate_valid_zone(self):
        """Test validation of valid zone."""
        zone = SafetyZone(zone_id=1, zone_name="Main Floor")
        self.assertTrue(zone.validate())

    def test_validate_empty_name(self):
        """Test validation fails for empty zone name."""
        zone = SafetyZone(zone_id=1, zone_name="")

        with self.assertRaises(ValidationError) as cm:
            zone.validate()
        self.assertIn("Zone name", str(cm.exception))

    def test_validate_negative_id(self):
        """Test validation fails for negative zone ID."""
        zone = SafetyZone(zone_id=-1, zone_name="Test Zone")

        with self.assertRaises(ValidationError) as cm:
            zone.validate()
        self.assertIn("Zone ID", str(cm.exception))

    def test_to_dict(self):
        """Test serialization to dictionary."""
        zone = SafetyZone(
            zone_id=5,
            zone_name="Second Floor",
            sensor_ids=[11, 12, 13],
            is_armed=True,
            description="Upper level",
        )

        data = zone.to_dict()

        self.assertIsInstance(data, dict)
        self.assertEqual(data["zone_id"], 5)
        self.assertEqual(data["zone_name"], "Second Floor")
        self.assertEqual(data["sensor_ids"], [11, 12, 13])
        self.assertTrue(data["is_armed"])
        self.assertEqual(data["description"], "Upper level")

    def test_to_dict_zero_zone_id(self):
        """Test that zone_id=0 is converted to None in dict."""
        zone = SafetyZone(zone_id=0, zone_name="New Zone")
        data = zone.to_dict()

        self.assertIsNone(data["zone_id"])

    def test_from_dict(self):
        """Test deserialization from dictionary."""
        data = {
            "zone_id": 3,
            "zone_name": "Basement",
            "sensor_ids": [20, 21, 22],
            "is_armed": False,
            "description": "Lower level",
        }

        zone = SafetyZone.from_dict(data)

        self.assertEqual(zone.zone_id, 3)
        self.assertEqual(zone.zone_name, "Basement")
        self.assertEqual(zone.sensor_ids, [20, 21, 22])
        self.assertFalse(zone.is_armed)
        self.assertEqual(zone.description, "Lower level")

    def test_from_dict_with_json_string_sensors(self):
        """Test deserialization when sensor_ids is JSON string."""
        data = {
            "zone_id": 1,
            "zone_name": "Garage",
            "sensor_ids": "[5, 10, 15]",  # JSON string
        }

        zone = SafetyZone.from_dict(data)
        self.assertEqual(zone.sensor_ids, [5, 10, 15])

    def test_from_dict_empty_sensor_string(self):
        """Test deserialization with empty sensor string."""
        data = {
            "zone_id": 1,
            "zone_name": "Porch",
            "sensor_ids": "",
        }

        zone = SafetyZone.from_dict(data)
        self.assertEqual(zone.sensor_ids, [])

    def test_from_dict_default_values(self):
        """Test deserialization with missing optional fields."""
        data = {
            "zone_name": "Attic",
        }

        zone = SafetyZone.from_dict(data)
        self.assertEqual(zone.zone_id, 0)
        self.assertEqual(zone.sensor_ids, [])
        self.assertFalse(zone.is_armed)
        self.assertEqual(zone.description, "")

    def test_roundtrip_serialization(self):
        """Test that serialization and deserialization preserve data."""
        original = SafetyZone(
            zone_id=7,
            zone_name="Perimeter",
            sensor_ids=[1, 2, 3, 4],
            is_armed=True,
            description="Outer boundary",
        )

        data = original.to_dict()
        restored = SafetyZone.from_dict(data)

        self.assertEqual(restored.zone_id, original.zone_id)
        self.assertEqual(restored.zone_name, original.zone_name)
        self.assertEqual(restored.sensor_ids, original.sensor_ids)
        self.assertEqual(restored.is_armed, original.is_armed)
        self.assertEqual(restored.description, original.description)

    def test_multiple_zones(self):
        """Test creating multiple distinct zones."""
        zones = [
            SafetyZone(zone_id=1, zone_name="First Floor"),
            SafetyZone(zone_id=2, zone_name="Second Floor"),
            SafetyZone(zone_id=3, zone_name="Basement"),
        ]

        for idx, zone in enumerate(zones, start=1):
            self.assertEqual(zone.zone_id, idx)
            self.assertIsInstance(zone.zone_name, str)


if __name__ == "__main__":
    unittest.main()
