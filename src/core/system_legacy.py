"""Legacy helper mixin retained for backward compatibility tests."""

from __future__ import annotations

from .legacy.sensor_mixin import LegacySensorMixin
from .legacy.auth_mixin import LegacyAuthMixin
from .legacy.messaging_mixin import LegacyMessagingMixin
from .legacy.mode_mixin import LegacyModeMixin


class SystemLegacyMixin(
    LegacySensorMixin, LegacyAuthMixin, LegacyMessagingMixin, LegacyModeMixin
):
    """Combines all legacy APIs required by legacy/unit tests."""

    pass
