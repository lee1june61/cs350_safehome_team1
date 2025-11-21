# SafeHome Project - Directory Structure

## Project Structure

```
safehome/
├── README.md
├── requirements.txt
├── setup.py
├── docs/
│   ├── SDS_document.pdf
│   ├── SRS_document.pdf
│   ├── Implementation_and_Testing.pdf
│   └── user_manual.pdf
├── safehome/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── system.py                              # System
│   │   └── constants.py                           # Enums, Constants
│   ├── configuration/
│   │   ├── __init__.py
│   │   ├── configuration_manager.py               # ConfigurationManager
│   │   ├── system_settings.py                     # SystemSettings
│   │   ├── safehome_mode.py                       # SafeHomeMode
│   │   ├── safety_zone.py                         # SafetyZone
│   │   ├── storage_manager.py                     # StorageManager
│   │   ├── log.py                                 # Log
│   │   ├── log_manager.py                         # LogManager
│   │   ├── login_interface.py                     # LoginInterface
│   │   └── login_manager.py                       # LoginManager
│   ├── devices/
│   │   ├── __init__.py
│   │   ├── sensors/
│   │   │   ├── __init__.py
│   │   │   ├── interface_sensor.py                # InterfaceSensor (ABC)
│   │   │   ├── sensor.py                          # Sensor
│   │   │   ├── sensor_controller.py               # SensorController
│   │   │   ├── motion_sensor.py                   # MotionSensor (extends Sensor)
│   │   │   ├── window_door_sensor.py              # WindowDoorSensor (extends Sensor)
│   │   │   ├── device_motion_detector.py          # DeviceMotionDetector
│   │   │   ├── device_windoor_sensor.py           # DeviceWinDoorSensor
│   │   │   └── device_sensor_tester.py            # DeviceSensorTester (ABC)
│   │   ├── cameras/
│   │   │   ├── __init__.py
│   │   │   ├── interface_camera.py                # InterfaceCamera (ABC)
│   │   │   ├── safehome_camera.py                 # SafeHomeCamera
│   │   │   ├── camera_controller.py               # CameraController
│   │   │   └── device_camera.py                   # DeviceCamera (Thread)
│   │   └── alarm/
│   │       ├── __init__.py
│   │       └── alarm.py                           # Alarm
│   ├── interfaces/
│   │   ├── __init__.py
│   │   └── control_panel/
│   │       ├── __init__.py
│   │       ├── device_control_panel_abstract.py   # DeviceControlPanelAbstract (ABC, Toplevel)
│   │       ├── control_panel.py                   # ControlPanel
│   │       └── safehome_control_panel.py          # SafeHomeControlPanel
│   └── utils/
│       ├── __init__.py
│       ├── database_utils.py                      # Database utility functions
│       └── validation_utils.py                    # Validation utility functions
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_configuration/
│   │   │   ├── __init__.py
│   │   │   ├── test_configuration_manager.py      # TestConfigurationManager
│   │   │   ├── test_login_manager.py              # TestLoginManager
│   │   │   ├── test_log_manager.py                # TestLogManager
│   │   │   ├── test_safety_zone.py                # TestSafetyZone
│   │   │   └── test_safehome_mode.py              # TestSafeHomeMode
│   │   ├── test_devices/
│   │   │   ├── __init__.py
│   │   │   ├── test_sensor_controller.py          # TestSensorController
│   │   │   ├── test_camera_controller.py          # TestCameraController
│   │   │   ├── test_motion_sensor.py              # TestMotionSensor
│   │   │   ├── test_window_door_sensor.py         # TestWindowDoorSensor
│   │   │   └── test_alarm.py                      # TestAlarm
│   │   ├── test_interfaces/
│   │   │   ├── __init__.py
│   │   │   └── test_control_panel.py              # TestControlPanel
│   │   └── test_core/
│   │       ├── __init__.py
│   │       └── test_system.py                     # TestSystem
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_login_process.py                  # TestLoginProcess
│   │   ├── test_sensor_alarm_integration.py       # TestSensorAlarmIntegration
│   │   ├── test_camera_integration.py             # TestCameraIntegration
│   │   ├── test_configuration_integration.py      # TestConfigurationIntegration
│   │   ├── test_arm_disarm_integration.py         # TestArmDisarmIntegration
│   │   ├── test_safety_zone_integration.py        # TestSafetyZoneIntegration
│   │   └── test_system_startup_integration.py     # TestSystemStartupIntegration
│   └── system/
│       ├── __init__.py
│       ├── test_login_via_control_panel.py        # TestLoginViaControlPanel
│       ├── test_arm_disarm_system.py              # TestArmDisarmSystem
│       └── test_alarm_scenarios.py                # TestAlarmScenarios
├── resources/
│   ├── images/
│   │   ├── camera1.jpg
│   │   ├── camera2.jpg
│   │   └── camera3.jpg
│   ├── database/
│   │   ├── schema.sql
│   │   └── initial_data.sql
│   └── config/
│       ├── default_config.json
│       └── test_config.json
├── examples/
│   ├── __init__.py
│   ├── example_camera.py                          # Camera demo with GUI
│   ├── example_control_panel.py                   # TestControlPanel (example impl)
│   ├── example_all_sensors.py                     # Sensor demo
│   └── README.md
├── scripts/
│   ├── setup_database.py
│   ├── run_tests.py
│   └── generate_coverage.py
└── .github/
    └── workflows/
        └── ci.yml
```
