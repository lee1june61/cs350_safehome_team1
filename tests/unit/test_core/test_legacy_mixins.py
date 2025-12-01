"""
Tests for the legacy mixins introduced during refactoring to ensure their logic
is exercised and branch coverage increases.
"""

from types import SimpleNamespace
from unittest.mock import Mock, call

from src.core.legacy.auth_mixin import LegacyAuthMixin
from src.core.legacy.messaging_mixin import LegacyMessagingMixin
from src.core.legacy.mode_mixin import LegacyModeMixin
from src.core.legacy.sensor_mixin import LegacySensorMixin


class AuthHarness(LegacyAuthMixin):
    """Minimal concrete class to drive LegacyAuthMixin."""

    def __init__(self):
        self.is_locked = False
        self.login_tries = 0
        self.is_authenticated = False
        self.access_level = None
        self.status = "OFF"
        self.login_manager = Mock()
        self.config_manager = Mock()
        self.config_manager.get_monitoring_phone.return_value = None
        self.settings_service = Mock()
        self.settings_service.get_settings.return_value = SimpleNamespace(
            monitoring_service_phone=None
        )
        self.alarm = Mock()
        self.security_handler = Mock()
        self.sensor_controller = SimpleNamespace(
            disarm_all_sensors=Mock(return_value=True)
        )
        self.camera_controller = SimpleNamespace(
            disable_all_camera=Mock(return_value=True)
        )


class MessagingHarness(LegacyMessagingMixin):
    """Concrete helper for LegacyMessagingMixin."""

    def __init__(self):
        self._config_manager = SimpleNamespace(name="primary-config")
        self._login_manager = SimpleNamespace(name="primary-login")
        self.config_manager = None
        self.login_manager = None
        self.sensor_service = SimpleNamespace(_controller="sensor-controller")
        self.camera_service = SimpleNamespace(_controller="camera-controller")
        self.message_buffer = []
        self._next_message = None
        self._write_result = False
        self._captured_write = None

    def _read_from_interface(self):
        return self._next_message

    def _write_to_interface(self, response_data, target_interface):
        self._captured_write = (response_data, target_interface)
        return self._write_result


class ModeHarness(LegacyModeMixin):
    """Concrete helper for LegacyModeMixin."""

    def __init__(self):
        self.config_manager = Mock()
        self.sensor_controller = Mock()
        self.sensor_service = Mock()


class SensorHarness(LegacySensorMixin):
    """Concrete helper for LegacySensorMixin."""

    def __init__(self):
        self.sensor_controller = Mock()
        self.sensor_service = Mock()
        self.alarm = Mock()


class TestLegacyAuthMixin:
    def test_authenticate_user_success_updates_flags(self):
        harness = AuthHarness()
        harness.login_manager.authenticate.return_value = "MASTER"

        result = harness.authenticate_user("user", "pw", "web")

        assert result == "MASTER"
        assert harness.is_authenticated is True
        assert harness.access_level == "MASTER"
        assert harness.login_tries == 0
        assert harness.is_locked is False
        harness.login_manager.authenticate.assert_called_once_with("user", "pw", "web")

    def test_authenticate_user_failure_locks_after_three_attempts(self):
        harness = AuthHarness()
        harness.login_manager.authenticate.return_value = None

        for _ in range(3):
            assert harness.authenticate_user("user", "bad", "web") is None

        assert harness.is_locked is True
        assert harness.login_tries == 3

    def test_authenticate_user_returns_none_when_locked(self):
        harness = AuthHarness()
        harness.is_locked = True

        assert harness.authenticate_user("user", "pw", "panel") is None
        harness.login_manager.authenticate.assert_not_called()

    def test_make_panic_phone_call_uses_config_phone_and_triggers_panic(self):
        harness = AuthHarness()
        harness.config_manager.get_monitoring_phone.return_value = "010-0000-0000"
        harness.alarm.is_ringing.return_value = True

        assert harness.make_panic_phone_call() is True
        harness.security_handler.panic.assert_called_once_with()

    def test_make_panic_phone_call_falls_back_to_settings(self):
        harness = AuthHarness()
        harness.config_manager.get_monitoring_phone.return_value = None
        harness.settings_service.get_settings.return_value = SimpleNamespace(
            monitoring_service_phone="010-1111-2222"
        )
        harness.alarm.is_ringing.return_value = False

        assert harness.make_panic_phone_call() is True
        harness.security_handler.panic.assert_not_called()

    def test_make_panic_phone_call_returns_false_without_contact(self):
        harness = AuthHarness()
        harness.config_manager.get_monitoring_phone.return_value = ""
        harness.settings_service.get_settings.return_value = SimpleNamespace(
            monitoring_service_phone=""
        )

        assert harness.make_panic_phone_call() is False

    def test_reset_clears_state_and_calls_dependencies(self):
        harness = AuthHarness()
        harness.status = "ON"
        harness.login_tries = 2
        harness.access_level = "MASTER"
        harness.is_authenticated = True

        assert harness.reset() is True
        assert harness.status == "OFF"
        assert harness.login_tries == 0
        assert harness.access_level is None
        assert harness.is_authenticated is False
        harness.config_manager.reset_to_default.assert_called_once_with()
        harness.sensor_controller.disarm_all_sensors.assert_called_once_with()
        harness.camera_controller.disable_all_camera.assert_called_once_with()


