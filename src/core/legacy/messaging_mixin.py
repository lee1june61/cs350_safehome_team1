"""Legacy messaging methods for backward compatibility."""

from __future__ import annotations


class LegacyMessagingMixin:
    """Provides legacy messaging APIs required by older unit tests."""

    def init_system(self) -> bool:
        if self.config_manager is None:
            self.config_manager = self._config_manager
        if self.login_manager is None:
            self.login_manager = self._login_manager
        self.sensor_controller = self.sensor_service._controller
        self.camera_controller = self.camera_service._controller
        return True

    def process_message(self, stream) -> bool:
        if not hasattr(stream, "read"):
            return False
        message = stream.read()
        return bool(message)

    def receive_message(self):
        message = self._read_from_interface()
        if message:
            self.message_buffer.append(message)
        return message

    def send_message(self, response_data, target_interface) -> bool:
        return bool(self._write_to_interface(response_data, target_interface))

    def _read_from_interface(self):
        return None

    def _write_to_interface(self, response_data, target_interface):
        return False

