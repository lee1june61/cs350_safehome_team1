# Camera Module Integration Guide

이 문서는 SafeHome 카메라 모듈을 다른 팀원의 코드와 통합하는 방법을 설명합니다.

## 📦 Import 방법

### 기본 Import
```python
# 전체 컨트롤러 import
from safehome.devices.cameras import CameraController

# 개별 카메라 클래스 import
from safehome.devices.cameras import SafeHomeCamera

# 모두 import
from safehome.devices.cameras import (
    CameraController,
    SafeHomeCamera,
    InterfaceCamera,
    DeviceCamera
)
```

### 패키지 레벨에서 Import
```python
# devices 패키지에서
from safehome.devices import CameraController

# safehome 루트에서 (safehome/__init__.py에 추가 필요)
from safehome.devices.cameras import CameraController
```

## 🏗️ 클래스 구조

### 1. SafeHomeCamera 클래스

```python
class SafeHomeCamera(InterfaceCamera):
    # 클래스 상수
    MIN_ZOOM = 1
    MAX_ZOOM = 9
    MIN_PAN = -5
    MAX_PAN = 5
    
    def __init__(self, camera_id: int, x_coord: int, y_coord: int):
        # Public attributes
        self.camera_id: int = camera_id
        self.location: Tuple[int, int] = (x_coord, y_coord)
        self.pan_angle: int = 0
        self.zoom_setting: int = 2
        self.password: Optional[str] = None
        self.enabled: bool = False
        
        # Private attributes
        self._has_password: bool = False
        self._device: DeviceCamera = DeviceCamera(camera_id)
```

**Public Attributes:**
- `camera_id` (int): 카메라 고유 ID
- `location` (Tuple[int, int]): (x, y) 좌표
- `pan_angle` (int): 팬 각도 (-5 ~ +5)
- `zoom_setting` (int): 줌 레벨 (1 ~ 9)
- `password` (Optional[str]): 비밀번호
- `enabled` (bool): 활성화 상태

**Public Methods:**
- `display_view()` → Any
- `zoom_in()` → bool
- `zoom_out()` → bool
- `pan_left()` → bool
- `pan_right()` → bool
- `set_password(password: str)` → None
- `get_password()` → Optional[str]
- `has_password()` → bool
- `enable()` → None
- `disable()` → None
- `is_enabled()` → bool
- `get_id()` → int
- `get_location()` → Tuple[int, int]
- `get_pan_angle()` → int
- `get_zoom_setting()` → int
- `cleanup()` → None

### 2. CameraController 클래스

```python
class CameraController:
    # 제어 상수
    CONTROL_PAN_LEFT = 1
    CONTROL_PAN_RIGHT = 2
    CONTROL_ZOOM_IN = 3
    CONTROL_ZOOM_OUT = 4
    
    def __init__(self):
        # Public attributes
        self.next_camera_id: int = 1
        self.total_camera_number: int = 0
        
        # Private attributes
        self._cameras: Dict[int, SafeHomeCamera] = {}
```

**Public Attributes:**
- `next_camera_id` (int): 다음 카메라 ID
- `total_camera_number` (int): 전체 카메라 수

**Public Methods:**
- `add_camera(x_coord: int, y_coord: int)` → int
- `delete_camera(camera_id: int)` → bool
- `get_camera_by_id(camera_id: int)` → Optional[SafeHomeCamera]
- `get_total_camera_number()` → int
- `enable_cameras(camera_id_list: List[int])` → int
- `disable_cameras(camera_id_list: List[int])` → int
- `enable_all_cameras()` → None
- `disable_all_cameras()` → None
- `control_single_camera(camera_id: int, control_id: int)` → bool
- `display_single_view(camera_id: int)` → Optional[Any]
- `display_thumbnail_view()` → List[Tuple[int, Optional[Any]]]
- `set_camera_password(camera_id: int, password: str)` → bool
- `validate_camera_password(camera_id: int, password: str)` → bool
- `get_all_camera_info()` → List[Dict[str, Any]]
- `cleanup()` → None

## 💡 통합 예제

### System 클래스와 통합

```python
from safehome.devices.cameras import CameraController

class System:
    def __init__(self):
        # 다른 속성들...
        self.camera_controller = CameraController()
        
    def initialize_cameras(self):
        """시스템 초기화 시 카메라 설정"""
        # 카메라 추가
        cam1 = self.camera_controller.add_camera(100, 200)
        cam2 = self.camera_controller.add_camera(300, 400)
        
        # 기본 카메라 활성화
        self.camera_controller.enable_all_cameras()
    
    def get_camera_status(self):
        """카메라 상태 조회"""
        return self.camera_controller.get_all_camera_info()
```

### ConfigurationManager와 통합

```python
from safehome.devices.cameras import CameraController

class ConfigurationManager:
    def __init__(self, camera_controller: CameraController):
        self.camera_controller = camera_controller
    
    def configure_camera(self, camera_id: int, config: dict):
        """카메라 설정"""
        camera = self.camera_controller.get_camera_by_id(camera_id)
        if camera:
            if 'password' in config:
                camera.set_password(config['password'])
            if 'enabled' in config:
                if config['enabled']:
                    camera.enable()
                else:
                    camera.disable()
```

