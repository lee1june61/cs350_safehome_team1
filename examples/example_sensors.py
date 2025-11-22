"""
SafeHome 센서 시스템 사용 예제

이 예제는 센서 컨트롤러를 사용하여 센서를 추가하고, 
활성화/비활성화하며, 센서 상태를 읽는 방법을 보여줍니다.
"""

import sys
import os

# safehome 패키지를 import할 수 있도록 경로 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from safehome.devices.sensors import (
    SensorController,
    DeviceWinDoorSensor,
    DeviceMotionDetector,
)
from safehome.devices.alarm import Alarm


def main():
    print("=" * 50)
    print("SafeHome 센서 시스템 예제")
    print("=" * 50)
    
    # 1. 센서 컨트롤러 생성
    print("\n1. 센서 컨트롤러 생성")
    controller = SensorController(initial_sensor_number=0)
    print("   ✓ 센서 컨트롤러 생성 완료")
    
    # 2. 센서 추가
    print("\n2. 센서 추가")
    # 창문/문 센서 추가 (타입 1)
    controller.addSensor(100, 200, SensorController.SENSOR_TYPE_WINDOW_DOOR)
    print("   ✓ 창문/문 센서 추가 (ID: 1, 위치: 100, 200)")
    
    # 모션 센서 추가 (타입 2)
    controller.addSensor(300, 400, SensorController.SENSOR_TYPE_MOTION)
    print("   ✓ 모션 센서 추가 (ID: 2, 위치: 300, 400)")
    
    # 추가 센서들
    controller.addSensor(150, 250, SensorController.SENSOR_TYPE_WINDOW_DOOR)
    print("   ✓ 창문/문 센서 추가 (ID: 3, 위치: 150, 250)")
    
    # 3. 모든 센서 정보 확인
    print("\n3. 모든 센서 정보 확인")
    sensors_info = controller.getAllSensorsInfo()
    print("   센서 개수:", len(sensors_info))
    for info in sensors_info:
        sensor_id, sensor_type, x, y, armed, detected = info
        type_name = "창문/문" if sensor_type == 1 else "모션"
        print(f"   - ID: {sensor_id}, 타입: {type_name}, 위치: ({x}, {y}), "
              f"활성화: {bool(armed)}, 감지: {bool(detected)}")
    
    # 4. 센서 활성화
    print("\n4. 센서 활성화")
    controller.armSensors([1, 2])
    print("   ✓ 센서 1, 2 활성화 완료")
    
    # 5. 센서 상태 확인
    print("\n5. 센서 상태 읽기 (활성화 후)")
    for sensor_id in [1, 2, 3]:
        is_triggered = controller.readSensor(sensor_id)
        print(f"   - 센서 {sensor_id}: {'감지됨' if is_triggered else '정상'}")
    
    # 6. 물리적 디바이스 생성 및 연결
    print("\n6. 물리적 디바이스 시뮬레이션")
    device1 = DeviceWinDoorSensor()
    device2 = DeviceMotionDetector()
    print("   ✓ 물리적 디바이스 생성 완료")
    
    # 센서와 디바이스 연결
    sensor1 = controller.getSensor(1)
    sensor2 = controller.getSensor(2)
    if sensor1:
        sensor1.setDevice(device1)
        print("   ✓ 센서 1과 창문/문 디바이스 연결")
    if sensor2:
        sensor2.setDevice(device2)
        print("   ✓ 센서 2와 모션 디바이스 연결")
    
    # 7. 디바이스로 침입 시뮬레이션
    print("\n7. 침입 시뮬레이션")
    device1.intrude()  # 창문/문 열림
    print("   ✓ 창문/문 열림 감지")
    device2.intrude()  # 모션 감지
    print("   ✓ 모션 감지")
    
    # 8. 센서 상태 다시 확인
    print("\n8. 센서 상태 읽기 (침입 후)")
    for sensor_id in [1, 2, 3]:
        is_triggered = controller.readSensor(sensor_id)
        print(f"   - 센서 {sensor_id}: {'⚠️ 감지됨!' if is_triggered else '정상'}")
    
    # 9. 알람 테스트
    print("\n9. 알람 시스템 테스트")
    alarm = Alarm(alarm_id=1, xCoord=500, yCoord=600)
    print(f"   ✓ 알람 생성 (ID: {alarm.getID()}, 위치: {alarm.getLocation()})")
    
    # 침입 감지 시 알람 울림
    triggered_count = controller.read()
    if triggered_count > 0:
        alarm.ring(True)
        print(f"   ⚠️ {triggered_count}개 센서에서 침입 감지! 알람 울림")
        print(f"   - 알람 상태: {'울림' if alarm.isRinging() else '정상'}")
    
    # 10. 센서 비활성화
    print("\n10. 모든 센서 비활성화")
    controller.disarmAllSensors()
    print("   ✓ 모든 센서 비활성화 완료")
    
    # 알람 종료
    alarm.ring(False)
    print("   ✓ 알람 종료")
    
    # 11. 센서 제거
    print("\n11. 센서 제거")
    controller.removeSensor(3)
    print("   ✓ 센서 3 제거 완료")
    print(f"   - 남은 센서 개수: {len(controller.getAllSensorsInfo())}")
    
    print("\n" + "=" * 50)
    print("예제 실행 완료")
    print("=" * 50)


if __name__ == "__main__":
    main()

