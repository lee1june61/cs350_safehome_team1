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

### Control Panel Workflows
1. **Power On & Login**
   - System boots in `OFF`. Press `1` to power up, then enter a 4-digit PIN.
   - Default codes: Master `1234`, Guest `5678`.
2. **Arming & Disarming**
   - `7` → **AWAY** (all sensors armed).
   - `8` → **HOME** (perimeter only).
   - `2` → **OFF`**, `3` → **RESET** to return to idle if something goes wrong.
3. **Changing the Panel PIN**
   - Press `9 (CODE)` once logged in → enter current PIN → enter new PIN twice.
4. **Panic / Emergency**
   - Press `*` or `#` to trigger panic.
   - Control Panel screen flashes `ALARM`; enter master PIN to clear.
5. **LED & Message Indicators**
   - Short message lines show current mode/errors.
   - Watch the armed (green) and not-ready (red) LEDs while issuing commands.

### Web Interface Workflows
Use `admin / password / password` to log in (user ID, password 1, password 2).

| Goal | Navigation & Steps |
| --- | --- |
| **Monitor system summary** | `Main Page` → check widgets for mode, alarm, recent events. |
| **Manage sensors & zones** | `Safety Zone Page` → select a zone from the left list, use `Edit Sensors` to add/remove devices, click `Save` to persist. |
| **Zone arming** | Same page → use `Arm`/`Disarm` buttons in the right panel; status label confirms results. |
| **Camera control** | `Single Camera View` or `Camera List` → pick a camera, use PTZ buttons (`Pan`, `Tilt`, `Zoom`) or enable/disable toggles. |
| **Security actions** | `Security Page` → use `Arm Home/Away` or `Panic` buttons; follow on-screen verification dialogs. |
| **View logs & history** | `View Log` page to filter by date and export records. |
| **Configure system settings** | `Configure System Setting Page` → adjust contact info, monitoring numbers, and save/reset via the top-right actions. |

## 🧪 Testing & Coverage

### Common Test Commands
```bash
# Quick sanity test run
pytest

# Verbose output for debugging
pytest -v

# Branch-aware coverage with terminal summary and HTML report
pytest --cov=src --cov-branch --cov-report=term-missing --cov-report=html
```

The HTML report is written to `htmlcov/index.html`; open it in a browser to drill down to specific files.

### Method-Level Coverage Drill-Down
While `coverage.py` reports line coverage by default, you can inspect per-function/method metrics in two ways:

1. **HTML detail view**  
   - Run `pytest --cov=src --cov-branch --cov-report=html`.  
   - Open `htmlcov/<module>.py.html`. Each function header lists executed / missing lines, giving a quick method-level snapshot.

2. **XML/JSON exports for tooling**  
   - Run `pytest --cov=src --cov-branch --cov-report=xml --cov-report=json`.  
   - Import `coverage.xml` (or `coverage.json`) into IDE plugins such as VS Code Coverage Gutters or CI dashboards—these files include per-function statistics you can filter/sort.

For ad-hoc inspection of a single module, you can run `coverage run -m pytest tests/unit/... && coverage report src/path/to/file.py` to limit the output to the methods you care about.

#### JSON-Based Method Coverage (scripted)
If you prefer a table that lists **every method in a file with its covered / missing lines**, use the helper script we ship in `tools/method_coverage_json.py`:

```bash
# 1) Produce coverage.json (the script uses this file)
pytest --cov=. --cov-report=json

# 2) Generate the method-level table for a given module
python tools/method_coverage_json.py \
  --file src/interfaces/pages/safety_zone_page/zone_manager.py
#     (you can also pass paths without the leading src/, e.g. --file interfaces/pages/... )
```

The script parses the module via `ast`, cross-references `coverage.json`, and prints a Markdown table such as:

```
| Method | Total | Covered | Missing | Coverage |
| --- | ---: | ---: | ---: | ---: |
| __init__ | 12 | 12 | 0 | 100.0% |
| handle_device_click_info | 20 | 18 | 2 | 90.0% |
...
```

Use `--format json` if you prefer machine-readable output, or point `--file` at any other module that appears in `coverage.json`.

#### Class-Level Coverage
Need a class-by-class breakdown like `ConfigurationManager`, `StorageManager`, etc.? Run the companion script `tools/class_coverage_json.py`:

```bash
# make sure coverage.json is fresh
pytest --cov=. --cov-report=json

# produce Markdown for every file beneath src/interfaces/pages/
python tools/class_coverage_json.py \
  --path-prefix src/interfaces/pages/ \
  --output class_coverage_report.md

# or focus on a single module
python tools/class_coverage_json.py \
  --file interfaces/pages/safehome_mode_configure_page/safehome_mode_configure_page.py
```

Use `--format json` to emit machine-readable output or pass `--output somefile.md` to save the Markdown tables.

## ⚠️ Notes
- **Control Panel** simulates local hardware devices; operate the buttons by clicking with your mouse.
- **Web Interface** simulates remote access; interact by clicking icons on the Floor Plan.
- Both interfaces share a single `System` core instance to synchronize state.
