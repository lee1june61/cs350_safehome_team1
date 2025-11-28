"""SingleCameraViewPage - SRS V.3.a,b,c,d."""
from ...components.page import Page
from .ui_builder import SingleCameraViewUIBuilder
from .password_manager import CameraPasswordManager
from .video_feed import VideoFeedManager
from .lock_manager import CameraLockManager


class SingleCameraViewPage(Page):
    """Single camera view with pan/zoom and password controls."""

    def __init__(self, parent, web_interface):
        super().__init__(parent, web_interface)
        self._cam_id = None
        self._is_visible = False
        self._video = None
        self._info = None
        self._btn_en = None
        self._btn_dis = None
        self._pw_manager = CameraPasswordManager(self)
        self._lock_manager = CameraLockManager(self)
        self._video_feed = VideoFeedManager(self)

    def _build_ui(self):
        builder = SingleCameraViewUIBuilder(self)
        builder.build()

    def _pan(self, direction: str):
        self.send_to_system("camera_pan", camera_id=self._cam_id, direction=direction)
        self._update_info()

    def _zoom(self, direction: str):
        self.send_to_system("camera_zoom", camera_id=self._cam_id, direction=direction)
        self._update_info()

    def _tilt(self, direction: str):
        self.send_to_system("camera_tilt", camera_id=self._cam_id, direction=direction)
        self._update_info()

    def _enable(self):
        self.send_to_system("enable_camera", camera_id=self._cam_id)
        self._update_info()

    def _disable(self):
        self.send_to_system("disable_camera", camera_id=self._cam_id)
        self._update_info()

    def _update_info(self):
        """Update camera info display."""
        res = self.send_to_system("get_camera", camera_id=self._cam_id)
        if not res.get("success"):
            return
        c = res.get("data", {})
        en = c.get("enabled", False)
        pw = "Yes" if c.get("password") else "No"
        text = (
            f"ID: {c.get('id')}\n"
            f"Loc: {c.get('location')}\n"
            f"Pan: {c.get('pan', 0)} Tilt: {c.get('tilt', 0)} Zoom: {c.get('zoom', 1)}x\n"
            f"Status: {'On' if en else 'Off'}\n"
            f"Password: {pw}"
        )
        self._info.config(text=text)
        self._btn_en.config(state="disabled" if en else "normal")
        self._btn_dis.config(state="normal" if en else "disabled")

    def on_show(self):
        self._is_visible = True
        self._cam_id = self._web_interface.get_context("camera_id", "C1")
        self._update_info()
        self._video_feed.start()

    def on_hide(self):
        self._is_visible = False
        self._video_feed.stop()

