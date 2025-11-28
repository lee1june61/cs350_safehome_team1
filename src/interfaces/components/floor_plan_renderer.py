"""Floor plan rendering utilities."""
import tkinter as tk
from pathlib import Path
from typing import Optional, Set, Dict, TYPE_CHECKING
from .floor_plan_data import DEVICES, DEVICE_COLORS

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
        Path.cwd() / "src" / "resources" / "images" / "floorplan.png",
        Path.cwd() / "virtual_device_v4" / "floorplan.png",
    ]
    for p in candidates:
        if p.exists():
            return p
    return None


def draw_fallback(canvas: tk.Canvas, w: int, h: int):
    """Draw simple room layout if image unavailable."""
    canvas.create_rectangle(
        10, 10, w*0.42, h*0.45, fill='#fafafa', outline='#555', width=2)
    canvas.create_text(
        w*0.22, h*0.25, text='DR', font=('Arial', 16, 'italic'), fill='#888')
    canvas.create_rectangle(
        10, h*0.45, w*0.42, h-10, fill='#fafafa', outline='#555', width=2)
    canvas.create_text(
        w*0.22, h*0.72, text='KIT', font=('Arial', 16, 'italic'), fill='#888')
    canvas.create_rectangle(
        w*0.5, 10, w-10, h-10, fill='#fafafa', outline='#555', width=2)
    canvas.create_text(
        w*0.75, h*0.5, text='LR', font=('Arial', 16, 'italic'), fill='#888')
    canvas.create_rectangle(
        w*0.42, h*0.3, w*0.5, h*0.7, fill='#e8e8e8', outline='#777')


def load_image(canvas: tk.Canvas, w: int, h: int):
    """Load and display floor plan image. Returns PhotoImage or None."""
    img_path = find_image()
    if not HAS_PIL or not img_path:
        draw_fallback(canvas, w, h)
        return None

    try:
        img = Image.open(img_path)
        ratio = min(w / img.width, h / img.height)
        new_w, new_h = int(img.width * ratio), int(img.height * ratio)
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        x_off, y_off = (w - new_w) // 2, (h - new_h) // 2
        canvas.create_image(x_off, y_off, image=photo, anchor='nw')
        return photo
    except Exception:
        draw_fallback(canvas, w, h)
        return None


def draw_device(canvas: tk.Canvas, dev_id: str, x: int, y: int, dtype: str,
                armed: bool, selected: bool, click_handler):
    """Draw a single device icon."""
    r = 10
    fill = DEVICE_COLORS.get(dtype, '#666')

    if selected:
        outline, width = '#f39c12', 3
    elif armed:
        outline, width = '#27ae60', 3
    else:
        outline, width = '#333', 2

    tag = f'd_{dev_id}'
    canvas.create_oval(x-r, y-r, x+r, y+r, fill=fill, outline=outline,
                       width=width, tags=(tag, 'device', dtype))
    canvas.create_text(x, y+16, text=dev_id, font=('Arial', 9, 'bold'),
                       fill='#333', tags=(f'lbl_{dev_id}',))
    canvas.tag_bind(tag, '<Button-1>',
                    lambda e, d=dev_id, t=dtype: click_handler(d, t))

