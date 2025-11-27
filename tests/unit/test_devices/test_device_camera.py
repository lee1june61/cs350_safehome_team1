"""
Unit tests for DeviceCamera following SDS responsibilities.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest  # type: ignore[import]

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "safehome" / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from safehome.src.devices.cameras.device_camera import DeviceCamera


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


def test_set_tilt_and_zoom(device_camera: DeviceCamera) -> None:
    assert device_camera.set_tilt(-30) is True
    assert device_camera.get_tilt() == -30
    assert device_camera.set_tilt(-120) is False

    assert device_camera.set_zoom(25) is True
    assert device_camera.get_zoom() == 25
    assert device_camera.set_zoom(150) is False


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

