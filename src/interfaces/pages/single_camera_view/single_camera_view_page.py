"""SingleCameraViewPage - SRS V.3.a,b,c,d."""

from tkinter import messagebox

from ...components.page import Page
from ..camera_list.access_manager import CameraAccessManager
from .ui_builder import SingleCameraViewUIBuilder
from .password_manager import CameraPasswordManager
from .video_feed import VideoFeedManager
from .lock_manager import CameraLockManager
from .controls import CameraControls
from .info_panel import CameraInfoPanel
from .navigation import BackNavigation


class SingleCameraViewPage(Page):
    """Single camera view with pan/zoom and password controls."""

    def __init__(self, parent, web_interface):
        super().__init__(parent, web_interface)
        self._cam_id = None
        self._is_visible = False
        self._video_paused = False
        self._video = None
        self._info = None
        self._btn_en = None
        self._btn_dis = None
        self._info_panel = CameraInfoPanel(self)
        self._pw_manager = CameraPasswordManager(self)
        self._lock_manager = CameraLockManager(self)
        self._video_feed = VideoFeedManager(self)
        self._controls = CameraControls(self, self._info_panel)
        self._back_nav = BackNavigation(self)
        self._access_manager = CameraAccessManager(self)
        self._requires_password = False

    @property
    def controls(self) -> CameraControls:
        return self._controls

    def _build_ui(self):
        builder = SingleCameraViewUIBuilder(self)
        builder.build()

    def blank_video(self, message: str, pause_feed: bool = True):
        """Immediately hide the live view with a message."""
        if pause_feed:
            self._video_feed.stop()
            self._video_paused = True
        if self._video:
            self._video.config(
                image="",
                text=message,
                font=('Arial', 14, 'bold'),
                foreground='#555',
                compound='center'
            )
            self._video.image = None

    def on_show(self):
        self._is_visible = True
        self._back_nav.apply()
        self._cam_id = self._web_interface.get_context("camera_id", "C1")
        if not self._ensure_camera_access():
            self._is_visible = False
            return
        self._video_paused = False
        if self._video:
            self._video.config(text="")
        self._info_panel.refresh()
        self._video_feed.start()

    def on_hide(self):
        self._is_visible = False
        self._video_feed.stop()

    def refresh_camera_info(self):
        """Public helper so other components can refresh metadata safely."""
        self._info_panel.refresh()

    def _update_info(self):
        """Backward-compatible alias used by password manager."""
        self.refresh_camera_info()

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #
    def _ensure_camera_access(self) -> bool:
        """Ensure the current user is authorized to view the selected camera."""
        info = self.send_to_system("get_camera", camera_id=self._cam_id)
        if not info.get("success"):
            messagebox.showerror("Camera Error", info.get("message", "Camera not found"))
            self._navigate_back()
            return False

        data = info.get("data") or {}
        self._requires_password = bool(
            data.get("has_password") or data.get("password")
        )
        if not self._requires_password:
            return True

        if self._access_manager.is_locked(self._cam_id):
            self.blank_video("Camera is locked.\nPlease wait 60 seconds.", pause_feed=True)
            self._navigate_back()
            return False

        self.blank_video("Password required.\nEnter camera password.", pause_feed=True)
        if self._access_manager.verify_password(self._cam_id):
            if self._video:
                self._video.config(text="")
            return True

        self.blank_video("Password verification failed.", pause_feed=True)
        self._navigate_back()
        return False

    def _navigate_back(self):
        target = self._web_interface.get_context("camera_back_page", "camera_list")
        self.navigate_to(target)

