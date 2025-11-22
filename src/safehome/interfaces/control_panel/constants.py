"""Control Panel Constants.

UI-related constants for context-aware button functionality.
"""

# Panel States
STATE_IDLE = "IDLE"
STATE_ENTERING_PASSWORD = "ENTERING_PASSWORD"
STATE_LOGGED_IN = "LOGGED_IN"
STATE_ARMED_AWAY = "ARMED_AWAY"
STATE_ARMED_STAY = "ARMED_STAY"
STATE_LOCKED = "LOCKED"
STATE_ALARM = "ALARM"
STATE_CHANGE_PASSWORD = "CHANGE_PASSWORD"
STATE_ENTER_OLD_PASSWORD = "ENTER_OLD_PASSWORD"
STATE_ENTER_NEW_PASSWORD = "ENTER_NEW_PASSWORD"
STATE_CONFIRM_NEW_PASSWORD = "CONFIRM_NEW_PASSWORD"
STATE_DISARMING = "DISARMING"

# UI Configuration
PASSWORD_LENGTH = 4
MAX_LOGIN_ATTEMPTS = 3
PASSWORD_MASK_CHAR = "*"

# Display Messages - Login
MSG_READY = "SafeHome Ready"
MSG_ENTER_PASSWORD = "Enter Password"
MSG_LOGIN_OK = "Login OK"
MSG_WRONG_PASSWORD = "Wrong Password"
MSG_SYSTEM_LOCKED = "SYSTEM LOCKED"
MSG_WAIT = "Wait 5 minutes"

# Display Messages - Main Menu
MSG_MAIN_MENU = "Main Menu"
MSG_SELECT_FUNCTION = "Select Function"
MSG_ARM_MENU = "1:Away 2:Stay"
MSG_FUNCTION_MENU_1 = "3:Pass 4:Call"
MSG_FUNCTION_MENU_2 = "5:Set 9:Reset 0:Off"

# Display Messages - Armed
MSG_ARMED_AWAY = "ARMED - AWAY"
MSG_ARMED_STAY = "ARMED - STAY"
MSG_SYSTEM_DISARMED = "System Disarmed"
MSG_ENTER_TO_DISARM = "Enter code"
MSG_PRESS_EXIT = "Press # to exit"

# Display Messages - Password Change
MSG_CHANGE_PASSWORD = "Change Password"
MSG_ENTER_OLD_PASS = "Enter old code"
MSG_ENTER_NEW_PASS = "Enter new code"
MSG_CONFIRM_NEW_PASS = "Confirm new code"
MSG_PASSWORD_CHANGED = "Password Changed"
MSG_PASSWORD_MISMATCH = "Codes mismatch"

# Display Messages - System Control
MSG_SYSTEM_OFF = "System OFF"
MSG_SHUTTING_DOWN = "Shutting down..."
MSG_SYSTEM_RESET = "Resetting..."
MSG_PLEASE_WAIT = "Please wait"

# Display Messages - Monitoring
MSG_PANIC = "** PANIC **"
MSG_CALLING_SERVICE = "Calling Service..."
MSG_CALL_SERVICE = "Calling Service"
MSG_SERVICE_CALLED = "Service Called"

# Display Messages - Errors
MSG_CANNOT_CANCEL = "Cannot Cancel"
MSG_INPUT_CLEARED = "Input Cleared"
MSG_CANNOT_ARM = "Cannot Arm"
MSG_CHECK_SENSORS = "Check sensors"
MSG_LOGIN_FIRST = "Login first"
MSG_INVALID_OPTION = "Invalid Option"

# Demo Credentials (for demo mode only)
DEMO_MASTER_PASSWORD = "1234"
DEMO_GUEST_PASSWORD = "5678"

# Button Function Labels (for display)
BUTTON_LABELS = {
    'idle': {
        '0-9': 'Enter Password',
        '*': 'PANIC',
        '#': 'Clear'
    },
    'logged_in': {
        '1': 'Arm Away',
        '2': 'Arm Stay',
        '3': 'Change Pass',
        '4': 'Call Service',
        '5': 'Settings',
        '9': 'Reset',
        '0': 'Turn Off',
        '*': 'PANIC',
        '#': 'Logout'
    },
    'armed': {
        '0-9': 'Disarm Code',
        '*': 'PANIC',
        '#': 'Cancel'
    },
    'change_password': {
        '0-9': 'Enter Code',
        '*': 'PANIC',
        '#': 'Cancel'
    }
}