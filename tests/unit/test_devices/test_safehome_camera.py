"""
Unit tests for SafeHomeCamera aligned with SDS requirements.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest  # type: ignore[import]

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "safehome" / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from safehome.src.devices.cameras.safehome_camera import SafeHomeCamera
from safehome.src.utils.exceptions import CameraDisabledError


@pytest.fixture(autouse=True)
def fake_device(monkeypatch):
    """Patch DeviceCamera to avoid dependency on virtual device assets."""

    class FakeDevice:
        def __init__(self):
            self.current_id = None
            self.stopped = False

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
            self.stopped = True

    monkeypatch.setattr(
        "safehome.src.devices.cameras.safehome_camera_base.DeviceCamera",
        FakeDevice,
    )


@pytest.fixture
def camera() -> SafeHomeCamera:
    """Create a SafeHomeCamera at coordinates [200, 250]."""
    return SafeHomeCamera(1, 200, 250)


def test_get_location_returns_coordinates(camera: SafeHomeCamera) -> None:
    assert camera.get_location() == [200, 250]


def test_set_location_updates_coordinates(camera: SafeHomeCamera) -> None:
    new_location = [180, 220]
    camera.set_location(new_location)
    new_location[0] = 0  # ensure defensive copy is stored
    assert camera.get_location() == [180, 220]


def test_get_and_set_id(camera: SafeHomeCamera) -> None:
    assert camera.get_id() == 1
    camera.set_id(5)
    assert camera.get_id() == 5


def test_display_view_requires_enabled(camera: SafeHomeCamera) -> None:
    with pytest.raises(CameraDisabledError):
        camera.display_view()


def test_display_view_returns_frame_when_enabled(camera: SafeHomeCamera) -> None:
    camera.enable()
    assert camera.display_view() == "frame-5" if camera.get_id() == 5 else "frame-1"


def test_zoom_increases_level_when_enabled(camera: SafeHomeCamera) -> None:
    camera.enable()
    assert camera.zoom_level == 2
    assert camera.zoom_in() is True
    assert camera.get_zoom_level() == 3


def test_zoom_out_decreases_level_when_enabled(camera: SafeHomeCamera) -> None:
    camera.enable()
    camera.zoom_level = 4
    assert camera.zoom_out() is True
    assert camera.get_zoom_level() == 3


def test_pan_left_and_right_adjust_angles(camera: SafeHomeCamera) -> None:
    camera.enable()
    assert camera.pan_left() is True
    assert camera.get_pan_angle() == -1
    assert camera.pan_right() is True
    assert camera.get_pan_angle() == 0


def test_password_roundtrip(camera: SafeHomeCamera) -> None:
    assert camera.has_password() is False
    camera.set_password("secure123")
    assert camera.has_password() is True
    assert camera.get_password() == "secure123"
    camera.clear_password()
    assert camera.has_password() is False


def test_enable_disable_and_status(camera: SafeHomeCamera) -> None:
    assert camera.is_enabled() is False
    assert camera.enable() is True
    assert camera.is_enabled() is True
    assert camera.disable() is True
    assert camera.is_enabled() is False


def test_save_info_runs_validation(camera: SafeHomeCamera) -> None:
    camera.enable()
    camera.set_location([150, 180])
    assert camera.save_info() is True
