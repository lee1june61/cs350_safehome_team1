"""
Integration Tests for Interface Components

Tests complete flows: login, security, camera operations
Run: cd safehome_team1 && python -m pytest tests/unit/test_interfaces/test_integration.py -v
"""
import pytest


class TestLoginFlow:
    """Integration tests for login flows"""
    
    def test_web_login_success(self, web_interface, mock_system):
        """Test web login success flow"""
        result = web_interface.send_message(
            'login_web', 
            user_id='admin',
            password1='password', 
            password2='password'
        )
        assert result['success'] == True
    
    def test_web_login_failure(self, web_interface, mock_system):
        """Test web login failure with wrong password"""
        result = web_interface.send_message(
            'login_web',
            user_id='admin',
            password1='wrong',
            password2='wrong'
        )
        assert result['success'] == False
        assert 'attempts_remaining' in result
    
    def test_logout(self, web_interface, mock_system):
        """Test logout flow"""
        web_interface.send_message(
            'login_web',
            user_id='admin',
            password1='password',
            password2='password'
        )
        result = web_interface.send_message('logout')
        assert result['success'] == True


class TestSecurityFlow:
    """Integration tests for security operations"""
    
    def test_arm_disarm_flow(self, web_interface, mock_system):
        """Test arm and disarm flow"""
        arm_result = web_interface.send_message('arm_system', mode='AWAY')
        assert arm_result['success'] == True
        
        status_after_arm = web_interface.send_message('get_status')
        assert status_after_arm['data']['armed'] == True
        
        disarm_result = web_interface.send_message('disarm_system')
        assert disarm_result['success'] == True
        
        status_after_disarm = web_interface.send_message('get_status')
        assert status_after_disarm['data']['armed'] == False
    
    def test_panic_trigger(self, web_interface, mock_system):
        """Test panic alarm trigger"""
        panic_result = web_interface.send_message('panic')
        assert panic_result['success'] == True
        
        status = web_interface.send_message('get_status')['data']
        assert status['state'] == 'ALARM'
    
    def test_safety_zone_operations(self, web_interface, mock_system):
        """Test safety zone operations"""
        # Login so zone operations are authorized
        login = web_interface.send_message(
            "login_web", user_id="admin", password1="password", password2="password"
        )
        assert login["success"] is True

        # Get zones
        result = web_interface.send_message('get_safety_zones')
        assert len(result['data']) >= 2
        
        # Create zone
        result = web_interface.send_message(
            'create_safety_zone',
            name='Test Zone',
            sensors=['S1']
        )
        assert result['success'] == True
        
        # Arm zone
        zone_id = result['zone_id']
        result = web_interface.send_message(
            'arm_zone',
            zone_id=zone_id
        )
        assert result['success'] == True


class TestCameraFlow:
    """Integration tests for camera operations"""
    
    def test_camera_list(self, web_interface, mock_system):
        """Test getting camera list"""
        result = web_interface.send_message('get_cameras')
        assert len(result['data']) == 3
    
    def test_camera_enable_disable(self, web_interface, mock_system):
        """Test enable/disable camera"""
        result = web_interface.send_message('disable_camera', camera_id='C1')
        assert result['success'] == True
        
        result = web_interface.send_message('enable_camera', camera_id='C1')
        assert result['success'] == True
    
    def test_camera_password_verify(self, web_interface, mock_system):
        """Test camera password verification"""
        result = web_interface.send_message(
            'verify_camera_password',
            camera_id='C2',
            password=''
        )
        assert result['success'] == True
    
    def test_camera_password_wrong(self, web_interface, mock_system):
        """Test wrong camera password"""
        # First, set a password
        web_interface.send_message('set_camera_password', camera_id='C2', old_password="", password='123')
        # Then, try to verify with a wrong one
        result = web_interface.send_message(
            'verify_camera_password',
            camera_id='C2',
            password='wrong'
        )
        assert result['success'] == False


class TestSystemSettings:
    """Integration tests for system settings"""
    
    def test_get_settings(self, web_interface, mock_system):
        """Test getting system settings"""
        result = web_interface.send_message('get_system_settings')
        assert result['success'] == True
        assert 'delay_time' in result['data']
    
    def test_configure_settings(self, web_interface, mock_system):
        """Test configuring settings"""
        result = web_interface.send_message(
            'configure_system_settings',
            delay_time=60
        )
        assert result['success'] == True
    
    def test_get_intrusion_logs(self, web_interface, mock_system):
        """Test getting intrusion logs"""
        web_interface.send_message('panic')
        result = web_interface.send_message('get_intrusion_log')
        assert result['success'] == True
        assert len(result['data']) >= 1


class TestMockSystem:
    """Tests for the System class itself"""
    
    def test_system_state_changes(self, mock_system):
        """Test that system state changes correctly after commands"""
        status = mock_system.handle_request('test', 'get_status')['data']
        assert status['armed'] == False
        
        mock_system.handle_request('test', 'arm_system', mode='AWAY')
        
        status = mock_system.handle_request('test', 'get_status')['data']
        assert status['armed'] == True
    
    def test_unknown_command(self, mock_system):
        """Test handling unknown command"""
        result = mock_system.handle_request('web', 'unknown_cmd')
        assert 'Unknown' in result['message']
