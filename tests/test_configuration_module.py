"""
Unit tests for SafeHome configuration module.

These tests focus on the configuration and data management classes:
- StorageManager
- SystemSettings
- LoginInterface / LoginManager
- SafeHomeMode
- SafetyZone
- Log / LogManager
- ConfigurationManager
"""

from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from src.configuration import (
    AuthenticationError,
    ConfigurationError,
    LoginInterface,
    AccessLevel,
    LoginManager,
    Log,
    LogManager,
    SafeHomeMode,
    SafetyZone,
    StorageManager,
    SystemSettings,
    ValidationError,
    ConfigurationManager,
)


@pytest.fixture
def storage_manager(tmp_path):
    """Create a fresh StorageManager instance backed by a temp DB file."""
    # Reset singleton to ensure isolation between tests.
    StorageManager._instance = None  # type: ignore[attr-defined]
    db_path = tmp_path / "config_test.db"
    manager = StorageManager({"db_path": str(db_path)})
    manager.connect()
    yield manager
    manager.disconnect()


def test_system_settings_roundtrip(storage_manager):
    """SystemSettings should validate and persist correctly."""
    settings = SystemSettings(
        monitoring_service_phone="+12345678901",
        homeowner_phone="+10987654321",
        system_lock_time=60,
        alarm_delay_time=30,
        max_login_attempts=5,
        session_timeout=20,
    )
    assert settings.validate_settings() is True

    assert settings.save_to_database(storage_manager) is True

    loaded = SystemSettings()
    assert loaded.load_from_database(storage_manager) is True
    assert loaded.monitoring_service_phone == settings.monitoring_service_phone
    assert loaded.homeowner_phone == settings.homeowner_phone
    assert loaded.system_lock_time == settings.system_lock_time
    assert loaded.alarm_delay_time == settings.alarm_delay_time
    assert loaded.max_login_attempts == settings.max_login_attempts
    assert loaded.session_timeout == settings.session_timeout


def test_system_settings_validation_failure():
    """Invalid settings should fail validation."""
    settings = SystemSettings(
        monitoring_service_phone="bad-phone",
        homeowner_phone="+12345678901",
        system_lock_time=10,  # too small
        alarm_delay_time=4,  # too small
    )
    assert settings.validate_settings() is False
    with pytest.raises(ValidationError):
        # Saving invalid settings should raise.
        settings.save_to_database(StorageManager({"db_path": ":memory:"}))


def test_system_settings_allows_emergency_phone(storage_manager):
    """Emergency numbers should be accepted for monitoring phone."""
    settings = SystemSettings(
        monitoring_service_phone="911",
        homeowner_phone="+12345678901",
        alarm_delay_time=5,
    )
    assert settings.validate_settings() is True
    settings.save_to_database(storage_manager)


def test_login_interface_password_policy_and_hashing():
    """LoginInterface enforces password policy and hashing."""
    interface = LoginInterface(
        username="user1",
        password="pass1234",
        interface="control_panel",
        access_level=AccessLevel.USER_ACCESS,
    )
    assert interface.verify_password("pass1234") is True
    assert interface.verify_password("wrong") is False

    # Too short password should fail.
    with pytest.raises(ValidationError):
        interface.set_password("123")


def test_login_manager_success_and_lockout(storage_manager):
    """LoginManager should handle successful logins and lockouts."""
    # Persist system settings with max_login_attempts=3
    settings = SystemSettings(max_login_attempts=3)
    settings.save_to_database(storage_manager)

    # Create a user in the database.
    login_if = LoginInterface(
        username="master",
        password="secret123",
        interface="control_panel",
        access_level=AccessLevel.MASTER_ACCESS,
    )
    storage_manager.save_login_interface(login_if.to_dict())

    manager = LoginManager(storage_manager)

    # Wrong password attempts should eventually lock the account.
    assert manager.login("master", "wrong", "control_panel") is None
    assert manager.login("master", "wrong", "control_panel") is None
    assert manager.login("master", "wrong", "control_panel") is None

    assert manager.is_account_locked("master", "control_panel") is True

    # Correct password after lockout should still fail.
    assert manager.login("master", "secret123", "control_panel") is None


def test_login_manager_change_password(storage_manager):
    """Password changes via LoginManager should require old password."""
    settings = SystemSettings()
    settings.save_to_database(storage_manager)

    login_if = LoginInterface(
        username="user2",
        password="oldpass1",
        interface="web",
        access_level=AccessLevel.USER_ACCESS,
    )
    storage_manager.save_login_interface(login_if.to_dict())

    manager = LoginManager(storage_manager)

    # Wrong old password should raise.
    with pytest.raises(AuthenticationError):
        manager.change_password("user2", "wrong", "newpass1", "web")

    # Correct old password should succeed.
    assert manager.change_password("user2", "oldpass1", "newpass1", "web") is True
    assert manager.login("user2", "newpass1", "web") == AccessLevel.USER_ACCESS


