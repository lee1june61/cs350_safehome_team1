"""
DeviceRenderer - Rendering logic for device icons

Single Responsibility: Draw device icons on canvas.
"""
import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .device_icon import DeviceIcon


class DeviceRenderer:
    """Handles rendering of device icons on canvas"""
    
    @staticmethod
    def draw(icon: 'DeviceIcon', canvas: tk.Canvas) -> None:
        """Draw device icon on canvas"""
        tag = f'device_{icon.device_id}'
        canvas.delete(tag)
        
        pos = icon.position
        x, y = pos.x, pos.y
        w, h = pos.width, pos.height
        color = icon.get_color()
        line_width = 2 if icon.is_active else 1
        
        # Draw shape based on type
        if icon.device_type in ['CAMERA', 'ALARM']:
            DeviceRenderer._draw_circle(
                canvas, x, y, w, h, color, line_width, tag
            )
        else:
            DeviceRenderer._draw_rectangle(
                canvas, x, y, w, h, color, line_width, tag
            )
        
        # Draw symbol
        canvas.create_text(
            x, y, text=icon.get_symbol(),
            fill='white', font=('Arial', 10, 'bold'), tags=tag
        )
    
    @staticmethod
    def _draw_circle(canvas: tk.Canvas, x: int, y: int, 
                     w: int, h: int, color: str, 
                     line_width: int, tag: str) -> None:
        """Draw circular icon"""
        canvas.create_oval(
            x - w//2, y - h//2, x + w//2, y + h//2,
            fill=color, outline='black', width=line_width, tags=tag
        )
    
    @staticmethod
    def _draw_rectangle(canvas: tk.Canvas, x: int, y: int,
                        w: int, h: int, color: str,
                        line_width: int, tag: str) -> None:
        """Draw rectangular icon"""
        canvas.create_rectangle(
            x - w//2, y - h//2, x + w//2, y + h//2,
            fill=color, outline='black', width=line_width, tags=tag
        )
    
    @staticmethod
    def bind_click(icon: 'DeviceIcon', canvas: tk.Canvas, 
                   callback) -> None:
        """Bind click event to icon"""
        tag = f'device_{icon.device_id}'
        canvas.tag_bind(tag, '<Button-1>', lambda e: callback(icon))
