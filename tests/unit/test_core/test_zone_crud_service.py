"""
Unit tests for ZoneCrudService focusing on validation and repo interactions.
"""

from unittest.mock import Mock

from src.core.services.zone.zone_crud import ZoneCrudService


class FakeRepo:
    def __init__(self):
        self.zones = []
        self.next_id = 1
        self.fail_add = False
        self.fail_update = False

    def add_zone(self, name, sensors):
        if self.fail_add:
            return None
        zone = {"id": self.next_id, "name": name, "sensors": sensors}
        self.next_id += 1
        self.zones.append(zone)
        return zone["id"]

    def update_zone(self, zone_id, name, sensors):
        if self.fail_update:
            return False
        for zone in self.zones:
            if zone["id"] == zone_id:
                if name:
                    zone["name"] = name
                if sensors is not None:
                    zone["sensors"] = sensors
                return True
        return False

    def delete_zone(self, zone_id):
        for zone in list(self.zones):
            if zone["id"] == zone_id:
                self.zones.remove(zone)
                return zone["name"]
        return None


class TestZoneCrudService:
    def _service(self):
        repo = FakeRepo()
        logger = Mock()
        refresh_calls = {"count": 0}

        def zone_list():
            return list(repo.zones)

        def refresh():
            refresh_calls["count"] += 1

        service = ZoneCrudService(repo, logger, zone_list, refresh)
        return service, repo, logger, refresh_calls

    def test_create_validates_name_and_sensors(self):
        service, repo, logger, refresh_calls = self._service()

        assert service.create("", [], None) == {
            "success": False,
            "message": "Select new safety zone and type safety zone name",
        }

        assert service.create("Zone A", [], None)["success"] is False

    def test_create_handles_duplicates_and_repo_failure(self):
        service, repo, logger, refresh_calls = self._service()
        repo.add_zone("Zone A", ["1"])
        result = service.create("Zone A ", ["1"], None)
        assert result == {"success": False, "message": "Same safety zone exists"}

        repo.fail_add = True
        result = service.create("Zone B", ["1"], None)
        assert result == {"success": False, "message": "Failed to create zone"}

    def test_create_success_logs_and_refreshes(self):
        service, repo, logger, refresh_calls = self._service()
        result = service.create(" Zone C ", ["1", "1", " 2 "], "admin")

        assert result["success"] is True
        assert refresh_calls["count"] >= 2  # before and after creation
        logger.add_event.assert_called_once()

    def test_update_validates_inputs(self):
        service, repo, logger, refresh_calls = self._service()
        assert service.update(1, "", None, None)["success"] is False
        assert service.update(1, None, [], None) == {
            "success": False,
            "message": "Select at least one sensor",
        }

    def test_update_duplicate_and_repo_failure(self):
        service, repo, logger, refresh_calls = self._service()
        repo.add_zone("Zone A", ["1"])
        repo.add_zone("Zone B", ["2"])

        assert service.update(2, "Zone A", None, None) == {
            "success": False,
            "message": "Same safety zone exists",
        }

        repo.fail_update = True
        assert service.update(2, "Zone C", None, None) == {
            "success": False,
            "message": "Zone not found",
        }

    def test_update_success_logs(self):
        service, repo, logger, refresh_calls = self._service()
        zone_id = repo.add_zone("Zone A", ["1"])

        result = service.update(zone_id, "Zone B", ["3"], "admin")

        assert result == {"success": True, "message": "Safety zone updated"}
        logger.add_event.assert_called_once()

    def test_delete_success_and_failure(self):
        service, repo, logger, refresh_calls = self._service()
        assert service.delete(1, None) == {"success": False, "message": "Zone not found"}

        zone_id = repo.add_zone("Zone A", ["1"])
        result = service.delete(zone_id, "admin")

        assert result == {"success": True, "message": "Safety zone deleted"}
        logger.add_event.assert_called_once()

