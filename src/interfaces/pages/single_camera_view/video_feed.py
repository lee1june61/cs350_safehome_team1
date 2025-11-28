"""Video feed manager for camera view."""
from typing import TYPE_CHECKING, Optional
from PIL import ImageTk

if TYPE_CHECKING:
    from .single_camera_view_page import SingleCameraViewPage


class VideoFeedManager:
    """Manages live video feed display."""

    def __init__(self, page: "SingleCameraViewPage"):
        self._page = page
        self._job: Optional[int] = None

    def start(self):
        """Start video feed loop."""
        self._update()

    def stop(self):
        """Stop video feed loop."""
        if self._job:
            self._page._frame.after_cancel(self._job)
            self._job = None

    def _update(self):
        """Fetch and display latest camera view."""
        if not self._page._is_visible:
            return

        res = self._page.send_to_system(
            "get_camera_view",
            camera_id=self._page._cam_id
        )

        if res.get("success"):
            view = res.get("view")
            if view:
                photo = ImageTk.PhotoImage(view)
                self._page._video.config(image=photo)
                self._page._video.image = photo

        self._job = self._page._frame.after(1000, self._update)

