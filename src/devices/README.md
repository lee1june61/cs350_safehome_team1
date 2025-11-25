# src/devices - Virtual Device Integration

이 폴더는 `virtual_device_v3`의 필요한 파일들을 직접 통합하여 **sys.path 조작 없이** 직접 import할 수 있도록 구성되었습니다.

## 파일 구조

```
src/devices/
├── __init__.py                  # 패키지 초기화
├── interfaces.py                # InterfaceSensor (원본: virtual_device_v3/device/interface_sensor.py)
├── window_door_sensor.py        # DeviceWinDoorSensor (원본: virtual_device_v3/device/device_windoor_sensor.py)
├── motion_sensor.py             # DeviceMotionDetector (원본: virtual_device_v3/device/device_motion_detector.py)
└── device_sensor_tester.py      # DeviceSensorTester (원본: virtual_device_v3/device/device_sensor_tester.py)
```

## 사용 방법

### 이전 방식 (sys.path 조작 필요)

```python
import sys
import os
sys.path.insert(0, '../virtual_device_v3/virtual_device_v3')
from device.device_windoor_sensor import DeviceWinDoorSensor
```

### 새로운 방식 (직접 import)

```python
from src.devices.window_door_sensor import DeviceWinDoorSensor
from src.devices.motion_sensor import DeviceMotionDetector
from src.devices.interfaces import InterfaceSensor
```

## 예제 코드

```python
from src.devices.window_door_sensor import DeviceWinDoorSensor

# 디바이스 생성
device = DeviceWinDoorSensor()

# 센서 활성화
device.arm()

# 침입 시뮬레이션
device.intrude()

# 센서 읽기
if device.read():
    print("침입 감지!")

# 해제
device.release()
device.disarm()
```

## 테스트

```bash
# 간단한 import 테스트
python test_devices_simple.py
```

## 특징

- ✅ **sys.path 조작 불필요**: 프로젝트 구조 내에서 직접 import
- ✅ **명확한 경로**: `src.devices`로 일관된 import 경로
- ✅ **유지보수 용이**: virtual_device_v3와 독립적으로 관리
- ✅ **팀 협업 친화적**: 명확한 모듈 구조

## 주의사항

- 이 파일들은 `virtual_device_v3`에서 복사된 것입니다
- 원본 파일 업데이트 시 수동으로 동기화 필요
- import 경로는 반드시 `src.devices`로 시작해야 합니다


