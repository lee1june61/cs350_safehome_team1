"""
SafeHome System - Central controller (SDS: System class)
All UI components communicate ONLY through handle_request().

SRS References:
- V.1: Common functions (login, settings, on/off/reset)
- V.2: Security functions (arm/disarm, zones, modes, alarm, panic)
- V.3: Surveillance functions (camera view, pan/zoom, enable/disable, passwords)
"""

from datetime import datetime
from typing import Any, Dict

from ..controllers.camera_controller import CameraController
from ..devices.sensors.sensor_controller import SensorController
from ..configuration import (
    ConfigurationManager,
    LogManager,
    LoginManager,
    StorageManager,
)
from .configuration.system_initializer import SystemInitializer
from .logging.system_logger import SystemLogger
from .services.alarm_service import AlarmService
from .services.auth_service import AuthService
from .services.camera_service import CameraService
from .services.mode_service import ModeService
from .services.sensor_service import SensorService
from .services.settings_service import SettingsService
from .services.zone_service import ZoneService
from .handlers.lifecycle_handler import LifecycleHandler
from .handlers.security_handler import SecurityHandler
from .handlers.mode_handler import ModeHandler
from .handlers.camera_handler import CameraHandler
from .handlers.settings_handler import SettingsHandler
from .handlers.log_handler import LogHandler
from .system_legacy import SystemLegacyMixin


