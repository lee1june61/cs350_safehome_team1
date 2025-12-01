"""
SafeHome Resources Package
--------------------------
Provides access helpers for bundled static assets (images, icons, etc.).

Structure:
- images/
  - floorplan.png
  - camera.png
  - sensor.png
"""
from pathlib import Path


def get_resources_path() -> Path:
    """Get the path to resources directory."""
    return Path(__file__).parent


def get_images_path() -> Path:
    """Get the path to resources/images directory."""
    return get_resources_path() / "images"


def get_image(name: str) -> Path:
    """Get path to a specific image file.
    
    Args:
        name: Image filename (e.g., 'floorplan.png')
    
    Returns:
        Path to the image file
    """
    return get_images_path() / name
