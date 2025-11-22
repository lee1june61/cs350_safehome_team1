from abc import ABC, abstractmethod


class DeviceSensorTester(ABC):
    """센서 디바이스 테스터의 추상 기본 클래스"""
    
    safeHomeSensorTest = None
    safehome_sensor_test = None  # alias for compatibility
    head_WinDoorSensor = None
    head_windoor_sensor = None  # alias
    head_MotionDetector = None
    head_motion_detector = None  # alias
    newIdSequence_WinDoorSensor = 0
    newIdSequence_MotionDetector = 0
    
    def __init__(self):
        self.next = None
        self.next_sensor = None  # alias
        self.sensor_id = 0  # alias
    
    @abstractmethod
    def intrude(self):
        """침입/감지를 시뮬레이션합니다."""
        pass
    
    @abstractmethod
    def release(self):
        """침입/감지 상태를 해제합니다."""
        pass
    
    @staticmethod
    def showSensorTester():
        """센서 테스터 GUI를 표시합니다."""
        if DeviceSensorTester.safeHomeSensorTest is not None:
            return
        try:
            import os
            if os.environ.get("SAFEHOME_HEADLESS") == "1":
                return
            import tkinter as tk
            from .safehome_sensor_test_gui import SafeHomeSensorTest
            root = tk._default_root
            if root is None:
                root = tk.Tk()
                root.withdraw()
            gui = SafeHomeSensorTest(master=root)
            # Java의 setVisible(true) 동작 미러링
            try:
                gui.deiconify()
                gui.lift()
            except Exception:
                pass
            DeviceSensorTester.safeHomeSensorTest = gui
            DeviceSensorTester.safehome_sensor_test = gui
        except Exception:
            # 디스플레이/Tkinter가 없는 환경에서는 조용히 실패
            DeviceSensorTester.safeHomeSensorTest = None
            DeviceSensorTester.safehome_sensor_test = None

