# SafeHome 카메라 모듈 (PEP 8 스타일)

SafeHome 보안 시스템의 카메라 서브시스템에 대한 완전한 구현입니다.

## 파일 구조

```
safehome/devices/cameras/
├── __init__.py              # 패키지 초기화 및 exports
├── interface_camera.py      # InterfaceCamera 추상 기본 클래스
├── device_camera.py         # DeviceCamera 하드웨어 추상화
├── safehome_camera.py       # SafeHomeCamera 메인 로직 클래스
├── camera_controller.py     # CameraController 관리 클래스
└── README.md               # 이 파일
```

## 명명 규칙

이 모듈은 **PEP 8** Python 스타일 가이드를 따릅니다:
- **클래스**: `PascalCase` (예: `SafeHomeCamera`, `CameraController`)
- **메서드/함수**: `snake_case` (예: `display_view()`, `zoom_in()`)
- **변수**: `snake_case` (예: `pan_angle`, `zoom_setting`)
- **상수**: `UPPER_CASE` (예: `MAX_ZOOM`, `MIN_PAN`)
- **비공개 속성**: `_leading_underscore` (예: `_has_password`, `_device`)

## 모듈 설명

### 1. interface_camera.py
**목적**: SafeHomeCamera를 위한 추상 인터페이스 정의

**클래스**: `InterfaceCamera` (ABC)

**추상 메서드**:
- `display_view()` - 현재 카메라 뷰 반환
- `zoom_in()` / `zoom_out()` - 줌 제어
- `pan_left()` / `pan_right()` - 팬 제어
- `set_password()` / `get_password()` - 비밀번호 관리
- `enable()` / `disable()` - 카메라 활성화/비활성화
- `get_id()` / `get_location()` - 정보 조회
- `is_enabled()` / `has_password()` - 상태 확인
- `get_pan_angle()` / `get_zoom_setting()` - 설정값 조회

### 2. device_camera.py
**목적**: 저수준 하드웨어 추상화 (시뮬레이션)

**클래스**: `DeviceCamera`

**주요 기능**:
- virtual_device_v3의 DeviceCamera 래핑
- 정적 이미지를 사용한 비디오 피드 시뮬레이션
- `get_frame()` - 이미지 객체 반환
- 하드웨어 수준의 팬/줌 작업

**의존성**: 
- `virtual_device_v3/virtual_device_v3/device/device_camera.py`
- PIL/Pillow 라이브러리

### 3. safehome_camera.py
**목적**: 단일 카메라의 메인 로직 클래스

**클래스**: `SafeHomeCamera` (InterfaceCamera 구현)

**속성**:
- `camera_id`: int - 고유 식별자
- `location`: Tuple[int, int] - (x, y) 좌표
- `pan_angle`: int - 현재 팬 각도 (-5 ~ +5)
- `zoom_setting`: int - 현재 줌 레벨 (1 ~ 9)
- `_has_password`: bool - 비밀번호 설정 여부 (비공개)
- `password`: Optional[str] - 카메라 비밀번호
- `enabled`: bool - 활성화 상태
- `_device`: DeviceCamera - 하드웨어 장치 인스턴스 (비공개)

**주요 기능**:
- InterfaceCamera의 모든 추상 메서드 구현
- DeviceCamera 인스턴스를 통한 composition 패턴
- 줌/팬 한계 검증 (MIN_ZOOM=1, MAX_ZOOM=9, MIN_PAN=-5, MAX_PAN=5)
- 비활성화 시 작업 차단
- 에러 처리 및 검증

### 4. camera_controller.py
**목적**: 여러 SafeHomeCamera 인스턴스 관리

**클래스**: `CameraController`

**속성**:
- `next_camera_id`: int - 다음 카메라 ID
- `total_camera_number`: int - 현재 관리 중인 카메라 수
- `_cameras`: Dict[int, SafeHomeCamera] - 카메라 딕셔너리 (ID로 인덱싱)

