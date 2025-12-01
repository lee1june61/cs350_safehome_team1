"""Shared camera lock state helpers."""

from __future__ import annotations

from typing import Dict

_locked: Dict[str, bool] = {}


def is_locked(camera_id: str) -> bool:
    """Return True if the given camera is currently locked."""
    return _locked.get(camera_id, False)


def lock_camera(camera_id: str) -> None:
    """Mark a camera as locked."""
    _locked[camera_id] = True


def unlock_camera(camera_id: str) -> None:
    """Mark a camera as unlocked."""
    _locked[camera_id] = False



