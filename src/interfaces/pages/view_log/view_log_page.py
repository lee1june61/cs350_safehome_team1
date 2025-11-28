"""ViewLogPage - View intrusion logs (SRS V.2.j)."""
from tkinter import ttk
from ...components.page import Page
from .log_table import LogTable


class ViewLogPage(Page):
    """View intrusion and security event log."""

    def _build_ui(self):
        self._create_header("Security Event Log", back_page="security")

        main = ttk.Frame(self._frame)
        main.pack(fill="both", expand=True, padx=20, pady=10)

        log_frame = ttk.LabelFrame(main, text="Event Log", padding=10)
        log_frame.pack(fill="both", expand=True)

        self._table = LogTable(log_frame, self)

        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill="x", pady=10)
        ttk.Button(btn_frame, text="Refresh", command=self._load, width=12).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear Log", command=self._clear, width=12).pack(side="left", padx=5)

        self._status = ttk.Label(main, text="", font=("Arial", 9))
        self._status.pack()

    def _load(self):
        res = self.send_to_system("get_intrusion_log")
        if res.get("success"):
            logs = res.get("data", [])
            self._table.load(logs)
            self._status.config(text=f"Showing {len(logs)} entries")
        else:
            self._status.config(text="Failed to load log")

    def _clear(self):
        self._table.clear()
        self._status.config(text="Log cleared from display")

    def on_show(self):
        self._load()

