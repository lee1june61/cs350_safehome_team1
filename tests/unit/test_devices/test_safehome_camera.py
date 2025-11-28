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

import safehome.src.devices.cameras.safehome_camera_base as camera_base
from safehome.src.devices.cameras.safehome_camera import SafeHomeCamera
from safehome.src.utils.exceptions import (
    CameraDisabledError,
    CameraPasswordError,
    CameraValidationError,
)


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


def test_pan_boundaries_and_disabled(camera: SafeHomeCamera) -> None:
    camera.enable()
    camera.pan_angle = camera.MIN_PAN
    assert camera.pan_left() is False
    camera.pan_angle = camera.MAX_PAN
    assert camera.pan_right() is False
    camera.disable()
    assert camera.pan_left() is False


def test_password_roundtrip(camera: SafeHomeCamera) -> None:
    assert camera.has_password() is False
    camera.set_password("secure123")
    assert camera.has_password() is True
    assert camera.get_password() == "secure123"
    camera.clear_password()
    assert camera.has_password() is False


def test_password_validation_and_alias(camera: SafeHomeCamera) -> None:
    with pytest.raises(CameraPasswordError):
        camera.set_password("")
    camera.set_password("secret")
    assert camera.delete_password() is True
    assert camera.has_password() is False


def test_enable_disable_and_status(camera: SafeHomeCamera) -> None:
    assert camera.is_enabled() is False
    assert camera.enable() is True
    assert camera.is_enabled() is True
    assert camera.disable() is True
    assert camera.is_enabled() is False


def test_zoom_boundaries_and_disabled(camera: SafeHomeCamera) -> None:
    camera.enable()
    camera.zoom_level = camera.MAX_ZOOM
    assert camera.zoom_in() is False
    camera.zoom_level = camera.MIN_ZOOM
    assert camera.zoom_out() is False
    camera.disable()
    assert camera.zoom_in() is False


def test_save_info_runs_validation(camera: SafeHomeCamera) -> None:
    camera.enable()
    camera.set_location([150, 180])
    assert camera.save_info() is True


def test_validation_errors_detected(camera: SafeHomeCamera) -> None:
    camera.camera_id = -1
    with pytest.raises(CameraValidationError):
        camera.validate()
    camera.camera_id = 1
    camera.pan_angle = camera.MAX_PAN + 1
    with pytest.raises(CameraValidationError):
        camera.validate()
    camera.pan_angle = 0
    camera.zoom_level = camera.MAX_ZOOM + 1
    with pytest.raises(CameraValidationError):
        camera.validate()


def test_set_location_invalid_input(camera: SafeHomeCamera) -> None:
    with pytest.raises(CameraValidationError):
        camera.set_location([1])


def test_set_id_reinitializes_device(camera: SafeHomeCamera, monkeypatch) -> None:
    recorded = {}

    def fake_set_id(new_id: int) -> None:
        recorded["value"] = new_id

    monkeypatch.setattr(camera._device, "set_id", fake_set_id)
    camera.set_id(10)
    assert recorded["value"] == 10


def test_cleanup_and_repr(camera: SafeHomeCamera, monkeypatch) -> None:
    stopped = {"value": False}

    def fake_stop() -> None:
        stopped["value"] = True

    monkeypatch.setattr(camera._device, "stop", fake_stop)
    camera.cleanup()
    assert stopped["value"] is True
    description = repr(camera)
    assert "SafeHomeCamera" in description
    assert f"id={camera.get_id()}" in description


def test_temporary_asset_directory(monkeypatch, camera: SafeHomeCamera) -> None:
    calls: list[Path] = []

    def fake_chdir(path: Path) -> None:
        calls.append(Path(path))

    monkeypatch.setattr(camera_base.os, "chdir", fake_chdir)
    original = Path("/tmp/original")
    monkeypatch.setattr(
        camera_base.Path,
        "cwd",
        classmethod(lambda cls: original),
    )
    with camera._temporary_asset_directory():
        assert calls[-1] == camera._asset_dir
    assert calls[-1] == original


def test_initialize_device_invokes_set_id(camera: SafeHomeCamera, monkeypatch) -> None:
    recorded = {}

    def fake_set_id(new_id: int) -> None:
        recorded["value"] = new_id

    monkeypatch.setattr(camera._device, "set_id", fake_set_id)
    camera._initialize_device(77)
    assert recorded["value"] == 77
