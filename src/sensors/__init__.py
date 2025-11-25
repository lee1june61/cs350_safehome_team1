"""센서 패키지"""

import sys
import os

# virtual_device_v3의 device 모듈을 import할 수 있도록 경로 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..', '..', '..')
virtual_device_path = os.path.join(project_root, 'virtual_device_v3', 'virtual_device_v3')
if virtual_device_path not in sys.path:
    sys.path.insert(0, virtual_device_path)

# 자체 구현 클래스들
from .sensor import Sensor
from .window_door_sensor import WindowDoorSensor
from .motion_sensor import MotionSensor
from .sensor_controller import SensorController

# virtual_device_v3에서 제공하는 디바이스 클래스들 import
try:
    from device.interface_sensor import InterfaceSensor
    from device.device_sensor_tester import DeviceSensorTester
    from device.device_windoor_sensor import DeviceWinDoorSensor
    from device.device_motion_detector import DeviceMotionDetector
except ImportError:
    # virtual_device를 찾을 수 없는 경우 자체 구현 사용
    from .interface_sensor import InterfaceSensor
    from .device_sensor_tester import DeviceSensorTester
    from .device_windoor_sensor import DeviceWinDoorSensor
    from .device_motion_detector import DeviceMotionDetector

__all__ = [
    'InterfaceSensor',
    'Sensor',
    'WindowDoorSensor',
    'MotionSensor',
    'SensorController',
    'DeviceSensorTester',
    'DeviceWinDoorSensor',
    'DeviceMotionDetector',
]
