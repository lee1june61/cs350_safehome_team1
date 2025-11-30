"""
Integration Tests: Security Functions (IT-008 ~ IT-017)
Based on SafeHome_Integration_Test_Cases.md

Tests:
- IT-008: Arm/disarm system through control panel
- IT-009: Arm/disarm system through web browser
- IT-010: Alarm condition encountered
- IT-011: Configure safety zone
- IT-012: Create new safety zone
- IT-013: Delete safety zone
- IT-014: Update an exist safety zone
- IT-015: Configure SafeHome modes
- IT-016: View intrusion log
- IT-017: Call monitoring service through control panel
"""
import pytest


class TestIT008ArmDisarmControlPanel:
    """IT-008: Arm/disarm system through control panel."""

    def test_arm_away_all_closed(self, system_logged_in_master):
        """Normal: Arm AWAY when all doors/windows closed."""
        # Ensure all sensors are closed
        for sensor in system_logged_in_master._sensors:
            if hasattr(sensor, "set_open"):
                sensor.set_open(False)

        result = system_logged_in_master.handle_request(
            "control_panel", "arm_system", mode="AWAY"
        )
        assert result["success"] is True
        status = system_logged_in_master.handle_request("control_panel", "get_status")
        assert status["data"]["mode"] == "AWAY"

    def test_arm_home(self, system_logged_in_master):
        """Normal: Arm HOME mode."""
        for sensor in system_logged_in_master._sensors:
            if hasattr(sensor, "set_open"):
                sensor.set_open(False)

        result = system_logged_in_master.handle_request(
            "control_panel", "arm_system", mode="HOME"
        )
        assert result["success"] is True

    def test_disarm_system(self, system_armed_away):
        """Normal: Disarm armed system."""
        result = system_armed_away.handle_request("control_panel", "disarm_system")
        assert result["success"] is True
        status = system_armed_away.handle_request("control_panel", "get_status")
        assert status["data"]["mode"] == "DISARMED"

    def test_arm_fails_door_open(self, system_logged_in_master):
        """Exception 2a: Arm fails if door/window open."""
        # Open a window/door sensor
        for sensor in system_logged_in_master._sensors:
            if hasattr(sensor, "set_open"):
                sensor.set_open(True)
                break

        result = system_logged_in_master.handle_request(
            "control_panel", "arm_system", mode="AWAY"
        )
        assert result["success"] is False
        assert "cannot arm" in result.get("message", "").lower()


class TestIT009ArmDisarmWebBrowser:
    """IT-009: Arm/disarm system through web browser."""

    def test_arm_via_web(self, system_web_logged_in):
        """Normal: Arm system via web interface."""
        for sensor in system_web_logged_in._sensors:
            if hasattr(sensor, "set_open"):
                sensor.set_open(False)

        result = system_web_logged_in.handle_request(
            "web", "arm_system", mode="AWAY"
        )
        assert result["success"] is True

    def test_disarm_via_web(self, system_web_logged_in):
        """Normal: Disarm system via web interface."""
        # First arm
        for sensor in system_web_logged_in._sensors:
            if hasattr(sensor, "set_open"):
                sensor.set_open(False)
        system_web_logged_in.handle_request("web", "arm_system", mode="AWAY")

        result = system_web_logged_in.handle_request("web", "disarm_system")
        assert result["success"] is True


class TestIT010AlarmCondition:
    """IT-010: Alarm condition encountered."""

    def test_alarm_triggered_on_intrusion(self, system_armed_away):
        """Normal: Alarm triggered when sensor detects intrusion."""
        # Simulate intrusion by opening a sensor
        for sensor in system_armed_away._sensors:
            if hasattr(sensor, "set_open"):
                sensor.set_open(True)
                break

        # Poll for intrusion
        result = system_armed_away.handle_request(
            "control_panel", "poll_sensors"
        )
        # The system should detect intrusion
        alarm_state = system_armed_away.alarm_service.state
        assert result.get("intrusion_detected") or alarm_state == "ALARM"


class TestSecurityVerification:
    """Additional: Security verification lock behavior."""

    def test_identity_lockout_after_failures(self, system_on):
        """Three failed attempts should lock verification."""
        for _ in range(2):
            res = system_on.handle_request("web", "verify_identity", value="123")
            assert res["success"] is False
            assert not res.get("locked")

        third = system_on.handle_request("web", "verify_identity", value="123")
        assert third["success"] is False
        assert third.get("locked")

        locked = system_on.handle_request(
            "web", "verify_identity", value="1234567890"
        )
        assert locked.get("locked") is True


class TestIT011ConfigureSafetyZone:
    """IT-011: Configure safety zone."""

    def test_get_safety_zones(self, system_web_logged_in):
        """Normal: Get existing safety zones."""
        result = system_web_logged_in.handle_request("web", "get_safety_zones")
        assert result["success"] is True
        assert "data" in result
        assert len(result["data"]) >= 1


