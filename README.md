# SafeHome Project · Team 1 Field Manual

> “Flip the switch, watch every zone, and keep both interfaces honest.”  
This document is meant to be a living operations guide. Treat it like a miniature encyclopedia for everything that happens inside `safehome_team1`.

---

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture at a Glance](#architecture-at-a-glance)
3. [Environment Setup](#environment-setup)
4. [Launching SafeHome](#launching-safehome)
5. [Data & Defaults](#data--defaults)
6. [Control Panel Handbook](#control-panel-handbook)
7. [Web Interface Handbook](#web-interface-handbook)
8. [System Settings & Password Policy](#system-settings--password-policy)
9. [Testing, Coverage & Tooling](#testing-coverage--tooling)
10. [Troubleshooting & FAQ](#troubleshooting--faq)
11. [Developer Notes](#developer-notes)

---

## System Overview
SafeHome is a dual-interface residential security platform. The **Control Panel** simulates the wall-mounted keypad used by homeowners, while the **Web Interface** behaves like a monitoring portal that an off-site operator would use. Both surfaces talk to the same in-memory system core, so every keystroke and browser click updates a single truth source.

Key goals:
- Reproduce a realistic arm/disarm flow with lockouts, panic triggers, and per-zone sensors.
- Keep master and guest identities distinct, including unique PIN rules and lockout timers.
- Provide testability: every meaningful service is isolated to allow deterministic unit and integration tests.

---

## Architecture at a Glance
```
safehome_team1/
├── src/
│   ├── core/                # Alarm logic, handlers, orchestration services
│   ├── configuration/       # Persistent settings, login interfaces, storage access
│   ├── controllers/         # Translators between UI events and device models
│   ├── devices/             # Physical/virtual device abstractions (sensors, cams)
│   ├── interfaces/
│   │   ├── control_panel/   # Tkinter keypad UI + state machine
│   │   └── web_interface/   # Tkinter pseudo-browser for remote operator
│   ├── virtual_devices/     # Sensor/camera simulators used by controllers
│   └── utils/               # Misc helpers and constants
├── tests/                   # Unit + integration suites
└── main.py                  # Launches both interfaces in a single process
```

- **Core services** (auth, alarm, settings) expose command handlers that the interfaces call through a registry.  
- **Configuration layer** persists state to `safehome.db` via `StorageManager`; the default DB ships with sample users, zones, and sensors.  
- **Interfaces** are intentionally Tkinter-based so the project stays cross-platform and easy to grade.

---

## Environment Setup
1. **Python Version**: 3.8+ (3.10 recommended). `tkinter` must be available; on Windows/macOS it ships with CPython, on some Linux distros install `python3-tk`.
2. **Virtual Environment (recommended)**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   ```
3. **Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **SQLite Tools (optional)**: install `sqlite3` CLI if you plan to inspect `safehome.db`.

---

## Launching SafeHome
From `safehome_team1/`:
```bash
python main.py
```
Two windows appear:
1. **Control Panel**: keypad on the left, indicator LEDs on the bottom.  
2. **Web Interface**: multi-tab window showing the floor plan, logs, and configuration pages.

Shut down both windows (or the Python process) to stop the system. State persists because the SQLite DB is updated live.

---

## Data & Defaults
- **Login database**: `safehome_team1/safehome.db` holds users, hashed PINs, lockout counters, and system settings.
- **Default Control Panel PINs**
  - Master: `1234`
  - Guest: `5678`
  - The system enforces *unique* PINs; trying to reuse the other role’s PIN returns `Pin reserved`.
- **Web credentials**
  - User ID: `admin`
  - Password 1 / Password 2: both `password`
  - Monitoring Phone: `010-1234-1234`
- **Alarm settings**: See `configuration/system_settings.py` for defaults (delay time, lockouts, session timeout, etc.).

If the DB becomes inconsistent during testing, delete `safehome.db` and rerun the app—`ConfigurationManager` seeds a fresh copy.

---

## Control Panel Handbook
The keypad is driven by a state machine under `interfaces/control_panel/control_panel_states/`.

### 1. Turning the System On/Off
- **Power On**: Press `1` (POWER) when the display is OFF. The `Power` LED (Green) will light up, and the screen will read `READY` or `NOT READY`.
- **Power Off**: Press `1` again. The LED turns off.
- **Disarm / Idle**: If an alarm is sounding or the system is armed, enter your PIN + `2` (OFF) to return to idle state.

### 2. Logging In & Access Levels
- **Master Access**: Enter `1234` (default). Allows Arming, Disarming, Panic, and Password Changes.
- **Guest Access**: Enter `5678` (default). Allows Arming/Disarming only. Cannot change settings or clear panic states.
- **Lockout**: After 3 failed attempts, the keypad locks for 60 seconds.

### 3. Arming the System
- **Away Mode (All Sensors)**:
  1. Ensure `Ready` LED is Green (all zones closed).
  2. Press `7` (AWAY).
  3. Enter PIN.
  4. System arms; `Armed` LED lights up.
- **Home Mode (Perimeter Only)**:
  1. Press `8` (HOME).
  2. Enter PIN.
  3. System arms; `Armed` LED lights up.

### 4. Handling Alarms (Intrusion / Panic)
- **Triggering Panic**: Press `*` or `#`. The screen flashes `ALARM` and sirens activate.
- **Clearing Alarm**:
  1. Enter **Master PIN**.
  2. Press `2` (OFF).
  3. The alarm silences and the system disarms.

### 5. Changing the Panel PIN
*(Master users only)*
1. Log in with Master PIN.
2. Press `9` (CODE).
3. Screen prompts for **Current PIN**. Enter it.
4. Screen prompts for **New PIN**. Enter the new 4-digit code.
5. Screen prompts to **Confirm**. Re-enter the new code.
6. Success: "Password Changed". Failure: "Change Failed" or "Pin reserved" (if it duplicates the guest PIN).

---

## Web Interface Handbook
The remote console mirrors what an operator would see. Use `admin / password / password` to log in.

### 1. Dashboard & Monitoring
- **Dashboard**: Overview of current system state (Armed/Disarmed), Alarm status, and recent event log.
- **Status Display**: The top-right widget always reflects the current core state (e.g., `AWAY`, `HOME`, `ALARM`).

### 2. Managing Safety Zones
Navigate to the **Safety Zone Page**.
1. **Select a Zone**: Click a zone name in the left sidebar (e.g., "Living Room").
2. **Edit Sensors**: Click the `Edit Sensors` button. A dialog appears.
   - **Add**: Choose a sensor type (Motion, Door, Window) and click Add.
   - **Remove**: Select a sensor from the list and click Remove.
   - **Save**: Click Save to persist changes.
3. **Arm/Disarm Zone**: Use the `Arm` or `Disarm` buttons in the right panel to toggle that specific zone's state.

### 3. Camera Control & Locking
Navigate to **Single Camera View** or **Camera List**.
- **Viewing**: Click a camera to see its live feed (simulated static image).
- **PTZ Control**: Use the arrow buttons and Zoom +/- to adjust the view.
- **Locking/Unlocking**:
  - If a camera is locked, you will see a "LOCKED" banner.
  - **Unlock**: Click the camera/banner -> Enter password.
  - **Lock**: Failing the password 3 times locks the camera for 60 seconds globally (on both web and single-view pages).
- **Password Management**: Use `Set Password` or `Delete Password` to secure a camera feed.

### 4. Security Actions
Navigate to the **Security Page**.
- **Quick Arming**: Click `Arm Home` or `Arm Away`. Triggers the same flow as the keypad.
- **Panic Button**: Click `Panic` to trigger the system-wide alarm. Requires Master PIN on the keypad to clear.

### 5. System Configuration
Navigate to **Configure System Setting Page**.
- **Contact Info**: Update Homeowner or Monitoring Center phone numbers.
- **Timers**: Adjust `Entry Delay`, `Exit Delay`, or `Lockout Duration`.
- **Change PINs**:
  - You can update the Control Panel's Master/Guest PINs here.
  - Requires entering the *current* PIN for verification.
  - **Rule**: Master and Guest PINs must be unique.

---

## System Settings & Password Policy
- **Unique PIN rule**: The backend compares proposed master and guest PINs. Matching values are rejected with `Pin reserved`. This applies both when editing through the Control Panel and the Configure System Setting page.
- **Lockout policy**: Set via *System Lock Time* and *Max Login Attempts*. These values drive the `LockManager` used by both interfaces.
- **Contact information**: Updating monitor/homeowner numbers also refreshes the identity verification service so notifications go to the right phone.
- **Factory reset**:
  - From the web UI, click *Reset to default*.  
  - Internally calls `SettingsHandler.reset_settings`, resets timers, and re-applies default master (`1234`) / guest (`5678`) PINs.

---

## Testing, Coverage & Tooling
### Core Commands
```bash
# Run entire suite
pytest

# Focus on integration tests
pytest tests/integration -v

# Coverage with branch metrics + HTML
pytest --cov=src --cov-branch --cov-report=term-missing --cov-report=html
```

### Linting
We rely on `pytest` plugins for static checks. If you add flake8 or ruff locally, run them from the repo root so relative imports resolve correctly.

---

## Troubleshooting & FAQ
**Q: The Control Panel shows “Change failed / Pin reserved”. What happened?**  
A: You attempted to assign the same 4-digit PIN to both master and guest roles. Use a unique value for each.

**Q: “Must be logged in” appears when changing a PIN.**  
A: You are not authenticated, or `current_password` was empty. Enter the active PIN before choosing a new one.

**Q: Panel is stuck because of lockout. How do I recover?**  
- Wait for the configured `system_lock_time`, or  
- In the Configure System Setting page, lower the lock duration or reset to defaults.

**Q: Web interface buttons stop responding.**  
A: The session likely expired. Log out/in or restart `main.py`. Check the terminal for stack traces if the Tk window froze.

**Q: How do I inspect the database?**  
```bash
sqlite3 safehome_team1/safehome.db
sqlite> .tables
sqlite> SELECT * FROM login_interfaces;
```
Always exit the CLI before restarting the app to avoid locking the DB file.

---

## Developer Notes
- **Command Registry**: `src/core/command_registry.py` wires service methods to string keys. Interfaces call `send_request("command_name", **params)`; add new commands here.
- **Logging**: `SystemLogger` writes to in-memory buffers. Extend it to output to disk if needed for audits.
- **Extending Devices**: add virtual sensors/cameras under `virtual_devices/`, then expose them through controllers and zone definitions.
- **Testing strategy**: prefer deterministic unit tests in `tests/unit/` for new services, then add integration coverage to verify UI-level flows.
- **CI hooks** (if integrating elsewhere): run `pytest --maxfail=1` first for fast feedback, then the full coverage suite.

When in doubt, start the app (`python main.py`), reproduce the scenario, and watch the terminal output—handlers print meaningful logs whenever passwords, settings, or zones change.

Happy securing! 🛡️
