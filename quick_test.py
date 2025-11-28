import os
os.environ["SAFEHOME_HEADLESS"] = "1"

# Test 1: src.devices에서 import
print("Test 1: src.devices import")
from src.devices import Sensor, WindowDoorSensor, MotionSensor, SensorController
from src.devices import DeviceSensorTester, DeviceWinDoorSensor, DeviceMotionDetector, Alarm
print("OK - All imports from src.devices successful")

# Test 2: 직접 경로로 import
print("\nTest 2: Direct path import")
from src.devices.sensors.sensor import Sensor as S
from src.devices.sensors.sensor_controller import SensorController as SC
print("OK - Direct path imports successful")

# Test 3: 기본 기능
print("\nTest 3: Basic functionality")
controller = SensorController()
controller.addSensor(100, 200, 1)
info = controller.getAllSensorsInfo()
print(f"OK - Created controller with {len(info)} sensor(s)")

# Test 4: Device 생성
print("\nTest 4: Device creation")
device = DeviceWinDoorSensor()
print(f"OK - Device created with ID: {device.get_id()}")

print("\n=== ALL TESTS PASSED ===")


