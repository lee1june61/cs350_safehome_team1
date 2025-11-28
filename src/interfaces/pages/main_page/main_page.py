from ...components.page import Page
import tkinter as tk
from tkinter import ttk

class MainPage(Page):
    def __init__(self, parent, web_interface):
        super().__init__(parent, web_interface)

    def _build_ui(self):
        # Placeholder UI for MainPage
        ttk.Label(self._frame, text="Main Page - Under Construction", font=('Arial', 20)).pack(pady=20)
