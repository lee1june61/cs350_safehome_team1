"""Resource loading service."""

from pathlib import Path
from typing import Optional, Tuple

try:
    from PIL import Image, ImageTk

    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    Image = None
    ImageTk = None


class ResourceLoader:
    """Service for loading external resources like floor plans."""

    def __init__(self, resources_path: Optional[Path] = None):
        """Initialize resource loader.

        Args:
            resources_path: Path to resources directory
        """
        if resources_path is None:
            # Default path relative to this file
            base = Path(__file__).parent.parent.parent.parent / "resources"
            self.resources_path = base / "images"
        else:
            self.resources_path = resources_path

    def load_floor_plan(
        self, target_width: int = 650
    ) -> Tuple[Optional[object], Optional[object]]:
        """Load and resize floor plan image.

        Args:
            target_width: Target width for resized image

        Returns:
            Tuple of (PIL Image, ImageTk PhotoImage) or (None, None) if failed
        """
        if not HAS_PIL:
            print("Warning: PIL not available, floor plan cannot be loaded")
            return None, None

        try:
            floor_path = self.resources_path / "floorplan.png"
            if not floor_path.exists():
                print(f"Warning: Floor plan not found at {floor_path}")
                return None, None

            # Load and resize
            image = Image.open(floor_path)
            original_width, original_height = image.size
            target_height = int(original_height * (target_width / original_width))
            image = image.resize(
                (target_width, target_height), Image.Resampling.LANCZOS
            )
            photo = ImageTk.PhotoImage(image)

            print(f"✓ Floor plan loaded: {target_width}x{target_height}")
            return image, photo

        except Exception as e:
            print(f"Warning: Could not load floor plan: {e}")
            return None, None
