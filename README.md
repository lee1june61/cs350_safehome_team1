# SafeHome Project

## 🎯 핵심 차이점: Control Panel vs Web Interface

### Control Panel (로컬 접근)
- ✅ **4자리 PIN** 인증
- ✅ **버튼만** (HOME/AWAY/CODE/PANIC)
- ✅ **Floor Plan 없음!**
- ✅ 로컬 하드웨어 접근
- ❌ 복잡한 설정 불가

### Web Interface (원격 접근)
- ✅ **User ID + 2단계 8자리** 비밀번호
- ✅ **Floor Plan 기반** 인터페이스
- ✅ Device 아이콘 클릭 제어
- ✅ Safety Zone 설정
- ✅ 카메라 감시
- ✅ 전체 시스템 설정

## 📁 새로운 프로젝트 구조

```
safehome_team1/
├── src/
│   ├── core/              # System & Alarm
│   ├── configuration/     # Configuration managers & models
│   ├── devices/           # Sensors & Cameras
│   └── ui/
│       ├── control_panel/   # LOCAL: 버튼만!
│       │   └── screens/
│       │       └── main_screen.py  # Floor Plan 제거됨
│       └── web_interface/   # REMOTE: Floor Plan 포함!
│           └── pages/
│               └── main_page.py    # Floor Plan 있음
│
├── virtual_device_v4/     # TA 제공 Virtual Device v4
├── tests/
├── docs/
└── scripts/
```

## 🔧 설치 방법

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. Virtual Device v4 확인
- `virtual_device_v4/` 폴더 확인
- TA가 제공한 최신 버전 사용

## 🚀 실행 방법

### Control Panel 실행 (로컬)
```bash
python main.py
# 또는
python scripts/run_control_panel.py
```

**기본 비밀번호:**
- Master: `1234`
- Guest: `5678`

### Web Interface 실행 (원격)
```bash
python -m src.ui.web_interface.app
# 또는
python scripts/run_web_interface.py
```

**기본 로그인:**
- User ID: `admin`
- Password 1: `password`
- Password 2: `password`

## 📊 주요 변경사항

### 1. Control Panel Main Screen 수정
**Before (잘못됨):**
```python
class MainScreen:
    def _create_floor_plan_panel(self):  # ❌ Control Panel에 있으면 안 됨!
        # Floor plan...
```

**After (올바름):**
```python
class MainScreen:
    def _create_control_buttons(self):   # ✅ 버튼만!
        # HOME/AWAY/CODE/PANIC
    def _create_status_display(self):    # ✅ 상태 표시 (텍스트만)
```

### 2. Web Interface에 Floor Plan 추가
```python
class MainPage:
    def _create_floor_plan_panel(self):  # ✅ Web Interface만!
        # Floor plan with device icons
    def add_device_icon(self, ...):      # ✅ Device 아이콘 추가
```

## 🧪 테스트

### 단위 테스트
```bash
pytest tests/unit/
```

### 통합 테스트
```bash
pytest tests/integration/
```

### 전체 테스트
```bash
pytest tests/
```

## 📚 SRS/SDS 참조

### Control Panel (SRS Section V.1.a)
- 4자리 비밀번호 ✅
- 버튼 인터페이스 ✅
- Floor Plan 없음 ✅

### Web Interface (SRS Section V.2, V.3)
- User ID + 2단계 비밀번호 ✅
- Floor Plan 표시 ✅
- Device 아이콘 클릭 ✅

## 📝 문서

- `docs/SRS_document.docx` - 요구사항 명세
- `docs/SDS_document.docx` - 설계 명세
- `docs/USER_MANUAL.md` - 사용자 매뉴얼
- `docs/TEST_DOCUMENT.docx` - 테스트 문서

## 👥 팀 구성

- 팀원 A: Core System & Alarm
- 팀원 B: Configuration & Data
- 팀원 C: Devices (Sensors & Cameras)
- 팀원 D: Control Panel UI
- 팀원 E: Web Interface

## ⚠️ 중요 사항

1. **Control Panel = 로컬 = 버튼만 (Floor Plan 없음!)**
2. **Web Interface = 원격 = Floor Plan 기반**
3. SRS/SDS 명세를 정확히 따름
4. PEP8 스타일 가이드 준수
5. Virtual Device v4 사용

## 🐛 트러블슈팅

### Control Panel이 시작되지 않음
```bash
# Python 버전 확인
python --version  # 3.8 이상 필요

# tkinter 확인
python -c "import tkinter"
```

### Floor Plan이 보이지 않음 (Web Interface)
- Web Interface에서만 정상
- Control Panel에서는 보이면 안 됨!

## 📞 지원

- SRS 문서 참조
- SDS 문서 참조
- Integration Test Cases 참조
- 팀원에게 문의

---

**중요:** Control Panel과 Web Interface는 완전히 다른 인터페이스입니다!
