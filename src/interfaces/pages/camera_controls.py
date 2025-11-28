"""
CameraControls - Camera control handlers

Single Responsibility: Handle camera operations.
"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .single_camera_view_page import SingleCameraViewPage


class CameraControlsMixin:
    """Mixin providing camera control handlers"""
    
    def _get_camera(self):
        """Get current camera from context"""
        return self._web_interface.get_context('current_camera')
    
    def _pan(self, direction: str) -> None:
        """Pan camera in direction"""
        cam = self._get_camera()
        if cam:
            self.send_to_system('pan_camera', camera_id=cam['id'], direction=direction)
    
    def _zoom(self, direction: str) -> None:
        """Zoom camera in direction"""
        cam = self._get_camera()
        if cam:
            self.send_to_system('zoom_camera', camera_id=cam['id'], direction=direction)
    
    def _enable(self) -> None:
        """Enable camera"""
        cam = self._get_camera()
        if cam:
            response = self.send_to_system('enable_camera', camera_id=cam['id'])
            if response.get('success'):
                self._show_message("Success", "Camera enabled")
                self._update_buttons(True)
    
    def _disable(self) -> None:
        """Disable camera"""
        cam = self._get_camera()
        if cam:
            response = self.send_to_system('disable_camera', camera_id=cam['id'])
            if response.get('success'):
                self._show_message("Success", "Camera disabled")
                self._update_buttons(False)
    
    def _set_password(self) -> None:
        """Set camera password"""
        from .dialogs.camera_password_dialog import CameraPasswordDialog
        cam = self._get_camera()
        if cam:
            CameraPasswordDialog(
                self._frame.winfo_toplevel(), 
                self._web_interface, cam, 'set'
            ).show()
    
    def _delete_password(self) -> None:
        """Delete camera password"""
        from .dialogs.camera_password_dialog import CameraPasswordDialog
        cam = self._get_camera()
        if cam:
            CameraPasswordDialog(
                self._frame.winfo_toplevel(), 
                self._web_interface, cam, 'delete'
            ).show()
    
    def _update_buttons(self, enabled: bool) -> None:
        """Update enable/disable button states"""
        self._enable_btn.config(state='disabled' if enabled else 'normal')
        self._disable_btn.config(state='normal' if enabled else 'disabled')
