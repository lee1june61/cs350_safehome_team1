"""
SafeHome System - Central controller (SDS: System class)
All UI components communicate ONLY through handle_request().

SRS References:
- V.1: Common functions (login, settings, on/off/reset)
- V.2: Security functions (arm/disarm, zones, modes, alarm, panic)
- V.3: Surveillance functions (camera view, pan/zoom, enable/disable, passwords)
"""

from typing import List, Dict, Any, Optional, Union, Tuple
from datetime import datetime

from ..controllers.camera_controller import CameraController
from ..devices.cameras.safehome_camera import SafeHomeCamera
from ..devices.sensors.sensor_controller import SensorController
from ..devices.sensors.window_door_sensor import WindowDoorSensor
from ..devices.sensors.motion_sensor import MotionSensor
from ..utils.exceptions import CameraNotFoundError
from ..configuration import (
    StorageManager,
    ConfigurationManager,
    LoginManager,
    LogManager,
    AccessLevel,
    SystemSettings,
    SafetyZone,
    SafeHomeMode,
    LoginInterface,
)
from ..configuration.password_utils import hash_password

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

CAMERAS = [
    {"id": "C1", "location": "Front Entry", "x": 220, "y": 185},
    {"id": "C2", "location": "Living Room", "x": 438, "y": 609},
    {"id": "C3", "location": "Back Patio", "x": 775, "y": 827},
]

SENSOR_COORDS: Dict[str, Tuple[int, int]] = {
    "S1": (35, 90),
    "S2": (115, 36),
    "S3": (35, 255),
    "S4": (450, 42),
    "S5": (582, 140),
    "S6": (582, 275),
    "M1": (70, 140),
    "M2": (285, 190),
}


