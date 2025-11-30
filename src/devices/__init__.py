"""SafeHome devices namespace with lazy attribute exports."""

from importlib import import_module

__all__ = [
    "InterfaceCamera",
    "InterfaceSensor",
    "DeviceCamera",
    "SafeHomeCamera",
    "CustomDeviceCamera",
    "CustomMotionDetector",
    "CustomWinDoorSensor",
    "DeviceSensorTester",
    "DeviceWinDoorSensor",
    "DeviceMotionDetector",
    "DeviceControlPanelAbstract",
    "Sensor",
    "WindowDoorSensor",
    "MotionSensor",
    "SensorController",
    "Alarm",
]

_EXPORTS = {
    "InterfaceCamera": "src.devices.interfaces:InterfaceCamera",
    "InterfaceSensor": "src.devices.interfaces:InterfaceSensor",
    "DeviceCamera": "src.devices.cameras.device_camera:DeviceCamera",
    "SafeHomeCamera": "src.devices.cameras.safehome_camera:SafeHomeCamera",
    "CustomDeviceCamera": "src.devices.custom_device_camera:CustomDeviceCamera",
    "CustomMotionDetector": "src.devices.custom_motion_detector:CustomMotionDetector",
    "CustomWinDoorSensor": "src.devices.custom_window_door_sensor:CustomWinDoorSensor",
    "DeviceSensorTester": "src.devices.sensors.device_sensor_tester:DeviceSensorTester",
    "DeviceWinDoorSensor": "src.devices.sensors.device_windoor_sensor:DeviceWinDoorSensor",
    "DeviceMotionDetector": "src.devices.sensors.device_motion_detector:DeviceMotionDetector",
    "DeviceControlPanelAbstract": "src.devices.control_panel_abstract:DeviceControlPanelAbstract",
    "Sensor": "src.devices.sensors.sensor:Sensor",
    "WindowDoorSensor": "src.devices.sensors.window_door_sensor:WindowDoorSensor",
    "MotionSensor": "src.devices.sensors.motion_sensor:MotionSensor",
    "SensorController": "src.devices.sensors.sensor_controller:SensorController",
    "Alarm": "src.devices.alarm.alarm:Alarm",
}


def __getattr__(name):
    target = _EXPORTS.get(name)
    if not target:
        raise AttributeError(f"module 'src.devices' has no attribute {name!r}")
    module_name, attr_name = target.split(":")
    module = import_module(module_name)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value


def __dir__():
    return sorted(__all__)
