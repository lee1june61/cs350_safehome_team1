"""
SafeHome System - Central controller (SDS: System class)
All UI components communicate ONLY through handle_request().
"""

from typing import Any, Dict

from ..configuration import ConfigurationManager, LogManager, LoginManager, StorageManager
from .command_registry import build_command_map
from .configuration.system_initializer import SystemInitializer
from .handlers.camera_handler import CameraHandler
from .handlers.lifecycle_handler import LifecycleHandler
from .handlers.log_handler import LogHandler
from .handlers.mode_handler import ModeHandler
from .handlers.security_handler import SecurityHandler
from .handlers.settings_handler import SettingsHandler
from .logging.system_logger import SystemLogger
from .services.mode_service import ModeService
from .system_bootstrap import create_services, setup_legacy_attrs
from .system_legacy import SystemLegacyMixin
from .system_lifecycle import SystemLifecycleMixin


class System(SystemLegacyMixin, SystemLifecycleMixin):
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

        svcs = create_services(
            self._storage, self._config_manager, self._login_manager, self._log_manager, self.logger
        )
        self.sensor_service = svcs["sensor_service"]
        self.camera_service = svcs["camera_service"]
        self.zone_service = svcs["zone_service"]
        self.mode_service = svcs["mode_service"]
        self.settings_service = svcs["settings_service"]
        self.alarm_service = svcs["alarm_service"]
        self.auth_service = svcs["auth_service"]

        self._bootstrap_defaults()
        self._create_handlers()
        self._command_map = build_command_map(
            self.auth_service, self.lifecycle_handler, self.security_handler,
            self.mode_handler, self.camera_handler, self.settings_handler, self.log_handler,
        )
        self._doors_windows_open = False
        setup_legacy_attrs(self)

    def _bootstrap_defaults(self):
        SystemInitializer(
            self._storage, self.zone_service, self.mode_service, self.sensor_service, self.camera_service
        ).bootstrap_all()

    def _create_handlers(self):
        self.lifecycle_handler = LifecycleHandler(
            self, self.alarm_service, self.sensor_service, self.camera_service, self.auth_service, self.mode_service
        )
        self.security_handler = SecurityHandler(
            self.sensor_service, self.zone_service, self.mode_service, self.alarm_service,
            self.auth_service, self.camera_service, self.logger, door_state_supplier=self._doors_open_flag,
        )
        self.mode_handler = ModeHandler(self.mode_service, self.auth_service)
        self.camera_handler = CameraHandler(self.camera_service)
        self.settings_handler = SettingsHandler(self.settings_service, self.alarm_service, self.auth_service)
        self.log_handler = LogHandler(self._log_manager)

    def handle_request(self, source: str, command: str, **kw) -> Dict[str, Any]:
        handler = self._command_map.get(command)
        return handler(**kw) if handler else {"success": False, "message": f"Unknown command: {command}"}
