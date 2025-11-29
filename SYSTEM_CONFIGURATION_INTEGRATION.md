# System-Configuration Integration Guide

## 개요

SafeHome System 클래스가 Configuration 모듈과 성공적으로 통합되었습니다. 이제 모든 설정, 로그인, 존, 모드, 로그가 데이터베이스에 영구 저장됩니다.

## 주요 변경사항

### 1. Configuration 모듈 통합

```python
from ..configuration import (
    StorageManager,
    ConfigurationManager,
    LoginManager,
    LogManager,
    AccessLevel,
    SystemSettings,
    SafetyZone,
    SafeHomeMode,
)
```

### 2. System 초기화 변경

**이전:**

```python
def __init__(self):
    self._master_pw = "1234"  # 하드코딩
    self._delay_time = 30
    self._zones = [...]  # 하드코딩
```

**현재:**

```python
def __init__(self, db_path: str = "safehome.db"):
    # Configuration 모듈 초기화
    self._storage = StorageManager.get_instance(db_path)
    self._config_manager = ConfigurationManager(self._storage)
    self._login_manager = LoginManager(self._storage)
    self._log_manager = LogManager(self._storage)

    # DB에서 설정 로드
    self._settings = self._config_manager.get_system_settings()
    self._sync_zones_from_config()
    self._sync_modes_from_config()
```

### 3. 통합된 기능

#### 로그인/인증 (SRS V.1.a, V.1.b)

- `_cmd_login_control_panel()`: LoginManager 사용
- `_cmd_login_web()`: LoginManager 사용
- `_cmd_logout()`: LoginManager + LogManager 사용
- `_cmd_change_password()`: LoginManager 사용

**기본 사용자:**

- Master: username=`master`, password=`password1`
- Guest: username=`guest`, password=`guest123`

#### 시스템 설정 (SRS V.1.c)

- `_cmd_get_system_settings()`: ConfigurationManager에서 로드
- `_cmd_configure_system_settings()`: ConfigurationManager에 저장

**설정 항목:**

- `alarm_delay_time`: 알람 지연 시간 (10-60초)
- `monitoring_service_phone`: 모니터링 서비스 전화번호
- `homeowner_phone`: 집주인 전화번호
- `system_lock_time`: 시스템 잠금 시간 (30-300초)
- `max_login_attempts`: 최대 로그인 시도 횟수
- `session_timeout`: 세션 타임아웃 (분)

#### Safety Zones (SRS V.2.c-h)

- `_cmd_create_safety_zone()`: ConfigurationManager.add_safety_zone()
- `_cmd_update_safety_zone()`: ConfigurationManager.update_safety_zone()
- `_cmd_delete_safety_zone()`: ConfigurationManager.delete_safety_zone()
- `_cmd_get_safety_zones()`: 메모리 캐시 + DB 동기화

#### SafeHome Modes (SRS V.2.i)

- `_cmd_configure_safehome_mode()`: ConfigurationManager.update_safehome_mode()
- `_cmd_get_mode_configuration()`: 메모리 캐시
- `_cmd_get_all_modes()`: 메모리 캐시

**기본 모드:**

1. Home (ID: 1)
2. Away (ID: 2)
3. Overnight (ID: 3)
4. Extended (ID: 4)

#### 로깅 (SRS V.2.j)

- `_cmd_get_intrusion_log()`: LogManager.get_logs()
- `_add_log()`: LogManager.create_log() + save_log()

**로그 타입:**

- LOGIN/LOGOUT: 인증 이벤트
- CONFIGURATION: 설정 변경
- ARM/DISARM: 시스템 상태 변경
- INTRUSION: 침입 감지
- PANIC: 패닉 버튼

## 데이터 흐름

### 로그인 플로우

```
UI → System._cmd_login_control_panel()
    → LoginManager.login()
    → StorageManager.get_login_interface()
    → LoginInterface.verify_password()
    → LogManager.save_log()
    ← AccessLevel 반환
```

### 설정 변경 플로우

