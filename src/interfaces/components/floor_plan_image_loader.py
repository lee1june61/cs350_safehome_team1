"""
Image loader for the FloorPlan component.
"""
from pathlib import Path
from typing import Optional

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

def find_image() -> Optional[Path]:
    """Find floorplan.png from multiple possible locations."""
    src_dir = Path(__file__).resolve().parent.parent.parent
    candidates = [
        src_dir / "resources" / "images" / "floorplan.png",
        src_dir.parent / "virtual_device_v4" / "floorplan.png",
        src_dir.parent / "virtual_device_v4" / "virtual_device_v4" / "floorplan.png", # Added from utils.py
        Path.cwd() / "src" / "resources" / "images" / "floorplan.png",
        Path.cwd() / "virtual_device_v4" / "floorplan.png",
        Path.cwd() / "virtual_device_v4" / "virtual_device_v4" / "floorplan.png", # Added from utils.py
    ]
    for p in candidates:
        if p.exists():
            return p
    return None

def load_floor_plan_image(canvas_width: int, canvas_height: int) -> Optional[ImageTk.PhotoImage]:
    """
    Load and resize the floor plan image to fit the canvas.
    """
    if not HAS_PIL:
        return None
        
    img_path = find_image()
    if not img_path:
        return None

    try:
        img = Image.open(img_path)
        ratio = min(canvas_width / img.width, canvas_height / img.height)
        new_w, new_h = int(img.width * ratio), int(img.height * ratio)
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        return photo, new_w, new_h
    except Exception as e:
        print(f"[FloorPlan] Image load error: {e}")
        return None
