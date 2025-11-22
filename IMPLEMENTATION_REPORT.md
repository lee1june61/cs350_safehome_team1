# SafeHome 센서 및 알람 시스템 구현 완료

## 구현된 클래스들

### 1. 센서 관련 클래스 (safehome/devices/sensors/)

#### InterfaceSensor (interface_sensor.py)
- 센서의 추상 인터페이스 정의
- 메서드: `get_id()`, `read()`, `arm()`, `disarm()`, `test_armed_state()`

#### Sensor (sensor.py)
- 센서의 기본 추상 클래스
- **속성 (Class Diagram 준수):**
  - `_id`: int - 센서 ID
  - `_type`: int - 센서 타입
  - `_sensorID`: int - 센서 ID (별칭)
  - `_detectedSignal`: int - 감지된 신호
  - `_sensorLocation`: List[int] - 센서 위치 [x, y]
  - `_armed`: bool - 활성화 상태

- **메서드 (Class Diagram 준수):**
  - `read()`: int - 센서 상태 읽기 (추상 메서드)
  - `arm()`: void - 센서 활성화
  - `disarm()`: bool - 센서 비활성화
  - `isArmed()`: bool - 활성화 상태 확인
  - `setID(id)`: void - ID 설정
  - `getID()`: int - ID 반환
  - `setType(type)`: void - 타입 설정
  - `getType()`: int - 타입 반환
  - `setSensorLocation(location)`: bool - 위치 설정
  - `getSensorLocation()`: List[int] - 위치 반환
  - `getLocation()`: List[int] - 위치 반환 (별칭)

#### WindowDoorSensor (window_door_sensor.py)
- Sensor를 상속받는 창문/문 센서 클래스
- **추가 메서드:**
  - `isOpen()`: bool - 창문/문 열림 상태 확인
  - `setDevice(device)`: void - 물리적 디바이스 연결
  - `setOpened(opened)`: void - 테스트용 상태 설정

#### MotionSensor (motion_sensor.py)
- Sensor를 상속받는 모션 감지 센서 클래스
- **추가 메서드:**
  - `isDetected()`: bool - 모션 감지 상태 확인
  - `setDevice(device)`: void - 물리적 디바이스 연결
  - `setDetected(detected)`: void - 테스트용 상태 설정

#### SensorController (sensor_controller.py)
- 센서들을 관리하는 컨트롤러 클래스
- **속성 (Class Diagram 준수):**
  - `nextSensorID`: int - 다음 센서 ID
  - `initialSensorNumber`: int - 초기 센서 개수
  - `_sensors`: Dict[int, Sensor] - 센서 딕셔너리

- **메서드 (Class Diagram 준수):**
  - `addSensor(xCoord, yCoord, inType)`: bool - 센서 추가
  - `removeSensor(sensorID)`: bool - 센서 제거
  - `armSensors(sensorIDList)`: bool - 여러 센서 활성화
  - `armSensor(sensorID)`: bool - 단일 센서 활성화
  - `disarmSensors(sensorIDList)`: bool - 여러 센서 비활성화
  - `disarmAllSensors()`: bool - 모든 센서 비활성화
  - `readSensor(sensorID)`: bool - 센서 상태 읽기
  - `read()`: int - 모든 센서 상태 읽기
  - `checkSafezone(sensorID, inSafeZone)`: bool - 안전 구역 확인
  - `getAllSensorsInfo()`: List[List[int]] - 모든 센서 정보 반환

- **추가 헬퍼 메서드:**
  - `getSensor(sensorID)`: Optional[Sensor] - 센서 객체 반환
  - `getAllSensors()`: Dict[int, Sensor] - 모든 센서 반환

#### 물리적 디바이스 클래스들
- **DeviceSensorTester** (device_sensor_tester.py) - 센서 테스터 추상 클래스
- **DeviceWinDoorSensor** (device_windoor_sensor.py) - 창문/문 센서 디바이스
- **DeviceMotionDetector** (device_motion_detector.py) - 모션 감지 센서 디바이스

### 2. 알람 클래스 (safehome/devices/alarm/)

#### Alarm (alarm.py)
- 알람 시스템 클래스
- **속성 (Class Diagram 준수):**
  - `id`: int - 알람 ID
  - `xCoord`: int - X 좌표
  - `yCoord`: int - Y 좌표
  - `status`: bool - 알람 상태 (True: 울림, False: 꺼짐)