class TestLegacyMessagingMixin:
    def test_init_system_populates_dependencies(self):
        harness = MessagingHarness()

        assert harness.init_system() is True
        assert harness.config_manager is harness._config_manager
        assert harness.login_manager is harness._login_manager
        assert harness.sensor_controller == "sensor-controller"
        assert harness.camera_controller == "camera-controller"

    def test_process_message_requires_readable_stream(self):
        harness = MessagingHarness()

        class NoRead:
            pass

        class Stream:
            def __init__(self, payload):
                self._payload = payload

            def read(self):
                return self._payload

        assert harness.process_message(NoRead()) is False
        assert harness.process_message(Stream("")) is False
        assert harness.process_message(Stream("payload")) is True

    def test_receive_message_buffers_non_empty_values(self):
        harness = MessagingHarness()
        harness._next_message = "ping"
        assert harness.receive_message() == "ping"
        assert harness.message_buffer == ["ping"]

        harness._next_message = ""
        assert harness.receive_message() == ""
        assert harness.message_buffer == ["ping"]

    def test_send_message_reflects_interface_response(self):
        harness = MessagingHarness()
        harness._write_result = "sent"
        assert harness.send_message({"ok": True}, "ui") is True
        assert harness._captured_write == ({"ok": True}, "ui")

        harness._write_result = ""
        assert harness.send_message({"ok": False}, "ui") is False


class TestLegacyModeMixin:
    def test_arm_by_mode_uses_sensor_controller(self):
        harness = ModeHarness()
        harness.config_manager.get_mode_sensors.return_value = [1, 2]
        harness.sensor_controller.arm_sensors.return_value = True

        assert harness.arm_by_safe_home_mode("home") is True
        harness.sensor_controller.arm_sensors.assert_called_once_with([1, 2])

    def test_arm_by_mode_falls_back_to_sensor_service(self):
        harness = ModeHarness()
        harness.config_manager.get_mode_sensors.return_value = ["a"]
        harness.sensor_controller = SimpleNamespace()
        harness.sensor_service = Mock()
        harness.sensor_service.set_sensor_armed.return_value = True

        assert harness.arm_by_safe_home_mode("away") is True
        harness.sensor_service.set_sensor_armed.assert_called_once_with("a", True)

    def test_arm_by_mode_returns_false_without_sensors(self):
        harness = ModeHarness()
        harness.config_manager.get_mode_sensors.return_value = []

        assert harness.arm_by_safe_home_mode("unknown") is False

    def test_disarm_by_mode_uses_sensor_controller(self):
        harness = ModeHarness()
        harness.config_manager.get_mode_sensors.return_value = [3]
        harness.sensor_controller.disarm_sensors.return_value = True

        assert harness.disarm_by_safe_home_mode("night") is True
        harness.sensor_controller.disarm_sensors.assert_called_once_with([3])

    def test_disarm_by_mode_falls_back_to_sensor_service(self):
        harness = ModeHarness()
        harness.config_manager.get_mode_sensors.return_value = ["x", "y"]
        harness.sensor_controller = SimpleNamespace()
        harness.sensor_service = Mock()
        harness.sensor_service.set_sensor_armed.return_value = True

        assert harness.disarm_by_safe_home_mode("night") is True
        assert harness.sensor_service.set_sensor_armed.call_args_list == [
            call("x", False),
            call("y", False),
        ]


class TestLegacySensorMixin:
    def test_arm_sensors_handles_empty_input(self):
        harness = SensorHarness()
        assert harness.arm_sensors([]) is False

    def test_arm_sensors_prefers_controller(self):
        harness = SensorHarness()
        harness.sensor_controller.arm_sensors.return_value = True

        assert harness.arm_sensors([1, 2]) is True
        harness.sensor_controller.arm_sensors.assert_called_once_with([1, 2])

    def test_arm_sensors_falls_back_to_service(self):
        harness = SensorHarness()
        harness.sensor_controller = SimpleNamespace()
        harness.sensor_service = Mock()
        harness.sensor_service.set_sensor_armed.return_value = True

        assert harness.arm_sensors([1]) is True
        harness.sensor_service.set_sensor_armed.assert_called_once_with("1", True)

    def test_disarm_sensors_prefers_controller(self):
        harness = SensorHarness()
        harness.sensor_controller.disarm_sensors.return_value = True

        assert harness.disarm_sensors([3]) is True
        harness.sensor_controller.disarm_sensors.assert_called_once_with([3])

    def test_disarm_sensors_falls_back_to_service(self):
        harness = SensorHarness()
        harness.sensor_controller = SimpleNamespace()
        harness.sensor_service = Mock()
        harness.sensor_service.set_sensor_armed.return_value = True

        assert harness.disarm_sensors([4]) is True
        harness.sensor_service.set_sensor_armed.assert_called_once_with("4", False)

    def test_read_sensor_prefers_controller_then_service(self):
        harness = SensorHarness()
        harness.sensor_controller.read.return_value = {"id": 1}
        assert harness.read_sensor() == {"id": 1}

        harness.sensor_controller = SimpleNamespace()
        harness.sensor_service = Mock()
        harness.sensor_service.collect_statuses.return_value = [{"id": 2}]
        assert harness.read_sensor() == [{"id": 2}]

    def test_get_alarm_info_handles_ringing_and_idle(self):
        harness = SensorHarness()
        harness.alarm.is_ringing.return_value = True
        harness.alarm.get_id.return_value = "A1"
        harness.alarm.get_location.return_value = "Hallway"

        ringing_info = harness.get_alarm_info()
        assert ringing_info["is_ringing"] is True
        assert ringing_info["alarm_id"] == "A1"
        assert ringing_info["location"] == "Hallway"
        assert ringing_info["timestamp"] is not None

        harness.alarm.is_ringing.return_value = False
        idle_info = harness.get_alarm_info()
        assert idle_info["is_ringing"] is False
        assert idle_info["timestamp"] is None

