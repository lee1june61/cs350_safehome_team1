"""
Image loader for the FloorPlan component.
"""
from typing import Optional
from pathlib import Path
from src.resources import get_image

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

def find_image() -> Optional[Path]:
    """Locate the packaged floorplan image."""
    candidates = [
        get_image("floorplan.png"),
        Path.cwd() / "src" / "resources" / "images" / "floorplan.png",
    ]
    for path in candidates:
        if path.exists():
            return path
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
