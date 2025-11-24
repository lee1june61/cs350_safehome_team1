"""
Camera Controller Module
=========================
Manages a collection of SafeHomeCamera instances.

This class provides centralized control over all cameras in the SafeHome system,
including creation, deletion, enabling/disabling, and command execution.
"""

from __future__ import annotations

import threading
from typing import Dict, List, Optional, Any, Tuple

from ..models.camera import SafeHomeCamera
from ..utils.exceptions import CameraNotFoundError, CameraPasswordError


class CameraController:
    """
    Controller for managing multiple SafeHomeCamera instances.
    
    This class manages a collection of cameras, providing methods to add,
    remove, enable/disable, and control cameras. Cameras are stored in a
    dictionary indexed by their ID for efficient lookup.
    
    Attributes:
        next_camera_id (int): The ID to assign to the next created camera
        total_camera_number (int): The total number of cameras currently managed
    """
    
    # Control ID constants
    CONTROL_PAN_LEFT = 1
    CONTROL_PAN_RIGHT = 2
    CONTROL_ZOOM_IN = 3
    CONTROL_ZOOM_OUT = 4
    
    def __init__(self) -> None:
        """Initialize the camera controller."""
        # Public attributes
        self.next_camera_id: int = 1
        self.total_camera_number: int = 0
        
        # Private attributes
        self._cameras: Dict[int, SafeHomeCamera] = {}
        self._lock: threading.RLock = threading.RLock()
    
    # ------------------------------------------------------------------
    # Camera management methods
    # ------------------------------------------------------------------
    
    def add_camera(self, x_coord: int, y_coord: int) -> int:
        """
        Create and add a new camera to the system.
        
        Args:
            x_coord (int): X coordinate of the camera location
            y_coord (int): Y coordinate of the camera location
        
        Returns:
            int: The ID of the newly created camera
        """
        with self._lock:
            camera_id = self.next_camera_id
            camera = SafeHomeCamera(camera_id, x_coord, y_coord)
            camera.validate()
            self._cameras[camera_id] = camera
            self.next_camera_id += 1
            self.total_camera_number += 1
            return camera_id
    
    def delete_camera(self, camera_id: int) -> bool:
        """
        Remove a camera from the system.
        
        Args:
            camera_id (int): The ID of the camera to remove
        
        Returns:
            bool: True if camera was successfully removed, False if not found
        """
        with self._lock:
            if camera_id not in self._cameras:
                return False
            camera = self._cameras[camera_id]
            camera.cleanup()
            del self._cameras[camera_id]
            self.total_camera_number -= 1
            return True
    
    def get_camera_by_id(self, camera_id: int) -> SafeHomeCamera:
        """
        Get a camera instance by its ID.
        
        Args:
            camera_id (int): The ID of the camera to retrieve
        
        Returns:
            SafeHomeCamera: The camera instance
        
        Raises:
            CameraNotFoundError: If camera ID is not found
        """
        with self._lock:
            if camera_id not in self._cameras:
                raise CameraNotFoundError(f"Camera with ID {camera_id} not found")
            return self._cameras[camera_id]
    
    def get_all_cameras(self) -> List[SafeHomeCamera]:
        """
        Get all camera instances.
        
        Returns:
            List[SafeHomeCamera]: List of all camera instances
        """
        with self._lock:
            return list(self._cameras.values())
    
    def get_total_camera_number(self) -> int:
        """
        Get the total number of cameras currently managed.
        
        Returns:
            int: The total number of cameras
        """
        with self._lock:
            return self.total_camera_number
    
    # ------------------------------------------------------------------
    # Enable/Disable methods
    # ------------------------------------------------------------------
    
    def enable_cameras(self, camera_id_list: List[int]) -> int:
        """
        Enable multiple cameras by their IDs.
        
        Args:
            camera_id_list (List[int]): List of camera IDs to enable
        
        Returns:
            int: The number of cameras successfully enabled
        """
        with self._lock:
            enabled_count = 0
            for camera_id in camera_id_list:
                if camera_id in self._cameras:
                    self._cameras[camera_id].enable()
                    enabled_count += 1
            return enabled_count
    
    def disable_cameras(self, camera_id_list: List[int]) -> int:
        """
        Disable multiple cameras by their IDs.
        
        Args:
            camera_id_list (List[int]): List of camera IDs to disable
        
        Returns:
            int: The number of cameras successfully disabled
        """
        with self._lock:
            disabled_count = 0
            for camera_id in camera_id_list:
                if camera_id in self._cameras:
                    self._cameras[camera_id].disable()
                    disabled_count += 1
            return disabled_count
    
    def enable_all_cameras(self) -> None:
        """Enable all cameras in the system."""
        with self._lock:
            for camera in self._cameras.values():
                camera.enable()
    
    def disable_all_cameras(self) -> None:
        """Disable all cameras in the system."""
        with self._lock:
            for camera in self._cameras.values():
                camera.disable()
    
    # ------------------------------------------------------------------
    # Camera control methods
    # ------------------------------------------------------------------
    
    def control_single_camera(self, camera_id: int, control_id: int) -> bool:
        """
        Execute a control command on a specific camera.
        
        Args:
            camera_id (int): The ID of the camera to control
            control_id (int): The control command to execute:
                             1 = Pan Left
                             2 = Pan Right
                             3 = Zoom In
                             4 = Zoom Out
        
        Returns:
            bool: True if command was successful, False otherwise
        
        Raises:
            CameraNotFoundError: If camera ID is invalid
            ValueError: If control ID is unknown
        """
        with self._lock:
            camera = self.get_camera_by_id(camera_id)
            
            if control_id == self.CONTROL_PAN_LEFT:
                return camera.pan_left()
            elif control_id == self.CONTROL_PAN_RIGHT:
                return camera.pan_right()
            elif control_id == self.CONTROL_ZOOM_IN:
                return camera.zoom_in()
            elif control_id == self.CONTROL_ZOOM_OUT:
                return camera.zoom_out()
            else:
                raise ValueError(f"Unknown control ID: {control_id}")
    
    # ------------------------------------------------------------------
    # Display methods
    # ------------------------------------------------------------------
    
    def display_single_view(self, camera_id: int) -> Optional[Any]:
        """
        Get the current view from a specific camera.
        
        Args:
            camera_id (int): The ID of the camera to get the view from
        
        Returns:
            Optional[Any]: The camera frame (PIL Image) or None if error
        
        Raises:
            CameraNotFoundError: If camera ID is invalid
        """
        with self._lock:
            camera = self.get_camera_by_id(camera_id)
            try:
                return camera.display_view()
            except Exception as e:
                print(f"Error displaying view from camera {camera_id}: {e}")
                return None
    
    def display_thumbnail_view(self) -> List[Tuple[int, Optional[Any]]]:
        """
        Get thumbnail views from all enabled cameras.
        
        Returns:
            List[Tuple[int, Optional[Any]]]: List of tuples containing
                                              (camera_id, image) for each enabled camera
        """
        with self._lock:
            thumbnails = []
            for camera_id, camera in self._cameras.items():
                if camera.is_enabled():
                    try:
                        view = camera.display_view()
                        thumbnails.append((camera_id, view))
                    except Exception:
                        thumbnails.append((camera_id, None))
            return thumbnails
    
    # ------------------------------------------------------------------
    # Password management methods
    # ------------------------------------------------------------------
    
    def set_camera_password(self, camera_id: int, password: str) -> bool:
        """
        Set a password for a specific camera.
        
        Args:
            camera_id (int): The ID of the camera
            password (str): The password to set
        
        Returns:
            bool: True if password was set successfully
        
        Raises:
            CameraNotFoundError: If camera not found
            CameraPasswordError: If password is invalid
        """
        with self._lock:
            camera = self.get_camera_by_id(camera_id)
            camera.set_password(password)
            return True
    
    def validate_camera_password(self, camera_id: int, password: str) -> bool:
        """
        Validate a password for a specific camera.
        
        Args:
            camera_id (int): The ID of the camera
            password (str): The password to validate
        
        Returns:
            bool: True if password is correct, False otherwise
        """
        with self._lock:
            try:
                camera = self.get_camera_by_id(camera_id)
                if not camera.has_password():
                    return False
                return camera.get_password() == password
            except CameraNotFoundError:
                return False
    
    # ------------------------------------------------------------------
    # Information methods
    # ------------------------------------------------------------------
    
    def get_all_camera_info(self) -> List[Dict[str, Any]]:
        """
        Get information about all cameras in the system.
        
        Returns:
            List[Dict[str, Any]]: List of dictionaries containing camera information.
                                  Each dictionary includes:
                                  - id: Camera ID
                                  - location: (x, y) coordinates
                                  - enabled: Whether camera is enabled
                                  - pan_angle: Current pan angle
                                  - zoom_setting: Current zoom level
                                  - has_password: Whether camera has a password
        """
        with self._lock:
            camera_info_list = []
            for camera_id, camera in self._cameras.items():
                info = {
                    'id': camera.get_id(),
                    'location': camera.get_location(),
                    'enabled': camera.is_enabled(),
                    'pan_angle': camera.get_pan_angle(),
                    'zoom_level': camera.get_zoom_level(),
                    'has_password': camera.has_password()
                }
                camera_info_list.append(info)
            return camera_info_list
    
    # ------------------------------------------------------------------
    # Cleanup methods
    # ------------------------------------------------------------------
    
    def cleanup(self) -> None:
        """
        Cleanup all cameras and release resources.
        This method should be called when the controller is no longer needed.
        """
        with self._lock:
            for camera in self._cameras.values():
                camera.cleanup()
            self._cameras.clear()
            self.total_camera_number = 0
    
    # ------------------------------------------------------------------
    # Special methods
    # ------------------------------------------------------------------
    
    def __del__(self) -> None:
        """Destructor to ensure cleanup."""
        self.cleanup()
    
    def __repr__(self) -> str:
        """
        String representation of the camera controller.
        
        Returns:
            str: A string describing the controller state
        """
        with self._lock:
            return (f"CameraController(total_cameras={self.total_camera_number}, "
                    f"next_id={self.next_camera_id})")