class TestIT012CreateSafetyZone:
    """IT-012: Create new safety zone."""

    def test_create_new_zone(self, system_web_logged_in):
        """Normal: Create a new safety zone."""
        result = system_web_logged_in.handle_request(
            "web", "create_safety_zone",
            name="Test Zone", sensors=["S1", "S2"]
        )
        assert result["success"] is True

    def test_create_duplicate_zone_fails(self, system_web_logged_in):
        """Exception 3a: Duplicate zone name fails."""
        system_web_logged_in.handle_request(
            "web", "create_safety_zone",
            name="Duplicate Zone", sensors=["S1"]
        )
        result = system_web_logged_in.handle_request(
            "web", "create_safety_zone",
            name="Duplicate Zone", sensors=["S2"]
        )
        assert result["success"] is False
        assert result["message"] == "Same safety zone exists"

    def test_create_zone_requires_sensors(self, system_web_logged_in):
        """Exception 3b: Must select sensors when creating."""
        result = system_web_logged_in.handle_request(
            "web", "create_safety_zone", name="Empty Zone", sensors=[]
        )
        assert result["success"] is False
        assert result["message"] == "Select new safety zone and type safety zone name"


class TestIT013DeleteSafetyZone:
    """IT-013: Delete safety zone."""

    def test_delete_zone(self, system_web_logged_in):
        """Normal: Delete an existing zone."""
        # Get zones first
        zones_result = system_web_logged_in.handle_request(
            "web", "get_safety_zones"
        )
        if zones_result.get("data"):
            zone_id = zones_result["data"][0]["id"]
            result = system_web_logged_in.handle_request(
                "web", "delete_safety_zone", zone_id=zone_id
            )
            assert result["success"] is True


class TestIT014UpdateSafetyZone:
    """IT-014: Update an exist safety zone."""

    def test_update_zone_sensors(self, system_web_logged_in):
        """Normal: Update zone sensors."""
        zones_result = system_web_logged_in.handle_request(
            "web", "get_safety_zones"
        )
        if zones_result.get("data"):
            zone_id = zones_result["data"][0]["id"]
            result = system_web_logged_in.handle_request(
                "web", "update_safety_zone",
                zone_id=zone_id, sensors=["S1", "S3", "M1"]
            )
            assert result["success"] is True


class TestZoneArmingRules:
    """SRS-specific safety zone arming rules."""

    def test_arm_zone_blocks_open_door(self, system_web_logged_in):
        """Arming fails when a door/window inside the zone is open."""
        zones = system_web_logged_in.handle_request("web", "get_safety_zones")["data"]
        target_zone = next(z for z in zones if "S5" in z.get("sensors", []))
        door_sensor = system_web_logged_in.sensor_service.get_sensor("S5")
        assert door_sensor is not None
        door_sensor.set_open(True)

        result = system_web_logged_in.handle_request(
            "web", "arm_zone", zone_id=target_zone["id"]
        )
        assert result["success"] is False
        assert result["message"] == "Doors and windows not closed"
        door_sensor.set_open(False)

    def test_shared_sensor_stays_armed_until_all_zones_disarmed(self, system_web_logged_in):
        """Sensors shared by zones must stay armed until every zone is disarmed."""
        zone_one = system_web_logged_in.handle_request(
            "web", "create_safety_zone", name="Shared One", sensors=["S1"]
        )
        zone_two = system_web_logged_in.handle_request(
            "web", "create_safety_zone", name="Shared Two", sensors=["S1", "M1"]
        )
        assert zone_one["success"] and zone_two["success"]

        sensor = system_web_logged_in.sensor_service.get_sensor("S1")
        assert sensor is not None

        system_web_logged_in.handle_request("web", "arm_zone", zone_id=zone_one["zone_id"])
        system_web_logged_in.handle_request("web", "arm_zone", zone_id=zone_two["zone_id"])
        assert sensor.isArmed() is True

        system_web_logged_in.handle_request("web", "disarm_zone", zone_id=zone_one["zone_id"])
        assert sensor.isArmed() is True

        system_web_logged_in.handle_request("web", "disarm_zone", zone_id=zone_two["zone_id"])
        assert sensor.isArmed() is False


class TestIT015ConfigureSafeHomeModes:
    """IT-015: Configure SafeHome modes."""

    def test_get_mode_configuration(self, system_web_logged_in):
        """Normal: Get mode sensor configuration."""
        result = system_web_logged_in.handle_request(
            "web", "get_mode_configuration", mode="HOME"
        )
        assert result["success"] is True
        assert "data" in result

    def test_configure_mode(self, system_web_logged_in):
        """Normal: Configure sensors for a mode."""
        result = system_web_logged_in.handle_request(
            "web", "configure_safehome_mode",
            mode="HOME", sensors=["S1", "S2", "S3"]
        )
        assert result["success"] is True


class TestIT016ViewIntrusionLog:
    """IT-016: View intrusion log."""

    def test_get_intrusion_logs(self, system_web_logged_in):
        """Normal: Retrieve intrusion logs."""
        result = system_web_logged_in.handle_request("web", "get_intrusion_logs")
        assert result["success"] is True
        assert "data" in result


class TestIT017CallMonitoringService:
    """IT-017: Call monitoring service through control panel (Panic)."""

    def test_panic_button(self, system_logged_in_master):
        """Normal: Trigger panic alarm."""
        result = system_logged_in_master.handle_request("control_panel", "panic")
        assert result["success"] is True

    def test_panic_works_without_login(self, system_on):
        """Panic should work even without login."""
        result = system_on.handle_request("control_panel", "panic")
        assert result["success"] is True

