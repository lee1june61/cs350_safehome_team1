"""Shared UI helpers for the interfaces package."""

from typing import Iterable, Optional, Set

DOOR_SENSOR_IDS: Set[str] = {"S2", "S5"}

_TYPE_LABEL_MAP = {
    "WINDOW": "W",
    "SENSOR": "W",
    "MOTION": "M",
    "MOTION_SENSOR": "M",
    "DOOR": "D",
    "DOOR_SENSOR": "D",
    "CAMERA": "C",
}


def sensor_type_letter(sensor_id: str, sensor_type: Optional[str] = None) -> str:
    """Return the single-letter shorthand for a sensor."""
    if sensor_type:
        letter = _TYPE_LABEL_MAP.get(sensor_type.upper())
        if letter:
            return letter

    sid = (sensor_id or "").upper()
    if not sid:
        return "?"

    if sid.startswith("M"):
        return "M"
    if sid.startswith("C"):
        return "C"
    if sid in DOOR_SENSOR_IDS:
        return "D"
    if sid.startswith("S"):
        return "W"
    return sid[:1]


def sensor_display_name(sensor_id: str, sensor_type: Optional[str] = None) -> str:
    """Combine sensor ID with its type letter, e.g., 'S1 (W)'."""
    letter = sensor_type_letter(sensor_id, sensor_type)
    return f"{sensor_id} ({letter})" if sensor_id else letter


def format_sensor_labels(sensor_ids: Iterable[str]) -> str:
    """Return a comma-separated display string for a collection of sensor IDs."""
    labels = [sensor_display_name(sid) for sid in sensor_ids]
    return ", ".join(labels)
