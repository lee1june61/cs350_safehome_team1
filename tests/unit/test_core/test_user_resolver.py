"""
Unit tests for ControlPanelUserResolver to exercise branch coverage.
"""

from dataclasses import dataclass
from typing import Dict, Tuple

import pytest

from src.configuration.password_utils import hash_password
from src.core.services.auth.user_resolver import ControlPanelUserResolver


@dataclass
class StubStorage:
    records: Dict[Tuple[str, str], Dict]

    def get_login_interface(self, username, interface):
        return self.records.get((username, interface))


def build_storage(master_locked: bool = False):
    records = {
        ("master", "control_panel"): {
            "password_hash": hash_password("1111"),
            "is_locked": master_locked,
        },
        ("guest", "control_panel"): {
            "password_hash": hash_password("2222"),
            "is_locked": False,
        },
    }
    return StubStorage(records)


class TestControlPanelUserResolver:
    def test_returns_explicit_username_when_provided(self):
        resolver = ControlPanelUserResolver(build_storage())

        assert resolver.resolve("operator", "any") == ["operator"]

    def test_password_matching_master_and_guest(self):
        resolver = ControlPanelUserResolver(build_storage())

        assert resolver.resolve("", "1111") == ["master"]
        assert resolver.resolve("", "2222") == ["guest"]

    def test_locked_master_falls_back_to_guest_only(self):
        resolver = ControlPanelUserResolver(build_storage(master_locked=True))

        # master is locked, so only guest should match
        assert resolver.resolve("", "2222") == ["guest"]
        # locked master causes no matches -> defaults to master identifier
        assert resolver.resolve("", "1111") == ["master"]

    def test_missing_password_defaults_to_master(self):
        resolver = ControlPanelUserResolver(build_storage())

        assert resolver.resolve("", "") == ["master"]



