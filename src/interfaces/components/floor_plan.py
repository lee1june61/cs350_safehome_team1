"""FloorPlan - House blueprint with clickable devices (SDS: FloorPlan class)"""
import tkinter as tk
from pathlib import Path
from typing import Dict, Optional, Callable, Set

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("[FloorPlan] PIL not installed. Run: pip install Pillow")

# Device positions from floorplan.png analysis (image ~605x305)
# Coordinates adjusted to match actual device labels in image
DEVICES = {
    # Cameras (gray triangles with C labels)
    'C1': (0.28, 0.23, 'camera'),   # DR room - inside triangle
    'C2': (0.52, 0.49, 'camera'),   # Center/hallway - near stairs
    'C3': (0.77, 0.69, 'camera'),   # LR room - inside triangle
    # Window/Door Sensors (red dots with S labels)
    'S1': (0.10, 0.05, 'sensor'),   # Top-left corner, above DR
    'S2': (0.07, 0.92, 'sensor'),   # Bottom-left, below KIT
    'S3': (0.07, 0.48, 'sensor'),   # Left side, KIT area
    'S4': (0.84, 0.05, 'sensor'),   # Top-right, above LR
    'S5': (0.97, 0.31, 'sensor'),   # Right side upper
    'S6': (0.97, 0.66, 'sensor'),   # Right side lower
    # Motion Sensors (blue/black dots with M labels)
    'M1': (0.04, 0.20, 'motion'),   # Left side, DR area
    'M2': (0.44, 0.44, 'motion'),   # Center hallway
}


