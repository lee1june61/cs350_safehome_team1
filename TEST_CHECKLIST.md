# SafeHome 시스템 테스트 체크리스트

본 문서는 SafeHome 시스템의 전체적인 테스트 시나리오를 정의합니다. 코드를 기반으로 작성되었으며, 각 페이지에서 표시되어야 할 **UI 요소**와 **기능 액션(버튼)**을 함께 정리했습니다.

모든 테스트는 **로그인 후** 진행하는 것을 기본으로 합니다.

---

## 1. 하드웨어 제어 패널 (Control Panel)

Control Panel은 하드웨어 키패드 시뮬레이션입니다. 

### UI 체크리스트 (표시 요소)
- [ ] **메시지 화면 (LCD):** 상단/하단 2줄 텍스트 표시 영역
- [ ] **LED:** Armed(보안 설정) 상태 표시등
- [ ] **키패드:** `0`~`9` 숫자 키, `*`, `#` 키
- [ ] **기능 버튼:** `ON`, `OFF`, `RESET`, `AWAY`, `HOME`, `CODE`

### 기능 테스트
#### 시스템 켜기 (ON 버튼)
- **버튼:** `ON` (숫자 키 1)
- **테스트 방법:** 시스템이 꺼진 상태에서 `1`번 키 클릭
- **기대 결과:** "Starting...", "Please wait" 메시지 점멸 후 "Enter password" 표시

#### 시스템 끄기 (OFF 버튼)
- **버튼:** `OFF` (숫자 키 3)
- **테스트 방법:** 로그인된 상태에서 `3`번 키 클릭
- **기대 결과:** "Stopping..." 메시지 후 시스템 종료

#### 비밀번호 입력 (숫자 키패드)
- **버튼:** `0` ~ `9` 키
- **테스트 방법:** 비밀번호 4자리 입력 (기본 Master: `1234`, Guest: `5678`)
- **기대 결과:**
  1. 입력 시마다 화면에 `*` 표시
  2. 4자리 입력 완료 시 자동 로그인 시도
  3. 성공: "Welcome (MASTER/GUEST)" 및 메뉴 표시
  4. 실패: "Wrong password" 및 남은 횟수 표시 (3회 실패 시 60초 Lock)

#### 비밀번호 변경 (CODE 버튼)
- **버튼:** `CODE` (숫자 키 9)
- **테스트 방법:** 로그인 후 `9`번 클릭 -> 새 비밀번호(4자리) 입력
- **기대 결과:** "New password:" 프롬프트 -> 입력 즉시 "Password changed" 완료

#### 보안 설정 (AWAY 버튼)
- **버튼:** `AWAY` (숫자 키 7)
- **테스트 방법:** 로그인 후 `7`번 클릭
- **기대 결과:** Armed LED(빨간불) 켜짐, 화면에 "Armed: AWAY" 표시

#### 보안 해제 (HOME 버튼)
- **버튼:** `HOME` (숫자 키 8)
- **테스트 방법:** Arm 상태에서 `8`번 클릭
- **기대 결과:** Armed LED 꺼짐(초록불), 화면에 "HOME mode" 표시

#### 비상 호출 (PANIC 버튼)
- **버튼:** `*` 또는 `#`
- **테스트 방법:** 아무 상태에서나 `*` 또는 `#` 클릭
- **기대 결과:** "PANIC!", "Calling service..." 메시지 표시

#### 리셋 (RESET 버튼)
- **버튼:** `RESET` (숫자 키 6)
- **테스트 방법:** 로그인 후 `6`번 클릭
- **기대 결과:** "Resetting..." 메시지 후 재부팅

---

## 2. 웹 로그인 (Login Page)

### UI 체크리스트
- [ ] **타이틀:** "SafeHome Login"
- [ ] **입력 필드:** User ID, Password 1, Password 2
- [ ] **메시지 영역:** 에러/상태 메시지 표시 라벨

### 기능 테스트
#### 로그인 (Login 버튼)
- **버튼:** `Login`
- **테스트 대상:**
  - Case 1: 정상 로그인 (ID: `admin`, PW1: `password`, PW2: `password`)
  - Case 2: 틀린 정보 입력
- **기대 결과:**
  - Case 1: 메인 화면(MajorFunctionPage)으로 이동
  - Case 2: "Failed. X left" 메시지 (3회 실패 시 잠김)

