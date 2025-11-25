"""Geometry utility functions."""


def point_in_rect(px: int, py: int, x: int, y: int, size: int) -> bool:
    """Check if point is inside rectangle.

    Args:
        px, py: Point coordinates
        x, y: Rectangle center coordinates
        size: Rectangle size (half-width)

    Returns:
        True if point is inside rectangle
    """
    return x - size <= px <= x + size and y - size <= py <= y + size


def point_in_circle(px: int, py: int, cx: int, cy: int, radius: int) -> bool:
    """Check if point is inside circle.

    Args:
        px, py: Point coordinates
        cx, cy: Circle center coordinates
        radius: Circle radius

    Returns:
        True if point is inside circle
    """
    return (px - cx) ** 2 + (py - cy) ** 2 <= radius**2