class System(SystemLegacyMixin):
    """Main system controller - handles all requests from UI components."""

    MODE_HOME = "HOME"
    MODE_AWAY = "AWAY"
    MODE_DISARMED = ModeService.MODE_DISARMED

    def __init__(self, db_path: str = "safehome.db"):
        self._storage = StorageManager.get_instance(db_path)
        self._storage.connect()
        self._config_manager = ConfigurationManager(self._storage)
        self._login_manager = LoginManager(self._storage)
        self._log_manager = LogManager(self._storage)

        self.logger = SystemLogger(self._log_manager)
        self.sensor_service = SensorService(SensorController())
        self.camera_service = CameraService(CameraController(), self.logger)
        self.zone_service = ZoneService(self._config_manager, self.logger)
        self.mode_service = ModeService(
            self._config_manager, self.sensor_service, self.logger
        )
        self.settings_service = SettingsService(self._config_manager, self.logger)

        settings = self.settings_service.get_settings()
        self.alarm_service = AlarmService(
            self.logger,
            settings.alarm_delay_time,
            settings.monitoring_service_phone,
        )

        max_attempts = settings.max_login_attempts or 3
        lock_duration = settings.system_lock_time or 60
        self.auth_service = AuthService(
            self._login_manager,
            self.logger,
            self._storage,
            max_attempts=max_attempts,
            lock_duration=lock_duration,
        )

        initializer = SystemInitializer(
            storage=self._storage,
            zone_service=self.zone_service,
            mode_service=self.mode_service,
            sensor_service=self.sensor_service,
            camera_service=self.camera_service,
        )
        initializer.bootstrap_all()

        self.lifecycle_handler = LifecycleHandler(
            system=self,
            alarm_service=self.alarm_service,
            sensor_service=self.sensor_service,
            camera_service=self.camera_service,
            auth_service=self.auth_service,
            mode_service=self.mode_service,
        )
        self.security_handler = SecurityHandler(
            sensor_service=self.sensor_service,
            zone_service=self.zone_service,
            mode_service=self.mode_service,
            alarm_service=self.alarm_service,
            auth_service=self.auth_service,
            camera_service=self.camera_service,
            logger=self.logger,
            door_state_supplier=self._doors_open_flag,
        )
        self.mode_handler = ModeHandler(self.mode_service, self.auth_service)
        self.camera_handler = CameraHandler(self.camera_service)
        self.settings_handler = SettingsHandler(
            self.settings_service, self.alarm_service, self.auth_service
        )
        self.log_handler = LogHandler(self._log_manager)

        self._command_map = self._build_command_map()
        self._doors_windows_open = False

        # Legacy compatibility fields (older unit tests expect these)
        self.status = "OFF"
        self.is_authenticated = True
        self.access_level = None
        self.login_tries = 0
        self.is_locked = False
        self.message_buffer = []
        self.sensor_controller = self.sensor_service._controller
        self.camera_controller = self.camera_service._controller
        self.login_manager = self._login_manager
        self.config_manager = self._config_manager
        self.alarm = self.alarm_service

    # ------------------------------------------------------------------ #
    # Core routing
    # ------------------------------------------------------------------ #
    def _build_command_map(self):
        return {
            # Authentication
            "login_control_panel": self.auth_service.login_control_panel,
            "login_web": self.auth_service.login_web,
            "web_login": self.auth_service.legacy_web_login,
            "logout": self.auth_service.logout,
            "verify_identity": self.auth_service.verify_identity,
            "is_verified": self.auth_service.is_identity_verified,
            "change_password": self.auth_service.change_password,
            # Lifecycle
            "turn_on": self.lifecycle_handler.turn_on,
            "turn_off": self.lifecycle_handler.turn_off,
            "reset_system": self.lifecycle_handler.reset,
            "get_status": self.lifecycle_handler.get_status,
            # Security
            "arm_system": self.security_handler.arm_system,
            "disarm_system": self.security_handler.disarm_system,
            "panic": self.security_handler.panic,
            # Zones
            "get_safety_zones": self.security_handler.get_safety_zones,
            "arm_zone": self.security_handler.arm_zone,
            "disarm_zone": self.security_handler.disarm_zone,
            "create_safety_zone": self.security_handler.create_safety_zone,
            "update_safety_zone": self.security_handler.update_safety_zone,
            "delete_safety_zone": self.security_handler.delete_safety_zone,
            # Sensors
            "get_sensors": self.security_handler.get_sensors,
            "get_all_devices_status": self.security_handler.get_all_devices_status,
            "arm_sensor": self.security_handler.arm_sensor,
            "disarm_sensor": self.security_handler.disarm_sensor,
            "poll_sensors": self.security_handler.poll_sensors,
            "trigger_alarm": self.security_handler.trigger_alarm,
            "clear_alarm": self.security_handler.clear_alarm,
            "get_alarm_status": self.security_handler.get_alarm_status,
            # Modes
            "get_mode_configuration": self.mode_handler.get_mode_configuration,
            "configure_safehome_mode": self.mode_handler.configure_mode,
            "get_all_modes": self.mode_handler.get_all_modes,
            # Cameras
            "get_cameras": self.camera_handler.get_cameras,
            "get_camera": self.camera_handler.get_camera,
            "get_camera_view": self.camera_handler.get_camera_view,
            "camera_pan": self.camera_handler.camera_pan,
            "pan_camera": self.camera_handler.camera_pan,
            "camera_zoom": self.camera_handler.camera_zoom,
            "zoom_camera": self.camera_handler.camera_zoom,
            "camera_tilt": self.camera_handler.camera_tilt,
            "enable_camera": self.camera_handler.enable_camera,
            "disable_camera": self.camera_handler.disable_camera,
            "set_camera_password": self.camera_handler.set_camera_password,
            "delete_camera_password": self.camera_handler.delete_camera_password,
            "verify_camera_password": self.camera_handler.verify_camera_password,
            "get_thumbnails": self.camera_handler.get_thumbnails,
            # Settings / Logs
            "get_system_settings": self.settings_handler.get_settings,
            "configure_system_settings": self.settings_handler.configure_settings,
            "get_intrusion_log": self.log_handler.get_intrusion_log,
            "get_intrusion_logs": self.log_handler.get_intrusion_log,
        }

    def handle_request(self, source: str, command: str, **kw) -> Dict[str, Any]:
        handler = self._command_map.get(command)
        if handler:
            return handler(**kw)
        return {"success": False, "message": f"Unknown command: {command}"}

    # ------------------------------------------------------------------ #
    # Lifecycle helpers
    # ------------------------------------------------------------------ #
    def turn_on(self):
        if getattr(self, "status", "OFF") == "ON":
            return False
        if hasattr(self.config_manager, "initialize"):
            self.config_manager.initialize()
        if hasattr(self.sensor_controller, "initialize"):
            self.sensor_controller.initialize()
        if hasattr(self.camera_controller, "initialize"):
            self.camera_controller.initialize()
        self.alarm_service.turn_on()
        self.status = "ON"
        return True

    def turn_off(self):
        if not getattr(self, "is_authenticated", True):
            return False
        if hasattr(self.sensor_controller, "disarm_all_sensors"):
            self.sensor_controller.disarm_all_sensors()
        if hasattr(self.camera_controller, "disable_all_camera"):
            self.camera_controller.disable_all_camera()
        self.alarm_service.turn_off()
        self.mode_service.disarm_system(self.zone_service, log_event=False)
        self.auth_service.logout()
        self.status = "OFF"
        return True

    def _doors_open_flag(self) -> bool:
        return bool(getattr(self, "_doors_windows_open", False))