- **메서드 (Class Diagram 준수):**
  - `starting(id)`: bool - 알람 시작
  - `ending(id)`: bool - 알람 종료
  - `getLocation()`: List[int] - 위치 반환 [x, y]
  - `isRinging()`: bool - 울림 상태 확인
  - `ring(statusValue)`: void - 알람 상태 설정

- **추가 헬퍼 메서드:**
  - `setLocation(xCoord, yCoord)`: void - 위치 설정
  - `getID()`: int - ID 반환

## 파일 구조

```
cs350_safehome_team1/
├── safehome/
│   └── devices/
│       ├── __init__.py
│       ├── sensors/
│       │   ├── __init__.py
│       │   ├── interface_sensor.py          # InterfaceSensor 인터페이스
│       │   ├── sensor.py                    # Sensor 추상 클래스
│       │   ├── window_door_sensor.py        # WindowDoorSensor
│       │   ├── motion_sensor.py             # MotionSensor
│       │   ├── sensor_controller.py         # SensorController
│       │   ├── device_sensor_tester.py      # DeviceSensorTester
│       │   ├── device_windoor_sensor.py     # DeviceWinDoorSensor
│       │   └── device_motion_detector.py    # DeviceMotionDetector
│       └── alarm/
│           ├── __init__.py
│           └── alarm.py                     # Alarm 클래스
└── examples/
    └── example_sensors.py                   # 사용 예제
```

## 사용 예제

```python
from safehome.devices.sensors import SensorController, DeviceWinDoorSensor
from safehome.devices.alarm import Alarm

# 센서 컨트롤러 생성
controller = SensorController()

# 센서 추가 (타입 1: 창문/문, 타입 2: 모션)
controller.addSensor(100, 200, 1)  # 창문/문 센서
controller.addSensor(300, 400, 2)  # 모션 센서

# 센서 활성화
controller.armSensors([1, 2])

# 물리적 디바이스 연결
device = DeviceWinDoorSensor()
sensor = controller.getSensor(1)
sensor.setDevice(device)

# 침입 시뮬레이션
device.intrude()

# 센서 상태 읽기
if controller.readSensor(1):
    print("센서 1에서 침입 감지!")

# 알람 생성 및 울림
alarm = Alarm(1, 500, 600)
alarm.ring(True)

# 모든 센서 비활성화
controller.disarmAllSensors()
```

## Class Diagram 준수 확인

### Sensor 클래스
✅ 모든 속성 구현: id, type, sensorID, detectedSignal, sensorLocation  
✅ 모든 메서드 구현: isArmed(), read(), arm(), disarm(), setID(), getLocation(), setType(), getID(), setSensorLocation(), getSensorLocation()

### WindowDoorSensor 클래스
✅ Sensor 상속  
✅ isOpen() 메서드 구현

### MotionSensor 클래스
✅ Sensor 상속  
✅ 기본 센서 기능 모두 구현

### SensorController 클래스
✅ 모든 속성 구현: nextSensorID, initialSensorNumber  
✅ 모든 메서드 구현: addSensor(), removeSensor(), armSensors() (오버로드), disarmSensors(), readSensor(), disarmAllSensors(), checkSafezone(), read(), getAllSensorsInfo()

### Alarm 클래스
✅ 모든 속성 구현: id, xCoord, yCoord, status  
✅ 모든 메서드 구현: starting(), ending(), getLocation(), isRinging(), ring()

## 특징

1. **Type Hints 사용**: 모든 메서드에 타입 힌트를 추가하여 코드 가독성 향상
2. **Docstring 작성**: 모든 클래스와 메서드에 한글 docstring 추가
3. **물리적 디바이스 통합**: Virtual device와 연동 가능한 구조
4. **확장 가능한 설계**: 새로운 센서 타입 추가 용이
5. **테스트 친화적**: 테스트를 위한 setter 메서드 제공

## 다음 단계

1. pytest를 사용한 단위 테스트 작성
2. 통합 테스트 작성
3. GUI 연동 (tkinter 기반)
4. 데이터베이스 연동
5. 로깅 시스템 통합

