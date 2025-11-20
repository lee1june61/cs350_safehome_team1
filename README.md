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
│   │   ├── system.py
│   │   └── constants.py
│   ├── configuration/
│   │   ├── __init__.py
│   │   ├── configuration_manager.py
│   │   ├── system_settings.py
│   │   ├── safehome_mode.py
│   │   ├── safety_zone.py
│   │   ├── storage_manager.py
│   │   ├── log.py
│   │   ├── log_manager.py
│   │   ├── login_interface.py
│   │   └── login_manager.py
│   ├── devices/
│   │   ├── __init__.py
│   │   ├── sensors/
│   │   │   ├── __init__.py
│   │   │   ├── interface_sensor.py
│   │   │   ├── sensor.py
│   │   │   ├── sensor_controller.py
│   │   │   ├── motion_sensor.py
│   │   │   ├── window_door_sensor.py
│   │   │   ├── device_motion_detector.py
│   │   │   ├── device_windoor_sensor.py
│   │   │   └── device_sensor_tester.py
│   │   ├── cameras/
│   │   │   ├── __init__.py
│   │   │   ├── interface_camera.py
│   │   │   ├── safehome_camera.py
│   │   │   ├── camera_controller.py
│   │   │   └── device_camera.py
│   │   └── alarm/
│   │       ├── __init__.py
│   │       └── alarm.py
│   ├── interfaces/
│   │   ├── __init__.py
│   │   └── control_panel/
│   │       ├── __init__.py
│   │       ├── device_control_panel_abstract.py
│   │       ├── control_panel.py
│   │       └── safehome_control_panel.py
│   └── utils/
│       ├── __init__.py
│       ├── database_utils.py
│       └── validation_utils.py
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_configuration/
│   │   │   ├── __init__.py
│   │   │   ├── test_configuration_manager.py
│   │   │   ├── test_login_manager.py
│   │   │   ├── test_log_manager.py
│   │   │   ├── test_safety_zone.py
│   │   │   └── test_safehome_mode.py
│   │   ├── test_devices/
│   │   │   ├── __init__.py
│   │   │   ├── test_sensor_controller.py
│   │   │   ├── test_camera_controller.py
│   │   │   ├── test_motion_sensor.py
│   │   │   ├── test_window_door_sensor.py
│   │   │   └── test_alarm.py
│   │   ├── test_interfaces/
│   │   │   ├── __init__.py
│   │   │   └── test_control_panel.py
│   │   └── test_core/
│   │       ├── __init__.py
│   │       └── test_system.py
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_login_process.py
│   │   ├── test_sensor_alarm_integration.py
│   │   ├── test_camera_integration.py
│   │   ├── test_configuration_integration.py
│   │   ├── test_arm_disarm_integration.py
│   │   ├── test_safety_zone_integration.py
│   │   └── test_system_startup_integration.py
│   └── system/
│       ├── __init__.py
│       ├── test_login_via_control_panel.py
│       ├── test_arm_disarm_system.py
│       └── test_alarm_scenarios.py
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
│   ├── example_camera.py
│   ├── example_control_panel.py
│   ├── example_all_sensors.py
│   └── README.md
├── scripts/
│   ├── setup_database.py
│   ├── run_tests.py
│   └── generate_coverage.py
└── .github/
    └── workflows/
        └── ci.yml
```
