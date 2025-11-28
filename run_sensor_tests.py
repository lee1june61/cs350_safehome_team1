"""
센서 테스트 실행 스크립트
pytest가 설치되지 않은 경우에도 unittest로 실행 가능
"""

import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# UTF-8 인코딩 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

os.environ["SAFEHOME_HEADLESS"] = "1"

print("=" * 70)
print("센서 테스트 실행")
print("=" * 70)

# pytest 사용 시도
try:
    import pytest
    print("\n[pytest 사용]")
    print("-" * 70)
    
    # 센서 관련 테스트만 실행
    exit_code = pytest.main([
        'tests/unit/test_devices/test_sensor_new.py',
        'tests/unit/test_devices/test_sensor_controller_new.py',
        '-v',
        '--tb=short'
    ])
    
    if exit_code == 0:
        print("\n✅ 모든 테스트 통과!")
    else:
        print(f"\n❌ 테스트 실패 (exit code: {exit_code})")
    
    sys.exit(exit_code)
    
except ImportError:
    print("\n[pytest 미설치 - 간단한 import 테스트 실행]")
    print("-" * 70)
    
    # pytest 없이 간단한 테스트
    try:
        from src.devices.sensors.sensor import Sensor
        from src.devices.sensors.window_door_sensor import WindowDoorSensor
        from src.devices.sensors.motion_sensor import MotionSensor
        from src.devices.sensors.sensor_controller import SensorController
        
        print("✓ 모든 센서 클래스 import 성공")
        
        # 기본 기능 테스트
        controller = SensorController()
        controller.addSensor(100, 200, 1)
        controller.addSensor(300, 400, 2)
        print(f"✓ SensorController 동작 확인 ({len(controller.getAllSensors())}개 센서)")
        
        # WindowDoorSensor 테스트
        wd_sensor = WindowDoorSensor(1, 1, [100, 200])
        wd_sensor.arm()
        wd_sensor.setOpened(True)
        assert wd_sensor.read() == 1
        print("✓ WindowDoorSensor 동작 확인")
        
        # MotionSensor 테스트
        m_sensor = MotionSensor(2, 2, [300, 400])
        m_sensor.arm()
        m_sensor.setDetected(True)
        assert m_sensor.read() == 1
        print("✓ MotionSensor 동작 확인")
        
        print("\n✅ 모든 기본 테스트 통과!")
        print("\n💡 pytest를 설치하면 더 자세한 테스트를 실행할 수 있습니다:")
        print("   pip install pytest pytest-cov")
        
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

