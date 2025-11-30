"""Custom Camera device implementation."""

import os
import threading
import time
from PIL import Image, ImageDraw, ImageFont
from ..virtual_devices.device_camera import DeviceCamera as BaseDeviceCamera
from .custom_camera_features import (
    CameraPasswordMixin,
    CameraStateMixin,
    CameraTiltMixin,
)

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "resources", "images")


class CustomDeviceCamera(
    CameraPasswordMixin, CameraStateMixin, CameraTiltMixin, BaseDeviceCamera
):
    """Custom camera device with password protection and location features."""

    def __init__(self, location: str, camera_id: int):
        threading.Thread.__init__(self, daemon=True)
        self.camera_id = camera_id
        self.time = 0
        self.pan = 0
        self.tilt = 0
        self.zoom = 2
        self.img_source = None
        self.center_width = 0
        self.center_height = 0
        self._running = True
        self._lock = threading.Lock()
        self.font = ImageFont.load_default()
        self._enabled = True
        self._password = None
        self._location = location
        self.set_id(camera_id)
        self.start()

    def set_id(self, id_: int):
        with self._lock:
            self.camera_id = id_
            filename = os.path.join(ASSETS_DIR, f"camera{id_}.jpg")
            try:
                self.img_source = Image.open(filename)
                self.center_width = self.img_source.width // 2
                self.center_height = self.img_source.height // 2
            except FileNotFoundError:
                self.img_source = None

    def get_view(self):
        with self._lock:
            if not self._enabled:
                img = Image.new("RGB", (self.RETURN_SIZE, self.RETURN_SIZE), "gray")
                draw = ImageDraw.Draw(img)
                try:
                    font = ImageFont.truetype("arial.ttf", 20)
                except IOError:
                    font = ImageFont.load_default()
                draw.text((200, 240), "DISABLED", fill="white", font=font)
                return img
            return self._render_view()

    def _render_view(self):
        view_text = f"Time={self.time:02d}, zoom x{self.zoom}, "
        view_text += (
            f"right {self.pan}"
            if self.pan > 0
            else "center" if self.pan == 0 else f"left {-self.pan}"
        )
        img_view = Image.new("RGB", (self.RETURN_SIZE, self.RETURN_SIZE), "black")
        if self.img_source:
            zoomed = self.SOURCE_SIZE * (10 - self.zoom) // 10
            panned = self.pan * self.SOURCE_SIZE // 5
            left, top = self.center_width + panned - zoomed, self.center_height - zoomed
            right, bottom = (
                self.center_width + panned + zoomed,
                self.center_height + zoomed,
            )
            try:
                cropped = self.img_source.crop((left, top, right, bottom))
                resized = cropped.resize(
                    (self.RETURN_SIZE, self.RETURN_SIZE), Image.LANCZOS
                )
                img_view.paste(resized, (0, 0))
            except Exception:
                pass
        draw = ImageDraw.Draw(img_view)
        bbox = draw.textbbox((0, 0), view_text, font=self.font)
        w_text, h_text = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.rounded_rectangle(
            [(0, 0), (w_text + 10, h_text + 5)], radius=h_text // 2, fill="gray"
        )
        draw.text((5, 2), view_text, fill="cyan", font=self.font)
        return img_view

    def run(self):
        while self._running:
            time.sleep(1.0)
            with self._lock:
                self.time = (self.time + 1) % 100
