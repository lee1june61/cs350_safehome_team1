"""
Import 테스트 스크립트
sensor 폴더가 src/devices/sensors로 이동한 후 import 확인
"""

import sys
import os

# UTF-8 인코딩 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

os.environ["SAFEHOME_HEADLESS"] = "1"  # GUI 비활성화

print("=" * 70)
print("센서 Import 테스트")
print("=" * 70)

# 1. src.devices에서 센서 클래스 import 테스트
print("\n[1단계] src.devices에서 센서 클래스 import")
print("-" * 70)

try:
    from src.devices import Sensor
    print("✓ Sensor import 성공")
except ImportError as e:
    print(f"✗ Sensor import 실패: {e}")
    sys.exit(1)

try:
    from src.devices import WindowDoorSensor
    print("✓ WindowDoorSensor import 성공")
except ImportError as e:
    print(f"✗ WindowDoorSensor import 실패: {e}")
    sys.exit(1)

try:
    from src.devices import MotionSensor
    print("✓ MotionSensor import 성공")
except ImportError as e:
    print(f"✗ MotionSensor import 실패: {e}")
    sys.exit(1)

try:
    from src.devices import SensorController
    print("✓ SensorController import 성공")
except ImportError as e:
    print(f"✗ SensorController import 실패: {e}")
    sys.exit(1)

try:
    from src.devices import DeviceSensorTester
    print("✓ DeviceSensorTester import 성공")
except ImportError as e:
    print(f"✗ DeviceSensorTester import 실패: {e}")
    sys.exit(1)

try:
    from src.devices import DeviceWinDoorSensor
    print("✓ DeviceWinDoorSensor import 성공")
except ImportError as e:
    print(f"✗ DeviceWinDoorSensor import 실패: {e}")
    sys.exit(1)

try:
    from src.devices import DeviceMotionDetector
    print("✓ DeviceMotionDetector import 성공")
except ImportError as e:
    print(f"✗ DeviceMotionDetector import 실패: {e}")
    sys.exit(1)

try:
    from src.devices import Alarm
    print("✓ Alarm import 성공")
except ImportError as e:
    print(f"✗ Alarm import 실패: {e}")
    sys.exit(1)

# 2. 직접 경로로 import 테스트
print("\n[2단계] 직접 경로로 센서 클래스 import")
print("-" * 70)

try:
    from src.devices.sensors import Sensor as Sensor2
    print("✓ src.devices.sensors.Sensor import 성공")
except ImportError as e:
    print(f"✗ import 실패: {e}")
    sys.exit(1)

try:
    from src.devices.sensors.sensor_controller import SensorController as SC
    print("✓ src.devices.sensors.sensor_controller.SensorController import 성공")
except ImportError as e:
    print(f"✗ import 실패: {e}")
    sys.exit(1)

try:
    from src.devices.sensors.window_door_sensor import WindowDoorSensor as WDS
    print("✓ src.devices.sensors.window_door_sensor.WindowDoorSensor import 성공")
except ImportError as e:
    print(f"✗ import 실패: {e}")
    sys.exit(1)

try:
    from src.devices.sensors.motion_sensor import MotionSensor as MS
    print("✓ src.devices.sensors.motion_sensor.MotionSensor import 성공")
except ImportError as e:
    print(f"✗ import 실패: {e}")
    sys.exit(1)

# 3. 기본 기능 테스트
print("\n[3단계] 기본 기능 테스트")
print("-" * 70)

try:
    controller = SensorController()
    print(f"✓ SensorController 생성 성공")
    
    # 센서 추가
    controller.addSensor(100, 200, 1)  # WindowDoorSensor
    controller.addSensor(300, 400, 2)  # MotionSensor
    print(f"✓ 센서 추가 성공")
    
    # 센서 정보 확인
    info = controller.getAllSensorsInfo()
    print(f"✓ 센서 정보 조회 성공: {len(info)}개 센서")
    
    # 센서 활성화
    controller.armSensor(1)
    print(f"✓ 센서 활성화 성공")
    
except Exception as e:
    print(f"✗ 기능 테스트 실패: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 4. Device 클래스 테스트
print("\n[4단계] Device 클래스 기능 테스트")
print("-" * 70)

try:
    device = DeviceWinDoorSensor()
    print(f"✓ DeviceWinDoorSensor 생성 성공 (ID: {device.get_id()})")
    
    device.arm()
    print(f"✓ Device arm 성공 (armed: {device.test_armed_state()})")
    
    device.intrude()
    result = device.read()
    print(f"✓ Device intrude/read 성공 (result: {result})")
    
except Exception as e:
    print(f"✗ Device 테스트 실패: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 5. 센서-디바이스 연동 테스트
print("\n[5단계] 센서-디바이스 연동 테스트")
print("-" * 70)

try:
    sensor = WindowDoorSensor(10, 1, [500, 600])
    device = DeviceWinDoorSensor()
    
    sensor.arm()
    sensor.setDevice(device)
    print(f"✓ 센서와 디바이스 연결 성공")
    
    device.arm()
    device.intrude()
    result = sensor.read()
    print(f"✓ 연동 테스트 성공 (result: {result})")
    
except Exception as e:
    print(f"✗ 연동 테스트 실패: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ 모든 import 테스트 통과!")
print("=" * 70)
print("\n요약:")
print("  ✓ src.devices에서 모든 센서 클래스 import 성공")
print("  ✓ 직접 경로에서 모든 센서 클래스 import 성공")
print("  ✓ 센서 기본 기능 정상 작동")
print("  ✓ Device 클래스 정상 작동")
print("  ✓ 센서-디바이스 연동 정상")
print("\n✅ sensor 폴더가 src/devices/sensors/에 정상적으로 위치하고 있으며")
print("   모든 import 경로가 올바르게 설정되었습니다!")


