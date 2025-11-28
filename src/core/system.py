"""
SafeHome System - Central controller (SDS: System class)
All UI components communicate ONLY through handle_request().

SRS References:
- V.1: Common functions (login, settings, on/off/reset)
- V.2: Security functions (arm/disarm, zones, modes, alarm, panic)
- V.3: Surveillance functions (camera view, pan/zoom, enable/disable, passwords)
"""

from typing import List, Dict, Any, Optional, Union
from datetime import datetime

from ..controllers.camera_controller import CameraController
from ..devices.cameras.safehome_camera import SafeHomeCamera
from ..devices.custom_motion_detector import CustomMotionDetector
from ..devices.custom_window_door_sensor import CustomWinDoorSensor
from ..utils.exceptions import CameraNotFoundError

# Device data matching floorplan.png (C=Camera, S=Sensor, M=Motion)
SENSORS = [
    {"id": "S1", "type": "WINDOW", "location": "DR Top", "armed": False},
    {"id": "S2", "type": "DOOR", "location": "DR Left", "armed": False},
    {"id": "S3", "type": "WINDOW", "location": "KIT Left", "armed": False},
    {"id": "S4", "type": "WINDOW", "location": "LR Top", "armed": False},
    {"id": "S5", "type": "DOOR", "location": "LR Right Top", "armed": False},
    {"id": "S6", "type": "WINDOW", "location": "LR Right Bottom", "armed": False},
    {"id": "M1", "type": "MOTION", "location": "DR", "armed": False},
    {"id": "M2", "type": "MOTION", "location": "Hallway", "armed": False},
]

SAFETY_ZONES = [
    {"id": 1, "name": "Front Zone", "sensors": ["S1", "S2", "M1"], "armed": False},
    {"id": 2, "name": "Kitchen Zone", "sensors": ["S3"], "armed": False},
    {
        "id": 3,
        "name": "Living Room",
        "sensors": ["S4", "S5", "S6", "M2"],
        "armed": False,
    },
]

# Default mode configurations (which sensors are active in each mode)
MODE_CONFIGS = {
    "HOME": ["S1", "S2", "S5", "S6"],  # Perimeter only
    "AWAY": ["S1", "S2", "S3", "S4", "S5", "S6", "M1", "M2"],  # All sensors
    "OVERNIGHT": ["S1", "S2", "S3", "S4", "S5", "S6"],  # All except motion
    "EXTENDED": ["S1", "S2", "S3", "S4", "S5", "S6", "M1", "M2"],  # All sensors
    "GUEST": ["S1", "S2", "S5", "S6"],  # Same as HOME
}


