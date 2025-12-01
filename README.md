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
├── main.py                  # Launches both interfaces in a single process
└── tools/                   # Coverage reporters and build helpers
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

### Boot & Login Flow
1. Press `1` (`POWER`) → panel transitions from *OFF* to *NOT READY*.
2. Enter a 4-digit PIN → master access enables mode changes, guest access is limited (no settings edits).
3. After three failed attempts the keypad locks; wait for the configured lock duration or reset via the web UI.

### Keypad Map
| Key | Action |
| --- | --- |
| 1 | Power toggle |
| 2 | Disarm / turn system OFF |
| 3 | Reset (clears alarms/panic if authenticated) |
| 6 | Status scroll (cycles through zone text) |
| 7 | Arm AWAY |
| 8 | Arm HOME |
| 9 | CODE (start password change workflow) |
| `*` / `#` | Panic trigger (requires master PIN to clear) |

### Password Change (panel side)
1. Logged-in master presses `9`.
2. Panel requests current PIN → enter it.
3. Panel asks for new PIN twice.
4. Backend rejects:
   - Any PIN already used by the opposite role (`Pin reserved`).
   - Non-numeric input, length < 4, or lockout state.

### Indicator Cheatsheet
- **Display line 1**: mode or immediate instruction (`Enter PIN`, `Change failed`, etc.).
- **Display line 2**: masked PIN entry or extended status message.
- **LEDs**:  
  - `armed` (green) = system is in HOME or AWAY.  
  - `power` (green) = panel powered.  
  - `ready` (not ready indicator) toggles based on sensor states.

### Panic & Alarm Handling
1. Trigger panic with `*` or `#`.  
2. Siren state flips, `ALARM` flashes, and zones log an event.  
3. Enter master PIN + `2` to silence. Guest PINs cannot clear panic.

---

## Web Interface Handbook
The remote console mirrors what an operator would see.

### Login
Use the default credentials (`admin / password / password`). Session timeout is configurable; idle tabs auto-log out after the configured minutes.

### Primary Tabs
- **Dashboard**: live summary (current mode, alarm status, last events).
- **Safety Zone Page**:
  - Left column lists zones; selecting one loads associated sensors.
  - Buttons: `Arm`, `Disarm`, `Edit Sensors`, `Save`.
  - Camera thumbnail indicates if video is available.
- **Camera Pages**:
  - *Single View*: manipulate PTZ via on-screen buttons.
  - *Camera List*: toggle multiple cameras at once (enable/disable).
- **Security Page**:
  - Quick arm/disarm buttons that issue master commands.
  - Panic button duplicates the keypad panic feature.
- **View Log**:
  - Filter by date, event type, and export to CSV.
- **Configure System Setting Page**:
  - Update contact numbers, lock times, login attempts.
  - Change control-panel master/guest PINs (requires the current PINs for verification).

### Tips
- Every action posts feedback underneath the button. If you see `Pin reserved` or lockout errors, fix the underlying issue on the panel first.
- When editing settings, unsaved fields keep blue outlines; click `Save` or `Reset to default`.

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

HTML output lands in `htmlcov/index.html`. Open in a browser for color-coded line details.

### JSON & Markdown Coverage Helpers
1. Generate `coverage.json`:
   ```bash
   pytest --cov=src --cov-branch --cov-report=json
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
