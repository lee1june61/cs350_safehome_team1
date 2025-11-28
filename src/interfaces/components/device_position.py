"""
DevicePosition - Position and size data for device icons

Single Responsibility: Store position/size information.
"""
from dataclasses import dataclass


@dataclass
class DevicePosition:
    """Position and size information for a device icon"""
    x: int
    y: int
    width: int = 30
    height: int = 30
    
    def contains(self, px: int, py: int) -> bool:
        """Check if point is within this position's bounds"""
        half_w = self.width // 2
        half_h = self.height // 2
        return (self.x - half_w <= px <= self.x + half_w and
                self.y - half_h <= py <= self.y + half_h)
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'x': self.x, 'y': self.y,
            'width': self.width, 'height': self.height
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'DevicePosition':
        """Create from dictionary"""
        return cls(
            x=data.get('x', 0),
            y=data.get('y', 0),
            width=data.get('width', 30),
            height=data.get('height', 30)
        )
