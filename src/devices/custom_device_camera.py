"""
Custom Camera device implementation.
Extends the base virtual camera with password protection and other features.
"""
import os
import threading
import time
from PIL import Image, ImageDraw, ImageFont
from ..virtual_devices.device_camera import DeviceCamera as BaseDeviceCamera

# Get assets directory path
ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', 'resources', 'images')


class CustomDeviceCamera(BaseDeviceCamera):
    """
    Custom camera device that extends the base camera with password protection
    and loads images from the project's assets folder.
    """
    
    def __init__(self, location: str, camera_id: int):
        # We don't call super().__init__() because the base class is a Thread
        # and starts itself immediately. We need to initialize properties first.
        threading.Thread.__init__(self, daemon=True)
        
        # --- Properties from Base Class ---
        self.camera_id = camera_id
        self.time = 0
        self.pan = 0
        self.zoom = 2
        self.img_source = None
        self.center_width = 0
        self.center_height = 0
        self._running = True
        self._lock = threading.Lock()
        self.font = ImageFont.load_default()
        
        # --- Custom Properties ---
        self._enabled = True
        self._password = None
        self._location = location
        
        # Set the ID and load the image before starting the thread
        self.set_id(camera_id)
        
        self.start()

    def get_status(self) -> dict:
        """Get comprehensive camera status as a dictionary."""
        return {
            'id': f"C{self.camera_id}",
            'location': self._location,
            'enabled': self._enabled,
            'password': self.has_password(),
            'pan': self.pan,
            'zoom': self.zoom,
        }

    # ============================================================
    # Override and extend base class methods
    # ============================================================

    def set_id(self, id_: int):
        """Set camera ID and load associated image from the assets folder."""
        with self._lock:
            self.camera_id = id_
            # Adjusted to look in the correct assets folder
            filename = os.path.join(ASSETS_DIR, f"camera{id_}.jpg")
            
            try:
                self.img_source = Image.open(filename)
                self.center_width = self.img_source.width // 2
                self.center_height = self.img_source.height // 2
            except FileNotFoundError:
                self.img_source = None
                print(f"Warning: Camera image '{filename}' not found.")

    def get_view(self):
        """Get current camera view as PIL Image, showing a disabled state if needed."""
        with self._lock:
            if not self._enabled:
                # Return disabled indicator
                img = Image.new('RGB', (self.RETURN_SIZE, self.RETURN_SIZE), 'gray')
                draw = ImageDraw.Draw(img)
                # Ensure font can be loaded
                try:
                    font = ImageFont.truetype("arial.ttf", 20)
                except IOError:
                    font = ImageFont.load_default()
                draw.text((200, 240), "DISABLED", fill='white', font=font)
                return img
            
            # If enabled, use the base class's get_view logic, but since we can't
            # call super() on it directly (it's the same method), we replicate and own it.
            view_text = f"Time={self.time:02d}, zoom x{self.zoom}, "
            if self.pan > 0:
                view_text += f"right {self.pan}"
            elif self.pan == 0:
                view_text += "center"
            else:
                view_text += f"left {-self.pan}"
            
            img_view = Image.new('RGB', (self.RETURN_SIZE, self.RETURN_SIZE), 'black')
            
            if self.img_source is not None:
                zoomed = self.SOURCE_SIZE * (10 - self.zoom) // 10
                panned = self.pan * self.SOURCE_SIZE // 5
                
                left = self.center_width + panned - zoomed
                top = self.center_height - zoomed
                right = self.center_width + panned + zoomed
                bottom = self.center_height + zoomed
                
                try:
                    cropped = self.img_source.crop((left, top, right, bottom))
                    resized = cropped.resize((self.RETURN_SIZE, self.RETURN_SIZE), Image.LANCZOS)
                    img_view.paste(resized, (0, 0))
                except Exception:
                    pass
            
            draw = ImageDraw.Draw(img_view)
            bbox = draw.textbbox((0, 0), view_text, font=self.font)
            w_text = bbox[2] - bbox[0]
            h_text = bbox[3] - bbox[1]
            
            draw.rounded_rectangle(
                [(0, 0), (w_text + 10, h_text + 5)],
                radius=h_text // 2,
                fill='gray'
            )
            draw.text((5, 2), view_text, fill='cyan', font=self.font)
            
            return img_view

    def run(self):
        """Thread run - updates time counter."""
        while self._running:
            time.sleep(1.0)
            with self._lock:
                self.time = (self.time + 1) % 100

    # ============================================================
    # Custom methods for this class
    # ============================================================

    def set_location(self, location: str):
        self._location = location
    
    def get_location(self) -> str:
        return self._location
    
    def enable(self):
        self._enabled = True
    
    def disable(self):
        self._enabled = False
    
    def is_enabled(self) -> bool:
        return self._enabled
    
    def set_password(self, password: str):
        self._password = password
    
    def get_password(self) -> str:
        return self._password
    
    def clear_password(self):
        self._password = None
    
    def has_password(self) -> bool:
        return self._password is not None
    
    def verify_password(self, password: str) -> bool:
        if self._password is None:
            return True
        return self._password == password
