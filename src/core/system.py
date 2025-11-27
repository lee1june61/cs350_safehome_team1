"""
SafeHome System - Main System Controller.
The central hub that coordinates all subsystems.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime


class System:
    """Main system controller for SafeHome."""
    
    def __init__(self):
        self._is_running = False
        self._current_mode = "DISARMED"
        self._current_user = None
        self._master_password = "1234"
        self._guest_password = "0000"
        self._web_password = "password"
    
    def turn_on(self):
        print("System: turn_on()")
        self._is_running = True
    
    def turn_off(self):
        print("System: turn_off()")
        self._is_running = False
    
    def reset(self):
        print("System: reset()")
        self.turn_off()
        self.turn_on()
    
    def login_control_panel(self, password: str) -> bool:
        if password == self._master_password:
            self._current_user = "master"
            return True
        elif password == self._guest_password:
            self._current_user = "guest"
            return True
        return False
    
    def login_web(self, user_id: str, password1: str, password2: str) -> bool:
        """Web login with two-level passwords"""
        if user_id and password1 == self._web_password and password2 == self._web_password:
            self._current_user = user_id
            return True
        return False
    
    def logout(self):
        self._current_user = None
    
    def arm_system(self, mode: str = "AWAY") -> bool:
        print(f"System: arm_system({mode})")
        self._current_mode = mode
        return True
    
    def disarm_system(self) -> bool:
        print("System: disarm_system()")
        self._current_mode = "DISARMED"
        return True
    
    def panic_button_pressed(self):
        print("System: PANIC! Calling monitoring service...")
    
    def get_alarm_state(self) -> str:
        return "INACTIVE"
    
    def is_running(self) -> bool:
        return self._is_running
    
    def get_current_user(self) -> Optional[str]:
        return self._current_user
    
    # Mock data methods
    def get_safety_zones(self) -> List[Dict[str, Any]]:
        return [
            {'id': 1, 'name': 'Front Door', 'armed': False},
            {'id': 2, 'name': 'Back Yard', 'armed': False},
        ]
    
    def get_all_sensors(self) -> List[Dict[str, Any]]:
        return [
            {'id': 1, 'type': 'DOOR', 'location': 'Front Door', 'armed': False},
            {'id': 2, 'type': 'WINDOW', 'location': 'Living Room', 'armed': False},
            {'id': 3, 'type': 'MOTION', 'location': 'Hallway', 'armed': False},
        ]
    
    def get_all_cameras(self) -> List[Dict[str, Any]]:
        return [
            {'id': 1, 'location': 'Front Door', 'enabled': True, 'has_password': False},
            {'id': 2, 'location': 'Back Yard', 'enabled': True, 'has_password': False},
            {'id': 3, 'location': 'Garage', 'enabled': False, 'has_password': True},
        ]
    
    def get_system_settings(self) -> Dict[str, Any]:
        return {'delay_time': 30, 'phone': '911'}
    
    def view_intrusion_log(self) -> List[Dict[str, Any]]:
        return [
            {'timestamp': '2024-01-15 10:30:00', 'event': 'Motion detected', 'zone': 'Hallway'},
            {'timestamp': '2024-01-14 22:15:00', 'event': 'Door opened', 'zone': 'Front Door'},
        ]
    
    def get_mode_configuration(self, mode: str) -> List[int]:
        return [1, 2, 3]
    
    # ============================================================
    # Request Handler
    # ============================================================
    
    def handle_request(self, source: str, command: str, **kwargs) -> Dict[str, Any]:
        """Handle request from Control Panel or Web Interface."""
        print(f"System: handle_request({source}, {command})")
        
        try:
            # === Authentication ===
            if command == 'login_control_panel':
                password = kwargs.get('password', '')
                success = self.login_control_panel(password)
                level = 'MASTER' if password == self._master_password else 'GUEST'
                return {'success': success, 'access_level': level if success else None}
            
            elif command == 'login_web':
                user_id = kwargs.get('user_id', '')
                pw1 = kwargs.get('password1', '')
                pw2 = kwargs.get('password2', '')
                success = self.login_web(user_id, pw1, pw2)
                return {'success': success}
            
            elif command == 'logout':
                self.logout()
                return {'success': True}
            
            elif command == 'change_password':
                self._master_password = kwargs.get('new_password', '1234')
                return {'success': True}
            
            # === System Lifecycle ===
            elif command == 'turn_off':
                self.turn_off()
                return {'success': True}
            
            elif command == 'reset_system':
                self.reset()
                return {'success': True}
            
            # === Security ===
            elif command == 'arm_system':
                mode = kwargs.get('mode', 'AWAY')
                return {'success': self.arm_system(mode)}
            
            elif command == 'disarm_system':
                return {'success': self.disarm_system()}
            
            elif command == 'panic':
                self.panic_button_pressed()
                return {'success': True}
            
            elif command == 'arm_zone':
                print(f"System: arm_zone({kwargs.get('zone_id')})")
                return {'success': True}
            
            elif command == 'disarm_zone':
                print(f"System: disarm_zone({kwargs.get('zone_id')})")
                return {'success': True}
            
            # === Status ===
            elif command == 'get_status':
                return {
                    'success': True,
                    'data': {
                        'armed': self._current_mode != 'DISARMED',
                        'mode': self._current_mode,
                        'alarm_state': self.get_alarm_state(),
                        'doors_windows_open': False,
                    }
                }
            
            # === Data Queries ===
            elif command == 'get_safety_zones':
                return {'success': True, 'data': self.get_safety_zones()}
            
            elif command == 'get_sensors':
                return {'success': True, 'data': self.get_all_sensors()}
            
            elif command == 'get_cameras':
                return {'success': True, 'data': self.get_all_cameras()}
            
            elif command == 'get_system_settings':
                return {'success': True, 'data': self.get_system_settings()}
            
            elif command == 'get_intrusion_log':
                return {'success': True, 'data': self.view_intrusion_log()}
            
            elif command == 'get_mode_configuration':
                mode = kwargs.get('mode', 'HOME')
                return {'success': True, 'data': self.get_mode_configuration(mode)}
            
            elif command == 'get_thumbnails':
                return {'success': True, 'data': {}}
            
            # === Modifications ===
            elif command == 'create_safety_zone':
                print(f"System: create_safety_zone({kwargs})")
                return {'success': True, 'zone_id': 99}
            
            elif command == 'update_safety_zone':
                print(f"System: update_safety_zone({kwargs})")
                return {'success': True}
            
            elif command == 'delete_safety_zone':
                print(f"System: delete_safety_zone({kwargs})")
                return {'success': True}
            
            elif command == 'configure_system_settings':
                print(f"System: configure_system_settings({kwargs})")
                return {'success': True}
            
            elif command == 'configure_safehome_mode':
                print(f"System: configure_safehome_mode({kwargs})")
                return {'success': True}
            
            # === Camera Controls ===
            elif command == 'camera_pan':
                print(f"System: camera_pan({kwargs})")
                return {'success': True}
            
            elif command == 'camera_zoom':
                print(f"System: camera_zoom({kwargs})")
                return {'success': True}
            
            elif command == 'enable_camera':
                print(f"System: enable_camera({kwargs})")
                return {'success': True}
            
            elif command == 'disable_camera':
                print(f"System: disable_camera({kwargs})")
                return {'success': True}
            
            elif command == 'set_camera_password':
                print(f"System: set_camera_password({kwargs})")
                return {'success': True}
            
            elif command == 'delete_camera_password':
                print(f"System: delete_camera_password({kwargs})")
                return {'success': True}
            
            else:
                print(f"System: Unknown command: {command}")
                return {'success': False, 'message': f'Unknown command: {command}'}
        
        except Exception as e:
            print(f"System: Error: {e}")
            return {'success': False, 'message': str(e)}
