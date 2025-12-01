"""SingleCameraViewPage - SRS V.3.a,b,c,d."""

from ...components.page import Page
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
        self._video_paused = False
        if self._video:
            self._video.config(text="")
        self._info_panel.refresh()
        self._video_feed.start()

    def on_hide(self):
        self._is_visible = False
        self._video_feed.stop()

