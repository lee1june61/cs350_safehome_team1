"""Base screen class for all views."""

import tkinter as tk
from abc import ABC, abstractmethod
from typing import Optional


class BaseScreen(ABC):
    """Abstract base class for all screen views.

    Following the Page class hierarchy from SDS document.
    """

    def __init__(self, parent: tk.Widget):
        """Initialize base screen.

        Args:
            parent: Parent widget
        """
        self.parent = parent
        self.frame: Optional[tk.Frame] = None

    @abstractmethod
    def build(self) -> tk.Frame:
        """Build and return the screen frame.

        Returns:
            Frame containing the screen UI
        """
        pass

    def show(self):
        """Show this screen."""
        if self.frame is None:
            self.frame = self.build()
        self.frame.pack(fill=tk.BOTH, expand=True)

    def hide(self):
        """Hide this screen."""
        if self.frame:
            self.frame.pack_forget()

    def destroy(self):
        """Destroy this screen."""
        if self.frame:
            self.frame.destroy()
            self.frame = None
