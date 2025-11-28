import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .single_camera_view_page import SingleCameraViewPage


class VideoFeedManager:
    """
    Manages the fetching and displaying of the camera's video feed.
    """
    def __init__(self, page_instance: 'SingleCameraViewPage', video_label: ttk.Label, frame: tk.Frame):
        self._page = page_instance
        self._video = video_label
        self._frame = frame
        self._video_job: Optional[str] = None

    @property
    def _cam_id(self) -> str:
        return self._page._cam_id

    @property
    def _is_visible(self) -> bool:
        return self._page._is_visible

    def start_feed(self):
        """Starts the video feed loop."""
        self._page._is_visible = True
        self._update_video_feed()

    def stop_feed(self):
        """Stops the video feed loop."""
        self._page._is_visible = False
        if self._video_job:
            self._frame.after_cancel(self._video_job)
            self._video_job = None

    def _update_video_feed(self):
        """Fetch and display the latest camera view."""
        if not self._is_visible:
            return  # Stop the loop if the page is hidden

        res = self._page.send_to_system('get_camera_view', camera_id=self._cam_id)
        if res.get('success'):
            view = res.get('view')
            if view:
                photo_img = ImageTk.PhotoImage(view)
                self._video.config(image=photo_img)
                self._video.image = photo_img # Keep reference to prevent garbage collection
        
        # Schedule the next update
        self._video_job = self._frame.after(1000, self._update_video_feed)
