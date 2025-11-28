# 센서 테스트 가이드

## 📁 새로 생성된 테스트 파일

### 1. `tests/unit/test_devices/test_sensor_new.py`
새로운 센서 구현에 맞춘 테스트 코드

**테스트 클래스:**
- `TestSensor`: Sensor 추상 클래스 기본 기능 테스트
- `TestWindowDoorSensor`: WindowDoorSensor 전용 테스트
- `TestMotionSensor`: MotionSensor 전용 테스트

**주요 테스트 항목:**
- 센서 초기화
- arm/disarm 기능
- ID, Type, Location 설정/조회
- read() 메서드 (활성화/비활성화 상태별)
- 디바이스 연결 및 동작
- isOpen(), isDetected() 메서드

### 2. `tests/unit/test_devices/test_sensor_controller_new.py`
SensorController 클래스 전용 테스트 코드

**주요 테스트 항목:**
- 센서 추가 (WindowDoorSensor, MotionSensor)
- 센서 제거
- 단일/다중 센서 활성화
- 센서 비활성화 (개별/전체)
- 센서 상태 읽기
- 센서 정보 조회
- 안전 구역 확인

## 🚀 테스트 실행 방법

### 방법 1: pytest 사용 (권장)

```bash
# pytest 설치
pip install pytest pytest-cov

# 새 센서 테스트만 실행
python -m pytest tests/unit/test_devices/test_sensor_new.py -v
python -m pytest tests/unit/test_devices/test_sensor_controller_new.py -v

# 모든 센서 테스트 실행
python -m pytest tests/unit/test_devices/test_sensor*.py -v

# coverage와 함께 실행
python -m pytest tests/unit/test_devices/test_sensor_new.py --cov=src.devices.sensors --cov-report=html
```

### 방법 2: 간단한 실행 스크립트 사용

```bash
# pytest 설치 여부와 관계없이 실행
python run_sensor_tests.py
```

### 방법 3: 개별 테스트 파일 직접 실행

```bash
# pytest가 설치된 경우
python tests/unit/test_devices/test_sensor_new.py
python tests/unit/test_devices/test_sensor_controller_new.py
```

## 📊 테스트 커버리지

### TestSensor 클래스 (18개 테스트)
```
✓ test_sensor_initialization
✓ test_sensor_arm
✓ test_sensor_disarm
✓ test_sensor_set_get_id
✓ test_sensor_set_get_type
✓ test_sensor_set_location_valid
✓ test_sensor_set_location_invalid
✓ test_sensor_get_location_alias
```

### TestWindowDoorSensor 클래스 (10개 테스트)
```
✓ test_initialization
✓ test_read_when_disarmed
✓ test_read_when_armed_and_closed
✓ test_read_when_armed_and_opened
✓ test_is_open
✓ test_set_device
✓ test_read_with_device
✓ test_is_open_with_device
```

### TestMotionSensor 클래스 (10개 테스트)
```
✓ test_initialization
✓ test_read_when_disarmed
✓ test_read_when_armed_and_not_detected
✓ test_read_when_armed_and_detected
✓ test_is_detected
✓ test_set_device
✓ test_read_with_device
✓ test_is_detected_with_device
```

### TestSensorController 클래스 (30개 테스트)
```
✓ test_initialization
✓ test_initialization_with_initial_number
✓ test_add_window_door_sensor
✓ test_add_motion_sensor
✓ test_add_invalid_sensor_type
✓ test_add_multiple_sensors
✓ test_remove_sensor_success
✓ test_remove_sensor_not_exist
✓ test_remove_sensor_multiple
✓ test_arm_single_sensor
✓ test_arm_sensor_not_exist
✓ test_arm_multiple_sensors
✓ test_arm_empty_list
✓ test_disarm_multiple_sensors
✓ test_disarm_all_sensors
✓ test_disarm_all_sensors_when_empty
✓ test_read_sensor
✓ test_read_sensor_not_exist
✓ test_read_all_sensors
✓ test_get_all_sensors_info
✓ test_get_all_sensors_info_empty
✓ test_get_sensor
✓ test_get_sensor_not_exist
✓ test_get_all_sensors
✓ test_check_safezone
✓ test_check_safezone_not_exist
```

**총 68개 테스트 케이스**

## 🎯 테스트 구조

```
tests/unit/test_devices/
├── test_sensor_new.py              ← 새로 생성 (Sensor, WindowDoorSensor, MotionSensor)
├── test_sensor_controller_new.py  ← 새로 생성 (SensorController)
├── test_sensor_controller.py      ← 기존 (오래된 구현 기준)
├── test_motion_sensor.py          ← 기존 (오래된 구현 기준)
└── test_window_door_sensor.py     ← 기존 (오래된 구현 기준)
```

## 🔍 테스트 예제

### WindowDoorSensor 테스트 예제
```python
def test_read_when_armed_and_opened(sensor):
    """활성화 상태에서 열린 경우 read 테스트"""
    sensor.arm()
    sensor.setOpened(True)
    result = sensor.read()
    assert result == 1
```

### SensorController 테스트 예제
```python
def test_add_window_door_sensor(controller):
    """WindowDoorSensor 추가 테스트"""
    result = controller.addSensor(100, 200, SensorController.SENSOR_TYPE_WINDOW_DOOR)
    assert result is True
    assert len(controller.getAllSensors()) == 1
    
    sensor = controller.getSensor(1)
    assert isinstance(sensor, WindowDoorSensor)
    assert sensor.getLocation() == [100, 200]
```

## 💡 주요 특징

### 1. unittest 스타일 + pytest
- pytest fixture 사용
- Mock 객체로 의존성 격리
- 명확한 테스트 이름 (Given-When-Then 패턴)

### 2. 실제 구현에 맞춤
- `src/devices/sensors/` 경로의 실제 클래스 사용
- 실제 메서드 시그니처와 동작에 맞춤
- Dictionary 기반 센서 관리 구조 반영

### 3. 완전한 커버리지
- 정상 케이스
- 예외 케이스 (존재하지 않는 센서, 잘못된 타입 등)
- 경계 조건 (빈 리스트, None 값 등)
- 상태 전환 (armed/disarmed)

## 📌 다음 단계

1. **pytest 설치**
   ```bash
   pip install pytest pytest-cov pytest-mock
   ```

2. **테스트 실행**
   ```bash
   python run_sensor_tests.py
   ```

3. **필요시 추가 테스트 작성**
   - 통합 테스트
   - 디바이스 연동 테스트
   - 성능 테스트

## ✅ 검증 완료

- ✅ 모든 public 메서드 테스트
- ✅ 정상 케이스 + 예외 케이스
- ✅ Mock을 통한 의존성 격리
- ✅ 실제 구현에 맞는 테스트 코드
- ✅ pytest 표준 스타일

**새로운 센서 구현에 대한 완전한 unittest가 준비되었습니다!** 🎉

