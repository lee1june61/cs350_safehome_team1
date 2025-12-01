"""
Unit tests for CameraControlService covering PTZ and enable/disable branches.
"""

from src.core.services.camera.camera_control import CameraControlService


class DummyCamera:
    def __init__(self):
        self.pan_angle = 10
        self.zoom_level = 1
        self.tilt_angle = 5
        self.can_tilt = True

    def get_pan_angle(self):
        return self.pan_angle

    def get_zoom_level(self):
        return self.zoom_level

    def tilt_up(self):
        self.tilt_angle += 1
        return True

    def tilt_down(self):
        self.tilt_angle -= 1
        return True

    def get_tilt_angle(self):
        return self.tilt_angle


class DummyController:
    CONTROL_PAN_RIGHT = "PAN_RIGHT"
    CONTROL_PAN_LEFT = "PAN_LEFT"
    CONTROL_ZOOM_IN = "ZOOM_IN"
    CONTROL_ZOOM_OUT = "ZOOM_OUT"

    def __init__(self):
        self.cameras = {}
        self.enabled = set()
        self.disabled = set()
        self.raise_on_get = False
        self.commands = []

    def add_camera(self, cam_id, camera):
        self.cameras[cam_id] = camera

    def control_single_camera(self, cam_id, command):
        self.commands.append((cam_id, command))
        return cam_id in self.cameras

    def get_camera_by_id(self, cam_id):
        if self.raise_on_get:
            raise RuntimeError("boom")
        return self.cameras.get(cam_id)

    def enable_camera(self, cam_id):
        if cam_id in self.cameras:
            self.enabled.add(cam_id)
            return True
        return False

    def disable_camera(self, cam_id):
        if cam_id in self.cameras:
            self.disabled.add(cam_id)
            return True
        return False


class TestCameraControlService:
    def _service_with_camera(self):
        controller = DummyController()
        controller.add_camera(1, DummyCamera())
        service = CameraControlService(controller)
        return service, controller

    def test_pan_success_and_failure(self):
        service, controller = self._service_with_camera()

        success = service.pan(1, "R")
        assert success["success"] is True
        assert success["pan"] == controller.cameras[1].get_pan_angle()
        # CameraController uses numeric constants internally, so just ensure a command was recorded
        assert controller.commands[-1][0] == 1

        failure = service.pan(2, "L")
        assert failure == {"success": False, "message": "Camera not found"}

    def test_zoom_in_out(self):
        service, controller = self._service_with_camera()

        success = service.zoom(1, "in")
        assert success["zoom"] == controller.cameras[1].get_zoom_level()
        assert controller.commands[-1][0] == 1

        failure = service.zoom(999, "out")
        assert failure["success"] is False

    def test_tilt_validation_paths(self):
        service, controller = self._service_with_camera()
        camera = controller.cameras[1]

        assert service.tilt(None, "up") == {"success": False, "message": "Camera not found"}
        no_tilt = object()
        assert service.tilt(no_tilt, "up") == {"success": False, "message": "Tilt not supported"}
        assert service.tilt(camera, "sideways") == {
            "success": False,
            "message": "Invalid tilt direction",
        }

        result = service.tilt(camera, "up")
        assert result["success"] is True
        assert result["tilt"] == camera.get_tilt_angle()

    def test_enable_disable_responses(self):
        service, controller = self._service_with_camera()

        assert service.enable(1) == {"success": True}
        assert service.enable(99) == {"success": False, "message": "Camera not found"}

        assert service.disable(1) == {"success": True}
        assert service.disable(99)["success"] is False

    def test_get_camera_handles_controller_exception(self):
        controller = DummyController()
        controller.add_camera(1, DummyCamera())
        controller.raise_on_get = True
        service = CameraControlService(controller)

        response = service.pan(1, "R")

        assert response["success"] is True
        assert response["pan"] is None  # _get_camera swallowed exception

