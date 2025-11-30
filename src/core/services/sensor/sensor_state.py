"""Sensor state aggregation helpers."""

from __future__ import annotations

from typing import Any, Dict, List

from .sensor_registry import SensorRegistry


class SensorStateService:
    """Produces sensor summaries for UI consumption."""

    def __init__(self, registry: SensorRegistry):
        self._registry = registry

    def collect_statuses(self) -> List[Dict[str, Any]]:
        statuses: List[Dict[str, Any]] = []
        for sensor_id in sorted(self._registry.lookup.keys()):
            sensor = self._registry.get_sensor(sensor_id)
            if not sensor:
                continue
            status = sensor.get_status()
            status.setdefault("id", sensor_id)
            if "name" not in status:
                try:
                    status["name"] = sensor.get_location()
                except Exception:  # pragma: no cover
                    status["name"] = sensor_id
            statuses.append(status)
        return statuses

    def devices_payload(
        self,
        camera_info: List[Dict[str, Any]],
        camera_labels: Dict[int, str],
    ) -> Dict[str, Dict[str, Any]]:
        devices: Dict[str, Dict[str, Any]] = {}
        for status in self.collect_statuses():
            dev_id = status.get("id", "Unknown")
            devices[dev_id] = {
                "type": status.get("type", "sensor"),
                "armed": status.get("armed", False),
                "location": status.get("location", "Unknown"),
                "status": status.get("status", "closed"),
                "name": status.get("name", dev_id),
            }

        for cam in camera_info:
            cam_id = cam.get("id", "Unknown")
            dev_id = str(cam_id)
            if isinstance(cam_id, int):
                dev_id = f"C{cam_id}"
            location = camera_labels.get(cam_id, cam.get("location", "Unknown"))
            devices[dev_id] = {
                "type": "camera",
                "armed": cam.get("enabled", False),
                "location": location,
                "enabled": cam.get("enabled", False),
            }
        return devices


