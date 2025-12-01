"""Unit tests for ConfigurationManager class."""

import unittest
import os
import tempfile
from src.configuration.configuration_manager import ConfigurationManager
from src.configuration.storage_manager import StorageManager
from src.configuration.system_settings import SystemSettings
from src.configuration.safehome_mode import SafeHomeMode
from src.configuration.safety_zone import SafetyZone


class TestConfigurationManager(unittest.TestCase):
    """Test ConfigurationManager facade operations."""

    def setUp(self):
        """Set up test fixtures with real database."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db_path = self.temp_db.name

        # Reset singleton
        StorageManager._instance = None

        self.storage = StorageManager({"db_path": self.db_path})
        self.storage.connect()

        self.config_manager = ConfigurationManager(self.storage)

    def tearDown(self):
        """Clean up test database."""
        if self.storage.is_connected():
            self.storage.disconnect()

        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

        StorageManager._instance = None

    def test_configuration_manager_creation(self):
        """Test ConfigurationManager instantiation."""
        self.assertIsNotNone(self.config_manager)

    def test_initialize_configuration(self):
        """Test initializing configuration with defaults."""
        result = self.config_manager.initialize_configuration()

        self.assertTrue(result)

        # Verify default modes were created
        modes = self.config_manager.get_all_safehome_modes()
        self.assertGreaterEqual(
            len(modes), 4
        )  # At least HOME, AWAY, OVERNIGHT, EXTENDED

    def test_initialize_legacy_alias(self):
        """Test legacy initialize() method."""
        result = self.config_manager.initialize()
        self.assertTrue(result)

    def test_reset_to_default(self):
        """Test resetting configuration to defaults."""
        result = self.config_manager.reset_to_default()
        self.assertTrue(result)

    def test_get_system_settings(self):
        """Test retrieving system settings."""
        # Initialize first
        self.config_manager.initialize_configuration()

        settings = self.config_manager.get_system_settings()

        self.assertIsInstance(settings, SystemSettings)
        self.assertIsNotNone(settings.monitoring_service_phone)

    def test_update_system_settings(self):
        """Test updating system settings."""
        settings = SystemSettings(
            monitoring_service_phone="911",
            homeowner_phone="010-1234-5678",
            system_lock_time=90,
            alarm_delay_time=45,
        )

        result = self.config_manager.update_system_settings(settings)

        self.assertTrue(result)

        # Verify settings were saved
        retrieved = self.config_manager.get_system_settings()
        self.assertEqual(retrieved.monitoring_service_phone, "911")
        self.assertEqual(retrieved.system_lock_time, 90)

    def test_get_safehome_mode_by_id(self):
        """Test retrieving specific SafeHome mode."""
        self.config_manager.initialize_configuration()

        mode = self.config_manager.get_safehome_mode(1)

        self.assertIsNotNone(mode)
        self.assertIsInstance(mode, SafeHomeMode)
        self.assertEqual(mode.mode_id, 1)

    def test_get_nonexistent_safehome_mode(self):
        """Test retrieving non-existent mode returns None."""
        mode = self.config_manager.get_safehome_mode(999)

        self.assertIsNone(mode)

    def test_get_all_safehome_modes(self):
        """Test retrieving all SafeHome modes."""
        self.config_manager.initialize_configuration()

        modes = self.config_manager.get_all_safehome_modes()

        self.assertIsInstance(modes, list)
        self.assertGreater(len(modes), 0)
        self.assertIsInstance(modes[0], SafeHomeMode)

    def test_update_safehome_mode(self):
        """Test updating SafeHome mode."""
        # Initialize and get a mode
        self.config_manager.initialize_configuration()
        mode = self.config_manager.get_safehome_mode(1)

        # Modify mode
        mode.add_sensor(100)
        mode.add_sensor(200)
        mode.description = "Updated description"

        # Update
        result = self.config_manager.update_safehome_mode(mode)
        self.assertTrue(result)

        # Verify changes
        retrieved = self.config_manager.get_safehome_mode(1)
        self.assertIn(100, retrieved.sensor_ids)
        self.assertIn(200, retrieved.sensor_ids)
        self.assertEqual(retrieved.description, "Updated description")

    def test_get_safety_zone_by_id(self):
        """Test retrieving specific safety zone."""
        # Create a zone
        zone = SafetyZone(zone_id=0, zone_name="Test Zone")
        self.config_manager.add_safety_zone(zone)

        # Get zones to find the ID
        zones = self.config_manager.get_all_safety_zones()
        zone_id = zones[0].zone_id

        # Retrieve by ID
        retrieved = self.config_manager.get_safety_zone(zone_id)

        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.zone_name, "Test Zone")

    def test_get_nonexistent_safety_zone(self):
        """Test retrieving non-existent zone returns None."""
        zone = self.config_manager.get_safety_zone(999)

        self.assertIsNone(zone)

    def test_get_all_safety_zones(self):
        """Test retrieving all safety zones."""
        # Create zones
        zone1 = SafetyZone(zone_id=0, zone_name="First Floor")
        zone2 = SafetyZone(zone_id=0, zone_name="Second Floor")

        self.config_manager.add_safety_zone(zone1)
        self.config_manager.add_safety_zone(zone2)

        # Retrieve all
        zones = self.config_manager.get_all_safety_zones()

        self.assertEqual(len(zones), 2)
        self.assertIsInstance(zones[0], SafetyZone)

    def test_add_safety_zone(self):
        """Test adding new safety zone."""
        zone = SafetyZone(
            zone_id=0,
            zone_name="Basement",
            sensor_ids=[10, 20],
            is_armed=True,
        )

        result = self.config_manager.add_safety_zone(zone)

        self.assertTrue(result)

        # Verify zone was added
        zones = self.config_manager.get_all_safety_zones()
        self.assertEqual(len(zones), 1)
        self.assertEqual(zones[0].zone_name, "Basement")

    def test_update_safety_zone(self):
        """Test updating existing safety zone."""
        # Create zone
        zone = SafetyZone(zone_id=0, zone_name="Living Room")
        self.config_manager.add_safety_zone(zone)

        # Get the zone with its assigned ID
        zones = self.config_manager.get_all_safety_zones()
        zone = zones[0]

        # Modify zone
        zone.add_sensor(50)
        zone.arm()

        # Update
        result = self.config_manager.update_safety_zone(zone)
        self.assertTrue(result)

        # Verify changes
        retrieved = self.config_manager.get_safety_zone(zone.zone_id)
        self.assertIn(50, retrieved.sensor_ids)
        self.assertTrue(retrieved.is_armed)

    def test_delete_safety_zone(self):
        """Test deleting safety zone."""
        # Create zone
        zone = SafetyZone(zone_id=0, zone_name="Garage")
        self.config_manager.add_safety_zone(zone)

        # Get zone ID
        zones = self.config_manager.get_all_safety_zones()
        zone_id = zones[0].zone_id

        # Delete
        result = self.config_manager.delete_safety_zone(zone_id)
        self.assertTrue(result)

        # Verify deletion
        zones = self.config_manager.get_all_safety_zones()
        self.assertEqual(len(zones), 0)

    def test_delete_nonexistent_zone(self):
        """Test deleting non-existent zone returns False."""
        result = self.config_manager.delete_safety_zone(999)

        self.assertFalse(result)

    def test_multiple_modes_with_different_sensors(self):
        """Test managing multiple modes with different sensor configurations."""
        self.config_manager.initialize_configuration()

        # Get modes and configure them differently
        home_mode = self.config_manager.get_safehome_mode(1)
        away_mode = self.config_manager.get_safehome_mode(2)

        # Clear existing sensors and configure HOME mode with minimal sensors
        home_mode.clear_sensors()
        home_mode.add_sensor(1)
        home_mode.add_sensor(2)
        self.config_manager.update_safehome_mode(home_mode)

        # Clear existing sensors and configure AWAY mode with all sensors
        away_mode.clear_sensors()
        for sensor_id in range(1, 11):
            away_mode.add_sensor(sensor_id)
        self.config_manager.update_safehome_mode(away_mode)

        # Verify configurations
        home = self.config_manager.get_safehome_mode(1)
        away = self.config_manager.get_safehome_mode(2)

        self.assertEqual(home.get_sensor_count(), 2)
        self.assertEqual(away.get_sensor_count(), 10)

    def test_zones_with_overlapping_sensors(self):
        """Test creating zones with overlapping sensors."""
        zone1 = SafetyZone(zone_id=0, zone_name="Perimeter", sensor_ids=[1, 2, 3])
        zone2 = SafetyZone(zone_id=0, zone_name="Interior", sensor_ids=[3, 4, 5])

        self.config_manager.add_safety_zone(zone1)
        self.config_manager.add_safety_zone(zone2)

        zones = self.config_manager.get_all_safety_zones()

        # Both zones should exist with their sensors
        self.assertEqual(len(zones), 2)
        self.assertTrue(zones[0].has_sensor(3))
        self.assertTrue(zones[1].has_sensor(3))

    def test_complete_configuration_workflow(self):
        """Test complete configuration setup workflow."""
        # 1. Initialize
        self.config_manager.initialize_configuration()

        # 2. Configure system settings
        settings = SystemSettings(
            monitoring_service_phone="911",
            homeowner_phone="010-1234-5678",
            system_lock_time=60,
            alarm_delay_time=30,
        )
        self.config_manager.update_system_settings(settings)

        # 3. Configure modes
        home_mode = self.config_manager.get_safehome_mode(1)
        home_mode.add_sensor(1)
        home_mode.add_sensor(2)
        self.config_manager.update_safehome_mode(home_mode)

        # 4. Create zones
        zone = SafetyZone(zone_id=0, zone_name="Main Floor", sensor_ids=[1, 2])
        self.config_manager.add_safety_zone(zone)

        # 5. Verify everything
        retrieved_settings = self.config_manager.get_system_settings()
        self.assertEqual(retrieved_settings.homeowner_phone, "010-1234-5678")

        retrieved_mode = self.config_manager.get_safehome_mode(1)
        self.assertEqual(retrieved_mode.get_sensor_count(), 2)

        zones = self.config_manager.get_all_safety_zones()
        self.assertEqual(len(zones), 1)


if __name__ == "__main__":
    unittest.main()
