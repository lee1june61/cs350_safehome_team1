"""
Unit tests for SensorStateService ensuring coverage of aggregation logic.
"""

from types import SimpleNamespace

from src.core.services.sensor.sensor_state import SensorStateService


class DummySensor:
    def __init__(self, sensor_id, status, location="Hallway"):
        self.sensor_id = sensor_id
        self._status = status
        self._location = location

    def get_status(self):
        return dict(self._status)

    def get_location(self):
        return self._location


class FakeRegistry:
    def __init__(self, sensors):
        self._sensors = sensors
        self.lookup = {sid: idx for idx, sid in enumerate(sorted(sensors))}

    def get_sensor(self, sensor_id):
        return self._sensors.get(sensor_id)


class TestSensorStateService:
    def _service(self):
        sensors = {
            "living": DummySensor(
                "living",
                {"type": "motion", "armed": True, "status": "active", "location": "LR"},
                location="LR",
            ),
            "front": DummySensor("front", {"armed": False, "status": "closed"}),
        }
        return SensorStateService(FakeRegistry(sensors))

    def test_collect_statuses_fills_missing_fields(self):
        service = self._service()
        statuses = service.collect_statuses()
        status_map = {item["id"]: item for item in statuses}

        assert status_map["front"]["name"] == "Hallway"  # fallback to get_location()
        assert status_map["front"]["status"] == "closed"
        assert status_map["living"]["name"] == "LR"
        assert status_map["living"]["status"] == "active"

    def test_devices_payload_merges_sensors_and_cameras(self):
        service = self._service()
        payload = service.devices_payload(
            camera_info=[
                {"id": 1, "enabled": True, "location": "Porch"},
                {"id": "camX", "enabled": False},
            ],
            camera_labels={1: "Front Door Cam"},
        )

        assert payload["front"]["type"] == "sensor"
        assert payload["front"]["armed"] is False
        assert payload["living"]["armed"] is True

        assert "C1" in payload
        assert payload["C1"]["type"] == "camera"
        assert payload["C1"]["location"] == "Front Door Cam"
        assert payload["camX"]["enabled"] is False