class System:
    """Main system controller - handles all requests from UI components."""

    MODE_HOME = "HOME"
    MODE_AWAY = "AWAY"
    MODE_DISARMED = "DISARMED"

    def __init__(self):
        self._state = "OFF"  # OFF, READY, ALARM
        self._mode = self.MODE_DISARMED
        self._user: Optional[str] = None
        self._verified = False

        # Passwords (SRS V.1.c)
        self._master_pw = "1234"  # 4 digits for control panel
        self._guest_pw = "5678"  # 4 digits for control panel
        self._web_pw1 = "password"  # 8+ chars for web
        self._web_pw2 = "password"  # 8+ chars for web

        # Settings (SRS V.1.c)
        self._delay_time = 30  # seconds before calling monitor
        self._monitor_phone = "911"

        # Data stores
        self._sensors: List[Union[CustomMotionDetector, CustomWinDoorSensor]] = []
        for sensor_data in SENSORS:
            sensor_id_str = sensor_data.get("id", "S0")
            try:
                # ID is like 'S1', 'M2', so we take the number
                sensor_id_int = int(sensor_id_str[1:])
            except (ValueError, IndexError):
                sensor_id_int = 0  # Default on parsing error

            if sensor_data["type"] == "MOTION":
                sensor_obj = CustomMotionDetector(
                    location=sensor_data.get("location", "Unknown"),
                    sensor_id=sensor_id_int,
                )
            else:  # 'WINDOW' or 'DOOR'
                sensor_obj = CustomWinDoorSensor(
                    location=sensor_data.get("location", "Unknown"),
                    sensor_id=sensor_id_int,
                    sensor_subtype=sensor_data.get("type", "window").lower(),
                )

            if sensor_data.get("armed"):
                sensor_obj.arm()

            self._sensors.append(sensor_obj)

        self.camera_controller = CameraController()
        self._zones = [
            {
                "id": z["id"],
                "name": z["name"],
                "sensors": z["sensors"][:],
                "armed": False,
            }
            for z in SAFETY_ZONES
        ]
        self._mode_configs = {k: v[:] for k, v in MODE_CONFIGS.items()}
        self._logs: List[Dict] = []

        # Login state
        self._attempts = 3
        self._locked = False
        self._lock_time: Optional[datetime] = None

    # ========== System Lifecycle ==========
    def turn_on(self):
        """Turn system on."""
        self._state = "READY"

    def turn_off(self):
        """Turn system off."""
        self._state = "OFF"
        self._user = None
        self._verified = False
        self._mode = self.MODE_DISARMED
        for s in self._sensors:
            s.disarm()

    # ========== Request Handler ==========
    def handle_request(self, source: str, command: str, **kw) -> Dict[str, Any]:
        """Central request handler - all UI interactions go through here."""
        handler = getattr(self, f"_cmd_{command}", None)
        if handler:
            return handler(**kw)
        return {"success": False, "message": f"Unknown command: {command}"}

    # ========== Authentication (SRS V.1.a, V.1.b) ==========
    def _check_lock(self) -> Optional[Dict]:
        """Check if system is locked."""
        if self._locked:
            if self._lock_time:
                elapsed = (datetime.now() - self._lock_time).seconds
                if elapsed >= 60:
                    self._locked = False
                    self._attempts = 3
                    self._lock_time = None
                    return None
            return {"success": False, "locked": True, "message": "System locked"}
        return None

    def _cmd_login_control_panel(self, password="", **kw) -> Dict:
        """Login via control panel (4-digit password)."""
        lock = self._check_lock()
        if lock:
            return lock

        if password == self._master_pw:
            self._user = "MASTER"
            self._attempts = 3
            return {"success": True, "access_level": "MASTER"}
        if password == self._guest_pw:
            self._user = "GUEST"
            self._attempts = 3
            return {"success": True, "access_level": "GUEST"}

        self._attempts -= 1
        if self._attempts <= 0:
            self._locked = True
            self._lock_time = datetime.now()
        return {"success": False, "attempts_remaining": self._attempts}

    def _cmd_login_web(self, user_id="", password1="", password2="", **kw) -> Dict:
        """Login via web (user ID + two 8-char passwords)."""
        lock = self._check_lock()
        if lock:
            return lock

        if user_id and password1 == self._web_pw1 and password2 == self._web_pw2:
            self._user = user_id
            self._attempts = 3
            return {"success": True}

        self._attempts -= 1
        if self._attempts <= 0:
            self._locked = True
            self._lock_time = datetime.now()
        return {"success": False, "attempts_remaining": self._attempts}

    def _cmd_logout(self, **kw) -> Dict:
        """Logout current user."""
        self._user = None
        self._verified = False
        return {"success": True}

    def _cmd_verify_identity(self, value="", **kw) -> Dict:
        """Verify identity with address or phone (SRS V.2.b step 3)."""
        v = value.strip().replace("-", "").replace(" ", "")
        if v and len(v) >= 3:
            self._verified = True
            return {"success": True}
        return {"success": False, "message": "Invalid verification"}

    def _cmd_is_verified(self, **kw) -> Dict:
        """Check if user identity is verified."""
        return {"success": True, "verified": self._verified}

    def _cmd_change_password(self, current_password="", new_password="", **kw) -> Dict:
        """Change master password (SRS V.1.g)."""
        if current_password != self._master_pw:
            return {"success": False, "message": "Current password incorrect"}
        if new_password and len(new_password) == 4 and new_password.isdigit():
            self._master_pw = new_password
            return {"success": True}
        return {"success": False, "message": "New password must be 4 digits"}

    # ========== System Lifecycle Commands ==========
    def _cmd_turn_on(self, **kw) -> Dict:
        self._state = "READY"
        return {"success": True, "state": self._state}

    def _cmd_turn_off(self, **kw) -> Dict:
        self.turn_off()
        return {"success": True}

    def _cmd_reset_system(self, **kw) -> Dict:
        """Reset system (SRS V.1.f)."""
        self._mode = self.MODE_DISARMED
        for s in self._sensors:
            s.disarm()
        for z in self._zones:
            z["armed"] = False
        return {"success": True}

    def _cmd_get_status(self, **kw) -> Dict:
        """Get current system status."""
        return {
            "success": True,
            "data": {
                "state": self._state,
                "mode": self._mode,
                "armed": self._mode != self.MODE_DISARMED,
                "user": self._user,
                "verified": self._verified,
            },
        }

    # ========== Security - Arm/Disarm (SRS V.2.a, V.2.b) ==========
    def _cmd_arm_system(self, mode="AWAY", **kw) -> Dict:
        """Arm system with specified mode."""
        # Check for test-specific mock attribute first
        if hasattr(self, "_doors_windows_open") and self._doors_windows_open:
            return {
                "success": False,
                "message": "Cannot arm, a door or window is open.",
            }

        # Check if all doors/windows are closed
        for s in self._sensors:
            if isinstance(s, CustomWinDoorSensor) and not s.can_arm():
                return {
                    "success": False,
                    "message": f"Cannot arm. {s.get_location()} is open.",
                }

        self._mode = mode
        # Arm sensors based on mode configuration
        active_sensors = self._mode_configs.get(mode, [])
        for s in self._sensors:
            s_id_str = f"{'M' if isinstance(s, CustomMotionDetector) else 'S'}{s.get_sensor_id()}"
            if s_id_str in active_sensors:
                s.arm()
            else:
                s.disarm()

        self._add_log("ARM", f"System armed: {mode}")
        return {"success": True, "mode": mode}

    def _cmd_disarm_system(self, **kw) -> Dict:
        """Disarm entire system."""
        self._mode = self.MODE_DISARMED
        for s in self._sensors:
            s.disarm()
        for z in self._zones:
            z["armed"] = False
        self._add_log("DISARM", "System disarmed")
        return {"success": True}

    def _cmd_panic(self, **kw) -> Dict:
        """Panic button - call monitoring service immediately (SRS V.2.k)."""
        self._state = "ALARM"
        self._add_log("PANIC", f"Emergency call to {self._monitor_phone}")
        return {"success": True, "message": f"Calling {self._monitor_phone}"}

    # ========== Safety Zones (SRS V.2.c-h) ==========
    def _cmd_get_safety_zones(self, **kw) -> Dict:
        """Get all safety zones."""
        return {"success": True, "data": self._zones}

    def _cmd_arm_zone(self, zone_id=None, **kw) -> Dict:
        """Arm a specific safety zone (SRS V.2.c)."""
        for z in self._zones:
            if z["id"] == zone_id:
                z["armed"] = True
                for sid in z["sensors"]:
                    self._set_sensor_armed(sid, True)
                self._add_log("ARM_ZONE", f"Zone '{z['name']}' armed")
                return {"success": True}
        return {"success": False, "message": "Zone not found"}

    def _cmd_disarm_zone(self, zone_id=None, **kw) -> Dict:
        """Disarm a specific safety zone (SRS V.2.c)."""
        for z in self._zones:
            if z["id"] == zone_id:
                z["armed"] = False
                for sid in z["sensors"]:
                    self._set_sensor_armed(sid, False)
                self._add_log("DISARM_ZONE", f"Zone '{z['name']}' disarmed")
                return {"success": True}
        return {"success": False, "message": "Zone not found"}

    def _cmd_create_safety_zone(self, name="", sensors=None, **kw) -> Dict:
        """Create new safety zone (SRS V.2.f)."""
        if not name:
            return {"success": False, "message": "Zone name required"}
        new_id = max((z["id"] for z in self._zones), default=0) + 1
        self._zones.append(
            {"id": new_id, "name": name, "sensors": sensors or [], "armed": False}
        )
        return {"success": True, "zone_id": new_id}

    def _cmd_update_safety_zone(
        self, zone_id=None, name=None, sensors=None, **kw
    ) -> Dict:
        """Update existing safety zone (SRS V.2.h)."""
        for z in self._zones:
            if z["id"] == zone_id:
                if name is not None:
                    z["name"] = name
                if sensors is not None:
                    z["sensors"] = sensors
                return {"success": True}
        return {"success": False, "message": "Zone not found"}

    def _cmd_delete_safety_zone(self, zone_id=None, **kw) -> Dict:
        """Delete safety zone (SRS V.2.g)."""
        original_len = len(self._zones)
        self._zones = [z for z in self._zones if z["id"] != zone_id]
        if len(self._zones) < original_len:
            return {"success": True}
        return {"success": False, "message": "Zone not found"}

    # ========== Sensors ==========
    def _get_sensor_obj_by_id(self, sensor_id: str):
        """Find a sensor object by its string ID (e.g., 'S1', 'M2')."""
        for s in self._sensors:
            # The custom sensor 'id' is an int, so need to construct the string id
            prefix = "M" if isinstance(s, CustomMotionDetector) else "S"
            if f"{prefix}{s.get_sensor_id()}" == sensor_id:
                return s
        return None

    def _cmd_get_sensors(self, **kw) -> Dict:
        """Get all sensors."""
        return {"success": True, "data": [s.get_status() for s in self._sensors]}

    def _cmd_arm_sensor(self, sensor_id="", **kw) -> Dict:
        """Arm individual sensor."""
        self._set_sensor_armed(sensor_id, True)
        return {"success": True}

    def _cmd_disarm_sensor(self, sensor_id="", **kw) -> Dict:
        """Disarm individual sensor."""
        self._set_sensor_armed(sensor_id, False)
        return {"success": True}

    def _set_sensor_armed(self, sensor_id: str, armed: bool):
        """Set sensor armed state."""
        sensor = self._get_sensor_obj_by_id(sensor_id)
        if sensor:
            if armed:
                sensor.arm()
            else:
                sensor.disarm()

    # ========== Alarm Handling (SRS V.2.d) ==========
    def _cmd_trigger_alarm(self, sensor_id="", **kw) -> Dict:
        """Handle alarm condition from sensor (IT-010)."""
        self._state = "ALARM"
        sensor_info = "Unknown"
        zone_info = "Unknown"

        sensor = self._get_sensor_obj_by_id(sensor_id)
        if sensor:
            status = sensor.get_status()
            sensor_info = f"{status.get('id', sensor_id)} ({status.get('type', 'N/A')} @ {status.get('location', 'N/A')})"

        for z in self._zones:
            if sensor_id in z.get("sensors", []):
                zone_info = z["name"]
                break

        self._add_log("INTRUSION", f"Sensor: {sensor_info}, Zone: {zone_info}")

        return {
            "success": True,
            "alarm": True,
            "sensor": sensor_info,
            "zone": zone_info,
            "delay_time": self._delay_time,
            "monitor_phone": self._monitor_phone,
        }

    def _cmd_clear_alarm(self, **kw) -> Dict:
        """Clear alarm state."""
        self._state = "READY"
        return {"success": True}

    # ========== Mode Configuration (SRS V.2.i) ==========
    def _cmd_get_mode_configuration(self, mode="", **kw) -> Dict:
        """Get sensor list for a mode."""
        if mode in self._mode_configs:
            return {"success": True, "data": self._mode_configs[mode]}
        return {"success": False, "message": "Unknown mode"}

    def _cmd_configure_safehome_mode(self, mode="", sensors=None, **kw) -> Dict:
        """Configure which sensors are active in a mode (SRS V.2.i)."""
        if mode and sensors is not None:
            self._mode_configs[mode] = sensors
            return {"success": True}
        return {"success": False, "message": "Mode and sensors required"}

    def _cmd_get_all_modes(self, **kw) -> Dict:
        """Get all mode configurations."""
        return {"success": True, "data": self._mode_configs}

    # ========== Cameras (SRS V.3) ==========
    def _cmd_get_cameras(self, **kw) -> Dict:
        """Get all cameras."""
        return {
            "success": True,
            "data": self.camera_controller.get_all_camera_info(),
        }

    def _cmd_get_camera(self, camera_id="", **kw) -> Dict:
        """Get specific camera."""
        cam_id = self._normalize_camera_id(camera_id)
        if cam_id is None:
            return {"success": False, "message": "Invalid camera ID"}
        try:
            camera = self.camera_controller.get_camera_by_id(cam_id)
        except CameraNotFoundError:
            return {"success": False, "message": "Camera not found"}

        data = {
            "id": camera.get_id(),
            "location": camera.get_location(),
            "enabled": camera.is_enabled(),
            "pan": camera.get_pan_angle(),
            "zoom": camera.get_zoom_level(),
            "has_password": camera.has_password(),
        }
        return {"success": True, "data": data}

    def _normalize_camera_id(self, camera_id: str) -> Optional[int]:
        """Convert identifiers like 'C1' into numeric IDs."""
        if isinstance(camera_id, int):
            return camera_id
        if not camera_id:
            return None
        normalized = str(camera_id).strip().upper()
        if normalized.startswith("C"):
            normalized = normalized[1:]
        try:
            return int(normalized)
        except (TypeError, ValueError):
            return None

    def _get_camera_obj_by_id(self, camera_id: str) -> Optional[SafeHomeCamera]:
        """Find a camera object by its string ID (e.g., 'C1')."""
        cam_id = self._normalize_camera_id(camera_id)
        if cam_id is None:
            return None
        try:
            return self.camera_controller.get_camera_by_id(cam_id)
        except CameraNotFoundError:
            return None

    def _cmd_get_camera_view(self, camera_id: str, **kw) -> Dict:
        """Get the live view (PIL Image) from a camera object."""
        cam_id = self._normalize_camera_id(camera_id)
        if cam_id is None:
            return {"success": False, "message": "Invalid camera ID"}
        view = self.camera_controller.display_single_view(cam_id)
        if view is None:
            return {"success": False, "message": "Camera not available"}
        return {"success": True, "view": view}

    def _cmd_camera_pan(self, camera_id="", direction="", **kw) -> Dict:
        """Pan camera left/right (SRS V.3.b)."""
        cam_id = self._normalize_camera_id(camera_id)
        if cam_id is None:
            return {"success": False, "message": "Invalid camera ID"}

        if direction.upper() == "R":
            control = CameraController.CONTROL_PAN_RIGHT
        else:
            control = CameraController.CONTROL_PAN_LEFT

        success = self.camera_controller.control_single_camera(cam_id, control)
        pan_value = None
        if success:
            camera = self._get_camera_obj_by_id(camera_id)
            pan_value = camera.get_pan_angle() if camera else None
            return {"success": True, "pan": pan_value}
        return {"success": False, "message": "Camera not found"}

    def _cmd_camera_zoom(self, camera_id="", direction="", **kw) -> Dict:
        """Zoom camera in/out (SRS V.3.b)."""
        cam_id = self._normalize_camera_id(camera_id)
        if cam_id is None:
            return {"success": False, "message": "Invalid camera ID"}

        if direction.lower() == "in":
            control = CameraController.CONTROL_ZOOM_IN
        else:
            control = CameraController.CONTROL_ZOOM_OUT

        success = self.camera_controller.control_single_camera(cam_id, control)
        zoom_value = None
        if success:
            camera = self._get_camera_obj_by_id(camera_id)
            zoom_value = camera.get_zoom_level() if camera else None
            return {"success": True, "zoom": zoom_value}
        return {"success": False, "message": "Camera not found"}

    def _cmd_enable_camera(self, camera_id="", **kw) -> Dict:
        """Enable camera (SRS V.3.f)."""
        cam_id = self._normalize_camera_id(camera_id)
        if cam_id is None:
            return {"success": False, "message": "Invalid camera ID"}
        success = self.camera_controller.enable_camera(cam_id)
        if not success:
            return {"success": False, "message": "Camera not found"}
        return {"success": True}

    def _cmd_disable_camera(self, camera_id="", **kw) -> Dict:
        """Disable camera (SRS V.3.g)."""
        cam_id = self._normalize_camera_id(camera_id)
        if cam_id is None:
            return {"success": False, "message": "Invalid camera ID"}
        success = self.camera_controller.disable_camera(cam_id)
        if not success:
            return {"success": False, "message": "Camera not found"}
        return {"success": True}

    def _cmd_set_camera_password(
        self, camera_id="", old_password="", password="", **kw
    ) -> Dict:
        """Set camera password (SRS V.3.c)."""
        cam = self._get_camera_obj_by_id(camera_id)
        if cam is None:
            return {"success": False, "message": "Camera not found"}
        if cam.has_password() and not cam.verify_password(old_password):
            return {"success": False, "message": "Old password incorrect"}

        cam_id = self._normalize_camera_id(camera_id)
        success = self.camera_controller.set_camera_password(cam_id, password)
        if not success:
            return {"success": False, "message": "Unable to set password"}
        return {"success": True}

    def _cmd_delete_camera_password(self, camera_id="", old_password="", **kw) -> Dict:
        """Delete camera password (SRS V.3.d)."""
        cam = self._get_camera_obj_by_id(camera_id)
        if cam is None:
            return {"success": False, "message": "Camera not found"}
        if cam.has_password() and not cam.verify_password(old_password):
            return {"success": False, "message": "Password incorrect"}

        cam_id = self._normalize_camera_id(camera_id)
        success = self.camera_controller.delete_camera_password(cam_id)
        if not success:
            return {"success": False, "message": "Unable to delete password"}
        return {"success": True}

    def _cmd_verify_camera_password(self, camera_id="", password="", **kw) -> Dict:
        """Verify camera password (SRS V.3.a step 8)."""
        cam_id = self._normalize_camera_id(camera_id)
        if cam_id is None:
            return {"success": False, "message": "Invalid camera ID"}
        is_valid = self.camera_controller.validate_camera_password(cam_id, password)
        if is_valid:
            camera = self._get_camera_obj_by_id(camera_id)
            has_password = camera.has_password() if camera else False
            return {"success": True, "has_password": has_password}
        return {"success": False, "message": "Wrong password"}

    def _cmd_get_thumbnails(self, **kw) -> Dict:
        """Get thumbnail data for all enabled cameras without password (SRS V.3.e)."""
        thumbnails = {}
        for cam_id, view in self.camera_controller.display_thumbnail_view():
            thumbnails[f"C{cam_id}"] = view
        return {"success": True, "data": thumbnails}

    # ========== System Settings (SRS V.1.c) ==========
    def _cmd_get_system_settings(self, **kw) -> Dict:
        """Get current system settings."""
        return {
            "success": True,
            "data": {
                "delay_time": self._delay_time,
                "monitor_phone": self._monitor_phone,
            },
        }

    def _cmd_configure_system_settings(
        self,
        delay_time=None,
        monitor_phone=None,
        web_password1=None,
        web_password2=None,
        master_password=None,
        guest_password=None,
        **kw,
    ) -> Dict:
        """Configure system settings (SRS V.1.c)."""
        if delay_time is not None:
            self._delay_time = delay_time
        if monitor_phone:
            self._monitor_phone = monitor_phone
        if web_password1:
            self._web_pw1 = web_password1
        if web_password2:
            self._web_pw2 = web_password2
        if master_password:
            self._master_pw = master_password
        if guest_password is not None:  # Can be empty string to clear
            self._guest_pw = guest_password if guest_password else ""
        return {"success": True}

    # ========== Intrusion Log (SRS V.2.j) ==========
    def _cmd_get_intrusion_log(self, **kw) -> Dict:
        """Get intrusion/event log."""
        return {"success": True, "data": self._logs}

    def _add_log(self, event: str, detail: str):
        """Add entry to log."""
        self._logs.insert(
            0,
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "event": event,
                "detail": detail,
            },
        )
        # Keep last 100 entries
        if len(self._logs) > 100:
            self._logs = self._logs[:100]
