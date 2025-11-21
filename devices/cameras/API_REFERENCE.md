# Camera Module API Reference

## 📖 빠른 참조

### Import
```python
from safehome.devices.cameras import CameraController, SafeHomeCamera
```

---

## 🎯 SafeHomeCamera

### 클래스 정의
```python
class SafeHomeCamera(InterfaceCamera):
    MIN_ZOOM = 1
    MAX_ZOOM = 9
    MIN_PAN = -5
    MAX_PAN = 5
```

### Constructor
```python
def __init__(self, camera_id: int, x_coord: int, y_coord: int)
```

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `camera_id` | int | 카메라 고유 ID |
| `location` | Tuple[int, int] | (x, y) 좌표 |
| `pan_angle` | int | 팬 각도 (-5 ~ +5) |
| `zoom_setting` | int | 줌 레벨 (1 ~ 9) |
| `password` | Optional[str] | 비밀번호 |
| `enabled` | bool | 활성화 상태 |

### Methods

#### Display Methods
| Method | Returns | Description |
|--------|---------|-------------|
| `display_view()` | Any | 현재 뷰 반환 (PIL Image) |

#### Control Methods
| Method | Returns | Description |
|--------|---------|-------------|
| `zoom_in()` | bool | 줌인 (성공 시 True) |
| `zoom_out()` | bool | 줌아웃 (성공 시 True) |
| `pan_left()` | bool | 왼쪽 팬 (성공 시 True) |
| `pan_right()` | bool | 오른쪽 팬 (성공 시 True) |

#### Password Methods
| Method | Returns | Description |
|--------|---------|-------------|
| `set_password(password: str)` | None | 비밀번호 설정 |
| `get_password()` | Optional[str] | 비밀번호 반환 |
| `has_password()` | bool | 비밀번호 존재 여부 |

#### State Methods
| Method | Returns | Description |
|--------|---------|-------------|
| `enable()` | None | 카메라 활성화 |
| `disable()` | None | 카메라 비활성화 |
| `is_enabled()` | bool | 활성화 여부 |

#### Getter Methods
| Method | Returns | Description |
|--------|---------|-------------|
| `get_id()` | int | 카메라 ID |
| `get_location()` | Tuple[int, int] | 위치 좌표 |
| `get_pan_angle()` | int | 팬 각도 |
| `get_zoom_setting()` | int | 줌 레벨 |

#### Cleanup Methods
| Method | Returns | Description |
|--------|---------|-------------|
| `cleanup()` | None | 리소스 정리 |

---

## 🎮 CameraController

### 클래스 정의
```python
class CameraController:
    CONTROL_PAN_LEFT = 1
    CONTROL_PAN_RIGHT = 2
    CONTROL_ZOOM_IN = 3
    CONTROL_ZOOM_OUT = 4
```

### Constructor
```python
def __init__(self)
```

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `next_camera_id` | int | 다음 카메라 ID |
| `total_camera_number` | int | 전체 카메라 수 |

### Methods

#### Camera Management
| Method | Returns | Description |
|--------|---------|-------------|
| `add_camera(x_coord: int, y_coord: int)` | int | 카메라 추가, ID 반환 |
| `delete_camera(camera_id: int)` | bool | 카메라 삭제 |
| `get_camera_by_id(camera_id: int)` | Optional[SafeHomeCamera] | ID로 카메라 조회 |
| `get_total_camera_number()` | int | 전체 카메라 수 |

#### Enable/Disable
| Method | Returns | Description |
|--------|---------|-------------|
| `enable_cameras(camera_id_list: List[int])` | int | 여러 카메라 활성화, 성공 개수 반환 |
| `disable_cameras(camera_id_list: List[int])` | int | 여러 카메라 비활성화, 성공 개수 반환 |
| `enable_all_cameras()` | None | 모든 카메라 활성화 |
| `disable_all_cameras()` | None | 모든 카메라 비활성화 |

#### Control
| Method | Returns | Description |
|--------|---------|-------------|
| `control_single_camera(camera_id: int, control_id: int)` | bool | 카메라 제어 명령 실행 |

#### Display
| Method | Returns | Description |
|--------|---------|-------------|
| `display_single_view(camera_id: int)` | Optional[Any] | 단일 카메라 뷰 |
| `display_thumbnail_view()` | List[Tuple[int, Optional[Any]]] | 모든 활성 카메라 썸네일 |

#### Password
| Method | Returns | Description |
|--------|---------|-------------|
| `set_camera_password(camera_id: int, password: str)` | bool | 카메라 비밀번호 설정 |
| `validate_camera_password(camera_id: int, password: str)` | bool | 비밀번호 검증 |

#### Information
| Method | Returns | Description |
|--------|---------|-------------|
| `get_all_camera_info()` | List[Dict[str, Any]] | 모든 카메라 정보 |

#### Cleanup
| Method | Returns | Description |
|--------|---------|-------------|
| `cleanup()` | None | 모든 카메라 리소스 정리 |

---

## 📊 Data Structures

### Camera Info Dictionary
```python
{
    'id': int,                    # 카메라 ID
    'location': (int, int),       # (x, y) 좌표
    'enabled': bool,              # 활성화 여부
    'pan_angle': int,             # 팬 각도 (-5 ~ +5)
    'zoom_setting': int,          # 줌 레벨 (1 ~ 9)
    'has_password': bool          # 비밀번호 존재 여부
}
```

### Thumbnail View
```python
[(camera_id: int, image: Optional[PIL.Image]), ...]
```

---

## ⚠️ Exceptions

### ValueError
- 잘못된 카메라 ID
- 알 수 없는 제어 ID
- 빈 비밀번호

### RuntimeError
- 비활성화된 카메라에서 뷰 가져오기

---

## 💡 Usage Examples

### 기본 사용
```python
from safehome.devices.cameras import CameraController

controller = CameraController()
cam_id = controller.add_camera(100, 200)
controller.enable_cameras([cam_id])
controller.control_single_camera(cam_id, CameraController.CONTROL_ZOOM_IN)
```

### 개별 카메라 사용
```python
from safehome.devices.cameras import SafeHomeCamera

camera = SafeHomeCamera(1, 100, 200)
camera.enable()
camera.zoom_in()
view = camera.display_view()
```

### 에러 처리
```python
try:
    view = controller.display_single_view(camera_id)
except ValueError:
    print("카메라를 찾을 수 없습니다")
except RuntimeError:
    print("카메라가 비활성화되어 있습니다")
```

---

## 🔗 Related Documents

- [README.md](README.md) - 전체 모듈 설명
- [INTEGRATION.md](INTEGRATION.md) - 통합 가이드
- [test_cameras.py](../../test_cameras.py) - 테스트 예제

