"""
SafeHome 센서 시스템 빠른 실행 예제

이 파일을 실행하면 센서와 알람 시스템의 기본 기능을 확인할 수 있습니다.
"""

import sys
import os

# safehome 패키지 경로 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from safehome.devices.sensors import (
    SensorController,
    WindowDoorSensor,
    MotionSensor,
)
from safehome.devices.alarm import Alarm


def main():
    print("\n" + "="*60)
    print("      SafeHome 센서 및 알람 시스템 데모")
    print("="*60 + "\n")
    
    # 1. 센서 컨트롤러 생성
    print("📋 1단계: 센서 컨트롤러 생성")
    controller = SensorController()
    print("   ✓ 센서 컨트롤러 생성 완료\n")
    
    # 2. 센서 추가
    print("📋 2단계: 센서 추가")
    controller.addSensor(100, 200, 1)  # 창문/문 센서
    print("   ✓ 창문/문 센서 추가 (ID: 1, 위치: 100, 200)")
    
    controller.addSensor(300, 400, 2)  # 모션 센서
    print("   ✓ 모션 센서 추가 (ID: 2, 위치: 300, 400)")
    
    controller.addSensor(150, 250, 1)  # 창문/문 센서
    print("   ✓ 창문/문 센서 추가 (ID: 3, 위치: 150, 250)\n")
    
    # 3. 센서 정보 출력
    print("📋 3단계: 등록된 센서 정보")
    sensors_info = controller.getAllSensorsInfo()
    for info in sensors_info:
        sensor_id, sensor_type, x, y, armed, detected = info
        type_name = "창문/문" if sensor_type == 1 else "모션"
        print(f"   - ID: {sensor_id}, 타입: {type_name}, "
              f"위치: ({x}, {y})")
    print()
    
    # 4. 센서 활성화
    print("📋 4단계: 센서 활성화")
    controller.armSensors([1, 2, 3])
    print("   ✓ 모든 센서 활성화 완료\n")
    
    # 5. 센서 테스트 (수동 설정)
    print("📋 5단계: 침입 시뮬레이션")
    sensor1 = controller.getSensor(1)
    sensor1.setOpened(True)
    print("   ⚠️  센서 1번: 창문/문 열림 감지!")
    
    sensor2 = controller.getSensor(2)
    sensor2.setDetected(True)
    print("   ⚠️  센서 2번: 모션 감지!\n")
    
    # 6. 센서 상태 확인
    print("📋 6단계: 센서 상태 확인")
    for sensor_id in [1, 2, 3]:
        is_triggered = controller.readSensor(sensor_id)
        status = "⚠️  감지됨!" if is_triggered else "✓ 정상"
        print(f"   센서 {sensor_id}: {status}")
    
    triggered_count = controller.read()
    print(f"\n   총 {triggered_count}개 센서에서 침입 감지됨\n")
    
    # 7. 알람 시스템
    print("📋 7단계: 알람 시스템")
    alarm = Alarm(alarm_id=1, xCoord=500, yCoord=600)
    print(f"   ✓ 알람 생성 (ID: {alarm.getID()}, "
          f"위치: {alarm.getLocation()})")
    
    if triggered_count > 0:
        alarm.ring(True)
        print("   🚨 알람 울림 시작!")
        print(f"   - 알람 상태: {'울림 중' if alarm.isRinging() else '정상'}\n")
    
    # 8. 시스템 종료
    print("📋 8단계: 시스템 종료")
    controller.disarmAllSensors()
    print("   ✓ 모든 센서 비활성화")
    
    alarm.ring(False)
    print("   ✓ 알람 종료\n")
    
    print("="*60)
    print("      데모 실행 완료! ✨")
    print("="*60 + "\n")
    
    # 추가 정보
    print("💡 추가 기능 테스트:")
    print("   - examples/test_simple.py : 전체 기능 테스트")
    print("   - examples/example_sensors.py : 상세 사용 예제\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()



