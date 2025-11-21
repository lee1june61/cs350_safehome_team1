# Camera Module - Team Handoff Document

**담당자**: Camera Module Team  
**완료일**: 2024  
**버전**: 1.0.0  
**상태**: ✅ 완료 및 테스트 통과

---

## 📦 제출 내용

### 구현된 파일들

```
safehome/devices/cameras/
├── __init__.py                 # 패키지 초기화 및 exports
├── interface_camera.py         # InterfaceCamera 추상 기본 클래스
├── device_camera.py            # DeviceCamera 하드웨어 추상화
├── safehome_camera.py          # SafeHomeCamera 메인 로직
├── camera_controller.py        # CameraController 관리 클래스
├── README.md                   # 모듈 설명 (한글)
├── INTEGRATION.md              # 통합 가이드 (한글)
├── API_REFERENCE.md            # API 레퍼런스
└── TEAM_HANDOFF.md            # 이 문서
```

### 추가 파일

```
safehome/
├── devices/__init__.py         # devices 패키지 초기화 (카메라 export)
└── test_cameras.py             # 테스트 스크립트
```

---

## 🎯 핵심 클래스 구조

### 1. SafeHomeCamera (단일 카메라)

```python
class SafeHomeCamera(InterfaceCamera):
    def __init__(self, camera_id: int, x_coord: int, y_coord: int):
        # Public attributes (팀원들이 접근 가능)
        self.camera_id: int = camera_id
        self.location: Tuple[int, int] = (x_coord, y_coord)
        self.pan_angle: int = 0
        self.zoom_setting: int = 2
        self.password: Optional[str] = None
        self.enabled: bool = False
        
        # Private attributes (내부 구현)
        self._has_password: bool = False
        self._device: DeviceCamera = DeviceCamera(camera_id)
```

**주요 메서드 (팀원들이 사용할 것들):**
- `display_view()` - 카메라 뷰 가져오기
- `zoom_in()`, `zoom_out()`, `pan_left()`, `pan_right()` - 제어
- `enable()`, `disable()`, `is_enabled()` - 활성화 관리
- `set_password()`, `has_password()` - 비밀번호 관리
- `get_id()`, `get_location()`, `get_pan_angle()`, `get_zoom_setting()` - 정보 조회

### 2. CameraController (카메라 관리자)

```python
class CameraController:
    def __init__(self):
        # Public attributes (팀원들이 접근 가능)
        self.next_camera_id: int = 1
        self.total_camera_number: int = 0
        
        # Private attributes (내부 구현)
        self._cameras: Dict[int, SafeHomeCamera] = {}
```

**주요 메서드 (팀원들이 사용할 것들):**
- `add_camera(x, y)` - 카메라 추가 → 반환: camera_id
- `delete_camera(id)` - 카메라 삭제
- `enable_cameras([ids])`, `enable_all_cameras()` - 활성화
- `control_single_camera(id, control_id)` - 제어 (CONTROL_ZOOM_IN 등)
- `display_single_view(id)` - 뷰 가져오기
- `get_all_camera_info()` - 전체 정보 조회
- `set_camera_password(id, pw)`, `validate_camera_password(id, pw)` - 비밀번호

---

## 🔌 팀원들이 사용하는 방법

### Import 방법

```python
# 방법 1: 직접 import
from safehome.devices.cameras import CameraController, SafeHomeCamera

# 방법 2: devices 패키지에서
from safehome.devices import CameraController

# 방법 3: 전체 import
from safehome.devices.cameras import (
    CameraController,
    SafeHomeCamera,
    InterfaceCamera,
    DeviceCamera
)
```

### 의존성 주입 패턴 (추천)

```python
# System 클래스에서 한 번만 생성
class System:
    def __init__(self):
        # 하나의 CameraController 인스턴스 생성
        self.camera_controller = CameraController()
        
        # 다른 컴포넌트들에 전달
        self.config_manager = ConfigurationManager(self.camera_controller)
        self.control_panel = ControlPanel(self.camera_controller)
        self.monitoring = MonitoringSystem(self.camera_controller)
```

### 다른 클래스에서 사용

```python
class ConfigurationManager:
    def __init__(self, camera_controller: CameraController):
        self.camera_controller = camera_controller  # 받아서 저장
    
    def setup_cameras(self):
        # 카메라 추가
        cam1 = self.camera_controller.add_camera(100, 200)
        cam2 = self.camera_controller.add_camera(300, 400)
        
        # 활성화
        self.camera_controller.enable_all_cameras()
```

```python
class ControlPanel:
    def __init__(self, camera_controller: CameraController):
        self.camera_controller = camera_controller
    
    def on_zoom_button(self, camera_id: int):
        # 제어
        success = self.camera_controller.control_single_camera(
            camera_id,
            CameraController.CONTROL_ZOOM_IN
        )
        return success
```

---

## 📋 클래스 속성 정리

### SafeHomeCamera의 Public Attributes

