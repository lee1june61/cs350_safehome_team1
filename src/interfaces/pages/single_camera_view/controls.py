"""Camera control dispatchers for SingleCameraViewPage."""
from __future__ import annotations

from tkinter import messagebox
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .single_camera_view_page import SingleCameraViewPage
    from .info_panel import CameraInfoPanel


class CameraControls:
    """Encapsulate PTZ and power commands for a single camera view."""

    def __init__(self, page: "SingleCameraViewPage", info_panel: "CameraInfoPanel"):
        self._page = page
        self._info_panel = info_panel

    def pan(self, direction: str) -> None:
        self._send_and_refresh("camera_pan", direction=direction)

    def tilt(self, direction: str) -> None:
        self._send_and_refresh("camera_tilt", direction=direction)

    def zoom(self, direction: str) -> None:
        self._send_and_refresh("camera_zoom", direction=direction)

    def enable(self) -> None:
        result = self._send("enable_camera")
        if result.get("success"):
            self._page._video_paused = False
            if self._page._video:
                self._page._video.config(text="", foreground="#000")
            self._page._video_feed.start()
            self._info_panel.refresh()
        else:
            messagebox.showerror(
                "Enable Camera", result.get("message", "Unable to enable camera.")
            )

    def disable(self) -> None:
        result = self._send("disable_camera")
        if result.get("success"):
            self._page.blank_video("Camera disabled.\nPress Enable to resume.")
            self._info_panel.refresh()
        else:
            messagebox.showerror(
                "Disable Camera", result.get("message", "Unable to disable camera.")
            )

    def _send_and_refresh(self, command: str, **kwargs) -> None:
        self._send(command, **kwargs)
        self._info_panel.refresh()

    def _send(self, command: str, **kwargs):
        if not self._page._cam_id:
            return {}
        return self._page.send_to_system(
            command,
            camera_id=self._page._cam_id,
            **kwargs,
        )

