"""Tests for CameraControlsManager - 브랜치 커버리지 향상"""

import pytest
from unittest.mock import Mock, MagicMock, patch

from src.interfaces.pages.camera_controls_manager import CameraControlsManager


class TestCameraControlsManager:
    """CameraControlsManager의 모든 브랜치를 커버하는 테스트"""
    
    @pytest.fixture
    def mock_page(self):
        """Mock page instance"""
        page = Mock()
        page.send_to_system = Mock()
        return page
    
    @pytest.fixture
    def mock_cam_id_ref(self):
        """Mock camera ID reference"""
        ref = Mock()
        ref.get_cam_id = Mock(return_value="CAM001")
        return ref
    
    @pytest.fixture
    def mock_widgets(self):
        """Mock tkinter widgets"""
        info_label = Mock()
        info_label.config = Mock()
        info_label.cget = Mock(return_value="")
        
        enable_btn = Mock()
        enable_btn.config = Mock()
        enable_btn.cget = Mock(return_value='normal')
        
        disable_btn = Mock()
        disable_btn.config = Mock()
        disable_btn.cget = Mock(return_value='normal')
        
        return info_label, enable_btn, disable_btn
    
    @pytest.fixture
    def manager(self, mock_page, mock_cam_id_ref, mock_widgets):
        """Create CameraControlsManager instance"""
        info_label, enable_btn, disable_btn = mock_widgets
        return CameraControlsManager(
            mock_page, 
            mock_cam_id_ref, 
            info_label, 
            enable_btn, 
            disable_btn
        )
    
    # 2-1 패턴: pan/zoom 테스트 (기본 경로)
    def test_pan_calls_system_and_updates(self, manager, mock_page):
        """pan 메서드가 시스템 호출 후 업데이트하는지 확인"""
        mock_page.send_to_system.return_value = {'success': True, 'data': {
            'id': 'CAM001', 'location': (100, 200), 'pan': 10, 'zoom': 1,
            'enabled': True, 'password': None
        }}
        
        manager.pan('left')
        
        mock_page.send_to_system.assert_any_call('camera_pan', camera_id='CAM001', direction='left')
        assert mock_page.send_to_system.call_count >= 2  # pan + update_info
    
    def test_zoom_calls_system_and_updates(self, manager, mock_page):
        """zoom 메서드가 시스템 호출 후 업데이트하는지 확인"""
        mock_page.send_to_system.return_value = {'success': True, 'data': {
            'id': 'CAM001', 'location': (100, 200), 'pan': 0, 'zoom': 2,
            'enabled': True, 'password': None
        }}
        
        manager.zoom('in')
        
        mock_page.send_to_system.assert_any_call('camera_zoom', camera_id='CAM001', direction='in')
    
    # 2-1 패턴: if/else - enable 성공/실패 브랜치
    @patch('tkinter.messagebox.showinfo')
    def test_enable_success_branch(self, mock_showinfo, manager, mock_page):
        """enable 성공 브랜치 테스트 (if res.get('success'))"""
        mock_page.send_to_system.return_value = {'success': True}
        
        manager.enable()
        
        mock_showinfo.assert_called_once_with("Success", "Camera enabled")
        mock_page.send_to_system.assert_any_call('enable_camera', camera_id='CAM001')
    
    @patch('tkinter.messagebox.showerror')
    def test_enable_failure_branch(self, mock_showerror, manager, mock_page):
        """enable 실패 브랜치 테스트 (else)"""
        mock_page.send_to_system.return_value = {'success': False, 'message': 'Camera not found'}
        
        manager.enable()
        
        mock_showerror.assert_called_once_with("Error", "Camera not found")
    
    @patch('tkinter.messagebox.showerror')
    def test_enable_failure_no_message(self, mock_showerror, manager, mock_page):
        """enable 실패 시 메시지가 없는 경우 (기본 메시지 사용)"""
        mock_page.send_to_system.return_value = {'success': False}
        
        manager.enable()
        
        mock_showerror.assert_called_once_with("Error", "Failed to enable camera")
    
    # 2-1 패턴: if/else - disable 성공/실패 브랜치
    @patch('tkinter.messagebox.showinfo')
    def test_disable_success_branch(self, mock_showinfo, manager, mock_page):
        """disable 성공 브랜치 테스트"""
        mock_page.send_to_system.return_value = {'success': True}
        
        manager.disable()
        
        mock_showinfo.assert_called_once_with("Success", "Camera disabled")
    
    @patch('tkinter.messagebox.showerror')
    def test_disable_failure_branch(self, mock_showerror, manager, mock_page):
        """disable 실패 브랜치 테스트"""
        mock_page.send_to_system.return_value = {'success': False, 'message': 'Permission denied'}
        
        manager.disable()
        
        mock_showerror.assert_called_once_with("Error", "Permission denied")
    
    # 2-1 패턴: nested if - set_password의 여러 브랜치
    @patch('tkinter.simpledialog.askstring')
    @patch('tkinter.messagebox.showinfo')
    def test_set_password_success_all_branches(self, mock_showinfo, mock_askstring, manager, mock_page):
        """set_password 성공 브랜치 (if pw: 진입, if success: 진입)"""
        mock_askstring.side_effect = ['newpass123', 'oldpass']
        mock_page.send_to_system.return_value = {'success': True}
        
        manager.set_password()
        
        mock_page.send_to_system.assert_any_call(
            'set_camera_password', 
            camera_id='CAM001', 
            old_password='oldpass', 
            password='newpass123'
        )
        mock_showinfo.assert_called_once_with("Success", "Password set")
    
    @patch('tkinter.simpledialog.askstring')
    @patch('tkinter.messagebox.showerror')
    def test_set_password_failure_branch(self, mock_showerror, mock_askstring, manager, mock_page):
        """set_password 실패 브랜치 (if success: False)"""
        mock_askstring.side_effect = ['newpass123', 'wrongold']
        mock_page.send_to_system.return_value = {'success': False, 'message': 'Wrong old password'}
        
        manager.set_password()
        
        mock_showerror.assert_called_once_with("Error", "Wrong old password")
    
    @patch('tkinter.simpledialog.askstring')
    def test_set_password_cancelled_branch(self, mock_askstring, manager, mock_page):
        """set_password 취소 브랜치 (if pw: False - 비밀번호 입력 안 함)"""
        mock_askstring.return_value = None  # User cancelled
        
        manager.set_password()
        
        # send_to_system이 호출되지 않아야 함 (if pw 브랜치 진입 안 함)
        mock_page.send_to_system.assert_not_called()
    
    @patch('tkinter.simpledialog.askstring')
    def test_set_password_empty_string_branch(self, mock_askstring, manager, mock_page):
        """set_password 빈 문자열 브랜치 (if pw: False - empty string은 falsy)"""
        mock_askstring.return_value = ''  # Empty string
        
        manager.set_password()
        
        # if pw: 조건에서 빈 문자열은 False이므로 send_to_system 호출 안 됨
        mock_page.send_to_system.assert_not_called()
    
    # 2-1 패턴: delete_password의 여러 브랜치 (if old is not None)
    @patch('tkinter.simpledialog.askstring')
    @patch('tkinter.messagebox.showinfo')
    def test_delete_password_success_branch(self, mock_showinfo, mock_askstring, manager, mock_page):
        """delete_password 성공 브랜치 (if old is not None: 진입, if success: 진입)"""
        mock_askstring.return_value = 'correctpass'
        mock_page.send_to_system.return_value = {'success': True}
        
        manager.delete_password()
        
        mock_page.send_to_system.assert_any_call(
            'delete_camera_password',
            camera_id='CAM001',
            old_password='correctpass'
        )
        mock_showinfo.assert_called_once_with("Success", "Password deleted")
    
    @patch('tkinter.simpledialog.askstring')
    @patch('tkinter.messagebox.showerror')
    def test_delete_password_failure_branch(self, mock_showerror, mock_askstring, manager, mock_page):
        """delete_password 실패 브랜치 (if success: False)"""
        mock_askstring.return_value = 'wrongpass'
        mock_page.send_to_system.return_value = {'success': False}
        
        manager.delete_password()
        
        mock_showerror.assert_called_once_with("Error", "Wrong password")
    
    @patch('tkinter.simpledialog.askstring')
    def test_delete_password_cancelled_branch(self, mock_askstring, manager, mock_page):
        """delete_password 취소 브랜치 (if old is not None: False)"""
        mock_askstring.return_value = None  # User cancelled
        
        manager.delete_password()
        
        # if old is not None: 조건에서 None이므로 send_to_system 호출 안 됨
        mock_page.send_to_system.assert_not_called()
    
    # 2-1 패턴: update_info의 success 브랜치와 데이터 처리
    def test_update_info_success_with_password(self, manager, mock_page, mock_widgets):
        """update_info 성공 브랜치 - 비밀번호 있는 경우"""
        info_label, enable_btn, disable_btn = mock_widgets
        mock_page.send_to_system.return_value = {
            'success': True,
            'data': {
                'id': 'CAM001',
                'location': (150, 250),
                'pan': 15,
                'zoom': 2.5,
                'enabled': True,
                'password': 'encrypted_pw'
            }
        }
        
        manager.update_info()
        
        # info_label.config가 호출되었는지 확인
        info_label.config.assert_called_once()
        call_args = info_label.config.call_args[1]
        assert 'CAM001' in call_args['text']
        assert 'Password: Yes' in call_args['text']
        
        # enabled=True이므로 enable 버튼 disabled, disable 버튼 enabled
        enable_btn.config.assert_called_with(state='disabled')
        disable_btn.config.assert_called_with(state='normal')
    
    def test_update_info_success_without_password(self, manager, mock_page, mock_widgets):
        """update_info 성공 브랜치 - 비밀번호 없는 경우"""
        info_label, enable_btn, disable_btn = mock_widgets
        mock_page.send_to_system.return_value = {
            'success': True,
            'data': {
                'id': 'CAM002',
                'location': (200, 300),
                'pan': 0,
                'zoom': 1,
                'enabled': False,
                'password': None  # 비밀번호 없음
            }
        }
        
        manager.update_info()
        
        # info_label.config가 호출되었는지 확인
        call_args = info_label.config.call_args[1]
        assert 'Password: No' in call_args['text']
        
        # enabled=False이므로 enable 버튼 enabled, disable 버튼 disabled
        enable_btn.config.assert_called_with(state='normal')
        disable_btn.config.assert_called_with(state='disabled')
    
    def test_update_info_failure_branch(self, manager, mock_page, mock_widgets):
        """update_info 실패 브랜치 (if success: False)"""
        info_label, _, _ = mock_widgets
        mock_page.send_to_system.return_value = {'success': False}
        
        manager.update_info()
        
        # 실패 시에는 info_label.config가 호출되지 않아야 함
        info_label.config.assert_not_called()
    
    # 추가: 엣지 케이스 - 데이터가 없는 경우
    def test_update_info_success_but_no_data(self, manager, mock_page):
        """update_info 성공이지만 data가 없는 경우"""
        mock_page.send_to_system.return_value = {'success': True, 'data': {}}
        
        # 예외가 발생하지 않고 정상 처리되는지 확인
        manager.update_info()
        # get() 메서드로 기본값을 사용하므로 에러 없이 처리됨

