from abc import ABC, abstractmethod


class InterfaceSensor(ABC):
    """센서의 추상 인터페이스 클래스"""

    @abstractmethod
    def get_id(self):
        """센서 ID를 반환합니다."""
        raise NotImplementedError

    @abstractmethod
    def read(self):
        """센서 상태를 읽습니다."""
        raise NotImplementedError

    @abstractmethod
    def arm(self):
        """센서를 활성화합니다."""
        raise NotImplementedError

    @abstractmethod
    def disarm(self):
        """센서를 비활성화합니다."""
        raise NotImplementedError

    @abstractmethod
    def test_armed_state(self):
        """센서의 활성화 상태를 확인합니다."""
        raise NotImplementedError




