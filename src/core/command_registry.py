"""Command routing registry for System."""

from __future__ import annotations

from typing import Callable, Dict


def build_command_map(
    auth_service,
    lifecycle_handler,
    security_handler,
    mode_handler,
    camera_handler,
    settings_handler,
    log_handler,
) -> Dict[str, Callable]:
    """Build the master command -> handler mapping."""
    return {
        # Authentication
        "login_control_panel": auth_service.login_control_panel,
        "login_web": auth_service.login_web,
        "web_login": auth_service.legacy_web_login,
        "logout": auth_service.logout,
        "verify_identity": auth_service.verify_identity,
        "is_verified": auth_service.is_identity_verified,
        "change_password": auth_service.change_password,
        "verify_control_panel_password": auth_service.verify_control_panel_password,
        # Lifecycle
        "turn_on": lifecycle_handler.turn_on,
        "turn_off": lifecycle_handler.turn_off,
        "reset_system": lifecycle_handler.reset,
        "get_status": lifecycle_handler.get_status,
        # Security
        "arm_system": security_handler.arm_system,
        "disarm_system": security_handler.disarm_system,
        "panic": security_handler.panic,
        # Zones
        "get_safety_zones": security_handler.get_safety_zones,
        "arm_zone": security_handler.arm_zone,
        "disarm_zone": security_handler.disarm_zone,
        "create_safety_zone": security_handler.create_safety_zone,
        "update_safety_zone": security_handler.update_safety_zone,
        "delete_safety_zone": security_handler.delete_safety_zone,
        # Sensors
        "get_sensors": security_handler.get_sensors,
        "get_all_devices_status": security_handler.get_all_devices_status,
        "arm_sensor": security_handler.arm_sensor,
        "disarm_sensor": security_handler.disarm_sensor,
        "poll_sensors": security_handler.poll_sensors,
        "trigger_alarm": security_handler.trigger_alarm,
        "clear_alarm": security_handler.clear_alarm,
        "get_alarm_status": security_handler.get_alarm_status,
        # Modes
        "get_mode_configuration": mode_handler.get_mode_configuration,
        "configure_safehome_mode": mode_handler.configure_mode,
        "get_all_modes": mode_handler.get_all_modes,
        # Cameras
        "get_cameras": camera_handler.get_cameras,
        "get_camera": camera_handler.get_camera,
        "get_camera_view": camera_handler.get_camera_view,
        "camera_pan": camera_handler.camera_pan,
        "pan_camera": camera_handler.camera_pan,
        "camera_zoom": camera_handler.camera_zoom,
        "zoom_camera": camera_handler.camera_zoom,
        "camera_tilt": camera_handler.camera_tilt,
        "enable_camera": camera_handler.enable_camera,
        "disable_camera": camera_handler.disable_camera,
        "set_camera_password": camera_handler.set_camera_password,
        "delete_camera_password": camera_handler.delete_camera_password,
        "verify_camera_password": camera_handler.verify_camera_password,
        "get_thumbnails": camera_handler.get_thumbnails,
        # Settings / Logs
        "get_system_settings": settings_handler.get_settings,
        "configure_system_settings": settings_handler.configure_settings,
        "get_intrusion_log": log_handler.get_intrusion_log,
        "get_intrusion_logs": log_handler.get_intrusion_log,
    }