---

## 3. 메인 대시보드 (Major Function Page)

### UI 체크리스트
- [ ] **헤더:** "SafeHome", 현재 로그인 사용자, 로그아웃 버튼
- [ ] **상태 표시:** "● ARMED" (빨강) 또는 "● DISARMED" (초록)
- [ ] **메인 버튼 3개:** Security, Surveillance, Configure System Setting

### 기능 테스트
#### 시스템 설정 이동
- **버튼:** `Configure System Setting`
- **기대 결과:** 시스템 설정 페이지(ConfigureSystemSettingPage)로 이동

#### 감시 기능 이동
- **버튼:** `Surveillance Function`
- **기대 결과:** 감시 페이지(SurveillancePage)로 이동

#### 보안 기능 이동
- **버튼:** `Security Function`
- **기대 결과:** 보안 페이지(SecurityPage)로 이동

#### 로그아웃 (Logout 버튼)
- **버튼:** `Logout` (우측 상단)
- **기대 결과:** 로그인 화면으로 복귀

---

## 4. 시스템 설정 (System Settings)

### UI 체크리스트
- [ ] **Web Password 섹션:** Password 1 & 2 (각각 입력+확인 필드)
- [ ] **Control Panel Password 섹션:** Master & Guest (각각 입력+확인 필드)
- [ ] **Alarm/Monitor 섹션:** Delay Time, Phone Number 입력 필드
- [ ] **하단 버튼:** Save, Reset Defaults

### 기능 테스트
#### 저장 (Save 버튼)
- **버튼:** `Save` (또는 Submit)
- **테스트 항목:** 아래 값들을 입력 후 저장
  - Web Password 1 & 2
  - Master / Guest Password
  - Delay Time (5분 이상)
  - Phone Number
- **기대 결과:** "Settings saved successfully" 메시지 표시

#### 초기화 (Reset Defaults 버튼)
- **버튼:** `Reset Defaults`
- **기대 결과:** 입력 필드가 기본값(Delay 5, Phone 911 등)으로 복구됨 (저장 전 상태)

---

## 5. 보안 관리 (Security Page)

**주의:** 이 페이지의 기능 버튼들은 본인 인증 전까지 비활성화(Gray) 상태여야 합니다.

### UI 체크리스트
- [ ] **인증 섹션:** "Identity Confirmation" (입력창 + Verify 버튼)
- [ ] **기능 버튼들:** Safety Zone, Set SafeHome Mode, View Intrusion Log, Redefine Security Modes (초기엔 비활성화)

### 기능 테스트
#### 본인 인증 (Verify 버튼)
- **버튼:** `Verify`
- **입력:** 전화번호 또는 주소 입력
- **기대 결과:** "Verified" 메시지(초록색)와 함께 하단 4개 버튼 활성화

#### 구역 관리 이동 (Safety Zone)
- **버튼:** `Safety Zone`
- **기대 결과:** SafetyZonePage로 이동

#### 모드 설정 이동 (Set SafeHome Mode)
- **버튼:** `Set SafeHome Mode`
- **기대 결과:** SafeHomeModePage로 이동

#### 로그 확인 이동 (View Intrusion Log)
- **버튼:** `View Intrusion Log`
- **기대 결과:** ViewLogPage로 이동

#### 모드 정의 이동 (Redefine Security Modes)
- **버튼:** `Redefine Security Modes`
- **기대 결과:** SafeHomeModeConfigurePage로 이동

---

## 6. 보안 구역 관리 (Safety Zone Page)

### UI 체크리스트
- [ ] **좌측 패널:** 평면도 (Floor Plan), 선택된 센서 정보 표시
- [ ] **우측 패널:** 구역 목록(Listbox), 구역 관리 버튼들 (Create, Delete, Update, Arm, Disarm)

### 기능 테스트
#### 구역 생성 (Create Zone 버튼)
- **버튼:** `Create New Zone` -> 맵에서 센서 선택 -> `Finish`
- **테스트 대상:**
  - `S1`, `S3`, `S4`, `S6` (창문), `S2`, `S5` (문), `M1`~`M2` (동작) 중 선택하여 구역 생성
- **기대 결과:** 구역 목록에 새 구역 추가됨

#### 구역 삭제 (Delete Zone 버튼)
- **버튼:** 구역 선택 -> `Delete Zone`
- **기대 결과:** 팝업 확인 후 목록에서 삭제됨

