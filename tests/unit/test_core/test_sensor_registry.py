"""
Unit tests for SensorRegistry covering initialization branches.
"""

from src.core.services.sensor.sensor_registry import SensorRegistry


class SensorWithMetadata:
    def __init__(self, internal_id, sensor_type, location):
        self.internal_id = internal_id
        self.sensor_type = sensor_type
        self.location = location
        self.metadata = {}
        self.is_armed = False

    def set_metadata(self, **kwargs):
        self.metadata = kwargs

    def arm(self):
        self.is_armed = True

    def disarm(self):
        self.is_armed = False


class SensorWithoutMetadata:
    def __init__(self, internal_id, sensor_type, location):
        self.internal_id = internal_id
        self.sensor_type = sensor_type
        self.location = location
        self.is_armed = True  # defaults to armed so disarm branch toggles it

    def arm(self):
        self.is_armed = True

    def disarm(self):
        self.is_armed = False


class StubSensorController:
    SENSOR_TYPE_WINDOW_DOOR = 1
    SENSOR_TYPE_MOTION = 2

    def __init__(self):
        self.nextSensorID = 1
        self._sensors = {}
        self.fail_next = False

    def queue_failure(self):
        self.fail_next = True

    def addSensor(self, x_coord, y_coord, sensor_type):
        if self.fail_next:
            self.fail_next = False
            return False
        sensor_cls = (
            SensorWithMetadata
            if sensor_type == self.SENSOR_TYPE_WINDOW_DOOR
            else SensorWithoutMetadata
        )
        internal_id = self.nextSensorID
        self.nextSensorID += 1
        self._sensors[internal_id] = sensor_cls(internal_id, sensor_type, [x_coord, y_coord])
        return True

    def getSensor(self, internal_id):
        return self._sensors.get(internal_id)


class TestSensorRegistry:
    def test_initialize_sets_metadata_and_arms(self):
        controller = StubSensorController()
        registry = SensorRegistry(controller)
        sensor_data = [
            {
                "id": "front",
                "type": "WINDOW",
                "name": "Front Door",
                "location": "Entry",
                "armed": True,
            }
        ]
        coords = {"front": (10, 20)}

        registry.initialize(sensor_data, coords)

        assert registry.lookup["front"] == 1
        sensor = controller.getSensor(1)
        assert sensor.is_armed is True
        assert sensor.metadata["friendly_id"] == "front"
        assert sensor.metadata["location_name"] == "Front Door"
        assert registry.instances and sensor in registry.instances

    def test_initialize_handles_missing_id_and_add_failure(self):
        controller = StubSensorController()
        registry = SensorRegistry(controller)
        controller.queue_failure()
        sensor_data = [
            {"type": "WINDOW", "name": "No Id"},
            {"id": "skip", "type": "WINDOW", "location": "Hall"},
            {"id": "motion", "type": "MOTION", "armed": False},
        ]
        coords = {"skip": (0, 0), "motion": (5, 5)}

        registry.initialize(sensor_data, coords)

        assert "skip" not in registry.lookup  # addSensor failure skipped entry
        sensor_id = registry.lookup["motion"]
        sensor = controller.getSensor(sensor_id)
        assert sensor.is_armed is False  # disarm branch executed
        assert getattr(sensor, "friendly_id") == "motion"  # fallback setattr branch

    def test_get_sensor_returns_none_when_unknown(self):
        controller = StubSensorController()
        registry = SensorRegistry(controller)

        assert registry.get_sensor("missing") is None

