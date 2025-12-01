"""SecurityPage - Security menu with identity verification (SRS V.2)"""
import tkinter as tk
from tkinter import ttk
from ...components.page import Page
from .security_actions import create_security_actions
from .identity_verification import IdentityVerificationController


class SecurityPage(Page):
    """Security functions - requires phone/address verification first."""

    def _build_ui(self):
        self._create_header("Security Function", back_page="major_function")
        self._verifier = None

        # Verification frame
        vf = ttk.LabelFrame(self._frame, text="Identity Confirmation", padding=10)
        vf.pack(fill="x", padx=30, pady=10)

        ttk.Label(vf, text="Monitoring Phone:").pack(side="left")
        entry_var = tk.StringVar()
        entry = ttk.Entry(vf, textvariable=entry_var, width=30)
        entry.pack(side="left", padx=5)
        verify_btn = ttk.Button(vf, text="Verify")
        verify_btn.pack(side="left")
        status = ttk.Label(vf, text="")
        status.pack(side="left", padx=10)

        action_buttons = create_security_actions(self._frame, self.navigate_to)
        self._verifier = IdentityVerificationController(
            page=self,
            entry_var=entry_var,
            entry=entry,
            status_label=status,
            verify_button=verify_btn,
            action_buttons=action_buttons,
        )

    def on_show(self):
        """Check if identity has already been verified in this session."""
        if self._verifier:
            self._verifier.on_show()
