"""Log table widget for view log page."""
from tkinter import ttk
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .view_log_page import ViewLogPage


class LogTable:
    """Treeview-based log display table."""

    COLUMNS = ("timestamp", "event", "detail")
    HEADINGS = {"timestamp": "Date/Time", "event": "Event Type", "detail": "Details"}
    WIDTHS = {"timestamp": 150, "event": 120, "detail": 350}
    ANCHORS = {"timestamp": "center", "event": "center", "detail": "w"}

    def __init__(self, parent, page: "ViewLogPage"):
        self._page = page
        self._tree = ttk.Treeview(parent, columns=self.COLUMNS, show="headings", height=15)
        self._setup_columns()
        self._setup_scrollbar(parent)
        self._setup_tags()

    def _setup_columns(self):
        for col in self.COLUMNS:
            self._tree.heading(col, text=self.HEADINGS[col])
            self._tree.column(col, width=self.WIDTHS[col], anchor=self.ANCHORS[col])

    def _setup_scrollbar(self, parent):
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)
        self._tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _setup_tags(self):
        self._tree.tag_configure("alert", foreground="red")
        self._tree.tag_configure("armed", foreground="green")
        self._tree.tag_configure("disarmed", foreground="gray")

    def clear(self):
        for item in self._tree.get_children():
            self._tree.delete(item)

    def load(self, logs: List[dict]):
        self.clear()
        for log in logs:
            event = log.get("event", "-")
            tag = self._get_tag(event)
            self._tree.insert("", "end", values=(
                log.get("timestamp", "-"),
                event,
                log.get("detail", "-")
            ), tags=(tag,))

    def _get_tag(self, event: str) -> str:
        if event in ("INTRUSION", "PANIC"):
            return "alert"
        elif event in ("ARM", "ARM_ZONE"):
            return "armed"
        elif event in ("DISARM", "DISARM_ZONE"):
            return "disarmed"
        return "normal"




