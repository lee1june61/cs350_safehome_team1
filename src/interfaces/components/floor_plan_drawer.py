"""
Drawing utility for the FloorPlan component.
"""
import tkinter as tk
from .floor_plan_definitions import DEVICES

def draw_fallback(canvas: tk.Canvas, width: int, height: int):
    """Draw simple room layout if image unavailable."""
    # DR room (top-left quadrant)
    canvas.create_rectangle(10, 10, width*0.42, height*0.45, fill='#fafafa', outline='#555', width=2)
    canvas.create_text(width*0.22, height*0.25, text='DR', font=('Arial', 16, 'italic'), fill='#888')
    # KIT room (bottom-left)
    canvas.create_rectangle(10, height*0.45, width*0.42, height-10, fill='#fafafa', outline='#555', width=2)
    canvas.create_text(width*0.22, height*0.72, text='KIT', font=('Arial', 16, 'italic'), fill='#888')
    # LR room (right side)
    canvas.create_rectangle(width*0.5, 10, width-10, height-10, fill='#fafafa', outline='#555', width=2)
    canvas.create_text(width*0.75, height*0.5, text='LR', font=('Arial', 16, 'italic'), fill='#888')
    # Hallway (center)
    canvas.create_rectangle(width*0.42, height*0.3, width*0.5, height*0.7, fill='#e8e8e8', outline='#777')

def draw_devices(
    canvas: tk.Canvas,
    width: int,
    height: int,
    states: dict,
    selected: set,
    show_cameras: bool,
    show_sensors: bool,
    handle_click: callable
):
    """Draw device icons at calculated positions."""
    colors = {'camera': '#9b59b6', 'sensor': '#e74c3c', 'motion': '#3498db'}
    
    for dev_id, (nx, ny, dtype) in DEVICES.items():
        if (dtype == 'camera' and not show_cameras) or \
           (dtype in ('sensor', 'motion') and not show_sensors):
            continue
        
        x, y, r = int(nx * width), int(ny * height), 10
        
        armed = states.get(dev_id, False)
        is_selected = dev_id in selected
        
        if is_selected:
            outline, outline_width = '#f39c12', 3  # Orange
        elif armed:
            outline, outline_width = '#27ae60', 3  # Green
        else:
            outline, outline_width = '#333', 2
        
        tag = f'd_{dev_id}'
        canvas.create_oval(x-r, y-r, x+r, y+r, fill=colors.get(dtype, '#666'),
                              outline=outline, width=outline_width, tags=(tag, 'device', dtype))
        canvas.create_text(x, y+16, text=dev_id, font=('Arial', 9, 'bold'),
                              fill='#333', tags=(f'lbl_{dev_id}',))
        canvas.tag_bind(tag, '<Button-1>', lambda e, d=dev_id, t=dtype: handle_click(d, t))
