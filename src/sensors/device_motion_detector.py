from .device_sensor_tester import DeviceSensorTester
from .interface_sensor import InterfaceSensor


class DeviceMotionDetector(DeviceSensorTester, InterfaceSensor):
    """모션 감지 센서 디바이스 클래스"""
    
    def __init__(self):
        super().__init__()
        
        # 고유 ID 할당
        DeviceSensorTester.newIdSequence_MotionDetector += 1
        self.sensor_id = DeviceSensorTester.newIdSequence_MotionDetector
        
        # 상태 초기화
        self.detected = False
        self.armed = False
        
        # 연결 리스트에 추가
        self.next = DeviceSensorTester.head_MotionDetector
        self.next_sensor = self.next  # alias
        DeviceSensorTester.head_MotionDetector = self
        DeviceSensorTester.head_motion_detector = self  # alias
        
        # GUI 업데이트 및 헤드 연결
        if DeviceSensorTester.safeHomeSensorTest is not None:
            DeviceSensorTester.safeHomeSensorTest.head_motion = DeviceSensorTester.head_MotionDetector
            DeviceSensorTester.safeHomeSensorTest.rangeSensorID_MotionDetector.set(
                f"1 ~ {DeviceSensorTester.newIdSequence_MotionDetector}")
    
    def intrude(self):
        """모션 감지를 시뮬레이션합니다."""
        self.detected = True
    
    def release(self):
        """모션 감지를 해제합니다."""
        self.detected = False

    def get_id(self):
        """센서 ID를 반환합니다."""
        return self.sensor_id
    
    def read(self):
        """센서 상태를 읽습니다."""
        if self.armed:
            return self.detected
        return False
    
    def arm(self):
        """센서를 활성화합니다."""
        self.armed = True
    
    def disarm(self):
        """센서를 비활성화합니다."""
        self.armed = False
    
    def test_armed_state(self):
        """센서의 활성화 상태를 확인합니다."""
        return self.armed




