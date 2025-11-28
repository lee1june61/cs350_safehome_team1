"""
PageRegistry - Central registry for all page classes
"""
from .pages.login_page import LoginPage
from .pages.major_function_page import MajorFunctionPage
from .pages.security_page import SecurityPage
from .pages.safety_zone_page import SafetyZonePage
from .pages.safehome_mode_page import SafeHomeModePage
from .pages.safehome_mode_configure_page import SafeHomeModeConfigurePage
from .pages.configure_system_setting_page import ConfigureSystemSettingPage
from .pages.surveillance_page import SurveillancePage
from .pages.camera_list_page import CameraListPage
from .pages.single_camera_view_page import SingleCameraViewPage
from .pages.thumbnail_view_page import ThumbnailViewPage
from .pages.view_log_page import ViewLogPage


PAGE_CLASSES = {
    'login': LoginPage,
    'major_function': MajorFunctionPage,
    'security': SecurityPage,
    'safety_zone': SafetyZonePage,
    'safehome_mode': SafeHomeModePage,
    'safehome_mode_configure': SafeHomeModeConfigurePage,
    'configure_system_setting': ConfigureSystemSettingPage,
    'surveillance': SurveillancePage,
    'camera_list': CameraListPage,
    'single_camera_view': SingleCameraViewPage,
    'thumbnail_view': ThumbnailViewPage,
    'view_log': ViewLogPage,
}


def get_page_class(page_name: str):
    return PAGE_CLASSES.get(page_name)


def get_all_page_names():
    return list(PAGE_CLASSES.keys())