#### 구역 수정 (Update Zone 버튼)
- **버튼:** 구역 선택 -> `Update Zone` -> 센서 변경 -> `Finish`
- **기대 결과:** 구역의 센서 구성이 변경됨

#### 개별 구역 Arm/Disarm
- **버튼:** 구역 선택 -> `Arm` / `Disarm`
- **기대 결과:** 해당 구역의 상태만 변경됨 (평면도 색상 변화 확인)

#### 구역 생성 및 Arm 유효성 검사 (Validation)
- **버튼:** `Create Zone`
- **테스트 방법:**
  1. **구역 이름 중복:** 이미 존재하는 이름을 입력하고 저장 -> "Same safety zone exists" 메시지 표시.
  2. **센서 미선택:** 이름만 입력하고 센서를 선택하지 않은 상태로 저장 -> "Select new safety zone and type safety zone name" 또는 "Select at least one sensor" 메시지 표시.
  3. **이름 누락:** 센서는 선택했으나 이름 입력 없이 저장 -> "Zone name required" 메시지 표시.
- **버튼:** `Arm Zone`
- **테스트 방법:**
  1. **창문 열림:** 해당 구역에 포함된 창문/문 센서를 클릭해 열림 상태로 만든 뒤 Arm 시도 -> "Doors and windows not closed" 메시지와 함께 Arm 실패.
  2. **공유 센서:** 여러 구역이 공유하는 센서가 포함된 경우, 모든 구역이 Disarm 될 때까지 해당 센서가 Arm 상태(빨간색)를 유지하는지 확인.

---

## 7. 보안 모드 설정 (SafeHome Mode Page)

### UI 체크리스트
- [ ] **현재 상태:** "Current Status" 라벨
- [ ] **모드 선택:** 라디오 버튼 (HOME, AWAY, OVERNIGHT, EXTENDED)
- [ ] **제어 버튼:** Apply Mode, Arm All, Disarm All

### 기능 테스트
#### 모드 선택 및 적용
- **버튼:** 라디오 버튼(`HOME`, `AWAY` 등) -> `Apply Mode`
- **테스트 대상 모드:**
  - `HOME`: 재택 모드
  - `AWAY`: 외출 모드
  - `OVERNIGHT`: 취침 모드
  - `EXTENDED`: 장기 외출 모드
- **기대 결과:** 시스템 상태가 해당 모드로 변경됨 ("ARMED - [MODE]" 표시)

#### 전체 Arm/Disarm (Quick Buttons)
- **버튼:** `Arm All` / `Disarm All`
- **기대 결과:** 즉시 모든 구역이 Arm 또는 Disarm 됨

---

## 8. 감시/카메라 (Surveillance Page)

### UI 체크리스트
- [ ] **좌측 패널:** 평면도 (Floor Plan) - 클릭 가능한 카메라 아이콘
- [ ] **우측 패널:** 카메라 목록(Listbox), "Pick a Camera" / "All Cameras" 버튼

### 기능 테스트
#### 전체 보기 (All Cameras 버튼)
- **버튼:** `All cameras`
- **기대 결과:** 썸네일 그리드 화면(ThumbnailViewPage) 로드

#### 개별 선택 (목록/지도 클릭)
- **버튼:** 리스트의 항목 또는 지도의 카메라 아이콘(`C1`, `C2`, `C3`) 클릭
- **기대 결과:** 해당 카메라의 상세 화면(SingleCameraViewPage) 로드

---

## 9. 카메라 상세 제어 (Single Camera View)

아래 테스트는 **카메라 C1, C2, C3 각각에 대해** 반복 수행하세요.

### UI 체크리스트
- [ ] **비디오 영역:** 실시간(시뮬레이션) 영상 표시 프레임
- [ ] **Info 패널:** ID, 위치, Pan/Tilt/Zoom 값, 상태(On/Off), 비밀번호 여부
- [ ] **제어 패널:** PTZ 버튼, Enable/Disable, Password 설정 버튼

### 기능 테스트
#### 팬/틸트/줌 (PTZ 버튼)
- **버튼:**
  - Pan: `◄ L`, `R ►`
  - Tilt: `↑ Up`, `↓ Down`
  - Zoom: `+ In`, `- Out`