```
UI → System._cmd_configure_system_settings()
    → ConfigurationManager.get_system_settings()
    → SystemSettings 수정
    → ConfigurationManager.update_system_settings()
    → StorageManager.save_system_settings()
    → LogManager.save_log()
    ← success 반환
```

### Zone 생성 플로우

```
UI → System._cmd_create_safety_zone()
    → SafetyZone 객체 생성
    → ConfigurationManager.add_safety_zone()
    → StorageManager.save_safety_zone()
    → System._sync_zones_from_config()
    → LogManager.save_log()
    ← zone_id 반환
```

## API 변경사항

### 로그인 메서드

**Control Panel 로그인:**

```python
# 이전
result = system.handle_request("ui", "login_control_panel", password="1234")

# 현재 (기본 사용자)
result = system.handle_request("ui", "login_control_panel",
                               username="master", password="password1")
```

**Web 로그인:**

```python
# 이전
result = system.handle_request("ui", "login_web",
                               user_id="user", password1="pass", password2="word")

# 현재
result = system.handle_request("ui", "login_web",
                               user_id="master", password="password1")
```

### 설정 메서드

```python
# 설정 조회
result = system.handle_request("ui", "get_system_settings")
# 반환: {
#   "success": True,
#   "data": {
#     "delay_time": 30,
#     "monitor_phone": "",
#     "homeowner_phone": "",
#     "system_lock_time": 60,
#     "max_login_attempts": 3,
#     "session_timeout": 30
#   }
# }

# 설정 변경
result = system.handle_request("ui", "configure_system_settings",
                               delay_time=45,
                               monitor_phone="911",
                               homeowner_phone="+1234567890")
```

### Zone 메서드

```python
# Zone 생성
result = system.handle_request("ui", "create_safety_zone",
                               name="First Floor",
                               sensors=["S1", "S2", "M1"])
# 반환: {"success": True, "zone_id": 1}

# Zone 수정
result = system.handle_request("ui", "update_safety_zone",
                               zone_id=1,
                               name="Ground Floor",
                               sensors=["S1", "S2"])

# Zone 삭제
result = system.handle_request("ui", "delete_safety_zone", zone_id=1)
```

## 데이터베이스 스키마

Configuration 모듈이 자동으로 다음 테이블을 생성합니다:

- `login_interfaces`: 사용자 인증 정보
- `system_settings`: 시스템 설정 (key-value)
- `safehome_modes`: SafeHome 모드 구성
- `safety_zones`: Safety Zone 정의
- `logs`: 시스템 이벤트 로그

## 테스트

### Configuration 통합 테스트

```bash
python test_system_config_integration.py
```

### Configuration 모듈 유닛 테스트

```bash
source .venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest tests/test_configuration_module.py -v
```

## 마이그레이션 가이드

기존 UI 코드를 새 API로 마이그레이션하려면:

1. **로그인 코드 업데이트**:

   - Control Panel: `username` 파라미터 추가 (기본값: "master")
   - Web: `password1`, `password2` 대신 단일 `password` 사용 가능

2. **설정 코드 업데이트**:

   - `get_system_settings()` 응답에 새 필드 추가됨
   - `configure_system_settings()`에서 password 관련 파라미터 제거됨

3. **Zone 코드**:
   - 기존 API 호환성 유지됨
   - Zone이 이제 DB에 영구 저장됨

## 주의사항

1. **비밀번호 정책**: 모든 비밀번호는 8자 이상, 숫자 1개 이상 필요
2. **DB 파일**: 기본적으로 `safehome.db` 파일에 저장됨
3. **초기 사용자**: 시스템 첫 실행 시 master/guest 사용자 자동 생성
4. **로그**: 모든 중요 작업이 자동으로 로그에 기록됨

## 향후 개선 사항

- [ ] 비밀번호 암호화 강화 (bcrypt 사용)
- [ ] 세션 관리 구현
- [ ] 사용자 역할 기반 권한 관리
- [ ] 로그 자동 정리 (오래된 로그 삭제)
- [ ] 설정 백업/복원 기능

---

**작성일**: 2025-11-29  
**버전**: 1.0  
**상태**: ✅ 통합 완료
