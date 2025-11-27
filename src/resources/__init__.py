"""
SafeHome Resources Package

Contains static resources like images, icons, etc.

Structure:
- images/
  - floorplan.png   # House floor plan from virtual_device_v4
  - camera.png      # Camera icon
  - sensor.png      # Sensor icon
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
