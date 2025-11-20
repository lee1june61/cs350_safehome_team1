safehome/
│
├── README.md # Project overview and setup instructions
├── requirements.txt # Python dependencies
├── setup.py # Package installation configuration
│
├── docs/ # Documentation
│ ├── SDS_document.pdf # Software Design Specification
│ ├── SRS_document.pdf # Software Requirements Specification
│ ├── Implementation_and_Testing.pdf # Implementation and testing documentation
│ └── user_manual.pdf # End-user documentation
│
├── safehome/ # Main application package
│ ├── **init**.py
│ │
│ ├── main.py # Application entry point
│ │
│ ├── core/ # Core system components
│ │ ├── **init**.py
│ │ ├── system.py # System class (main controller)
│ │ └── constants.py # System-wide constants and enums
│ │
│ ├── configuration/ # Configuration and data management
│ │ ├── **init**.py
│ │ ├── configuration_manager.py # ConfigurationManager class
│ │ ├── system_settings.py # SystemSettings class
│ │ ├── safehome_mode.py # SafeHomeMode class
│ │ ├── safety_zone.py # SafetyZone class
│ │ ├── storage_manager.py # StorageManager class (database access)
│ │ ├── log.py # Log class
│ │ ├── log_manager.py # LogManager class
│ │ ├── login_interface.py # LoginInterface class
│ │ └── login_manager.py # LoginManager class
│ │
│ ├── devices/ # Device management (sensors, cameras, alarm)
│ │ ├── **init**.py
│ │ │
│ │ ├── sensors/ # Sensor-related classes
│ │ │ ├── **init**.py
│ │ │ ├── interface_sensor.py # InterfaceSensor (abstract)
│ │ │ ├── sensor.py # Sensor base class
│ │ │ ├── sensor_controller.py # SensorController class
│ │ │ ├── motion_sensor.py # MotionSensor class
│ │ │ ├── window_door_sensor.py # WindowDoorSensor class
│ │ │ ├── device_motion_detector.py # DeviceMotionDetector (hardware wrapper)
│ │ │ ├── device_windoor_sensor.py # DeviceWinDoorSensor (hardware wrapper)
│ │ │ └── device_sensor_tester.py # DeviceSensorTester base class
│ │ │
│ │ ├── cameras/ # Camera-related classes
│ │ │ ├── **init**.py
│ │ │ ├── interface_camera.py # InterfaceCamera (abstract)
│ │ │ ├── safehome_camera.py # SafeHomeCamera class
│ │ │ ├── camera_controller.py # CameraController class
│ │ │ └── device_camera.py # DeviceCamera (hardware wrapper)
│ │ │
│ │ └── alarm/ # Alarm-related classes
│ │ ├── **init**.py
│ │ └── alarm.py # Alarm class
│ │
│ ├── interfaces/ # User interfaces
│ │ ├── **init**.py
│ │ │
│ │ └── control_panel/ # Control Panel interface
│ │ ├── **init**.py
│ │ ├── device_control_panel_abstract.py # Base control panel GUI
│ │ ├── control_panel.py # ControlPanel class (logic)
│ │ └── safehome_control_panel.py # SafeHomeControlPanel class
│ │
│ └── utils/ # Utility modules
│ ├── **init**.py
│ ├── database_utils.py # Database helper functions
│ └── validation_utils.py # Input validation utilities
│
├── tests/ # Test suite
│ ├── **init**.py
│ │
│ ├── unit/ # Unit tests
│ │ ├── **init**.py
│ │ ├── test_configuration/
│ │ │ ├── **init**.py
│ │ │ ├── test_configuration_manager.py
│ │ │ ├── test_login_manager.py
│ │ │ ├── test_log_manager.py
│ │ │ ├── test_safety_zone.py
│ │ │ └── test_safehome_mode.py
│ │ │
│ │ ├── test_devices/
│ │ │ ├── **init**.py
│ │ │ ├── test_sensor_controller.py
│ │ │ ├── test_camera_controller.py
│ │ │ ├── test_motion_sensor.py
│ │ │ ├── test_window_door_sensor.py
│ │ │ └── test_alarm.py
│ │ │
│ │ ├── test_interfaces/
│ │ │ ├── **init**.py
│ │ │ └── test_control_panel.py
│ │ │
│ │ └── test_core/
│ │ ├── **init**.py
│ │ └── test_system.py
│ │
│ ├── integration/ # Integration tests
│ │ ├── **init**.py
│ │ ├── test_login_process.py
│ │ ├── test_sensor_alarm_integration.py
│ │ ├── test_camera_integration.py
│ │ └── test_configuration_integration.py
│ │
│ └── system/ # System-level tests
│ ├── **init**.py
│ ├── test_login_via_control_panel.py
│ ├── test_arm_disarm_system.py
│ └── test_alarm_scenarios.py
│
├── resources/ # Resource files
│ ├── images/ # Image assets
│ │ ├── camera1.jpg # Camera feed images
│ │ ├── camera2.jpg
│ │ └── camera3.jpg
│ │
│ ├── database/ # Database files and schemas
│ │ ├── schema.sql # Database schema definition
│ │ └── initial_data.sql # Initial seed data
│ │
│ └── config/ # Configuration files
│ ├── default_config.json # Default system configuration
│ └── test_config.json # Test environment configuration
│
├── examples/ # Example scripts and demonstrations
│ ├── **init**.py
│ ├── example_camera.py # Camera demonstration
│ ├── example_control_panel.py # Control panel demonstration
│ ├── example_all_sensors.py # Sensor demonstration
│ └── README.md # Examples documentation
│
├── scripts/ # Utility scripts
│ ├── setup_database.py # Database initialization script
│ ├── run_tests.py # Test runner script
│ └── generate_coverage.py # Coverage report generator
│
└── .github/ # GitHub specific files (optional)
└── workflows/
└── ci.yml # Continuous integration configuration