- **테스트 대상:** C1, C2, C3 모두
- **기대 결과:** 화면의 수치(Pan/Tilt/Zoom)가 변경됨

#### 활성화/비활성화 (Enable/Disable 버튼)
- **버튼:** `Enable` / `Disable`
- **기대 결과:** 카메라 상태(On/Off)가 변경됨. Off 시 영상 안 나옴.

#### 비밀번호 설정 (Set Password 버튼)
- **버튼:** `Set Password` -> 새 비밀번호 입력
- **기대 결과:** Info 패널에 "Password: Yes"로 변경됨. 이후 접근 시 비밀번호 요구함.

#### 비밀번호 삭제 (Delete Password 버튼)
- **버튼:** `Delete Password` -> 기존 비밀번호 입력
- **기대 결과:** Info 패널에 "Password: No"로 변경됨.

---

## 10. 로그 및 네비게이션

### UI 체크리스트
- [ ] **로그 테이블:** 시간, 센서 ID, 이벤트 타입 표시
- [ ] **네비게이션:** 상단 헤더, `< Back` 버튼

### 기능 테스트
#### 로그 새로고침 (Refresh 버튼)
- **위치:** ViewLogPage
- **기대 결과:** 최신 침입 기록 표시

#### 로그 지우기 (Clear Log 버튼)
- **위치:** ViewLogPage
- **기대 결과:** 화면 목록 초기화

#### 뒤로 가기 (Back 버튼)
- **위치:** 각 서브 페이지 좌측 상단 (`< Back`)
- **테스트:** Security, Surveillance, Config 페이지 등에서 클릭
- **기대 결과:** 상위 메뉴(MajorFunctionPage 또는 SecurityPage)로 이동

---

## 11. 심화 및 예외 테스트 (Advanced & Edge Cases)

기본 기능 외에 시스템의 **예외 처리** 및 **데이터 연동**을 검증하는 테스트입니다.

### 11-1. 예외 상황 처리 (Negative Testing)
#### Arming 실패 조건 (창문 열림)
- **설정:** 평면도(Floor Plan)에서 `S1` 창문 센서를 클릭하여 'Open' 상태로 만듦 (빨간색)
- **액션:** Control Panel `AWAY` 버튼 또는 SafeHomeModePage `Apply Mode`
- **기대 결과:** "Doors and windows not closed" 에러 메시지와 함께 Arming 실패

#### 구역 생성 예외 (입력 누락)
- **위치:** Safety Zone Page -> `Create New Zone`
- **액션 1:** 이름을 비워두고 저장 -> **기대 결과:** "Zone name required" 경고
- **액션 2:** 센서를 하나도 선택하지 않고 저장 -> **기대 결과:** "Select at least one sensor" 경고

#### 중복 데이터 처리
- **위치:** Safety Zone Page
- **액션:** 이미 존재하는 구역 이름(예: "Living Room")으로 새 구역 생성 시도
- **기대 결과:** "Zone name already exists" 경고 및 생성 거부

### 11-2. 통합 시나리오 (End-to-End Flow)
#### 침입 감지 및 로그 기록
1. **준비:** 시스템 `AWAY` 모드로 설정 (Arm)
2. **침입:** 평면도에서 `M1` (동작 센서) 클릭하여 감지 상태로 변경
3. **확인:** Control Panel에 "ALARM!" 메시지 표시되는지 확인
4. **검증:** Web -> Security -> `View Intrusion Log` 진입 시, 방금 발생한 침입 기록(시간, M1, Motion Detected)이 리스트에 있는지 확인

#### 비밀번호 변경 연동 확인
1. **변경:** Web -> Config 페이지에서 `Master Password`를 `9999`로 변경 및 저장
2. **검증:** Control Panel로 이동하여 구 비밀번호(`1234`) 입력 시 로그인 실패, 새 비밀번호(`9999`) 입력 시 성공 확인

### 11-3. 데이터 영속성 (Persistence)
#### 재시작 후 설정 유지 확인
1. **설정:** Web -> Config 페이지에서 `Delay Time`을 `10`분으로 변경 후 저장
2. **종료:** 프로그램 전체 종료 (`python main.py` 중단)
3. **재시작:** 프로그램 다시 실행
4. **검증:** Web -> Config 페이지 진입 시 `Delay Time`이 `10`으로 유지되어 있는지 확인
