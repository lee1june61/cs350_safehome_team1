"""
센서 시스템 간단 테스트
Class Diagram의 모든 메서드가 정상 작동하는지 확인
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from safehome.devices.sensors import (
    Sensor,
    WindowDoorSensor,
    MotionSensor,
    SensorController,
)
from safehome.devices.alarm import Alarm


def test_sensor_basic():
    """센서 기본 기능 테스트"""
    print("=" * 60)
    print("1. 센서 기본 기능 테스트")
    print("=" * 60)
    
    # WindowDoorSensor 생성
    sensor = WindowDoorSensor(sensor_id=1, sensor_type=1, location=[100, 200])
    
    # Class Diagram의 모든 메서드 테스트
    print(f"✓ getID(): {sensor.getID()}")
    assert sensor.getID() == 1
    
    print(f"✓ getType(): {sensor.getType()}")
    assert sensor.getType() == 1
    
    print(f"✓ getLocation(): {sensor.getLocation()}")
    assert sensor.getLocation() == [100, 200]
    
    print(f"✓ getSensorLocation(): {sensor.getSensorLocation()}")
    assert sensor.getSensorLocation() == [100, 200]
    
    print(f"✓ isArmed() (초기): {sensor.isArmed()}")
    assert sensor.isArmed() == False
    
    # arm() 테스트
    sensor.arm()
    print(f"✓ arm() 후 isArmed(): {sensor.isArmed()}")
    assert sensor.isArmed() == True
    
    # disarm() 테스트
    result = sensor.disarm()
    print(f"✓ disarm() 반환값: {result}, isArmed(): {sensor.isArmed()}")
    assert result == True
    assert sensor.isArmed() == False
    
    # setID() 테스트
    sensor.setID(10)
    print(f"✓ setID(10) 후 getID(): {sensor.getID()}")
    assert sensor.getID() == 10
    
    # setType() 테스트
    sensor.setType(5)
    print(f"✓ setType(5) 후 getType(): {sensor.getType()}")
    assert sensor.getType() == 5
    
    # setSensorLocation() 테스트
    result = sensor.setSensorLocation([300, 400])
    print(f"✓ setSensorLocation([300, 400]) 반환값: {result}")
    print(f"  위치: {sensor.getSensorLocation()}")
    assert result == True
    assert sensor.getSensorLocation() == [300, 400]
    
    # read() 테스트
    sensor.arm()
    sensor.setOpened(True)
    read_value = sensor.read()
    print(f"✓ read() (armed, opened): {read_value}")
    assert read_value == 1
    
    # isOpen() 테스트 (WindowDoorSensor 전용)
    print(f"✓ isOpen(): {sensor.isOpen()}")
    assert sensor.isOpen() == True
    
    print("\n✅ 센서 기본 기능 테스트 통과!\n")


def test_sensor_controller():
    """센서 컨트롤러 테스트"""
    print("=" * 60)
    print("2. 센서 컨트롤러 테스트")
    print("=" * 60)
    
    controller = SensorController(initial_sensor_number=0)
    print(f"✓ SensorController 생성 (initialSensorNumber: 0)")
    print(f"  nextSensorID: {controller.nextSensorID}")
    
    # addSensor() 테스트
    result1 = controller.addSensor(100, 200, 1)  # WindowDoor
    result2 = controller.addSensor(300, 400, 2)  # Motion
    result3 = controller.addSensor(500, 600, 1)  # WindowDoor
    print(f"✓ addSensor() x3: {result1}, {result2}, {result3}")
    assert all([result1, result2, result3])
    
    # getAllSensorsInfo() 테스트
    info = controller.getAllSensorsInfo()
    print(f"✓ getAllSensorsInfo(): {len(info)}개 센서")
    for sensor_info in info:
        print(f"  - ID:{sensor_info[0]}, Type:{sensor_info[1]}, "
              f"Pos:({sensor_info[2]},{sensor_info[3]}), "
              f"Armed:{sensor_info[4]}, Detected:{sensor_info[5]}")
    assert len(info) == 3
    
    # armSensor() - 단일 센서 활성화
    result = controller.armSensor(1)
    print(f"✓ armSensor(1): {result}")
    assert result == True
    
    # armSensors() - 여러 센서 활성화
    result = controller.armSensors([2, 3])
    print(f"✓ armSensors([2, 3]): {result}")
    assert result == True
    
    # readSensor() 테스트
    sensor1 = controller.getSensor(1)
    sensor1.setOpened(True)
    result = controller.readSensor(1)
    print(f"✓ readSensor(1) (opened): {result}")
    assert result == True
    
    # read() - 모든 센서 읽기
    count = controller.read()
    print(f"✓ read() - 감지된 센서 개수: {count}")
    assert count >= 1
    
    # disarmSensors() 테스트
    result = controller.disarmSensors([1, 2])
    print(f"✓ disarmSensors([1, 2]): {result}")
    assert result == True
    
    # disarmAllSensors() 테스트
    result = controller.disarmAllSensors()
    print(f"✓ disarmAllSensors(): {result}")
    assert result == True
    
    # checkSafezone() 테스트
    result = controller.checkSafezone(1, True)
    print(f"✓ checkSafezone(1, True): {result}")
    
    # removeSensor() 테스트
    result = controller.removeSensor(3)
    print(f"✓ removeSensor(3): {result}")
    assert result == True
    
    info = controller.getAllSensorsInfo()
    print(f"  남은 센서: {len(info)}개")
    assert len(info) == 2
    
    print("\n✅ 센서 컨트롤러 테스트 통과!\n")


def test_alarm():
    """알람 시스템 테스트"""
    print("=" * 60)
    print("3. 알람 시스템 테스트")
    print("=" * 60)
    
    # Alarm 생성
    alarm = Alarm(alarm_id=1, xCoord=500, yCoord=600)
    print(f"✓ Alarm 생성 (id:1, pos:(500,600))")
    
    # getID() 테스트
    print(f"✓ getID(): {alarm.getID()}")
    assert alarm.getID() == 1
    
    # getLocation() 테스트
    location = alarm.getLocation()
    print(f"✓ getLocation(): {location}")
    assert location == [500, 600]
    
    # isRinging() 초기 상태
    print(f"✓ isRinging() (초기): {alarm.isRinging()}")
    assert alarm.isRinging() == False
    
    # starting() 테스트
    result = alarm.starting(1)
    print(f"✓ starting(1): {result}")
    print(f"  isRinging(): {alarm.isRinging()}")
    assert result == True
    assert alarm.isRinging() == True
    
    # ending() 테스트
    result = alarm.ending(1)
    print(f"✓ ending(1): {result}")
    print(f"  isRinging(): {alarm.isRinging()}")
    assert result == True
    assert alarm.isRinging() == False
    
    # ring() 테스트
    alarm.ring(True)
    print(f"✓ ring(True)")
    print(f"  isRinging(): {alarm.isRinging()}")
    assert alarm.isRinging() == True
    
    alarm.ring(False)
    print(f"✓ ring(False)")
    print(f"  isRinging(): {alarm.isRinging()}")
    assert alarm.isRinging() == False
    
    # setLocation() 테스트
    alarm.setLocation(700, 800)
    print(f"✓ setLocation(700, 800)")
    print(f"  getLocation(): {alarm.getLocation()}")
    assert alarm.getLocation() == [700, 800]
    
    print("\n✅ 알람 시스템 테스트 통과!\n")


def test_motion_sensor():
    """모션 센서 테스트"""
    print("=" * 60)
    print("4. 모션 센서 테스트")
    print("=" * 60)
    
    sensor = MotionSensor(sensor_id=2, sensor_type=2, location=[300, 400])
    print(f"✓ MotionSensor 생성")
    
    # 기본 센서 기능
    print(f"✓ getID(): {sensor.getID()}")
    assert sensor.getID() == 2
    
    print(f"✓ getType(): {sensor.getType()}")
    assert sensor.getType() == 2
    
    # 모션 감지
    sensor.arm()
    sensor.setDetected(True)
    print(f"✓ setDetected(True), isDetected(): {sensor.isDetected()}")
    assert sensor.isDetected() == True
    
    read_value = sensor.read()
    print(f"✓ read(): {read_value}")
    assert read_value == 1
    
    print("\n✅ 모션 센서 테스트 통과!\n")


if __name__ == "__main__":
    try:
        test_sensor_basic()
        test_sensor_controller()
        test_alarm()
        test_motion_sensor()
        
        print("=" * 60)
        print("🎉 모든 테스트 통과!")
        print("=" * 60)
        print("\n✅ Class Diagram의 모든 속성과 메서드가 정상 작동합니다.")
        print("✅ Sensor 클래스: 모든 메서드 구현 완료")
        print("✅ WindowDoorSensor 클래스: isOpen() 포함 구현 완료")
        print("✅ MotionSensor 클래스: 모든 기능 구현 완료")
        print("✅ SensorController 클래스: 모든 메서드 구현 완료")
        print("✅ Alarm 클래스: 모든 메서드 구현 완료")
        
    except AssertionError as e:
        print(f"\n❌ 테스트 실패: {e}")
        raise
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        raise