### ControlPanel과 통합

```python
from safehome.devices.cameras import CameraController

class ControlPanel:
    def __init__(self, camera_controller: CameraController):
        self.camera_controller = camera_controller
    
    def on_camera_button_pressed(self, camera_id: int):
        """카메라 버튼 클릭 처리"""
        view = self.camera_controller.display_single_view(camera_id)
        if view:
            self.display_on_screen(view)
    
    def on_zoom_in_pressed(self, camera_id: int):
        """줌인 버튼 클릭 처리"""
        success = self.camera_controller.control_single_camera(
            camera_id, 
            CameraController.CONTROL_ZOOM_IN
        )
        return success
```

## 🔄 데이터 흐름

### 카메라 정보 조회
```python
# 컨트롤러에서 정보 조회
info_list = camera_controller.get_all_camera_info()

# 반환 형식:
# [
#     {
#         'id': 1,
#         'location': (100, 200),
#         'enabled': True,
#         'pan_angle': 0,
#         'zoom_setting': 3,
#         'has_password': True
#     },
#     ...
# ]
```

### 카메라 뷰 가져오기
```python
# 단일 카메라 뷰
view = camera_controller.display_single_view(camera_id)  # PIL Image 객체

# 모든 카메라 썸네일
thumbnails = camera_controller.display_thumbnail_view()
# [(camera_id, PIL Image), (camera_id, PIL Image), ...]
```

## 🔒 에러 처리

### ValueError
```python
try:
    camera_controller.control_single_camera(999, 1)  # 존재하지 않는 카메라
except ValueError as e:
    print(f"카메라를 찾을 수 없습니다: {e}")
```

### RuntimeError
```python
camera = camera_controller.get_camera_by_id(1)
camera.disable()

try:
    view = camera.display_view()  # 비활성화된 카메라
except RuntimeError as e:
    print(f"카메라가 비활성화되어 있습니다: {e}")
```

## 🧹 리소스 관리

### 시스템 종료 시
```python
class System:
    def shutdown(self):
        """시스템 종료"""
        # 카메라 컨트롤러 정리
        if hasattr(self, 'camera_controller'):
            self.camera_controller.cleanup()
```

### 개별 카메라 정리
```python
# 카메라 삭제 시 자동으로 cleanup 호출됨
camera_controller.delete_camera(camera_id)

# 수동 정리
camera = camera_controller.get_camera_by_id(camera_id)
if camera:
    camera.cleanup()
```

## 📝 타입 힌팅

모든 메서드는 타입 힌팅을 포함합니다:

```python
from typing import Optional, List, Dict, Any, Tuple
from safehome.devices.cameras import CameraController, SafeHomeCamera

def process_cameras(
    controller: CameraController,
    camera_ids: List[int]
) -> List[Dict[str, Any]]:
    """타입 힌팅 예제"""
    results = []
    for cam_id in camera_ids:
        camera: Optional[SafeHomeCamera] = controller.get_camera_by_id(cam_id)
        if camera:
            info = {
                'id': camera.get_id(),
                'location': camera.get_location(),
                'enabled': camera.is_enabled()
            }
            results.append(info)
    return results
```

## 🧪 테스트 예제

```python
import unittest
from safehome.devices.cameras import CameraController

class TestCameraIntegration(unittest.TestCase):
    def setUp(self):
        self.controller = CameraController()
        
    def tearDown(self):
        self.controller.cleanup()
    
    def test_add_camera(self):
        cam_id = self.controller.add_camera(100, 200)
        self.assertEqual(cam_id, 1)
        self.assertEqual(self.controller.total_camera_number, 1)
    
    def test_enable_camera(self):
        cam_id = self.controller.add_camera(100, 200)
        self.controller.enable_cameras([cam_id])
        camera = self.controller.get_camera_by_id(cam_id)
        self.assertTrue(camera.is_enabled())
```

## 📚 추가 문서

- `README.md`: 전체 모듈 설명
- `interface_camera.py`: 추상 인터페이스
- `safehome_camera.py`: 카메라 구현
- `camera_controller.py`: 컨트롤러 구현
- `test_cameras.py`: 테스트 예제

## 🤝 팀원과의 협력

### 의존성 주입 패턴
```python
# 추천: 생성자를 통한 의존성 주입
class SomeOtherClass:
    def __init__(self, camera_controller: CameraController):
        self.camera_controller = camera_controller

# System 클래스에서 한 번만 생성
class System:
    def __init__(self):
        self.camera_controller = CameraController()
        self.other_component = SomeOtherClass(self.camera_controller)
```

### 공유 인터페이스
```python
# 다른 팀원이 InterfaceCamera를 확장할 수 있음
from safehome.devices.cameras import InterfaceCamera

class CustomCamera(InterfaceCamera):
    # 커스텀 구현...
    pass
```

## 📞 연락처

카메라 모듈 관련 질문이나 이슈가 있으면 팀 미팅에서 논의하거나
코드 리뷰를 요청해주세요.

