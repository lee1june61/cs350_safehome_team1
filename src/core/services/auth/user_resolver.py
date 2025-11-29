"""Control panel user resolution helpers."""

from __future__ import annotations

from typing import List, Sequence

from src.configuration import StorageManager
from src.configuration.password_utils import hash_password


class ControlPanelUserResolver:
    """Figures out which control-panel user a PIN should map to."""

    def __init__(self, storage: StorageManager):
        self._storage = storage

    def resolve(self, username: str, password: str) -> List[str]:
        if username and username not in {"master", ""}:
            return [username]
        matches = self._match_password_candidates(password, ["master", "guest"])
        if matches:
            return matches
        return [username or "master"]

    def _match_password_candidates(
        self, password: str, usernames: Sequence[str]
    ) -> List[str]:
        if not password or not self._storage:
            return []
        hashed = hash_password(password)
        matches: List[str] = []
        for candidate in usernames:
            record = self._storage.get_login_interface(candidate, "control_panel")
            if (
                record
                and not record.get("is_locked")
                and record.get("password_hash") == hashed
            ):
                matches.append(candidate)
        return matches


