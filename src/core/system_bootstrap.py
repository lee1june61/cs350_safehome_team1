"""System initialization helpers."""

from __future__ import annotations


def setup_legacy_attrs(system):
    """Initialize legacy compatibility fields on System."""
    system.status = "OFF"
    system.is_authenticated = True
    system.access_level = None
    system.login_tries = 0
    system.is_locked = False
    system.message_buffer = []
    system.sensor_controller = system.sensor_service._controller
    system.camera_controller = system.camera_service._controller
    system.login_manager = system._login_manager
    system.config_manager = system._config_manager
    system.alarm = system.alarm_service


def create_services(storage, config_manager, login_manager, log_manager, logger):
    """Create all service instances."""
    from ..controllers.camera_controller import CameraController
    from ..devices.sensors.sensor_controller import SensorController
    from .services.alarm_service import AlarmService
    from .services.auth_service import AuthService
    from .services.camera_service import CameraService
    from .services.mode_service import ModeService
    from .services.sensor_service import SensorService
    from .services.settings_service import SettingsService
    from .services.zone_service import ZoneService

    sensor_service = SensorService(SensorController())
    camera_service = CameraService(CameraController(), logger)
    zone_service = ZoneService(config_manager, logger)
    settings_service = SettingsService(config_manager, logger)
    settings = settings_service.get_settings()

    mode_service = ModeService(config_manager, sensor_service, logger)
    alarm_service = AlarmService(
        logger, settings.alarm_delay_time, settings.monitoring_service_phone
    )
    auth_service = AuthService(
        login_manager,
        logger,
        storage,
        max_attempts=settings.max_login_attempts or 3,
        lock_duration=settings.system_lock_time or 60,
    )
    auth_service.set_identity_contact(settings.monitoring_service_phone)

    return {
        "sensor_service": sensor_service,
        "camera_service": camera_service,
        "zone_service": zone_service,
        "mode_service": mode_service,
        "settings_service": settings_service,
        "alarm_service": alarm_service,
        "auth_service": auth_service,
    }

