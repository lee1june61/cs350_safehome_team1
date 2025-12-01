"""
Integration Tests: Surveillance Functions (IT-018 ~ IT-024)
Based on SafeHome_Integration_Test_Cases.md

Tests:
- IT-018: Display Specific camera view
- IT-019: Pan/Zoom specific camera view
- IT-020: Set camera password
- IT-021: Delete camera password
- IT-022: View thumbnail Shots
- IT-023: Enable camera
- IT-024: Disable camera
"""
import pytest


class TestIT018DisplayCameraView:
    """IT-018: Display Specific camera view."""

    def test_get_camera_list(self, system_web_logged_in):
        """Normal: Get list of available cameras."""
        result = system_web_logged_in.handle_request("web", "get_cameras")
        assert result["success"] is True
        assert "data" in result
        assert len(result["data"]) >= 1

    def test_get_camera_view(self, system_web_logged_in):
        """Normal: Get specific camera view."""
        cameras = system_web_logged_in.handle_request("web", "get_cameras")
        if cameras.get("data"):
            cam_id = cameras["data"][0]["id"]
            result = system_web_logged_in.handle_request(
                "web", "get_camera_view", camera_id=cam_id
            )
            assert result["success"] is True

    def test_password_protected_camera(self, system_web_logged_in):
        """Exception 8a: Password required for protected camera."""
        cameras = system_web_logged_in.handle_request("web", "get_cameras")
        if cameras.get("data"):
            cam_id = cameras["data"][0]["id"]
            # Set password first
            system_web_logged_in.handle_request(
                "web", "set_camera_password",
                camera_id=cam_id, password="cam123"
            )
            # Try to access without password
            result = system_web_logged_in.handle_request(
                "web", "verify_camera_password",
                camera_id=cam_id, password="wrong"
            )
            assert result["success"] is False


class TestIT019PanZoomCamera:
    """IT-019: Pan/Zoom specific camera view."""

    def test_pan_camera_left(self, system_web_logged_in):
        """Normal: Pan camera left."""
        result = system_web_logged_in.handle_request(
            "web", "pan_camera", camera_id="C1", direction="left"
        )
        assert result["success"] is True

    def test_pan_camera_right(self, system_web_logged_in):
        """Normal: Pan camera right."""
        result = system_web_logged_in.handle_request(
            "web", "pan_camera", camera_id="C1", direction="right"
        )
        assert result["success"] is True

    def test_zoom_camera_in(self, system_web_logged_in):
        """Normal: Zoom camera in."""
        result = system_web_logged_in.handle_request(
            "web", "zoom_camera", camera_id="C1", direction="in"
        )
        assert result["success"] is True

    def test_zoom_camera_out(self, system_web_logged_in):
        """Normal: Zoom camera out."""
        result = system_web_logged_in.handle_request(
            "web", "zoom_camera", camera_id="C1", direction="out"
        )
        assert result["success"] is True


class TestIT020SetCameraPassword:
    """IT-020: Set camera password."""

    def test_set_new_camera_password(self, system_web_logged_in):
        """Normal: Set password on camera without password."""
        result = system_web_logged_in.handle_request(
            "web", "set_camera_password",
            camera_id="C2", password="newpass123"
        )
        assert result["success"] is True

    def test_verify_camera_password(self, system_web_logged_in):
        """Normal: Verify correct camera password."""
        # Set password first
        system_web_logged_in.handle_request(
            "web", "set_camera_password",
            camera_id="C2", password="test123"
        )
        # Verify
        result = system_web_logged_in.handle_request(
            "web", "verify_camera_password",
            camera_id="C2", password="test123"
        )
        assert result["success"] is True

    def test_wrong_camera_password(self, system_web_logged_in):
        """Exception 8a: Wrong password rejected."""
        system_web_logged_in.handle_request(
            "web", "set_camera_password",
            camera_id="C2", password="correct"
        )
        result = system_web_logged_in.handle_request(
            "web", "verify_camera_password",
            camera_id="C2", password="wrong"
        )
        assert result["success"] is False


class TestIT021DeleteCameraPassword:
    """IT-021: Delete camera password."""

    def test_delete_camera_password(self, system_web_logged_in):
        """Normal: Delete camera password with correct old password."""
        cam_id = "C3"
        # Set password first
        system_web_logged_in.handle_request(
            "web", "set_camera_password",
            camera_id=cam_id, password="toDelete"
        )
        # Delete with correct password
        result = system_web_logged_in.handle_request(
            "web", "delete_camera_password",
            camera_id=cam_id, old_password="toDelete"
        )
        assert result["success"] is True


class TestIT022ViewThumbnailShots:
    """IT-022: View thumbnail Shots."""

    def test_get_all_cameras_thumbnails(self, system_web_logged_in):
        """Normal: Get thumbnail from all cameras."""
        result = system_web_logged_in.handle_request("web", "get_cameras")
        assert result["success"] is True
        # All unprotected cameras should be returned
        assert len(result["data"]) >= 1


class TestIT023EnableCamera:
    """IT-023: Enable camera."""

    def test_enable_disabled_camera(self, system_web_logged_in):
        """Normal: Enable a disabled camera."""
        cam_id = "C1"
        # Disable first
        system_web_logged_in.handle_request(
            "web", "disable_camera", camera_id=cam_id
        )
        # Enable
        result = system_web_logged_in.handle_request(
            "web", "enable_camera", camera_id=cam_id
        )
        assert result["success"] is True


class TestIT024DisableCamera:
    """IT-024: Disable camera."""

    def test_disable_enabled_camera(self, system_web_logged_in):
        """Normal: Disable an enabled camera."""
        result = system_web_logged_in.handle_request(
            "web", "disable_camera", camera_id="C1"
        )
        assert result["success"] is True

    def test_disabled_camera_view_blocked(self, system_web_logged_in):
        """Exception 10a: Disabled camera view blocked."""
        cam_id = "C1"
        system_web_logged_in.handle_request(
            "web", "disable_camera", camera_id=cam_id
        )
        result = system_web_logged_in.handle_request(
            "web", "get_camera_view", camera_id=cam_id
        )
        # Should indicate camera is disabled
        assert result.get("success") is False or "disabled" in str(result).lower()





