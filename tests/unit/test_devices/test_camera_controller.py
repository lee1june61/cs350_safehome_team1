"""
test_camera_controller.py
Unit tests for CameraController class
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from camera_controller import CameraController
from safe_home_camera import SafeHomeCamera


class TestCameraController:
    """Unit tests for CameraController class"""
    
    @pytest.fixture
    def camera_controller(self):
        """Fixture to create a CameraController instance"""
        return CameraController()
    
    @pytest.fixture
    def mock_camera(self):
        """Fixture to create a mock SafeHomeCamera"""
        camera = Mock(spec=SafeHomeCamera)
        camera.get_id = Mock(return_value=1)
        camera.get_location = Mock(return_value=[300, 400])
        camera.is_enabled = Mock(return_value=False)
        return camera
    
    # UT-CC-addCamera-Valid
    def test_add_camera_valid_location(self, camera_controller):
        """
        Test Case: addCamera()
        Description: Verifies camera is added at specified coordinates
        Reference: CRC Card for CameraController, Class Diagram page 16
        """
        # Arrange
        x_coord = 300
        y_coord = 400
        
        # Act
        camera_id = camera_controller.add_camera(x_coord, y_coord)
        
        # Assert
        assert camera_id is not None
        assert camera_id > 0
        assert len(camera_controller.camera_list) == 1
        
        added_camera = camera_controller.camera_list[0]
        assert added_camera.get_location() == [x_coord, y_coord]
    
    def test_add_camera_invalid_coordinates(self, camera_controller):
        """
        Test Case: addCamera() with out-of-bounds coordinates
        Description: Verifies rejection of invalid location
        """
        # Arrange
        x_coord = -50
        y_coord = 10000
        
        # Act
        camera_id = camera_controller.add_camera(x_coord, y_coord)
        
        # Assert
        assert camera_id is None
        assert len(camera_controller.camera_list) == 0
    
    def test_add_camera_multiple(self, camera_controller):
        """
        Test Case: addCamera() multiple cameras
        Description: Verifies multiple cameras can be added
        """
        # Arrange & Act
        id1 = camera_controller.add_camera(100, 100)
        id2 = camera_controller.add_camera(200, 200)
        id3 = camera_controller.add_camera(300, 300)
        
        # Assert
        assert len(camera_controller.camera_list) == 3
        assert id1 != id2 != id3
    
    # UT-CC-deleteCamera
    def test_delete_camera_existing(self, camera_controller, mock_camera):
        """
        Test Case: deleteCamera()
        Description: Verifies camera is properly removed
        Reference: CRC Card "Delete a camera that has specific id"
        """
        # Arrange
        camera_controller.camera_list = [mock_camera]
        camera_id = 1
        
        # Act
        result = camera_controller.delete_camera(camera_id)
        
        # Assert
        assert result is True
        assert len(camera_controller.camera_list) == 0
    
    def test_delete_camera_non_existing(self, camera_controller):
        """
        Test Case: deleteCamera() with invalid ID
        Description: Verifies handling of non-existent camera
        """
        # Arrange
        camera_id = 999
        
        # Act
        result = camera_controller.delete_camera(camera_id)
        
        # Assert
        assert result is False
    
    def test_delete_camera_from_multiple(self, camera_controller):
        """
        Test Case: deleteCamera() from multiple cameras
        Description: Verifies correct camera is removed
        """
        # Arrange
        cam1 = Mock(spec=SafeHomeCamera)
        cam1.get_id = Mock(return_value=1)
        cam2 = Mock(spec=SafeHomeCamera)
        cam2.get_id = Mock(return_value=2)
        cam3 = Mock(spec=SafeHomeCamera)
        cam3.get_id = Mock(return_value=3)
        
        camera_controller.camera_list = [cam1, cam2, cam3]
        
        # Act
        result = camera_controller.delete_camera(2)
        
        # Assert
        assert result is True
        assert len(camera_controller.camera_list) == 2
        assert cam2 not in camera_controller.camera_list
    
    # UT-CC-enableCameras
    def test_enable_cameras_valid_list(self, camera_controller):
        """
        Test Case: enableCameras()
        Description: Verifies multiple cameras enabled simultaneously
        Reference: CRC Card "Enable specific cameras to work"
        """
        # Arrange
        cam1 = Mock(spec=SafeHomeCamera)
        cam1.get_id = Mock(return_value=1)
        cam1.enable = Mock(return_value=True)
        
        cam2 = Mock(spec=SafeHomeCamera)
        cam2.get_id = Mock(return_value=2)
        cam2.enable = Mock(return_value=True)
        
        cam3 = Mock(spec=SafeHomeCamera)
        cam3.get_id = Mock(return_value=3)
        cam3.enable = Mock(return_value=True)
        
        camera_controller.camera_list = [cam1, cam2, cam3]
        camera_ids = [1, 3]
        
        # Act
        result = camera_controller.enable_cameras(camera_ids)
        
        # Assert
        assert result == [True, True]
        cam1.enable.assert_called_once()
        cam2.enable.assert_not_called()
        cam3.enable.assert_called_once()
    
    def test_enable_cameras_empty_list(self, camera_controller):
        """
        Test Case: enableCameras() with empty list
        Description: Verifies handling of empty camera list
        """
        # Arrange
        camera_ids = []
        
        # Act
        result = camera_controller.enable_cameras(camera_ids)
        
        # Assert
        assert result == []
    
    # UT-CC-disableCameras
    def test_disable_cameras_valid_list(self, camera_controller):
        """
        Test Case: disableCameras()
        Description: Verifies multiple cameras disabled together
        Reference: Sequence Diagram page 73 of SDS
        """
        # Arrange
        cam1 = Mock(spec=SafeHomeCamera)
        cam1.get_id = Mock(return_value=2)
        cam1.disable = Mock(return_value=True)
        cam1.is_enabled = Mock(return_value=True)
        
        cam2 = Mock(spec=SafeHomeCamera)
        cam2.get_id = Mock(return_value=4)
        cam2.disable = Mock(return_value=True)
        cam2.is_enabled = Mock(return_value=True)
        
        camera_controller.camera_list = [cam1, cam2]
        camera_ids = [2, 4]
        
        # Act
        result = camera_controller.disable_cameras(camera_ids)
        
        # Assert
        assert result == [True, True]
        cam1.disable.assert_called_once()
        cam2.disable.assert_called_once()
    
    # UT-CC-enableAllCamera
    def test_enable_all_camera(self, camera_controller):
        """
        Test Case: enableAllCamera()
        Description: Verifies all cameras enabled in single operation
        Reference: CRC Card "Enable all cameras to work"
        """
        # Arrange
        cameras = []
        for i in range(5):
            cam = Mock(spec=SafeHomeCamera)
            cam.get_id = Mock(return_value=i+1)
            cam.enable = Mock(return_value=True)
            cameras.append(cam)
        
        camera_controller.camera_list = cameras
        
        # Act
        count = camera_controller.enable_all_camera()
        
        # Assert
        assert count == 5
        for cam in cameras:
            cam.enable.assert_called_once()
    
    def test_enable_all_camera_empty(self, camera_controller):
        """
        Test Case: enableAllCamera() with no cameras
        Description: Verifies handling of empty camera list
        """
        # Arrange
        camera_controller.camera_list = []
        
        # Act
        count = camera_controller.enable_all_camera()
        
        # Assert
        assert count == 0
    
    # UT-CC-disableAllCamera
    def test_disable_all_camera(self, camera_controller):
        """
        Test Case: disableAllCamera()
        Description: Verifies all cameras disabled simultaneously
        Reference: CRC Card "Disable all cameras"
        """
        # Arrange
        cameras = []
        for i in range(3):
            cam = Mock(spec=SafeHomeCamera)
            cam.get_id = Mock(return_value=i+1)
            cam.disable = Mock(return_value=True)
            cam.is_enabled = Mock(return_value=True)
            cameras.append(cam)
        
        camera_controller.camera_list = cameras
        
        # Act
        count = camera_controller.disable_all_camera()
        
        # Assert
        assert count == 3
        for cam in cameras:
            cam.disable.assert_called_once()
    
    # UT-CC-enableCamera
    def test_enable_camera_single(self, camera_controller):
        """
        Test Case: enableCamera()
        Description: Verifies specific camera is enabled
        Reference: Sequence Diagram page 72 of SDS
        """
        # Arrange
        cam = Mock(spec=SafeHomeCamera)
        cam.get_id = Mock(return_value=2)
        cam.enable = Mock(return_value=True)
        
        camera_controller.camera_list = [cam]
        
        # Act
        result = camera_controller.enable_camera(2)
        
        # Assert
        assert result is True
        cam.enable.assert_called_once()
    
    def test_enable_camera_invalid_id(self, camera_controller):
        """
        Test Case: enableCamera() with invalid ID
        Description: Verifies handling of non-existent camera
        """
        # Arrange
        camera_controller.camera_list = []
        
        # Act
        result = camera_controller.enable_camera(999)
        
        # Assert
        assert result is False
    
    # UT-CC-disableCamera
    def test_disable_camera_single(self, camera_controller):
        """
        Test Case: disableCamera()
        Description: Verifies specific camera is disabled
        Reference: CRC Card "Disable a specific camera"
        """
        # Arrange
        cam = Mock(spec=SafeHomeCamera)
        cam.get_id = Mock(return_value=5)
        cam.disable = Mock(return_value=True)
        cam.is_enabled = Mock(return_value=True)
        
        camera_controller.camera_list = [cam]
        
        # Act
        result = camera_controller.disable_camera(5)
        
        # Assert
        assert result is True
        cam.disable.assert_called_once()
    
    # UT-CC-controlSingleCamera
    def test_control_single_camera_zoom_in(self, camera_controller):
        """
        Test Case: controlSingleCamera()
        Description: Verifies camera zoom control
        Reference: Sequence Diagram page 67 of SDS
        """
        # Arrange
        cam = Mock(spec=SafeHomeCamera)
        cam.get_id = Mock(return_value=3)
        cam.is_enabled = Mock(return_value=True)
        cam.zoom_in = Mock(return_value=True)
        
        camera_controller.camera_list = [cam]
        control_id = 1  # ZOOM_IN
        
        # Act
        result = camera_controller.control_single_camera(3, control_id)
        
        # Assert
        assert result is True
        cam.zoom_in.assert_called_once()
    
    def test_control_single_camera_pan_left(self, camera_controller):
        """
        Test Case: controlSingleCamera() pan left
        Description: Verifies camera pan control
        """
        # Arrange
        cam = Mock(spec=SafeHomeCamera)
        cam.get_id = Mock(return_value=3)
        cam.is_enabled = Mock(return_value=True)
        cam.pan_left = Mock(return_value=True)
        
        camera_controller.camera_list = [cam]
        control_id = 3  # PAN_LEFT
        
        # Act
        result = camera_controller.control_single_camera(3, control_id)
        
        # Assert
        assert result is True
        cam.pan_left.assert_called_once()
    
    def test_control_single_camera_disabled(self, camera_controller):
        """
        Test Case: controlSingleCamera() on disabled camera
        Description: Verifies control rejected for disabled camera
        """
        # Arrange
        cam = Mock(spec=SafeHomeCamera)
        cam.get_id = Mock(return_value=3)
        cam.is_enabled = Mock(return_value=False)
        
        camera_controller.camera_list = [cam]
        
        # Act
        result = camera_controller.control_single_camera(3, 1)
        
        # Assert
        assert result is False
    
    # UT-CC-displayThumbnailView
    def test_display_thumbnail_view(self, camera_controller):
        """
        Test Case: displayThumbnailView()
        Description: Verifies thumbnail view generation
        Reference: Sequence Diagram page 71 of SDS
        """
        # Arrange
        cameras = []
        for i in range(4):
            cam = Mock(spec=SafeHomeCamera)
            cam.get_id = Mock(return_value=i+1)
            cam.is_enabled = Mock(return_value=True)
            cam.display_view = Mock(return_value=f"frame_{i}")
            cameras.append(cam)
        
        camera_controller.camera_list = cameras
        
        # Act
        thumbnail_view = camera_controller.display_thumbnail_view()
        
        # Assert
        assert thumbnail_view is not None
        assert len(thumbnail_view) == 4
        for cam in cameras:
            cam.display_view.assert_called_once()
    
    def test_display_thumbnail_view_mixed_status(self, camera_controller):
        """
        Test Case: displayThumbnailView() with some disabled cameras
        Description: Verifies only enabled cameras appear in thumbnail
        """
        # Arrange
        cam1 = Mock(spec=SafeHomeCamera)
        cam1.get_id = Mock(return_value=1)
        cam1.is_enabled = Mock(return_value=True)
        cam1.display_view = Mock(return_value="frame_1")
        
        cam2 = Mock(spec=SafeHomeCamera)
        cam2.get_id = Mock(return_value=2)
        cam2.is_enabled = Mock(return_value=False)
        
        cam3 = Mock(spec=SafeHomeCamera)
        cam3.get_id = Mock(return_value=3)
        cam3.is_enabled = Mock(return_value=True)
        cam3.display_view = Mock(return_value="frame_3")
        
        camera_controller.camera_list = [cam1, cam2, cam3]
        
        # Act
        thumbnail_view = camera_controller.display_thumbnail_view()
        
        # Assert
        assert len(thumbnail_view) == 2
        cam1.display_view.assert_called_once()
        cam2.display_view.assert_not_called()
        cam3.display_view.assert_called_once()
    
    # UT-CC-displaySingleView
    def test_display_single_view(self, camera_controller):
        """
        Test Case: displaySingleView()
        Description: Verifies single camera full-screen view
        Reference: Sequence Diagram page 66 of SDS
        """
        # Arrange
        cam = Mock(spec=SafeHomeCamera)
        cam.get_id = Mock(return_value=2)
        cam.is_enabled = Mock(return_value=True)
        cam.display_view = Mock(return_value="full_frame_2")
        
        camera_controller.camera_list = [cam]
        
        # Act
        single_view = camera_controller.display_single_view(2)
        
        # Assert
        assert single_view == "full_frame_2"
        cam.display_view.assert_called_once()
    
    def test_display_single_view_disabled(self, camera_controller):
        """
        Test Case: displaySingleView() on disabled camera
        Description: Verifies view denied for disabled camera
        """
        # Arrange
        cam = Mock(spec=SafeHomeCamera)
        cam.get_id = Mock(return_value=2)
        cam.is_enabled = Mock(return_value=False)
        
        camera_controller.camera_list = [cam]
        
        # Act
        single_view = camera_controller.display_single_view(2)
        
        # Assert
        assert single_view is None
    
    # UT-CC-getAllCameraInfo
    def test_get_all_camera_info(self, camera_controller):
        """
        Test Case: getAllCameraInfo()
        Description: Verifies complete camera information retrieval
        Reference: CRC Card for CameraController
        """
        # Arrange
        cam1 = Mock(spec=SafeHomeCamera)
        cam1.get_id = Mock(return_value=1)
        cam1.get_location = Mock(return_value=[100, 150])
        cam1.is_enabled = Mock(return_value=True)
        cam1.get_pan_angle = Mock(return_value=15)
        cam1.get_zoom_level = Mock(return_value=2.0)
        
        cam2 = Mock(spec=SafeHomeCamera)
        cam2.get_id = Mock(return_value=2)
        cam2.get_location = Mock(return_value=[200, 250])
        cam2.is_enabled = Mock(return_value=False)
        cam2.get_pan_angle = Mock(return_value=0)
        cam2.get_zoom_level = Mock(return_value=1.0)
        
        camera_controller.camera_list = [cam1, cam2]
        
        # Act
        info = camera_controller.get_all_camera_info()
        
        # Assert
        assert len(info) == 2
        assert info[0]['id'] == 1
        assert info[0]['location'] == [100, 150]
        assert info[0]['enabled'] is True
        assert info[0]['pan'] == 15
        assert info[0]['zoom'] == 2.0
        assert info[1]['enabled'] is False
    
    def test_get_all_camera_info_empty(self, camera_controller):
        """
        Test Case: getAllCameraInfo() with no cameras
        Description: Verifies handling of empty camera list
        """
        # Arrange
        camera_controller.camera_list = []
        
        # Act
        info = camera_controller.get_all_camera_info()
        
        # Assert
        assert info == []
    
    # UT-CC-setCameraPassword
    def test_set_camera_password(self, camera_controller):
        """
        Test Case: setCameraPassword()
        Description: Verifies password protection is set
        Reference: Sequence Diagram page 68 of SDS
        """
        # Arrange
        cam = Mock(spec=SafeHomeCamera)
        cam.get_id = Mock(return_value=4)
        cam.has_password = Mock(return_value=False)
        cam.set_password = Mock(return_value=True)
        
        camera_controller.camera_list = [cam]
        password = "pass123"
        
        # Act
        result = camera_controller.set_camera_password(4, password)
        
        # Assert
        assert result is True
        cam.set_password.assert_called_once_with(password)
    
    def test_set_camera_password_existing(self, camera_controller):
        """
        Test Case: setCameraPassword() overwriting existing password
        Description: Verifies password can be changed
        """
        # Arrange
        cam = Mock(spec=SafeHomeCamera)
        cam.get_id = Mock(return_value=4)
        cam.has_password = Mock(return_value=True)
        cam.set_password = Mock(return_value=True)
        
        camera_controller.camera_list = [cam]
        new_password = "newpass456"
        
        # Act
        result = camera_controller.set_camera_password(4, new_password)
        
        # Assert
        assert result is True
        cam.set_password.assert_called_once_with(new_password)
    
    # UT-CC-validateCameraPassword
    def test_validate_camera_password_correct(self, camera_controller):
        """
        Test Case: validateCameraPassword()
        Description: Verifies correct password validation
        Reference: CRC Card for CameraController
        """
        # Arrange
        cam = Mock(spec=SafeHomeCamera)
        cam.get_id = Mock(return_value=4)
        cam.has_password = Mock(return_value=True)
        cam.get_password = Mock(return_value="pass123")
        
        camera_controller.camera_list = [cam]
        
        # Act
        result = camera_controller.validate_camera_password(4, "pass123")
        
        # Assert
        assert result is True
    
    def test_validate_camera_password_incorrect(self, camera_controller):
        """
        Test Case: validateCameraPassword() with wrong password
        Description: Verifies incorrect password rejection
        """
        # Arrange
        cam = Mock(spec=SafeHomeCamera)
        cam.get_id = Mock(return_value=4)
        cam.has_password = Mock(return_value=True)
        cam.get_password = Mock(return_value="pass123")
        
        camera_controller.camera_list = [cam]
        
        # Act
        result = camera_controller.validate_camera_password(4, "wrongpass")
        
        # Assert
        assert result is False
    
    def test_validate_camera_password_no_password(self, camera_controller):
        """
        Test Case: validateCameraPassword() on unprotected camera
        Description: Verifies camera without password allows access
        """
        # Arrange
        cam = Mock(spec=SafeHomeCamera)
        cam.get_id = Mock(return_value=4)
        cam.has_password = Mock(return_value=False)
        
        camera_controller.camera_list = [cam]
        
        # Act
        result = camera_controller.validate_camera_password(4, "anypass")
        
        # Assert
        assert result is True  # No password = always valid
    
    # UT-CC-deleteCameraPassword
    def test_delete_camera_password(self, camera_controller):
        """
        Test Case: deleteCameraPassword()
        Description: Verifies password protection is removed
        Reference: Sequence Diagram page 69-70 of SDS
        """
        # Arrange
        cam = Mock(spec=SafeHomeCamera)
        cam.get_id = Mock(return_value=2)
        cam.has_password = Mock(return_value=True)
        cam.delete_password = Mock(return_value=True)
        
        camera_controller.camera_list = [cam]
        
        # Act
        result = camera_controller.delete_camera_password(2)
        
        # Assert
        assert result is True
        cam.delete_password.assert_called_once()
    
    def test_delete_camera_password_no_password(self, camera_controller):
        """
        Test Case: deleteCameraPassword() on unprotected camera
        Description: Verifies handling of camera without password
        """
        # Arrange
        cam = Mock(spec=SafeHomeCamera)
        cam.get_id = Mock(return_value=2)
        cam.has_password = Mock(return_value=False)
        
        camera_controller.camera_list = [cam]
        
        # Act
        result = camera_controller.delete_camera_password(2)
        
        # Assert
        assert result is False  # Nothing to delete


if __name__ == '__main__':
    pytest.main([__file__, '-v'])