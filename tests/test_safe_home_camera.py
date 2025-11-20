"""
test_safe_home_camera.py
Unit tests for SafeHomeCamera class
"""

import pytest
from unittest.mock import Mock, patch
from safe_home_camera import SafeHomeCamera


class TestSafeHomeCamera:
    """Unit tests for SafeHomeCamera class"""
    
    @pytest.fixture
    def camera(self):
        """Fixture to create a SafeHomeCamera instance"""
        cam = SafeHomeCamera()
        cam.id = 1
        cam.location = [200, 250]
        cam.pan_angle = 0
        cam.zoom_level = 1.0
        cam.password = None
        cam.enabled = False
        return cam
    
    # UT-CAM-getLocation
    def test_get_location(self, camera):
        """
        Test Case: getLocation()
        Description: Verifies camera location is retrieved correctly
        Reference: State Diagram page 38 of SDS
        """
        # Arrange
        camera.location = [200, 250]
        
        # Act
        result = camera.get_location()
        
        # Assert
        assert result == [200, 250]
        assert isinstance(result, list)
    
    def test_get_location_after_move(self, camera):
        """
        Test Case: getLocation() after repositioning
        Description: Verifies location updates are reflected
        """
        # Arrange
        camera.location = [100, 150]
        camera.set_location([300, 350])
        
        # Act
        result = camera.get_location()
        
        # Assert
        assert result == [300, 350]
    
    # UT-CAM-setLocation
    def test_set_location_valid(self, camera):
        """
        Test Case: setLocation()
        Description: Verifies camera location is properly set
        Reference: CRC Card "Manage camera state information"
        """
        # Arrange
        new_location = [180, 220]
        
        # Act
        camera.set_location(new_location)
        
        # Assert
        assert camera.location == new_location
    
    def test_set_location_invalid_coordinates(self, camera):
        """
        Test Case: setLocation() with invalid coordinates
        Description: Verifies rejection of out-of-bounds location
        """
        # Arrange
        invalid_location = [-10, 5000]
        
        # Act & Assert
        with pytest.raises(ValueError, match="Location out of bounds"):
            camera.set_location(invalid_location)
    
    def test_set_location_updates_floor_plan(self, camera):
        """
        Test Case: setLocation() updates floor plan display
        Description: Verifies location change triggers UI update
        """
        # Arrange
        new_location = [250, 300]
        with patch.object(camera, '_update_floor_plan_position') as mock_update:
            # Act
            camera.set_location(new_location)
            
            # Assert
            mock_update.assert_called_once_with(new_location)
    
    # UT-CAM-getID
    def test_get_id(self, camera):
        """
        Test Case: getID()
        Description: Verifies camera ID is retrieved correctly
        Reference: State Diagram for SafeHomeCamera
        """
        # Arrange
        camera.id = 7
        
        # Act
        result = camera.get_id()
        
        # Assert
        assert result == 7
    
    # UT-CAM-setID
    def test_set_id_valid(self, camera):
        """
        Test Case: setID()
        Description: Verifies camera ID is assigned properly
        Reference: CRC Card for SafeHomeCamera
        """
        # Arrange
        camera_id = 5
        
        # Act
        camera.set_id(camera_id)
        
        # Assert
        assert camera.id == camera_id
    
    def test_set_id_negative(self, camera):
        """
        Test Case: setID() with negative value
        Description: Verifies rejection of invalid ID
        """
        # Arrange
        camera_id = -3
        
        # Act & Assert
        with pytest.raises(ValueError, match="Camera ID must be positive"):
            camera.set_id(camera_id)
    
    # UT-CAM-displayView
    def test_display_view_enabled(self, camera):
        """
        Test Case: displayView()
        Description: Verifies camera view is displayed correctly
        Reference: Sequence Diagram page 66 of SDS
        """
        # Arrange
        camera.enabled = True
        mock_frame = Mock()
        
        with patch.object(camera, '_get_current_frame', return_value=mock_frame):
            # Act
            result = camera.display_view()
            
            # Assert
            assert result == mock_frame
    
    def test_display_view_disabled(self, camera):
        """
        Test Case: displayView() when disabled
        Description: Verifies disabled camera returns no view
        """
        # Arrange
        camera.enabled = False
        
        # Act
        result = camera.display_view()
        
        # Assert
        assert result is None
    
    def test_display_view_with_overlay(self, camera):
        """
        Test Case: displayView() with status overlay
        Description: Verifies view includes camera status information
        """
        # Arrange
        camera.enabled = True
        with patch.object(camera, '_add_status_overlay', return_value=True) as mock_overlay:
            # Act
            result = camera.display_view()
            
            # Assert
            assert result is not None
            mock_overlay.assert_called_once()
    
    # UT-CAM-zoomIn
    def test_zoom_in_success(self, camera):
        """
        Test Case: zoomIn()
        Description: Verifies camera zoom increases correctly
        Reference: Sequence Diagram page 67 of SDS
        """
        # Arrange
        camera.zoom_level = 1.0
        camera.max_zoom = 10.0
        
        # Act
        new_zoom = camera.zoom_in()
        
        # Assert
        assert new_zoom > 1.0
        assert camera.zoom_level > 1.0
    
    def test_zoom_in_at_max(self, camera):
        """
        Test Case: zoomIn() at maximum zoom
        Description: Verifies zoom limit enforcement
        """
        # Arrange
        camera.zoom_level = 10.0
        camera.max_zoom = 10.0
        
        # Act
        new_zoom = camera.zoom_in()
        
        # Assert
        assert new_zoom == 10.0
        assert camera.zoom_level == 10.0
    
    def test_zoom_in_incremental(self, camera):
        """
        Test Case: zoomIn() multiple times
        Description: Verifies incremental zoom increase
        """
        # Arrange
        camera.zoom_level = 1.0
        camera.zoom_increment = 0.5
        
        # Act
        camera.zoom_in()
        camera.zoom_in()
        
        # Assert
        assert camera.zoom_level == 2.0
    
    # UT-CAM-zoomOut
    def test_zoom_out_success(self, camera):
        """
        Test Case: zoomOut()
        Description: Verifies camera zoom decreases correctly
        Reference: CRC Card "Zoom out"
        """
        # Arrange
        camera.zoom_level = 2.0
        camera.min_zoom = 1.0
        
        # Act
        new_zoom = camera.zoom_out()
        
        # Assert
        assert new_zoom < 2.0
        assert camera.zoom_level < 2.0
    
    def test_zoom_out_at_min(self, camera):
        """
        Test Case: zoomOut() at minimum zoom
        Description: Verifies minimum zoom limit enforcement
        """
        # Arrange
        camera.zoom_level = 1.0
        camera.min_zoom = 1.0
        
        # Act
        new_zoom = camera.zoom_out()
        
        # Assert
        assert new_zoom == 1.0
        assert camera.zoom_level == 1.0
    
    # UT-CAM-panLeft
    def test_pan_left_success(self, camera):
        """
        Test Case: panLeft()
        Description: Verifies camera pans left correctly
        Reference: Sequence Diagram page 67 of SDS
        """
        # Arrange
        camera.pan_angle = 0
        camera.min_pan = -90
        
        # Act
        new_angle = camera.pan_left()
        
        # Assert
        assert new_angle < 0
        assert camera.pan_angle < 0
    
    def test_pan_left_at_limit(self, camera):
        """
        Test Case: panLeft() at left limit
        Description: Verifies left pan limit enforcement
        """
        # Arrange
        camera.pan_angle = -90
        camera.min_pan = -90
        
        # Act
        new_angle = camera.pan_left()
        
        # Assert
        assert new_angle == -90
        assert camera.pan_angle == -90
    
    def test_pan_left_incremental(self, camera):
        """
        Test Case: panLeft() multiple times
        Description: Verifies incremental pan movement
        """
        # Arrange
        camera.pan_angle = 0
        camera.pan_increment = 15
        
        # Act
        camera.pan_left()
        camera.pan_left()
        
        # Assert
        assert camera.pan_angle == -30
    
    # UT-CAM-panRight
    def test_pan_right_success(self, camera):
        """
        Test Case: panRight()
        Description: Verifies camera pans right correctly
        Reference: CRC Card "Pan right"
        """
        # Arrange
        camera.pan_angle = 0
        camera.max_pan = 90
        
        # Act
        new_angle = camera.pan_right()
        
        # Assert
        assert new_angle > 0
        assert camera.pan_angle > 0
    
    def test_pan_right_at_limit(self, camera):
        """
        Test Case: panRight() at right limit
        Description: Verifies right pan limit enforcement
        """
        # Arrange
        camera.pan_angle = 90
        camera.max_pan = 90
        
        # Act
        new_angle = camera.pan_right()
        
        # Assert
        assert new_angle == 90
        assert camera.pan_angle == 90
    
    # UT-CAM-getPassword
    def test_get_password(self, camera):
        """
        Test Case: getPassword()
        Description: Verifies camera password is retrieved correctly
        Reference: Sequence Diagram page 68 of SDS
        """
        # Arrange
        camera.password = "camera1"
        
        # Act
        result = camera.get_password()
        
        # Assert
        assert result == "camera1"
    
    def test_get_password_none(self, camera):
        """
        Test Case: getPassword() when no password set
        Description: Verifies handling of unprotected camera
        """
        # Arrange
        camera.password = None
        
        # Act
        result = camera.get_password()
        
        # Assert
        assert result is None
    
    # UT-CAM-setPassword
    def test_set_password_valid(self, camera):
        """
        Test Case: setPassword()
        Description: Verifies camera password is set properly
        Reference: CRC Card "Get/Set password"
        """
        # Arrange
        password = "secure123"
        
        # Act
        result = camera.set_password(password)
        
        # Assert
        assert result is True
        assert camera.password == password
    
    def test_set_password_empty(self, camera):
        """
        Test Case: setPassword() with empty string
        Description: Verifies rejection of empty password
        """
        # Arrange
        password = ""
        
        # Act & Assert
        with pytest.raises(ValueError, match="Password cannot be empty"):
            camera.set_password(password)
    
    def test_set_password_overwrite(self, camera):
        """
        Test Case: setPassword() overwriting existing password
        Description: Verifies password can be changed
        """
        # Arrange
        camera.password = "oldpass"
        new_password = "newpass123"
        
        # Act
        result = camera.set_password(new_password)
        
        # Assert
        assert result is True
        assert camera.password == new_password
    
    # UT-CAM-isEnabled
    def test_is_enabled_true(self, camera):
        """
        Test Case: isEnabled()
        Description: Verifies enabled status is reported correctly
        Reference: State Diagram for SafeHomeCamera showing ENABLED state
        """
        # Arrange
        camera.enabled = True
        
        # Act
        result = camera.is_enabled()
        
        # Assert
        assert result is True
    
    def test_is_enabled_false(self, camera):
        """
        Test Case: isEnabled() when disabled
        Description: Verifies disabled status is reported
        """
        # Arrange
        camera.enabled = False
        
        # Act
        result = camera.is_enabled()
        
        # Assert
        assert result is False
    
    # UT-CAM-enable
    def test_enable_success(self, camera):
        """
        Test Case: enable()
        Description: Verifies camera is enabled and begins streaming
        Reference: Sequence Diagram page 72 of SDS
        """
        # Arrange
        camera.enabled = False
        
        with patch.object(camera, '_start_streaming') as mock_stream:
            # Act
            result = camera.enable()
            
            # Assert
            assert result is True
            assert camera.enabled is True
            mock_stream.assert_called_once()
    
    def test_enable_already_enabled(self, camera):
        """
        Test Case: enable() when already enabled
        Description: Verifies handling of already enabled camera
        """
        # Arrange
        camera.enabled = True
        
        # Act
        result = camera.enable()
        
        # Assert
        assert result is True
        assert camera.enabled is True
    
    # UT-CAM-disable
    def test_disable_success(self, camera):
        """
        Test Case: disable()
        Description: Verifies camera is disabled and stops streaming
        Reference: Sequence Diagram page 73 of SDS
        """
        # Arrange
        camera.enabled = True
        
        with patch.object(camera, '_stop_streaming') as mock_stream:
            # Act
            result = camera.disable()
            
            # Assert
            assert result is True
            assert camera.enabled is False
            mock_stream.assert_called_once()
    
    def test_disable_already_disabled(self, camera):
        """
        Test Case: disable() when already disabled
        Description: Verifies handling of already disabled camera
        """
        # Arrange
        camera.enabled = False
        
        # Act
        result = camera.disable()
        
        # Assert
        assert result is True
        assert camera.enabled is False
    
    # UT-CAM-hasPassword
    def test_has_password_true(self, camera):
        """
        Test Case: hasPassword()
        Description: Verifies password existence check
        Reference: Sequence Diagram page 69 of SDS
        """
        # Arrange
        camera.password = "secure123"
        
        # Act
        result = camera.has_password()
        
        # Assert
        assert result is True
    
    def test_has_password_false(self, camera):
        """
        Test Case: hasPassword() when no password set
        Description: Verifies detection of unprotected camera
        """
        # Arrange
        camera.password = None
        
        # Act
        result = camera.has_password()
        
        # Assert
        assert result is False
    
    # UT-CAM-saveInfo
    def test_save_info_success(self, camera):
        """
        Test Case: saveInfo()
        Description: Verifies camera configuration is persisted
        Reference: StorageManager integration
        """
        # Arrange
        camera.id = 5
        camera.location = [300, 400]
        camera.password = "pass123"
        camera.zoom_level = 2.0
        camera.pan_angle = 15
        
        with patch.object(camera, '_save_to_storage', return_value=True) as mock_save:
            # Act
            result = camera.save_info()
            
            # Assert
            assert result is True
            mock_save.assert_called_once()
    
    def test_save_info_no_changes(self, camera):
        """
        Test Case: saveInfo() with no changes
        Description: Verifies optimization when no changes exist
        """
        # Arrange
        camera._last_saved_state = camera._get_current_state()
        
        with patch.object(camera, '_save_to_storage') as mock_save:
            # Act
            result = camera.save_info()
            
            # Assert
            assert result is True
            mock_save.assert_not_called()  # No save needed
    
    def test_save_info_storage_failure(self, camera):
        """
        Test Case: saveInfo() with storage failure
        Description: Verifies error handling for save failures
        """
        # Arrange
        with patch.object(camera, '_save_to_storage', return_value=False):
            # Act
            result = camera.save_info()
            
            # Assert
            assert result is False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])