def test_safehome_mode_validation_and_persistence(storage_manager):
    """SafeHomeMode should validate and persist through StorageManager."""
    mode = SafeHomeMode(mode_id=1, mode_name="Home")
    assert mode.validate() is True
    assert mode.get_sensor_count() == 0
    assert mode.add_sensor(10) is True
    assert mode.add_sensor(10) is False  # duplicate
    assert mode.has_sensor(10) is True

    storage_manager.save_safehome_mode(mode.to_dict())
    rows = storage_manager.get_safehome_modes()
    assert len(rows) == 1

    loaded = SafeHomeMode.from_dict(rows[0])
    assert loaded.mode_id == mode.mode_id
    assert loaded.mode_name == mode.mode_name
    assert loaded.sensor_ids == mode.sensor_ids


def test_safety_zone_validation_and_persistence(storage_manager):
    """SafetyZone should validate, persist, update, and delete."""
    zone = SafetyZone(zone_id=0, zone_name="First Floor")
    assert zone.validate() is True
    assert zone.add_sensor(1) is True
    assert zone.add_sensor(2) is True
    zone.arm()
    assert zone.is_armed is True

    # Insert (zone_id will be assigned by DB).
    storage_manager.save_safety_zone(zone.to_dict())
    zones = storage_manager.get_safety_zones()
    assert len(zones) == 1

    loaded = SafetyZone.from_dict(zones[0])
    assert loaded.zone_name == "First Floor"
    assert loaded.get_sensor_count() == 2
    zone_id = loaded.zone_id

    # Update
    loaded.disarm()
    loaded.remove_sensor(1)
    storage_manager.save_safety_zone(loaded.to_dict())
    zones = storage_manager.get_safety_zones()
    updated = SafetyZone.from_dict(zones[0])
    assert updated.is_armed is False
    assert updated.get_sensor_count() == 1

    # Delete
    assert storage_manager.delete_safety_zone(zone_id) is True
    assert storage_manager.get_safety_zones() == []


def test_log_manager_crud(storage_manager):
    """LogManager should save and retrieve logs."""
    manager = LogManager(storage_manager)
    log = manager.create_log(
        event_type="INTRUSION",
        description="Motion detected in living room",
        severity="WARNING",
        user="master",
    )
    assert isinstance(log, Log)
    assert "living room" in str(log)

    assert manager.save_log(log) is True

    all_logs = manager.get_logs(limit=10)
    assert len(all_logs) == 1
    assert all_logs[0].event_type == "INTRUSION"

    intrusion_logs = manager.get_intrusion_logs()
    assert len(intrusion_logs) == 1

    # Clear logs older than 0 days should remove all (timestamp < now).
    deleted = manager.clear_old_logs(days_to_keep=0)
    assert deleted >= 1


def test_configuration_manager_initialize_and_modes(storage_manager):
    """ConfigurationManager should initialize settings and default modes."""
    config_manager = ConfigurationManager(storage_manager)
    assert config_manager.initialize_configuration() is True

    # System settings should now exist.
    settings = config_manager.get_system_settings()
    assert isinstance(settings, SystemSettings)

    # Default modes should exist.
    modes = config_manager.get_all_safehome_modes()
    assert len(modes) >= 4

    # Update a specific mode.
    home_mode = modes[0]
    home_mode.add_sensor(101)
    assert config_manager.update_safehome_mode(home_mode) is True
    reloaded = config_manager.get_safehome_mode(home_mode.mode_id)
    assert 101 in reloaded.sensor_ids


def test_configuration_manager_zones_flow(storage_manager):
    """ConfigurationManager should manage safety zones end‑to‑end."""
    config_manager = ConfigurationManager(storage_manager)
    config_manager.initialize_configuration()

    zone = SafetyZone(zone_id=0, zone_name="Bedrooms")
    zone.add_sensor(5)
    zone.add_sensor(6)
    assert config_manager.add_safety_zone(zone) is True

    zones = config_manager.get_all_safety_zones()
    assert len(zones) == 1
    stored_zone = zones[0]
    assert stored_zone.zone_name == "Bedrooms"

    # Update
    stored_zone.disarm()
    stored_zone.remove_sensor(5)
    assert config_manager.update_safety_zone(stored_zone) is True

    updated = config_manager.get_safety_zone(stored_zone.zone_id)
    assert updated.is_armed is False
    assert updated.get_sensor_count() == 1

    # Delete
    assert config_manager.delete_safety_zone(stored_zone.zone_id) is True
    assert config_manager.get_all_safety_zones() == []
