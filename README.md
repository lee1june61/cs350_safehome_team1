# SafeHome Project (Team 1)

## 📋 Project Overview
SafeHome is a smart home system that manages home security through a local Control Panel and a remote Web Interface.

## 🎯 Key Features

### Control Panel (Local Access)
- **Simplified Interface**: Simulates physical buttons (keypad style).
- **Security Authentication**: Uses a 4-digit PIN.
- **Functions**:
  - System ON/OFF
  - Security Mode Setting (HOME/AWAY)
  - Change Password
  - Emergency Alert (PANIC)
- **Characteristics**: No Floor Plan is displayed; uses text-based status indicators.

### Web Interface (Remote Access)
- **Graphical Interface**: Visual monitoring based on Floor Plan.
- **Security Authentication**: User ID + 2-step password.
- **Functions**:
  - Full system status monitoring
  - Control sensors and cameras per Safety Zone
  - View real-time camera feeds (Simulated)

## 📁 Project Structure
```
safehome_team1/
├── src/
│   ├── core/              # Core System Logic (System, Alarm, Handlers)
│   ├── configuration/     # System Configuration & Data Management
│   ├── controllers/       # Device Controllers (Camera, etc.)
│   ├── devices/           # Real/Virtual Device Implementations
│   ├── interfaces/        # User Interfaces
│   │   ├── control_panel/   # Local Control Panel UI
│   │   └── web_interface/   # Web Interface UI
│   ├── virtual_devices/   # Virtual Hardware Modules (Sensors, Cameras, etc.)
│   └── utils/             # Utilities and Constants
├── main.py                # Program Entry Point
├── requirements.txt       # Dependency List
└── tests/                 # Test Code (Unit, Integration)
```

## 🚀 Installation and Execution

### 1. Prerequisites
- Python 3.8 or higher
- `tkinter` (Usually included with Python installation)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Program
Execute the following command in the project root directory. Both the Control Panel and Web Interface will launch simultaneously.
```bash
python main.py
```

## 🎮 User Guide

### Control Panel (Local)
1. **Start**: The system is initially OFF when the program starts. Press the `1` button to turn the system ON.
2. **Login**: Enter the 4-digit PIN.
   - **Master Password**: `1234`
   - **Guest Password**: `5678`
3. **Commands**:
   - `7`: **AWAY** Mode (Arm all sensors)
   - `8`: **HOME** Mode (Disarm internal sensors)
   - `9`: **CODE** (Change password)
   - `2`: **OFF** (Turn off system)
   - `3`: **RESET** (Reset system)
   - `*` or `#`: **PANIC** (Trigger immediate alarm)

### Web Interface (Remote)
Login with the following credentials:
- **User ID**: `admin`
- **Password 1**: `password`
- **Password 2**: `password`

## 🧪 Testing
To verify the stability of the project, run the following commands:

```bash
# Run all tests
pytest

# View detailed results
pytest -v

# Generate coverage report
pytest --cov=src tests/
```

## ⚠️ Notes
- **Control Panel** simulates local hardware devices; operate the buttons by clicking with your mouse.
- **Web Interface** simulates remote access; interact by clicking icons on the Floor Plan.
- Both interfaces share a single `System` core instance to synchronize state.
