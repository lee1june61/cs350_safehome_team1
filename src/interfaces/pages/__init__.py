"""
SafeHome Pages Package

All UI pages for web interface.
"""
from .login_page import LoginPage
from .major_function_page import MajorFunctionPage
from .security_page import SecurityPage
from .safety_zone_page import SafetyZonePage
from .safehome_mode_page import SafeHomeModePage
from .safehome_mode_configure_page import SafeHomeModeConfigurePage
from .configure_system_setting_page import ConfigureSystemSettingPage
from .phone_number_validation_page import PhoneNumberValidationPage
from .surveillance_page import SurveillancePage
from .camera_list_page import CameraListPage
from .single_camera_view_page import SingleCameraViewPage
from .thumbnail_view_page import ThumbnailViewPage
from .view_log_page import ViewLogPage

# Action mixins
from .safety_zone_actions import SafetyZoneActionsMixin
from .security_actions import SecurityActionsMixin
from .camera_controls import CameraControlsMixin
from .status_display import StatusDisplayMixin

__all__ = [
    'LoginPage',
    'MajorFunctionPage',
    'SecurityPage',
    'SafetyZonePage',
    'SafeHomeModePage',
    'SafeHomeModeConfigurePage',
    'ConfigureSystemSettingPage',
    'PhoneNumberValidationPage',
    'SurveillancePage',
    'CameraListPage',
    'SingleCameraViewPage',
    'ThumbnailViewPage',
    'ViewLogPage',
    'SafetyZoneActionsMixin',
    'SecurityActionsMixin',
    'CameraControlsMixin',
    'StatusDisplayMixin',
]
