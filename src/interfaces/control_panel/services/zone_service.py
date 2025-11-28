"""Safety zone management service."""

from typing import List, Dict, Set


class ZoneService:
    """Service for managing safety zones.

    Following the SafetyZone class from SDS document.
    """

    def __init__(self, system):
        """Initialize zone service.

        Args:
            system: SafeHome system instance
        """
        self.system = system

    def create_zone(self, name: str, sensor_ids: List[int]) -> int:
        """Create a new safety zone.

        Args:
            name: Zone name
            sensor_ids: List of sensor IDs

        Returns:
            Zone ID

        Raises:
            ValueError: If zone creation fails
        """
        if not name or not name.strip():
            raise ValueError("Zone name cannot be empty")

        if not sensor_ids:
            raise ValueError("Zone must have at least one sensor")

        zone_id = self.system.create_safety_zone(name, sensor_ids)
        return zone_id

    def delete_zone(self, zone_id: int) -> bool:
        """Delete a safety zone.

        Args:
            zone_id: Zone ID to delete

        Returns:
            True if successful
        """
        return self.system.delete_safety_zone(zone_id)

    def update_zone(
        self, zone_id: int, name: str = None, sensor_ids: List[int] = None
    ) -> bool:
        """Update a safety zone.

        Args:
            zone_id: Zone ID
            name: New zone name (optional)
            sensor_ids: New sensor IDs (optional)

        Returns:
            True if successful
        """
        return self.system.update_safety_zone(zone_id, name, sensor_ids)

    def get_all_zones(self) -> List[Dict]:
        """Get all safety zones.

        Returns:
            List of zone dictionaries
        """
        return self.system.get_safety_zones()

    def arm_zone(self, zone_id: int) -> bool:
        """Arm a safety zone.

        Args:
            zone_id: Zone ID

        Returns:
            True if successful
        """
        return self.system.arm_safety_zone(zone_id)

    def disarm_zone(self, zone_id: int) -> bool:
        """Disarm a safety zone.

        Args:
            zone_id: Zone ID

        Returns:
            True if successful
        """
        return self.system.disarm_safety_zone(zone_id)