class System:
    """Main system controller - handles all requests from UI components."""

    MODE_HOME = "HOME"
    MODE_AWAY = "AWAY"
    MODE_DISARMED = "DISARMED"

    def __init__(self, db_path: str = "safehome.db"):
        self._state = "OFF"  # OFF, READY, ALARM
        self._mode = self.MODE_DISARMED
        self._user: Optional[str] = None
        self._verified = False
        self._access_level: Optional[int] = None

        # Initialize configuration subsystem
        self._storage = StorageManager.get_instance(db_path)
        self._storage.connect()
        self._config_manager = ConfigurationManager(self._storage)
        self._login_manager = LoginManager(self._storage)
        self._log_manager = LogManager(self._storage)

        # Initialize configuration with defaults if needed
        self._config_manager.initialize_configuration()
        self._initialize_default_users()

        # Load system settings
        self._settings = self._config_manager.get_system_settings()
        self._delay_time = self._settings.alarm_delay_time
        self._monitor_phone = self._settings.monitoring_service_phone

        # Sensor controller + metadata
        self.sensor_controller = SensorController()
        self._sensor_lookup: Dict[str, int] = {}
        self._sensor_metadata: Dict[str, Dict[str, Any]] = {}
        self._sensors: List[Union[WindowDoorSensor, MotionSensor]] = []
        self._initialize_sensors()

        self.camera_controller = CameraController()
        self._camera_lookup: Dict[str, int] = {}
        self._camera_labels: Dict[int, str] = {}
        self._initialize_cameras()

        # Load safety zones from configuration
        self._sync_zones_from_config()

        # Load mode configurations
        self._sync_modes_from_config()

        # Login state (kept for backward compatibility with lock mechanism)
        self._attempts = 3
        self._locked = False
        self._lock_time: Optional[datetime] = None

    # ========== Configuration Sync Helpers ==========
    def _initialize_default_users(self):
        """Create default users if they don't exist."""
        from datetime import datetime

        # Check if master user exists
        existing = self._storage.get_login_interface("master", "control_panel")
        if not existing:
            # Create master user with 4-digit password "1234" for control panel
            master_data = {
                "username": "master",
                "password_hash": hash_password("1234"),
                "interface": "control_panel",
                "access_level": int(AccessLevel.MASTER_ACCESS),
                "login_attempts": 0,
                "is_locked": False,
                "password_min_length": 4,
                "password_requires_digit": False,
                "password_requires_special": False,
                "created_at": datetime.utcnow().isoformat(),
                "last_login": None,
            }
            self._storage.save_login_interface(master_data)

        # Check if guest user exists
        existing_guest = self._storage.get_login_interface("guest", "control_panel")
        if not existing_guest:
            # Create guest user with 4-digit password "5678" for control panel
            guest_data = {
                "username": "guest",
                "password_hash": hash_password("5678"),
                "interface": "control_panel",
                "access_level": int(AccessLevel.GUEST_ACCESS),
                "login_attempts": 0,
                "is_locked": False,
                "password_min_length": 4,
                "password_requires_digit": False,
                "password_requires_special": False,
                "created_at": datetime.utcnow().isoformat(),
                "last_login": None,
            }
            self._storage.save_login_interface(guest_data)

        # Check if admin user exists for web interface
        existing_admin = self._storage.get_login_interface("admin", "web")
        if not existing_admin:
            # Create admin user with password "password" for web interface
            admin_data = {
                "username": "admin",
                "password_hash": hash_password("password"),
                "interface": "web",
                "access_level": int(AccessLevel.MASTER_ACCESS),
                "login_attempts": 0,
                "is_locked": False,
                "password_min_length": 4,
                "password_requires_digit": False,
                "password_requires_special": False,
                "created_at": datetime.utcnow().isoformat(),
                "last_login": None,
            }
            self._storage.save_login_interface(admin_data)

    def _sync_zones_from_config(self):
        """Load safety zones from configuration database."""
        config_zones = self._config_manager.get_all_safety_zones()
        if not config_zones:
            # Initialize with default zones if none exist
            for z in SAFETY_ZONES:
                zone = SafetyZone(
                    zone_id=0,
                    zone_name=z["name"],
                    sensor_ids=z["sensors"],
                    is_armed=False,
                )
                self._config_manager.add_safety_zone(zone)
            config_zones = self._config_manager.get_all_safety_zones()

        self._zones = [
            {
                "id": z.zone_id,
                "name": z.zone_name,
                "sensors": z.sensor_ids[:],
                "armed": z.is_armed,
            }
            for z in config_zones
        ]

    def _sync_modes_from_config(self):
        """Load mode configurations from configuration database."""
        config_modes = self._config_manager.get_all_safehome_modes()
        self._mode_configs = {}
        for mode in config_modes:
            mode_name = mode.mode_name.upper()
            self._mode_configs[mode_name] = mode.sensor_ids[:]

        # Ensure default modes exist
        if not self._mode_configs:
            self._mode_configs = {k: v[:] for k, v in MODE_CONFIGS.items()}

    # ========== System Lifecycle ==========
    def turn_on(self):
        """Turn system on."""
        self._state = "READY"

    def turn_off(self):
        """Turn system off."""
        self._state = "OFF"
        self._user = None
        self._verified = False
        self._access_level = None
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

    def _cmd_login_control_panel(self, password="", username="master", **kw) -> Dict:
        """Login via control panel (4-digit password) - SRS V.1.a."""
        lock = self._check_lock()
        if lock:
            return lock

        try:
            access_level = self._login_manager.login(
                username, password, "control_panel"
            )
            if access_level is not None:
                self._user = username
                self._access_level = access_level
                self._attempts = 3
                level_name = (
                    "MASTER" if access_level == AccessLevel.MASTER_ACCESS else "GUEST"
                )
                log = self._log_manager.create_log(
                    "LOGIN", f"Control panel login: {username}", "INFO", username
                )
                self._log_manager.save_log(log)
                return {"success": True, "access_level": level_name}
        except Exception as e:
            log = self._log_manager.create_log(
                "LOGIN", f"Login failed: {str(e)}", "WARNING"
            )
            self._log_manager.save_log(log)

        self._attempts -= 1
        if self._attempts <= 0:
            self._locked = True
            self._lock_time = datetime.now()
        return {"success": False, "attempts_remaining": self._attempts}

    def _cmd_login_web(
        self, user_id="", password1="", password2="", password="", **kw
    ) -> Dict:
        """Login via web (user ID + password) - SRS V.1.b."""
        lock = self._check_lock()
        if lock:
            return lock

        # Use single password if provided, otherwise use password1
        pwd = password or password1

        try:
            access_level = self._login_manager.login(user_id, pwd, "web")
            if access_level is not None:
                self._user = user_id
                self._access_level = access_level
                self._attempts = 3
                log = self._log_manager.create_log(
                    "LOGIN", f"Web login: {user_id}", "INFO", user_id
                )
                self._log_manager.save_log(log)
                return {"success": True}
        except Exception as e:
            log = self._log_manager.create_log(
                "LOGIN", f"Web login failed: {str(e)}", "WARNING"
            )
            self._log_manager.save_log(log)

        self._attempts -= 1
        if self._attempts <= 0:
            self._locked = True
            self._lock_time = datetime.now()
        return {"success": False, "attempts_remaining": self._attempts}

    def _cmd_web_login(
        self, user_id="", password="", password1="", password2="", **kw
    ) -> Dict:
        """Backward-compatible alias used by legacy interfaces."""
        if not password1 and not password2 and password:
            password1 = password2 = password
        return self._cmd_login_web(
            user_id=user_id, password1=password1, password2=password2
        )

    def _cmd_logout(self, **kw) -> Dict:
        """Logout current user - SRS V.1.a."""
        if self._user:
            log = self._log_manager.create_log(
                "LOGOUT", f"User logged out: {self._user}", "INFO", self._user
            )
            self._log_manager.save_log(log)
        self._login_manager.logout()
        self._user = None
        self._access_level = None
        self._verified = False
        return {"success": True}

    def _cmd_verify_identity(self, value="", **kw) -> Dict:
        """Verify identity with address or phone (SRS V.2.b step 3)."""
        v = value.strip()
        if not v:
            return {"success": False, "message": "Please enter address or phone number"}

        # Remove common formatting characters
        cleaned = v.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")

        # Check if it's all digits (phone number) - must be at least 10 digits
        if cleaned.isdigit():
            if len(cleaned) >= 10:
                self._verified = True
                return {"success": True}
            else:
                return {
                    "success": False,
                    "message": "Phone number must be at least 10 digits",
                }

        # Check if it's an address (contains letters and numbers/address components)
        # Address should have at least 5 characters and contain letters
        if len(v) >= 5 and any(c.isalpha() for c in v):
            self._verified = True
            return {"success": True}

        return {
            "success": False,
            "message": "Invalid verification. Enter a valid phone number (10+ digits) or address (5+ chars with letters)",
        }

    def _cmd_is_verified(self, **kw) -> Dict:
        """Check if user identity is verified."""
        return {"success": True, "verified": self._verified}

    def _cmd_change_password(
        self,
        current_password="",
        new_password="",
        username="master",
        interface="control_panel",
        **kw,
    ) -> Dict:
        """Change password (SRS V.1.g)."""
        if not self._user:
            return {"success": False, "message": "Must be logged in"}

        try:
            success = self._login_manager.change_password(
                username, current_password, new_password, interface
            )
            if success:
                log = self._log_manager.create_log(
                    "CONFIGURATION",
                    f"Password changed for {username}",
                    "INFO",
                    self._user,
                )
                self._log_manager.save_log(log)
                return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}

        return {"success": False, "message": "Password change failed"}

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
        sensor_states = self._collect_sensor_statuses()
        active_sensors = sum(1 for s in sensor_states if s.get("armed"))
        camera_states = self.camera_controller.get_all_camera_info()
        enabled_cameras = sum(1 for c in camera_states if c.get("enabled"))
        return {
            "success": True,
            "data": {
                "state": self._state,
                "mode": self._mode,
                "armed": self._mode != self.MODE_DISARMED,
                "user": self._user,
                "verified": self._verified,
                "alarm_active": self._state == "ALARM",
                "sensor_count": len(sensor_states),
                "active_sensors": active_sensors,
                "camera_count": len(camera_states),
                "enabled_cameras": enabled_cameras,
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
        for sensor_id, metadata in self._sensor_metadata.items():
            if metadata.get("type") not in {"WINDOW", "DOOR"}:
                continue
            sensor = self._get_sensor_obj_by_id(sensor_id)
            if sensor and hasattr(sensor, "can_arm") and not sensor.can_arm():
                location = (
                    metadata.get("location")
                    or getattr(sensor, "get_location", lambda: sensor_id)()
                )
                return {
                    "success": False,
                    "message": f"Cannot arm. {location} is open.",
                }

        self._mode = mode
        # Arm sensors based on mode configuration
        active_sensors = set(self._mode_configs.get(mode, []))
        for sensor_id in self._sensor_lookup.keys():
            self._set_sensor_armed(sensor_id, sensor_id in active_sensors)

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

        zone = SafetyZone(
            zone_id=0, zone_name=name, sensor_ids=sensors or [], is_armed=False
        )
        success = self._config_manager.add_safety_zone(zone)
        if success:
            self._sync_zones_from_config()
            log = self._log_manager.create_log(
                "CONFIGURATION", f"Safety zone created: {name}", "INFO", self._user
            )
            self._log_manager.save_log(log)
            # Find the newly created zone ID
            for z in self._zones:
                if z["name"] == name:
                    return {"success": True, "zone_id": z["id"]}
        return {"success": False, "message": "Failed to create zone"}

    def _cmd_update_safety_zone(
        self, zone_id=None, name=None, sensors=None, **kw
    ) -> Dict:
        """Update existing safety zone (SRS V.2.h)."""
        zone = self._config_manager.get_safety_zone(zone_id)
        if not zone:
            return {"success": False, "message": "Zone not found"}

        if name is not None:
            zone.zone_name = name
        if sensors is not None:
            zone.sensor_ids = sensors

        success = self._config_manager.update_safety_zone(zone)
        if success:
            self._sync_zones_from_config()
            log = self._log_manager.create_log(
                "CONFIGURATION",
                f"Safety zone updated: {zone.zone_name}",
                "INFO",
                self._user,
            )
            self._log_manager.save_log(log)
            return {"success": True}
        return {"success": False, "message": "Failed to update zone"}

    def _cmd_delete_safety_zone(self, zone_id=None, **kw) -> Dict:
        """Delete safety zone (SRS V.2.g)."""
        zone = self._config_manager.get_safety_zone(zone_id)
        if not zone:
            return {"success": False, "message": "Zone not found"}

        success = self._config_manager.delete_safety_zone(zone_id)
        if success:
            self._sync_zones_from_config()
            log = self._log_manager.create_log(
                "CONFIGURATION",
                f"Safety zone deleted: {zone.zone_name}",
                "INFO",
                self._user,
            )
            self._log_manager.save_log(log)
            return {"success": True}
        return {"success": False, "message": "Failed to delete zone"}

    # ========== Sensors ==========
    def _initialize_sensors(self):
        sensors: List[Union[WindowDoorSensor, MotionSensor]] = []
        for sensor_data in SENSORS:
            sensor_id = sensor_data.get("id")
            if not sensor_id:
                continue

            coords = SENSOR_COORDS.get(sensor_id, (0, 0))
            sensor_type = (
                SensorController.SENSOR_TYPE_MOTION
                if sensor_data.get("type") == "MOTION"
                else SensorController.SENSOR_TYPE_WINDOW_DOOR
            )
            added = self.sensor_controller.addSensor(coords[0], coords[1], sensor_type)
            if not added:
                continue

            controller_id = self.sensor_controller.nextSensorID - 1
            sensor_obj = self.sensor_controller.getSensor(controller_id)
            display_name = (
                sensor_data.get("name") or sensor_data.get("location") or sensor_id
            )
            category = sensor_data.get("type", "").lower()
            extra = {"label": sensor_data.get("location")}
            if hasattr(sensor_obj, "set_metadata"):
                sensor_obj.set_metadata(
                    friendly_id=sensor_id,
                    location_name=display_name,
                    category=category,
                    extra=extra,
                )
            else:  # Fallback (older sensor implementations)
                setattr(sensor_obj, "friendly_id", sensor_id)
                setattr(sensor_obj, "location_name", display_name)
            self._sensor_lookup[sensor_id] = controller_id
            self._sensor_metadata[sensor_id] = sensor_data

            if sensor_data.get("armed"):
                sensor_obj.arm()
            else:
                sensor_obj.disarm()

            sensors.append(sensor_obj)

        self._sensors = sensors

    def _initialize_cameras(self):
        """Instantiate default cameras for surveillance functions."""
        for cam_data in CAMERAS:
            cam_name = cam_data.get("id")
            if not cam_name:
                continue
            x_coord = int(cam_data.get("x", 0))
            y_coord = int(cam_data.get("y", 0))
            controller_id = self.camera_controller.add_camera(x_coord, y_coord)
            if controller_id is None:
                continue
            label = cam_data.get("location", cam_name)
            self._camera_lookup[cam_name] = controller_id
            self._camera_labels[controller_id] = label
            camera = self.camera_controller.get_camera_by_id(controller_id)
            if camera:
                camera.enable()

    def _collect_sensor_statuses(self) -> List[Dict[str, Any]]:
        """Return sensor statuses sorted by ID for UI queries."""
        statuses: List[Dict[str, Any]] = []
        for sensor_id in sorted(self._sensor_lookup.keys()):
            sensor = self._get_sensor_obj_by_id(sensor_id)
            if not sensor:
                continue
            status = sensor.get_status()
            status.setdefault("id", sensor_id)
            if "name" not in status:
                try:
                    status["name"] = sensor.get_location()
                except Exception:
                    status["name"] = sensor_id
            statuses.append(status)
        return statuses

    def _get_sensor_obj_by_id(self, sensor_id: str):
        """Find a sensor object by its string ID (e.g., 'S1', 'M2')."""
        internal_id = self._sensor_lookup.get(sensor_id)
        if internal_id is None:
            return None
        return self.sensor_controller.getSensor(internal_id)

    def _cmd_get_sensors(self, **kw) -> Dict:
        """Get all sensors."""
        return {"success": True, "data": self._collect_sensor_statuses()}

    def _cmd_get_all_devices_status(self, **kw) -> Dict:
        """Get status of all devices (sensors and cameras) for floorplan display."""
        devices: Dict[str, Dict[str, Any]] = {}

        for status in self._collect_sensor_statuses():
            dev_id = status.get("id", "Unknown")
            devices[dev_id] = {
                "type": status.get("type", "sensor"),
                "armed": status.get("armed", False),
                "location": status.get("location", "Unknown"),
                "status": status.get("status", "closed"),
                "name": status.get("name", dev_id),
            }

        for cam in self.camera_controller.get_all_camera_info():
            cam_id = cam.get("id", "Unknown")
            dev_id = str(cam_id)
            if isinstance(cam_id, int):
                dev_id = f"C{cam_id}"
            location = self._camera_labels.get(cam_id, cam.get("location", "Unknown"))
            devices[dev_id] = {
                "type": "camera",
                "armed": cam.get("enabled", False),
                "location": location,
                "enabled": cam.get("enabled", False),
            }

        return {"success": True, "data": devices}

    def _cmd_arm_sensor(self, sensor_id="", **kw) -> Dict:
        """Arm individual sensor."""
        if not self._set_sensor_armed(sensor_id, True):
            return {"success": False, "message": "Sensor not found"}
        return {"success": True}

    def _cmd_disarm_sensor(self, sensor_id="", **kw) -> Dict:
        """Disarm individual sensor."""
        if not self._set_sensor_armed(sensor_id, False):
            return {"success": False, "message": "Sensor not found"}
        return {"success": True}

    def _cmd_poll_sensors(self, **kw) -> Dict:
        """Poll armed sensors to detect intrusions (legacy command)."""
        if self._mode == self.MODE_DISARMED:
            return {"success": True, "intrusion_detected": False}

        for sensor_id in self._sensor_lookup.keys():
            sensor = self._get_sensor_obj_by_id(sensor_id)
            if not sensor:
                continue
            status = sensor.get_status()
            if not status.get("armed"):
                continue
            triggered = bool(status.get("is_open")) or bool(status.get("triggered"))
            if triggered:
                alarm = self._cmd_trigger_alarm(sensor_id=sensor_id)
                return {
                    "success": True,
                    "intrusion_detected": True,
                    "sensor_id": sensor_id,
                    "alarm": alarm,
                }

        return {"success": True, "intrusion_detected": False}

    def _set_sensor_armed(self, sensor_id: str, armed: bool):
        """Set sensor armed state."""
        sensor = self._get_sensor_obj_by_id(sensor_id)
        if not sensor:
            return False
        if armed:
            sensor.arm()
        else:
            sensor.disarm()
        return True

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

    def _cmd_get_alarm_status(self, **kw) -> Dict:
        """Get current alarm status for polling."""
        is_alarm = self._state == "ALARM"
        sensor_id = "Unknown"
        zone_name = "Unknown"
        alarm_type = "INTRUSION"

        # If alarm is active, try to get sensor/zone info from recent log
        if is_alarm and self._logs:
            latest = self._logs[0]
            if latest.get("event") == "INTRUSION":
                detail = latest.get("detail", "")
                # Parse detail string if needed
                if "Sensor:" in detail and "Zone:" in detail:
                    parts = detail.split("Zone:")
                    if len(parts) == 2:
                        zone_name = parts[1].strip()
                        sensor_part = parts[0].replace("Sensor:", "").strip()
                        # Extract sensor ID from format like "S1 (WINDOW @ DR Top)"
                        if "(" in sensor_part:
                            sensor_id = sensor_part.split("(")[0].strip()

        return {
            "success": True,
            "data": {
                "alarm_active": is_alarm,
                "sensor_id": sensor_id,
                "zone_name": zone_name,
                "alarm_type": alarm_type,
            },
        }

    # ========== Mode Configuration (SRS V.2.i) ==========
    def _cmd_get_mode_configuration(self, mode="", **kw) -> Dict:
        """Get sensor list for a mode."""
        if mode in self._mode_configs:
            return {"success": True, "data": self._mode_configs[mode]}
        return {"success": False, "message": "Unknown mode"}

    def _cmd_configure_safehome_mode(self, mode="", sensors=None, **kw) -> Dict:
        """Configure which sensors are active in a mode (SRS V.2.i)."""
        if not mode or sensors is None:
            return {"success": False, "message": "Mode and sensors required"}

        invalid = [sid for sid in sensors if sid not in self._sensor_lookup]
        if invalid:
            return {
                "success": False,
                "message": f"Unknown sensors: {', '.join(sorted(invalid))}",
            }

        # Find mode by name
        mode_name = mode.upper()
        modes = self._config_manager.get_all_safehome_modes()
        for m in modes:
            if m.mode_name.upper() == mode_name:
                m.sensor_ids = sensors
                success = self._config_manager.update_safehome_mode(m)
                if success:
                    self._sync_modes_from_config()
                    log = self._log_manager.create_log(
                        "CONFIGURATION",
                        f"Mode configured: {mode_name}",
                        "INFO",
                        self._user,
                    )
                    self._log_manager.save_log(log)
                    return {"success": True}
                return {"success": False, "message": "Failed to update mode"}

        return {"success": False, "message": "Mode not found"}

    def _cmd_get_all_modes(self, **kw) -> Dict:
        """Get all mode configurations."""
        return {"success": True, "data": self._mode_configs}

    # ========== Cameras (SRS V.3) ==========
    def _cmd_get_cameras(self, **kw) -> Dict:
        """Get all cameras."""
        cameras = []
        for cam in self.camera_controller.get_all_camera_info():
            cam_id = cam.get("id")
            if cam_id is None:
                continue
            label = self._camera_labels.get(cam_id, f"C{cam_id}")
            cameras.append(
                {
                    "id": f"C{cam_id}",
                    "location": label,
                    "coords": cam.get("location"),
                    "enabled": cam.get("enabled", False),
                    "pan": cam.get("pan"),
                    "zoom": cam.get("zoom"),
                    "has_password": cam.get("has_password"),
                }
            )
        return {"success": True, "data": cameras}

    def _cmd_get_camera(self, camera_id="", **kw) -> Dict:
        """Get specific camera."""
        cam_id = self._normalize_camera_id(camera_id)
        if cam_id is None:
            return {"success": False, "message": "Invalid camera ID"}
        try:
            camera = self.camera_controller.get_camera_by_id(cam_id)
        except CameraNotFoundError:
            return {"success": False, "message": "Camera not found"}

        coords = camera.get_location()
        label = self._camera_labels.get(cam_id, f"C{cam_id}")
        data = {
            "id": f"C{camera.get_id()}",
            "location": label,
            "coords": coords,
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

    def _cmd_pan_camera(self, **kw) -> Dict:
        """Alias for legacy command naming."""
        return self._cmd_camera_pan(**kw)

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

    def _cmd_zoom_camera(self, **kw) -> Dict:
        """Alias for legacy command naming."""
        return self._cmd_camera_zoom(**kw)

    def _cmd_camera_tilt(self, camera_id="", direction="", **kw) -> Dict:
        """Tilt camera up/down (SRS V.3.b)."""
        cam = self._get_camera_obj_by_id(camera_id)
        if cam:
            if hasattr(cam, "tilt_up") and hasattr(cam, "tilt_down"):
                success = cam.tilt_up() if direction == "up" else cam.tilt_down()
                return {"success": success, "tilt": cam.tilt_angle}
            else:
                return {"success": False, "message": "Tilt not supported"}
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
        """Get thumbnail data for all enabled cameras (SRS V.3.e).
        Includes cameras with passwords but marks them as locked."""
        thumbnails = {}
        for cam_id, view in self.camera_controller.display_thumbnail_view():
            thumbnails[f"C{cam_id}"] = view
        return {"success": True, "data": thumbnails}

    # ========== System Settings (SRS V.1.c) ==========
    def _cmd_get_system_settings(self, **kw) -> Dict:
        """Get current system settings - SRS V.1.c."""
        settings = self._config_manager.get_system_settings()
        return {
            "success": True,
            "data": {
                "delay_time": settings.alarm_delay_time,
                "monitor_phone": settings.monitoring_service_phone,
                "homeowner_phone": settings.homeowner_phone,
                "system_lock_time": settings.system_lock_time,
                "max_login_attempts": settings.max_login_attempts,
                "session_timeout": settings.session_timeout,
            },
        }

    def _cmd_configure_system_settings(
        self,
        delay_time=None,
        monitor_phone=None,
        homeowner_phone=None,
        system_lock_time=None,
        max_login_attempts=None,
        session_timeout=None,
        **kw,
    ) -> Dict:
        """Configure system settings (SRS V.1.c)."""
        settings = self._config_manager.get_system_settings()

        if delay_time is not None:
            settings.alarm_delay_time = delay_time
            self._delay_time = delay_time
        if monitor_phone is not None:
            settings.monitoring_service_phone = monitor_phone
            self._monitor_phone = monitor_phone
        if homeowner_phone is not None:
            settings.homeowner_phone = homeowner_phone
        if system_lock_time is not None:
            settings.system_lock_time = system_lock_time
        if max_login_attempts is not None:
            settings.max_login_attempts = max_login_attempts
        if session_timeout is not None:
            settings.session_timeout = session_timeout

        try:
            success = self._config_manager.update_system_settings(settings)
            if success:
                log = self._log_manager.create_log(
                    "CONFIGURATION", "System settings updated", "INFO", self._user
                )
                self._log_manager.save_log(log)
                return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}

        return {"success": False, "message": "Failed to update settings"}

    # ========== Intrusion Log (SRS V.2.j) ==========
    def _cmd_get_intrusion_log(self, **kw) -> Dict:
        """Get intrusion/event log."""
        logs = self._log_manager.get_logs(limit=100)
        log_data = [
            {
                "timestamp": (
                    log.timestamp.strftime("%Y-%m-%d %H:%M:%S") if log.timestamp else ""
                ),
                "event": log.event_type,
                "detail": log.description,
                "severity": log.severity,
            }
            for log in logs
        ]
        return {"success": True, "data": log_data}

    def _cmd_get_intrusion_logs(self, **kw) -> Dict:
        """Alias for pluralized command name."""
        return self._cmd_get_intrusion_log(**kw)

    def _add_log(self, event: str, detail: str):
        """Add entry to log - uses LogManager."""
        severity = "ERROR" if event in ("INTRUSION", "PANIC", "ALARM") else "INFO"
        log = self._log_manager.create_log(event, detail, severity, self._user)
        self._log_manager.save_log(log)