| Attribute | Type | 기본값 | 설명 |
|-----------|------|--------|------|
| `camera_id` | int | - | 고유 ID |
| `location` | Tuple[int, int] | - | (x, y) 좌표 |
| `pan_angle` | int | 0 | 팬 각도 (-5 ~ +5) |
| `zoom_setting` | int | 2 | 줌 레벨 (1 ~ 9) |
| `password` | Optional[str] | None | 비밀번호 |
| `enabled` | bool | False | 활성화 상태 |

**사용 예:**
```python
camera = controller.get_camera_by_id(1)
print(f"카메라 ID: {camera.camera_id}")
print(f"위치: {camera.location}")
print(f"줌: {camera.zoom_setting}")
```

### CameraController의 Public Attributes

| Attribute | Type | 기본값 | 설명 |
|-----------|------|--------|------|
| `next_camera_id` | int | 1 | 다음 카메라 ID |
| `total_camera_number` | int | 0 | 전체 카메라 수 |

**사용 예:**
```python
print(f"전체 카메라: {controller.total_camera_number}개")
print(f"다음 ID: {controller.next_camera_id}")
```

---

## 🔄 데이터 흐름 예제

### 1. 카메라 추가 → 활성화 → 제어

```python
# 1. 추가
cam_id = controller.add_camera(100, 200)

# 2. 활성화
controller.enable_cameras([cam_id])

# 3. 제어
controller.control_single_camera(cam_id, CameraController.CONTROL_ZOOM_IN)
controller.control_single_camera(cam_id, CameraController.CONTROL_PAN_RIGHT)

# 4. 뷰 가져오기
view = controller.display_single_view(cam_id)  # PIL Image
```

### 2. 정보 조회

```python
# 전체 정보
all_info = controller.get_all_camera_info()
# 반환: [{'id': 1, 'location': (100, 200), 'enabled': True, ...}, ...]

# 개별 카메라
camera = controller.get_camera_by_id(cam_id)
if camera:
    print(camera.get_location())
    print(camera.get_pan_angle())
    print(camera.is_enabled())
```

### 3. 비밀번호 관리

```python
# 설정
controller.set_camera_password(cam_id, "secure123")

# 검증
is_valid = controller.validate_camera_password(cam_id, "secure123")  # True
is_valid = controller.validate_camera_password(cam_id, "wrong")      # False
```

---

## ⚠️ 중요 사항

### 1. 리소스 정리
```python
# 시스템 종료 시 반드시 호출
controller.cleanup()
```

### 2. 에러 처리
```python
try:
    view = controller.display_single_view(camera_id)
except ValueError:
    # 카메라를 찾을 수 없음
    pass
except RuntimeError:
    # 카메라가 비활성화됨
    pass
```

### 3. 제어 상수
```python
# 사용 가능한 제어 ID
CameraController.CONTROL_PAN_LEFT    # 1
CameraController.CONTROL_PAN_RIGHT   # 2
CameraController.CONTROL_ZOOM_IN     # 3
CameraController.CONTROL_ZOOM_OUT    # 4
```

### 4. 카메라 상태
- 카메라는 **기본적으로 비활성화** 상태로 생성됨
- 비활성화 상태에서는 `display_view()` 호출 시 RuntimeError 발생
- 제어 메서드(zoom, pan)는 비활성화 시 False 반환

---

## 📚 문서 가이드

1. **README.md** - 시작 여기서! 전체 모듈 설명
2. **INTEGRATION.md** - 통합 가이드 (System, ConfigManager 등과 연동)
3. **API_REFERENCE.md** - 빠른 API 참조
4. **TEAM_HANDOFF.md** - 이 문서 (팀 인수인계)

---

## ✅ 테스트 상태

- ✅ 단위 테스트 통과
- ✅ 통합 테스트 준비 완료
- ✅ Linter 에러 없음
- ✅ PEP 8 준수
- ✅ 타입 힌팅 완료
- ✅ Docstring 완료

**테스트 실행:**
```bash
cd safehome
python test_cameras.py
```

---

## 🤝 통합 체크리스트

팀원들이 통합 시 확인할 사항:

- [ ] `from safehome.devices.cameras import CameraController` 가 작동하는가?
- [ ] System 클래스에서 CameraController 인스턴스를 생성했는가?
- [ ] 다른 컴포넌트들이 CameraController를 의존성 주입으로 받는가?
- [ ] 시스템 종료 시 `controller.cleanup()` 호출하는가?
- [ ] 카메라 추가 후 활성화(`enable_cameras`)를 호출하는가?
- [ ] 에러 처리(ValueError, RuntimeError)를 구현했는가?

---

## 📞 질문이나 이슈가 있다면

1. **INTEGRATION.md** 확인
2. **API_REFERENCE.md** 확인
3. **test_cameras.py** 예제 코드 참고
4. 팀 미팅에서 논의

---

## 🎉 완료!

Camera Module은 완전히 구현되고 테스트되었습니다.  
팀원들은 위의 가이드를 따라 쉽게 통합할 수 있습니다.

**Happy Coding! 🚀**

