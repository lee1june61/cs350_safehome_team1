"""
Unit tests for DeviceCamera following SDS responsibilities.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import Mock

import pytest  # type: ignore[import]

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "safehome" / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from safehome.src.controllers.camera_controller import CameraController
from safehome.src.devices.cameras.device_camera import DeviceCamera
from safehome.src.devices.cameras.safehome_camera import SafeHomeCamera
from safehome.src.utils.exceptions import CameraDisabledError, CameraValidationError


@pytest.fixture
def device_camera() -> DeviceCamera:
    """Create a DeviceCamera located at 'Front Door' with ID 7."""
    return DeviceCamera("Front Door", 7)


def test_initial_state_matches_sds_defaults(device_camera: DeviceCamera) -> None:
    assert device_camera.get_location() == "Front Door"
    assert device_camera.get_camera_id() == 7
    assert device_camera.is_enabled() is True
    assert device_camera.get_pan() == 0
    assert device_camera.get_tilt() == 0
    assert device_camera.get_zoom() == 0


def test_set_pan_respects_bounds_and_state(device_camera: DeviceCamera) -> None:
    assert device_camera.set_pan(45) is True
    assert device_camera.get_pan() == 45
    assert device_camera.set_pan(200) is False  # out of bounds
    device_camera.disable()
    assert device_camera.set_pan(0) is False  # disabled cameras ignore PTZ


def test_pan_boundaries_and_reenable(device_camera: DeviceCamera) -> None:
    assert device_camera.set_pan(DeviceCamera.PAN_MIN) is True
    assert device_camera.set_pan(DeviceCamera.PAN_MAX) is True
    device_camera.disable()
    assert device_camera.set_pan(10) is False
    device_camera.enable()
    assert device_camera.set_pan(0) is True


def test_set_tilt_and_zoom(device_camera: DeviceCamera) -> None:
    assert device_camera.set_tilt(-30) is True
    assert device_camera.get_tilt() == -30
    assert device_camera.set_tilt(-120) is False

    assert device_camera.set_zoom(25) is True
    assert device_camera.get_zoom() == 25
    assert device_camera.set_zoom(150) is False


def test_tilt_zoom_boundaries_and_disabled(device_camera: DeviceCamera) -> None:
    assert device_camera.set_tilt(DeviceCamera.TILT_MIN) is True
    assert device_camera.set_tilt(DeviceCamera.TILT_MAX) is True
    assert device_camera.set_zoom(DeviceCamera.ZOOM_MIN) is True
    assert device_camera.set_zoom(DeviceCamera.ZOOM_MAX) is True
    device_camera.disable()
    assert device_camera.set_tilt(0) is False
    assert device_camera.set_zoom(10) is False


def test_capture_frame_reflects_state(device_camera: DeviceCamera) -> None:
    device_camera.disable()
    assert device_camera.capture_frame() is None

    device_camera.enable()
    device_camera.set_pan(10)
    device_camera.set_tilt(5)
    device_camera.set_zoom(3)
    frame = device_camera.capture_frame()
    assert isinstance(frame, bytes)
    decoded = frame.decode("utf-8")
    assert "CAMERA_FRAME|" in decoded
    assert "ID=7" in decoded
    assert "LOC=Front Door" in decoded
    assert "PAN=10" in decoded
    assert "TILT=5" in decoded
    assert "ZOOM=3" in decoded


def test_enable_disable_flow(device_camera: DeviceCamera) -> None:
    device_camera.disable()
    assert device_camera.is_enabled() is False
    device_camera.enable()
    assert device_camera.is_enabled() is True


def test_password_management(device_camera: DeviceCamera) -> None:
    # No password means open access
    assert device_camera.verify_password("anything") is True

    device_camera.set_password("secure123")
    assert device_camera.verify_password("secure123") is True
    assert device_camera.verify_password("wrong") is False

    device_camera.clear_password()
    assert device_camera.verify_password("irrelevant") is True


def test_getters_after_state_changes(device_camera: DeviceCamera) -> None:
    device_camera.set_pan(15)
    device_camera.set_tilt(-5)
    device_camera.set_zoom(30)
    assert device_camera.get_pan() == 15
    assert device_camera.get_tilt() == -5
    assert device_camera.get_zoom() == 30
    assert device_camera.get_camera_id() == 7
    assert device_camera.get_location() == "Front Door"


def test_enable_disable_idempotent(device_camera: DeviceCamera) -> None:
    device_camera.enable()
    assert device_camera.is_enabled() is True
    device_camera.enable()
    assert device_camera.is_enabled() is True
    device_camera.disable()
    assert device_camera.is_enabled() is False
    device_camera.disable()
    assert device_camera.is_enabled() is False


@pytest.fixture
def controller_with_mock() -> tuple[CameraController, Mock]:
    controller = CameraController()
    mock_cam = Mock(spec=SafeHomeCamera)
    mock_cam.get_id.return_value = 1
    mock_cam.enable.return_value = True
    mock_cam.disable.return_value = True
    mock_cam.is_enabled.return_value = True
    mock_cam.get_location.return_value = [100, 200]
    mock_cam.get_pan_angle.return_value = 0
    mock_cam.get_zoom_level.return_value = 2
    mock_cam.has_password.return_value = True
    mock_cam.get_password.return_value = "pw"
    mock_cam.display_view.return_value = "frame"
    mock_cam.pan_left.return_value = True
    mock_cam.pan_right.return_value = True
    mock_cam.zoom_in.return_value = True
    mock_cam.zoom_out.return_value = True
    controller.camera_list = [mock_cam]
    return controller, mock_cam


def test_controller_enable_disable_from_device_suite(controller_with_mock) -> None:
    controller, mock_cam = controller_with_mock
    assert controller.enable_cameras([1]) == [True]
    assert controller.disable_cameras([1]) == [True]
    assert controller.enable_camera(1) is True
    assert controller.disable_camera(1) is True
    assert controller.enable_all_camera() == 1
    assert controller.disable_all_camera() == 1
    mock_cam.enable.assert_called()
    mock_cam.disable.assert_called()


def test_controller_password_and_info_from_device_suite(controller_with_mock) -> None:
    controller, mock_cam = controller_with_mock
    mock_cam.set_password.return_value = True
    mock_cam.delete_password.return_value = True
    assert controller.set_camera_password(1, "pw")
    assert controller.validate_camera_password(1, "pw") is True
    assert controller.validate_camera_password(1, "wrong") is False
    assert controller.delete_camera_password(1) is True
    info = controller.get_all_camera_info()
    assert info[0]["id"] == 1
    assert info[0]["location"] == [100, 200]


def test_controller_control_and_display_from_device_suite(controller_with_mock) -> None:
    controller, mock_cam = controller_with_mock
    assert controller.control_single_camera(1, controller.CONTROL_PAN_LEFT) is True
    assert controller.control_single_camera(1, controller.CONTROL_ZOOM_IN) is True
    view = controller.display_single_view(1)
    assert view == "frame"
    thumbnails = controller.display_thumbnail_view()
    assert thumbnails == [(1, "frame")]


def test_controller_invalid_add_returns_none() -> None:
    controller = CameraController()
    assert controller.add_camera(-1, 100) is None


@pytest.fixture(autouse=True)
def fake_device(monkeypatch):
    class FakeDevice:
        def __init__(self):
            self.current_id = None

        def set_id(self, camera_id: int) -> None:
            self.current_id = camera_id

        def zoom_in(self) -> bool:
            return True

        def zoom_out(self) -> bool:
            return True

        def pan_left(self) -> bool:
            return True

        def pan_right(self) -> bool:
            return True

        def get_view(self) -> str:
            return f"frame-{self.current_id}"

        def stop(self) -> None:
            pass

    monkeypatch.setattr(
        "safehome.src.devices.cameras.safehome_camera_base.DeviceCamera",
        FakeDevice,
    )


@pytest.fixture
def safehome_camera() -> SafeHomeCamera:
    return SafeHomeCamera(1, 150, 160)


def test_safehome_camera_zoom_pan_from_device_suite(
    safehome_camera: SafeHomeCamera,
) -> None:
    safehome_camera.enable()
    assert safehome_camera.zoom_in() is True
    assert safehome_camera.zoom_out() is True
    assert safehome_camera.pan_left() is True
    assert safehome_camera.pan_right() is True


def test_safehome_camera_location_validation_from_device_suite(
    safehome_camera: SafeHomeCamera,
) -> None:
    safehome_camera.set_location([120, 180])
    assert safehome_camera.get_location() == [120, 180]
    with pytest.raises(CameraValidationError):
        safehome_camera.set_location([1])


def test_safehome_camera_display_and_password_from_device_suite(
    safehome_camera: SafeHomeCamera,
) -> None:
    with pytest.raises(CameraDisabledError):
        safehome_camera.display_view()
    safehome_camera.enable()
    assert safehome_camera.display_view().startswith("frame-")
    safehome_camera.set_password("pw")
    assert safehome_camera.has_password() is True
    assert safehome_camera.get_password() == "pw"
