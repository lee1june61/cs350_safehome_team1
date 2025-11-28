"""UI configuration constants."""


class UIConfig:
    """UI constants and styling configuration."""

    # Window settings
    WINDOW_WIDTH = 1100
    WINDOW_HEIGHT = 800
    WINDOW_TITLE = "SafeHome Control Panel"
    WINDOW_BG = "#f0f0f0"

    # Colors
    COLOR_PRIMARY = "#2196F3"
    COLOR_SUCCESS = "#4CAF50"
    COLOR_DANGER = "#f44336"
    COLOR_WARNING = "#FF9800"
    COLOR_INFO = "#FFC107"
    COLOR_WHITE = "white"
    COLOR_BLACK = "black"
    COLOR_GRAY = "#BDBDBD"
    COLOR_GRAY_DARK = "#616161"
    COLOR_LIGHT_BLUE = "#E3F2FD"

    # Device colors
    COLOR_SENSOR_ARMED = "#FF5722"
    COLOR_SENSOR_ARMED_OUTLINE = "#C62828"
    COLOR_SENSOR_DISARMED = "#BDBDBD"
    COLOR_SENSOR_DISARMED_OUTLINE = "#616161"

    COLOR_MOTION_ARMED = "#2196F3"
    COLOR_MOTION_ARMED_OUTLINE = "#1565C0"
    COLOR_MOTION_DISARMED = "#90CAF9"
    COLOR_MOTION_DISARMED_OUTLINE = "#42A5F5"

    COLOR_CAMERA_ENABLED = "#4CAF50"
    COLOR_CAMERA_ENABLED_OUTLINE = "#2E7D32"
    COLOR_CAMERA_DISABLED = "#BDBDBD"
    COLOR_CAMERA_DISABLED_OUTLINE = "#616161"

    COLOR_SELECTION = "yellow"

    # Icon sizes
    ICON_SIZE = 25
    ICON_HOVER_SIZE = 32

    # Canvas settings
    CANVAS_WIDTH = 670
    CANVAS_HEIGHT = 420
    CANVAS_BG = "white"

    # Fonts
    FONT_TITLE = ("Arial", 32, "bold")
    FONT_SUBTITLE = ("Arial", 24, "bold")
    FONT_HEADER = ("Arial", 14, "bold")
    FONT_BUTTON = ("Arial", 11, "bold")
    FONT_BUTTON_SMALL = ("Arial", 8)
    FONT_LABEL = ("Arial", 10)
    FONT_LABEL_SMALL = ("Arial", 8)
    FONT_PASSWORD = ("Arial", 24)
    FONT_KEYPAD = ("Arial", 18, "bold")

    # Layout
    PADDING_SMALL = 5
    PADDING_MEDIUM = 10
    PADDING_LARGE = 20

    # Control panel specific
    CONTROL_PANEL_WIDTH = 280
    BUTTON_WIDTH = 22
    BUTTON_WIDTH_SMALL = 12
    BUTTON_HEIGHT = 2

    # Password
    PASSWORD_LENGTH = 4
    PASSWORD_MAX_ATTEMPTS = 3

    # Timing
    BOOT_DELAY_MS = 2000
