"""Control panel state model."""

from enum import Enum


class PanelState(Enum):
    """Control panel states following SDS state diagram."""

    SYSTEM_OFF = "off"
    BOOTING = "booting"
    READY = "ready"
    LOGGED_IN = "logged_in"