class FloorPlan:
    """Floor plan with clickable device icons for cameras, sensors, motion detectors."""

    def __init__(self, parent: tk.Widget, width: int = 450, height: int = 280,
                 show_cameras: bool = True, show_sensors: bool = True):
        self._parent = parent
        self._w, self._h = width, height
        self._canvas: Optional[tk.Canvas] = None
        self._photo: Optional[ImageTk.PhotoImage] = None
        self._on_click: Optional[Callable] = None
        self._on_sensor_click: Optional[Callable] = None
        self._states: Dict[str, bool] = {}  # armed state
        self._selected: Set[str] = set()    # selected sensors for zone editing
        self._show_cameras = show_cameras
        self._show_sensors = show_sensors
        self._select_mode = False  # mode for selecting sensors

    def create(self) -> tk.Canvas:
        """Create and return the canvas widget."""
        self._canvas = tk.Canvas(self._parent, width=self._w, height=self._h, 
                                  bg='#f0f0f0', highlightthickness=1, highlightbackground='#ccc')
        self._draw()
        return self._canvas

    def _find_image(self) -> Optional[Path]:
        """Find floorplan.png from multiple possible locations."""
        src_dir = Path(__file__).resolve().parent.parent.parent
        candidates = [
            src_dir / "resources" / "images" / "floorplan.png",
            src_dir.parent / "virtual_device_v4" / "floorplan.png",
            Path.cwd() / "src" / "resources" / "images" / "floorplan.png",
            Path.cwd() / "virtual_device_v4" / "floorplan.png",
        ]
        for p in candidates:
            if p.exists():
                return p
        return None

    def _draw(self):
        """Draw floor plan image and device icons."""
        if not self._canvas:
            return
        self._canvas.delete('all')
        
        # Try to load actual floor plan image
        img_path = self._find_image()
        if HAS_PIL and img_path:
            try:
                img = Image.open(img_path)
                # Scale to fit canvas while preserving aspect ratio
                ratio = min(self._w / img.width, self._h / img.height)
                new_w, new_h = int(img.width * ratio), int(img.height * ratio)
                img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                self._photo = ImageTk.PhotoImage(img)
                # Center the image
                x_off = (self._w - new_w) // 2
                y_off = (self._h - new_h) // 2
                self._canvas.create_image(x_off, y_off, image=self._photo, anchor='nw')
            except Exception as e:
                print(f"[FloorPlan] Image load error: {e}")
                self._draw_fallback()
        else:
            self._draw_fallback()
        
        self._draw_devices()

    def _draw_fallback(self):
        """Draw simple room layout if image unavailable."""
        w, h = self._w, self._h
        # DR room (top-left quadrant)
        self._canvas.create_rectangle(10, 10, w*0.42, h*0.45, fill='#fafafa', outline='#555', width=2)
        self._canvas.create_text(w*0.22, h*0.25, text='DR', font=('Arial', 16, 'italic'), fill='#888')
        # KIT room (bottom-left)
        self._canvas.create_rectangle(10, h*0.45, w*0.42, h-10, fill='#fafafa', outline='#555', width=2)
        self._canvas.create_text(w*0.22, h*0.72, text='KIT', font=('Arial', 16, 'italic'), fill='#888')
        # LR room (right side)
        self._canvas.create_rectangle(w*0.5, 10, w-10, h-10, fill='#fafafa', outline='#555', width=2)
        self._canvas.create_text(w*0.75, h*0.5, text='LR', font=('Arial', 16, 'italic'), fill='#888')
        # Hallway (center)
        self._canvas.create_rectangle(w*0.42, h*0.3, w*0.5, h*0.7, fill='#e8e8e8', outline='#777')

    def _draw_devices(self):
        """Draw device icons at calculated positions."""
        colors = {
            'camera': '#9b59b6',   # Purple
            'sensor': '#e74c3c',   # Red
            'motion': '#3498db',   # Blue
        }
        
        for dev_id, (nx, ny, dtype) in DEVICES.items():
            # Skip based on show flags
            if dtype == 'camera' and not self._show_cameras:
                continue
            if dtype in ('sensor', 'motion') and not self._show_sensors:
                continue
            
            x, y = int(nx * self._w), int(ny * self._h)
            r = 10  # radius
            
            # Determine appearance based on state
            armed = self._states.get(dev_id, False)
            selected = dev_id in self._selected
            fill = colors.get(dtype, '#666')
            
            # Outline: green if armed, yellow if selected, black otherwise
            if selected:
                outline = '#f39c12'  # Orange for selected
                width = 3
            elif armed:
                outline = '#27ae60'  # Green for armed
                width = 3
            else:
                outline = '#333'
                width = 2
            
            # Draw the icon
            tag = f'd_{dev_id}'
            self._canvas.create_oval(x-r, y-r, x+r, y+r, fill=fill, outline=outline,
                                    width=width, tags=(tag, 'device', dtype))
            # Label below
            self._canvas.create_text(x, y+16, text=dev_id, font=('Arial', 9, 'bold'),
                                    fill='#333', tags=(f'lbl_{dev_id}',))
            
            # Bind click events
            self._canvas.tag_bind(tag, '<Button-1>', 
                lambda e, d=dev_id, t=dtype: self._handle_click(d, t))

    def _handle_click(self, dev_id: str, dtype: str):
        """Handle device click."""
        if self._select_mode and dtype in ('sensor', 'motion'):
            # Toggle selection
            if dev_id in self._selected:
                self._selected.discard(dev_id)
            else:
                self._selected.add(dev_id)
            self.refresh()
            if self._on_sensor_click:
                self._on_sensor_click(dev_id, dtype, dev_id in self._selected)
        elif self._on_click:
            self._on_click(dev_id, dtype)

    def set_on_click(self, handler: Callable[[str, str], None]):
        """Set callback for device click: handler(device_id, device_type)."""
        self._on_click = handler

    def set_on_sensor_click(self, handler: Callable[[str, str, bool], None]):
        """Set callback for sensor selection: handler(device_id, device_type, is_selected)."""
        self._on_sensor_click = handler

    def set_select_mode(self, enabled: bool):
        """Enable/disable sensor selection mode for zone editing."""
        self._select_mode = enabled
        if not enabled:
            self._selected.clear()
        self.refresh()

    def set_armed(self, device_id: str, armed: bool):
        """Set armed state for a device."""
        self._states[device_id] = armed

    def set_selected(self, device_ids: list):
        """Set selected devices (for zone editing)."""
        self._selected = set(device_ids)
        self.refresh()

    def get_selected(self) -> list:
        """Get list of selected device IDs."""
        return list(self._selected)

    def clear_selection(self):
        """Clear all selections."""
        self._selected.clear()
        self.refresh()

    def refresh(self):
        """Redraw the floor plan."""
        self._draw()

    def get_devices(self, dtype: str = None) -> list:
        """Get list of device IDs, optionally filtered by type."""
        if dtype:
            return [d for d, (_, _, t) in DEVICES.items() if t == dtype]
        return list(DEVICES.keys())

    def get_sensors(self) -> list:
        """Get all sensor IDs (window/door + motion)."""
        return [d for d, (_, _, t) in DEVICES.items() if t in ('sensor', 'motion')]