**제어 상수**:
- `CONTROL_PAN_LEFT = 1`
- `CONTROL_PAN_RIGHT = 2`
- `CONTROL_ZOOM_IN = 3`
- `CONTROL_ZOOM_OUT = 4`

**주요 메서드**:
- `add_camera(x_coord, y_coord)` - 새 카메라 생성 및 추가
- `delete_camera(camera_id)` - ID로 카메라 제거
- `enable_cameras(camera_id_list)` - 여러 카메라 활성화
- `disable_cameras(camera_id_list)` - 여러 카메라 비활성화
- `enable_all_cameras()` - 모든 카메라 활성화
- `disable_all_cameras()` - 모든 카메라 비활성화
- `control_single_camera(camera_id, control_id)` - 특정 카메라 제어
- `display_single_view(camera_id)` - 특정 카메라의 뷰 반환
- `display_thumbnail_view()` - 모든 활성화된 카메라의 썸네일 반환
- `set_camera_password(camera_id, password)` - 카메라 비밀번호 설정
- `validate_camera_password(camera_id, password)` - 비밀번호 검증
- `get_all_camera_info()` - 모든 카메라 정보 반환

## 사용 예제

### 기본 사용법

```python
from safehome.devices.cameras import CameraController

# 컨트롤러 생성
controller = CameraController()

# 카메라 추가
cam1_id = controller.add_camera(100, 200)  # (x=100, y=200) 위치에 카메라 추가
cam2_id = controller.add_camera(300, 400)

# 카메라 활성화
controller.enable_cameras([cam1_id, cam2_id])

# 또는 모든 카메라 활성화
controller.enable_all_cameras()

# 카메라 제어
controller.control_single_camera(cam1_id, CameraController.CONTROL_ZOOM_IN)
controller.control_single_camera(cam1_id, CameraController.CONTROL_PAN_RIGHT)

# 카메라 뷰 가져오기
view = controller.display_single_view(cam1_id)

# 모든 카메라 정보 가져오기
all_info = controller.get_all_camera_info()
for info in all_info:
    print(f"Camera {info['id']}: enabled={info['enabled']}, zoom={info['zoom_setting']}")

# 비밀번호 설정
controller.set_camera_password(cam1_id, "secure123")

# 비밀번호 검증
is_valid = controller.validate_camera_password(cam1_id, "secure123")

# 카메라 제거
controller.delete_camera(cam2_id)

# 정리
controller.cleanup()
```

### 개별 카메라 사용

```python
from safehome.devices.cameras import SafeHomeCamera

# 카메라 생성
camera = SafeHomeCamera(camera_id=1, x_coord=100, y_coord=200)

# 카메라 활성화
camera.enable()

# 제어
camera.zoom_in()
camera.pan_right()

# 정보 조회
print(f"ID: {camera.get_id()}")
print(f"Location: {camera.get_location()}")
print(f"Pan: {camera.get_pan_angle()}")
print(f"Zoom: {camera.get_zoom_setting()}")

# 뷰 가져오기 (PIL Image)
view = camera.display_view()

# 비밀번호 설정
camera.set_password("mypassword")

# 정리
camera.cleanup()
```

## PEP 8 준수 사항

### ✅ 명명 규칙
- 모든 메서드와 함수는 `snake_case`
- 모든 변수와 속성은 `snake_case`
- 클래스는 `PascalCase`
- 상수는 `UPPER_CASE`

### ✅ 코드 스타일
- 들여쓰기: 4칸 공백
- 한 줄 최대 길이: 100자 이하 권장
- docstring: 모든 public 클래스/메서드에 포함
- 타입 힌팅: 모든 함수 시그니처에 포함

### ✅ 문서화
- 모든 모듈에 모듈 docstring
- 모든 클래스에 클래스 docstring
- 모든 public 메서드에 메서드 docstring
- Args, Returns, Raises 명시

## 에러 처리

모든 메서드는 적절한 에러 처리를 포함합니다:

- `ValueError`: 잘못된 매개변수 (예: 빈 비밀번호, 알 수 없는 제어 ID)
- `RuntimeError`: 비활성화된 카메라에서 뷰 가져오기 시도
- 반환값 `False`: 한계 도달 (최대 줌, 최대 팬 등)

## 제약사항 및 한계

### 카메라 제어 한계
- **줌 레벨**: 1 ~ 9
- **팬 각도**: -5 ~ +5
- 한계에 도달하면 메서드는 `False` 반환

### 의존성
- Python 3.7+
- Pillow (PIL) - 이미지 처리용
- virtual_device_v3 패키지

### 이미지 파일
DeviceCamera는 다음 이미지 파일을 찾습니다:
- `camera{id}.jpg` (예: camera1.jpg, camera2.jpg, camera3.jpg)
- 파일은 virtual_device_v3/virtual_device_v3/ 디렉토리에 있어야 함

## 테스트

테스트 스크립트 실행:
```bash
cd safehome
python test_cameras.py
```

## SDS 매핑

SDS 문서의 camelCase를 PEP 8의 snake_case로 변환:

| SDS (camelCase) | Python (snake_case) |
|-----------------|---------------------|
| `displayView()` | `display_view()` |
| `zoomIn()` | `zoom_in()` |
| `zoomOut()` | `zoom_out()` |
| `panLeft()` | `pan_left()` |
| `panRight()` | `pan_right()` |
| `setPassword()` | `set_password()` |
| `getPassword()` | `get_password()` |
| `getID()` | `get_id()` |
| `getLocation()` | `get_location()` |
| `isEnabled()` | `is_enabled()` |
| `hasPassword()` | `has_password()` |
| `getPanAngle()` | `get_pan_angle()` |
| `getZoomSetting()` | `get_zoom_setting()` |
| `addCamera()` | `add_camera()` |
| `deleteCamera()` | `delete_camera()` |
| `enableCameras()` | `enable_cameras()` |
| `disableCameras()` | `disable_cameras()` |
| `enableAllCamera()` | `enable_all_cameras()` |
| `disableAllCamera()` | `disable_all_cameras()` |
| `controlSingleCamera()` | `control_single_camera()` |
| `displaySingleView()` | `display_single_view()` |
| `displayThumbnailView()` | `display_thumbnail_view()` |
| `setCameraPassword()` | `set_camera_password()` |
| `validateCameraPassword()` | `validate_camera_password()` |
| `getAllCameraInfo()` | `get_all_camera_info()` |
| `panAngle` | `pan_angle` |
| `zoomSetting` | `zoom_setting` |
| `nextCameraID` | `next_camera_id` |
| `totalCameraNumber` | `total_camera_number` |

## 설계 원칙

1. **Composition over Inheritance**: SafeHomeCamera가 DeviceCamera를 포함
2. **Interface Segregation**: 깔끔한 추상 인터페이스
3. **Type Safety**: 모든 메서드에 타입 힌팅
4. **Error Handling**: 포괄적인 에러 처리
5. **Single Responsibility**: 각 클래스의 명확한 역할
6. **PEP 8 Compliance**: Python 표준 스타일 가이드 준수

## 주의사항

- 카메라는 기본적으로 **비활성화** 상태로 생성됨
- 비활성화된 카메라의 제어 메서드는 `False` 반환
- 비활성화된 카메라에서 `display_view()` 호출 시 `RuntimeError` 발생
- 삭제 시 항상 `cleanup()` 호출하여 리소스 해제
- DeviceCamera는 스레드를 사용하므로 적절한 정리 필요

## 향후 개선 사항

- 실시간 비디오 스트리밍 지원
- 녹화 기능
- 모션 감지 통합
- 카메라 프리셋 위치
- PTZ (Pan-Tilt-Zoom) 속도 제어
- 다중 카메라 동기화
- 네트워크 스트리밍

## 라이선스

SafeHome 프로젝트의 일부
