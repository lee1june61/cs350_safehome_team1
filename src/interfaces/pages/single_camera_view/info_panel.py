"""Information panel helpers for SingleCameraViewPage."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - for typing only
    from .single_camera_view_page import SingleCameraViewPage


class CameraInfoPanel:
    """Present camera metadata and keep enable/disable buttons in sync."""

    def __init__(self, page: "SingleCameraViewPage"):
        self._page = page

    def refresh(self) -> None:
        """Fetch latest camera info and update UI state."""
        if not self._page._cam_id:
            return

        res = self._page.send_to_system("get_camera", camera_id=self._page._cam_id)
        if not res.get("success"):
            return

        if not self._page._info:
            return

        camera = res.get("data", {})
        enabled = camera.get("enabled", False)
        password_flag = "Yes" if camera.get("has_password") else "No"

        info_lines = (
            f"ID: {camera.get('id')}\n"
            f"Loc: {camera.get('location')}\n"
            f"Pan: {camera.get('pan', 0)} Tilt: {camera.get('tilt', 0)} "
            f"Zoom: {camera.get('zoom', 1)}x\n"
            f"Status: {'On' if enabled else 'Off'}\n"
            f"Password: {password_flag}"
        )
        self._page._info.config(text=info_lines)

        if self._page._btn_en and self._page._btn_dis:
            self._page._btn_en.config(state="disabled" if enabled else "normal")
            self._page._btn_dis.config(state="normal" if enabled else "disabled")

        if enabled and not self._page._video_paused and self._page._is_visible:
            self._page._video_feed.start()



