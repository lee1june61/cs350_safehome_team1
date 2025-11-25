# SafeHome Configuration Module - Testing Guide

이 문서는 SafeHome 프로젝트의 Configuration 모듈을 테스트하는 방법을 단계별로 설명합니다.

## 📋 목차

1. [환경 설정](#환경-설정)
2. [테스트 실행 방법](#테스트-실행-방법)
3. [테스트 결과 해석](#테스트-결과-해석)
4. [커버리지 리포트 확인](#커버리지-리포트-확인)
5. [개별 테스트 실행](#개별-테스트-실행)

---

## 🛠️ 환경 설정

### 1단계: 가상환경 생성 (최초 1회만)

```bash
cd /Users/minjun/Desktop/cs350_safehome_team1
python3 -m venv .venv
```

### 2단계: 가상환경 활성화

```bash
source .venv/bin/activate
```

> **참고**: 가상환경이 활성화되면 터미널 프롬프트 앞에 `(.venv)`가 표시됩니다.

### 3단계: 테스트 패키지 설치 (최초 1회만)

```bash
pip install pytest pytest-cov pytest-mock
```

또는 requirements.txt를 사용:

```bash
pip install -r requirements.txt
```

---

## 🧪 테스트 실행 방법

### Configuration 모듈 전체 테스트

```bash
# 가상환경 활성화 후
source .venv/bin/activate

# 테스트 실행
pytest tests/test_configuration_module.py -v
```

### 예상 출력:

```
============================= test session starts ==============================
platform darwin -- Python 3.13.3, pytest-9.0.1, pluggy-1.6.0
collected 10 items

tests/test_configuration_module.py::test_system_settings_roundtrip PASSED [ 10%]
tests/test_configuration_module.py::test_system_settings_validation_failure PASSED [ 20%]
tests/test_configuration_module.py::test_login_interface_password_policy_and_hashing PASSED [ 30%]
tests/test_configuration_module.py::test_login_manager_success_and_lockout PASSED [ 40%]
tests/test_configuration_module.py::test_login_manager_change_password PASSED [ 50%]
tests/test_configuration_module.py::test_safehome_mode_validation_and_persistence PASSED [ 60%]
tests/test_configuration_module.py::test_safety_zone_validation_and_persistence PASSED [ 70%]
tests/test_configuration_module.py::test_log_manager_crud PASSED [ 80%]
tests/test_configuration_module.py::test_configuration_manager_initialize_and_modes PASSED [ 90%]
tests/test_configuration_module.py::test_configuration_manager_zones_flow PASSED [100%]

======================= 10 passed in 0.28s =========================
```

---

## 📊 테스트 결과 해석

### 각 테스트가 검증하는 내용:

| 테스트 이름 | 검증 내용 |
|------------|----------|
| `test_system_settings_roundtrip` | SystemSettings가 DB에 저장/로드되는지 확인 |
| `test_system_settings_validation_failure` | 잘못된 전화번호 입력 시 ValidationError 발생 확인 |
| `test_login_interface_password_policy_and_hashing` | 비밀번호 정책(최소 길이, 숫자 필수) 및 해싱 동작 확인 |
| `test_login_manager_success_and_lockout` | 로그인 성공/실패, 3회 실패 시 계정 잠금 확인 |
| `test_login_manager_change_password` | 비밀번호 변경 시 old password 검증 확인 |
| `test_safehome_mode_validation_and_persistence` | SafeHomeMode 저장/조회/업데이트 확인 |
| `test_safety_zone_validation_and_persistence` | SafetyZone 생성/수정/삭제 플로우 확인 |
| `test_log_manager_crud` | 로그 생성, 조회, 침입 로그 필터링, 오래된 로그 삭제 확인 |
| `test_configuration_manager_initialize_and_modes` | ConfigurationManager 초기화 및 4개 기본 모드 생성 확인 |
| `test_configuration_manager_zones_flow` | ConfigurationManager를 통한 존 추가/수정/삭제 확인 |

### 테스트 상태 표시:

- ✅ **PASSED**: 테스트 성공
- ❌ **FAILED**: 테스트 실패 (버그 또는 구현 오류)
- ⚠️ **SKIPPED**: 테스트 건너뜀
- 🔶 **WARNING**: 경고 (동작하지만 개선 필요)

---

## 📈 커버리지 리포트 확인

### 터미널에서 커버리지 확인

```bash
pytest tests/test_configuration_module.py -v \
  --cov=safehome/configuration \
  --cov-report=term-missing
```

### 현재 커버리지 결과:

```
Name                                              Cover   Missing
--------------------------------------------------------------------
safehome/configuration/configuration_manager.py    82%   68-71, 83, 108, 122, 131
safehome/configuration/log.py                      89%   51, 55
safehome/configuration/log_manager.py              87%   37, 58-72
safehome/configuration/login_interface.py          89%   102, 106, 170, 172, 177, 179
safehome/configuration/login_manager.py            79%   42, 62-64, 76, 90, 94, 110-114, 120, 130, 141
safehome/configuration/safehome_mode.py            74%   40-43, 47, 63, 65, 82-85
safehome/configuration/safety_zone.py              78%   33, 40, 44, 48, 71, 73, 93-96
safehome/configuration/storage_manager.py          71%   94, 97-98, 107, 136-137, ...
safehome/configuration/system_settings.py          77%   72, 75, 77, 79, 81, 94-113
--------------------------------------------------------------------
TOTAL                                              80%
```

> **참고**: SDS 요구사항은 75% 이상의 브랜치 커버리지입니다. 현재 **80%**로 요구사항을 충족합니다.

### HTML 커버리지 리포트 생성

```bash
pytest tests/test_configuration_module.py --cov=safehome/configuration --cov-report=html
```

리포트 확인:

```bash
open htmlcov/index.html  # macOS
# 또는
# xdg-open htmlcov/index.html  # Linux
# start htmlcov/index.html  # Windows
```

HTML 리포트에서는:
- 각 파일의 라인별 커버리지를 색상으로 표시
- 초록색: 실행된 코드
- 빨간색: 실행되지 않은 코드
- 노란색: 부분적으로 실행된 브랜치

---

## 🎯 개별 테스트 실행

### 특정 테스트만 실행하기

```bash
# 로그인 관련 테스트만
pytest tests/test_configuration_module.py::test_login_manager_success_and_lockout -v

# SafetyZone 테스트만
pytest tests/test_configuration_module.py::test_safety_zone_validation_and_persistence -v
```

### 키워드로 테스트 필터링

```bash
# "login"이 포함된 모든 테스트 실행
pytest tests/test_configuration_module.py -k login -v

# "manager"가 포함된 모든 테스트 실행
pytest tests/test_configuration_module.py -k manager -v
```

### 실패한 테스트만 재실행

```bash
pytest tests/test_configuration_module.py --lf -v
```

---

## 🐛 디버깅 옵션

### 상세한 출력 보기

```bash
# 더 자세한 트레이스백
pytest tests/test_configuration_module.py -vv

# print 문 출력 보기
pytest tests/test_configuration_module.py -v -s

# 실패 시 즉시 중단
pytest tests/test_configuration_module.py -v -x
```

### 특정 경고 무시

```bash
# DeprecationWarning 숨기기
pytest tests/test_configuration_module.py -v --disable-warnings
```

---

## 📝 테스트 작성 가이드

새로운 configuration 기능을 추가할 때는 `tests/test_configuration_module.py`에 테스트를 추가하세요:

```python
def test_my_new_feature(storage_manager):
    """새 기능에 대한 설명."""
    # Arrange: 테스트 데이터 준비
    # Act: 기능 실행
    # Assert: 결과 검증
    pass
```

### 테스트 작성 원칙:

1. **AAA 패턴 사용**: Arrange, Act, Assert
2. **독립성**: 각 테스트는 다른 테스트에 의존하지 않음
3. **명확한 이름**: 테스트 이름만 봐도 무엇을 테스트하는지 알 수 있게
4. **단일 책임**: 하나의 테스트는 하나의 기능만 검증

---

## 🔧 문제 해결

### pytest를 찾을 수 없다는 에러

```bash
# 가상환경이 활성화되었는지 확인
which python
# 출력: /Users/minjun/Desktop/cs350_safehome_team1/.venv/bin/python

# 가상환경 재활성화
source .venv/bin/activate
```

### 모듈을 찾을 수 없다는 에러

```bash
# PYTHONPATH 설정
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest tests/test_configuration_module.py -v
```

### 테스트 실패 시

1. 실패 메시지를 자세히 읽기
2. `-vv` 옵션으로 더 자세한 정보 확인
3. 해당 코드 파일 확인
4. 필요시 `print()` 디버깅 추가 후 `-s` 옵션으로 실행

---

## 📚 추가 리소스

- [pytest 공식 문서](https://docs.pytest.org/)
- [pytest-cov 문서](https://pytest-cov.readthedocs.io/)
- SafeHome SDS 문서: `docs/SDS_document.pdf`
- SafeHome SRS 문서: `docs/SRS_document.pdf`

---

## ✅ 체크리스트

코드 변경 후 다음을 확인하세요:

- [ ] 모든 테스트가 통과하는가?
- [ ] 커버리지가 75% 이상인가?
- [ ] 새로운 기능에 대한 테스트를 추가했는가?
- [ ] 린트 에러가 없는가?

```bash
# 전체 체크
source .venv/bin/activate
pytest tests/test_configuration_module.py -v --cov=safehome/configuration --cov-report=term-missing
```

---

**작성일**: 2025-11-25  
**버전**: 1.0  
**담당**: SafeHome Configuration Team

