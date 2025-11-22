# SafeHome 센서 및 알람 시스템 - 빠른 시작 가이드

## 📋 구현 완료 내역

### ✅ Class Diagram 기반 완벽 구현
제공된 Class Diagram의 **모든 속성과 메서드**가 구현되었습니다.

## 🚀 빠른 시작

### 1. 기본 사용법

```python
from safehome.devices.sensors import SensorController
from safehome.devices.alarm import Alarm

# 센서 컨트롤러 생성
controller = SensorController()

# 센서 추가
controller.addSensor(100, 200, 1)  # 창문/문 센서 (타입 1)
controller.addSensor(300, 400, 2)  # 모션 센서 (타입 2)

# 센서 활성화
controller.armSensors([1, 2])

# 알람 생성
alarm = Alarm(1, 500, 600)
```

### 2. 테스트 실행

```bash
# 프로젝트 디렉토리로 이동
cd "c:\safehome project\cs350_safehome_team1"

# 간단한 테스트 실행
python examples/test_simple.py

# 전체 예제 실행
python examples/example_sensors.py
```

## 📁 파일 구조

```
safehome/devices/
├── sensors/
│   ├── interface_sensor.py         # 센서 인터페이스
│   ├── sensor.py                    # 센서 추상 클래스 ⭐
│   ├── window_door_sensor.py        # 창문/문 센서 ⭐
│   ├── motion_sensor.py             # 모션 센서 ⭐
│   ├── sensor_controller.py         # 센서 컨트롤러 ⭐
│   ├── device_sensor_tester.py      # 디바이스 테스터
│   ├── device_windoor_sensor.py     # 창문/문 디바이스
│   └── device_motion_detector.py    # 모션 디바이스
└── alarm/
    └── alarm.py                     # 알람 클래스 ⭐

⭐ = Class Diagram 기반 핵심 클래스
```

## 🎯 Class Diagram 메서드 체크리스트

### Sensor 클래스
- [x] `id`: int
- [x] `type`: int  
- [x] `sensorID`: int
- [x] `detectedSignal`: int
- [x] `sensorLocation`: int[]
- [x] `isArmed()`: bool
- [x] `read()`: int
- [x] `arm()`: void
- [x] `disarm()`: bool
- [x] `setID(id)`: void
- [x] `getID()`: int
- [x] `setType(type)`: void
- [x] `getType()`: int
- [x] `setSensorLocation(location)`: bool
- [x] `getSensorLocation()`: int[]
- [x] `getLocation()`: int[]

### WindowDoorSensor 클래스
- [x] Sensor 상속
- [x] `isOpen()`: bool

### MotionSensor 클래스
- [x] Sensor 상속
- [x] 모든 Sensor 메서드 구현

### SensorController 클래스
- [x] `nextSensorID`: int
- [x] `initialSensorNumber`: int
- [x] `addSensor(xCoord, yCoord, inType)`: bool
- [x] `removeSensor(sensorID)`: bool
- [x] `armSensors(sensorIDList)`: bool
- [x] `armSensor(sensorID)`: bool (오버로드)
- [x] `disarmSensors(sensorIDList)`: bool
- [x] `disarmAllSensors()`: bool
- [x] `readSensor(sensorID)`: bool
- [x] `read()`: int
- [x] `checkSafezone(sensorID, inSafeZone)`: bool
- [x] `getAllSensorsInfo()`: int[][]

### Alarm 클래스
- [x] `id`: int
- [x] `xCoord`: int
- [x] `yCoord`: int
- [x] `status`: bool
- [x] `starting(id)`: bool
- [x] `ending(id)`: bool
- [x] `getLocation()`: int[2]
- [x] `isRinging()`: bool
- [x] `ring(statusValue)`: void

## 💡 주요 기능

### 1. 센서 관리
```python
# 센서 추가
controller.addSensor(x, y, type)

# 센서 활성화
controller.armSensor(sensor_id)         # 단일
controller.armSensors([id1, id2])       # 여러 개

# 센서 비활성화
controller.disarmSensors([id1, id2])    # 여러 개
controller.disarmAllSensors()           # 전체

# 센서 제거
controller.removeSensor(sensor_id)
```

### 2. 센서 읽기
```python
# 특정 센서 읽기
is_triggered = controller.readSensor(sensor_id)

# 모든 센서 읽기 (감지된 개수)
count = controller.read()

# 센서 정보 조회
info = controller.getAllSensorsInfo()
```

### 3. 알람 제어
```python
# 알람 생성
alarm = Alarm(id=1, xCoord=500, yCoord=600)

# 알람 울리기
alarm.ring(True)   # 시작
alarm.ring(False)  # 종료

# 상태 확인
if alarm.isRinging():
    print("알람이 울리고 있습니다!")
```

### 4. 물리적 디바이스 연동
```python
from safehome.devices.sensors import DeviceWinDoorSensor

# 물리적 디바이스 생성
device = DeviceWinDoorSensor()

# 센서와 연결
sensor = controller.getSensor(1)
sensor.setDevice(device)

# 침입 시뮬레이션
device.intrude()  # 창문/문 열기

# 센서 읽기
if sensor.isOpen():
    print("창문/문이 열렸습니다!")
```

## 🔍 예제 코드

### 완전한 사용 예제
```python
from safehome.devices.sensors import (
    SensorController,
    DeviceWinDoorSensor,
    DeviceMotionDetector,
)
from safehome.devices.alarm import Alarm

# 1. 초기화
controller = SensorController()
alarm = Alarm(1, 500, 600)

# 2. 센서 추가 및 활성화
controller.addSensor(100, 200, 1)  # ID: 1
controller.addSensor(300, 400, 2)  # ID: 2
controller.armSensors([1, 2])

# 3. 물리적 디바이스 연결
device1 = DeviceWinDoorSensor()
device2 = DeviceMotionDetector()
controller.getSensor(1).setDevice(device1)
controller.getSensor(2).setDevice(device2)

# 4. 침입 감지 시뮬레이션
device1.intrude()
device2.intrude()

# 5. 센서 확인 및 알람 울리기
if controller.read() > 0:
    alarm.ring(True)
    print("⚠️ 침입 감지! 알람 울림!")

# 6. 정리
controller.disarmAllSensors()
alarm.ring(False)
```

## 📚 추가 자료

- **상세 구현 보고서**: `IMPLEMENTATION_REPORT.md`
- **간단한 테스트**: `examples/test_simple.py`
- **전체 예제**: `examples/example_sensors.py`

## ✨ 특징

1. ✅ **완전한 Class Diagram 구현**
2. ✅ **Type Hints로 타입 안정성 확보**
3. ✅ **한글 Docstring으로 가독성 향상**
4. ✅ **Virtual Device 통합 지원**
5. ✅ **테스트 친화적 설계**
6. ✅ **확장 가능한 아키텍처**

## 🎓 다음 단계

1. `examples/test_simple.py`로 기본 기능 확인
2. `examples/example_sensors.py`로 실제 사용 시나리오 학습
3. 자신의 프로젝트에 통합하여 사용

---

**구현 완료!** 🎉

모든 클래스가 Class Diagram의 명세를 100% 준수하여 구현되었습니다.

