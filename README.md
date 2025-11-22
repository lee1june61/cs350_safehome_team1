# SafeHome Project - Directory Structure

## Project Structure

```
safehome_team1/
├── src/
│   ├── __init__.py
│   │
│   ├── core/                          # 핵심 시스템 (모든 팀원 공용)
│   │   ├── __init__.py
│   │   ├── system.py                  # System 클래스
│   │   └── alarm.py                   # Alarm 클래스
│   │
│   ├── devices/                       # virtual_device_v3 통합
│   │   ├── __init__.py
│   │   ├── interfaces.py              # InterfaceCamera, InterfaceSensor
│   │   ├── camera.py                  # DeviceCamera
│   │   ├── motion_sensor.py           # DeviceMotionDetector
│   │   ├── window_door_sensor.py      # DeviceWinDoorSensor
│   │   └── control_panel_abstract.py  # DeviceControlPanelAbstract
│   │
│   ├── controllers/                   # 디바이스 컨트롤러
│   │   ├── __init__.py
│   │   ├── camera_controller.py       # CameraController
│   │   ├── sensor_controller.py       # SensorController
│   │   └── device_manager.py          # (새로 추가) 통합 관리
│   │
│   ├── models/                        # 데이터 모델 & 엔티티
│   │   ├── __init__.py
│   │   ├── sensor.py                  # Sensor, MotionSensor, WindowDoorSensor
│   │   ├── camera.py                  # SafeHomeCamera
│   │   ├── safety_zone.py             # SafetyZone
│   │   ├── safehome_mode.py           # SafeHomeMode
│   │   └── log.py                     # Log
│   │
│   ├── config/                        # 설정 및 데이터 관리
│   │   ├── __init__.py
│   │   ├── configuration_manager.py   # ConfigurationManager
│   │   ├── system_settings.py         # SystemSettings
│   │   ├── storage_manager.py         # StorageManager
│   │   └── log_manager.py             # LogManager
│   │
│   ├── auth/                          # 인증 & 보안
│   │   ├── __init__.py
│   │   ├── login_manager.py           # LoginManager
│   │   └── login_interface.py         # LoginInterface
│   │
│   ├── interfaces/                    # UI 인터페이스 (당신 파트!)
│   │   ├── __init__.py
│   │   │
│   │   └── control_panel/             # 제어판 UI
│   │       ├── __init__.py
│   │       └── safehome_control_panel.py  # SafeHomeControlPanel
│   │
│   └── utils/                         # 유틸리티
│       ├── __init__.py
│       ├── constants.py               # 상수 정의
│       ├── exceptions.py              # 커스텀 예외
│       └── helpers.py                 # 헬퍼 함수
│
├── tests/                             # 테스트 코드
│   ├── __init__.py
│   ├── test_system.py
│   ├── test_controllers.py
│   ├── test_auth.py
│   └── test_ui.py
│
├── resources/                         # 리소스 파일
│   ├── database/
│   │   └── schema.sql
│   ├── config/
│   │   └── default_config.ini
│   └── images/                        # UI 이미지
│       └── floor_plan.png
│
├── docs/                              # 문서
│   ├── SRS_document.docx
│   ├── SDS_document.docx
│   └── API.md
│
├── requirements.txt
├── README.md
└── .gitignore
```
