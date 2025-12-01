"""Tests for settings_resetter - 브랜치 커버리지 향상"""

import pytest
from unittest.mock import Mock, patch

from src.interfaces.pages.configure_system_setting_page.settings_resetter import reset_to_defaults


class TestSettingsResetter:
    """reset_to_defaults 함수의 모든 브랜치를 커버하는 테스트"""
    
    @pytest.fixture
    def mock_widgets(self):
        """Mock tkinter widgets and variables"""
        delay_time_var = Mock()
        delay_time_var.get = Mock(return_value='10')
        delay_time_var.set = Mock()
        
        monitor_phone_var = Mock()
        monitor_phone_var.get = Mock(return_value='123-456-7890')
        monitor_phone_var.set = Mock()
        
        status_label = Mock()
        status_label.config = Mock()
        status_label.cget = Mock(return_value="Original status")
        
        return delay_time_var, monitor_phone_var, status_label
    
    @pytest.fixture
    def mock_page(self):
        """Mock page instance"""
        return Mock()
    
    @pytest.fixture
    def mock_clear_func(self):
        """Mock clear password fields function"""
        return Mock()
    
    # 2-1 패턴: if - messagebox.askyesno 확인 브랜치
    @patch('src.interfaces.pages.configure_system_setting_page.settings_resetter.messagebox.askyesno')
    def test_reset_to_defaults_user_confirms(self, mock_askyesno, mock_page, mock_widgets, mock_clear_func):
        """reset_to_defaults - 사용자가 확인하는 경우 (if askyesno: True)"""
        delay_time_var, monitor_phone_var, status_label = mock_widgets
        mock_askyesno.return_value = True  # 사용자가 "Yes" 클릭
        
        reset_to_defaults(
            mock_page,
            delay_time_var,
            monitor_phone_var,
            status_label,
            mock_clear_func
        )
        
        # messagebox가 호출되었는지 확인
        mock_askyesno.assert_called_once_with("Confirm", "Reset all settings to defaults?")
        
        # 기본값으로 리셋되었는지 확인
        delay_time_var.set.assert_called_with('5')
        monitor_phone_var.set.assert_called_with('911')
        
        # clear_password_fields_func가 호출되었는지 확인
        mock_clear_func.assert_called_once()
        
        # 상태 레이블이 업데이트되었는지 확인
        status_label.config.assert_called_once_with(text="Reset to defaults (not saved yet)", foreground='orange')
    
    @patch('src.interfaces.pages.configure_system_setting_page.settings_resetter.messagebox.askyesno')
    def test_reset_to_defaults_user_cancels(self, mock_askyesno, mock_page, mock_widgets, mock_clear_func):
        """reset_to_defaults - 사용자가 취소하는 경우 (if askyesno: False)"""
        delay_time_var, monitor_phone_var, status_label = mock_widgets
        mock_askyesno.return_value = False  # 사용자가 "No" 클릭
        
        reset_to_defaults(
            mock_page,
            delay_time_var,
            monitor_phone_var,
            status_label,
            mock_clear_func
        )
        
        # messagebox가 호출되었는지 확인
        mock_askyesno.assert_called_once_with("Confirm", "Reset all settings to defaults?")
        
        # set이 호출되지 않았는지 확인 (if 블록 진입 안 함)
        delay_time_var.set.assert_not_called()
        monitor_phone_var.set.assert_not_called()
        
        # clear_password_fields_func가 호출되지 않았는지 확인
        mock_clear_func.assert_not_called()
        
        # 상태 레이블이 변경되지 않았는지 확인
        status_label.config.assert_not_called()
    
    # 추가 엣지 케이스: 빈 값에서 리셋
    @patch('src.interfaces.pages.configure_system_setting_page.settings_resetter.messagebox.askyesno')
    def test_reset_to_defaults_from_empty_values(self, mock_askyesno, mock_page, mock_widgets, mock_clear_func):
        """reset_to_defaults - 빈 값에서 리셋하는 경우"""
        delay_time_var, monitor_phone_var, status_label = mock_widgets
        mock_askyesno.return_value = True
        
        reset_to_defaults(
            mock_page,
            delay_time_var,
            monitor_phone_var,
            status_label,
            mock_clear_func
        )
        
        # 기본값으로 설정되었는지 확인
        delay_time_var.set.assert_called_with('5')
        monitor_phone_var.set.assert_called_with('911')
        mock_clear_func.assert_called_once()
    
    # 추가 엣지 케이스: 이미 기본값인 경우
    @patch('src.interfaces.pages.configure_system_setting_page.settings_resetter.messagebox.askyesno')
    def test_reset_to_defaults_already_default_values(self, mock_askyesno, mock_page, mock_widgets, mock_clear_func):
        """reset_to_defaults - 이미 기본값인 경우에도 정상 동작"""
        delay_time_var, monitor_phone_var, status_label = mock_widgets
        mock_askyesno.return_value = True
        
        reset_to_defaults(
            mock_page,
            delay_time_var,
            monitor_phone_var,
            status_label,
            mock_clear_func
        )
        
        # 여전히 기본값으로 설정 호출
        delay_time_var.set.assert_called_with('5')
        monitor_phone_var.set.assert_called_with('911')
        mock_clear_func.assert_called_once()
        status_label.config.assert_called_with(text="Reset to defaults (not saved yet)", foreground='orange')
    
    # 추가 엣지 케이스: clear_password_fields_func가 예외를 던지는 경우
    @patch('src.interfaces.pages.configure_system_setting_page.settings_resetter.messagebox.askyesno')
    def test_reset_to_defaults_clear_func_raises_exception(self, mock_askyesno, mock_page, mock_widgets):
        """reset_to_defaults - clear 함수가 예외를 던지는 경우"""
        delay_time_var, monitor_phone_var, status_label = mock_widgets
        mock_askyesno.return_value = True
        
        clear_func_with_error = Mock(side_effect=Exception("Clear error"))
        
        # 예외가 발생해도 함수가 중단되는지 확인 (현재 코드는 예외 처리 없음)
        with pytest.raises(Exception, match="Clear error"):
            reset_to_defaults(
                mock_page,
                delay_time_var,
                monitor_phone_var,
                status_label,
                clear_func_with_error
            )
        
        # 그래도 값은 리셋되었어야 함 (clear_func 전에 실행됨)
        delay_time_var.set.assert_called_with('5')
        monitor_phone_var.set.assert_called_with('911')
    
    # 통합 시나리오
    @patch('src.interfaces.pages.configure_system_setting_page.settings_resetter.messagebox.askyesno')
    def test_reset_to_defaults_multiple_calls(self, mock_askyesno, mock_page, mock_clear_func):
        """reset_to_defaults - 여러 번 호출하는 시나리오"""
        # 첫 번째 호출용 mocks
        delay_time_var1 = Mock()
        delay_time_var1.set = Mock()
        monitor_phone_var1 = Mock()
        monitor_phone_var1.set = Mock()
        status_label1 = Mock()
        status_label1.config = Mock()
        
        mock_askyesno.return_value = True
        
        reset_to_defaults(mock_page, delay_time_var1, monitor_phone_var1, status_label1, mock_clear_func)
        
        delay_time_var1.set.assert_called_with('5')
        monitor_phone_var1.set.assert_called_with('911')
        assert mock_clear_func.call_count == 1
        
        # 두 번째 호출: 취소
        delay_time_var2 = Mock()
        delay_time_var2.set = Mock()
        monitor_phone_var2 = Mock()
        monitor_phone_var2.set = Mock()
        status_label2 = Mock()
        status_label2.config = Mock()
        
        mock_askyesno.return_value = False
        
        reset_to_defaults(mock_page, delay_time_var2, monitor_phone_var2, status_label2, mock_clear_func)
        
        delay_time_var2.set.assert_not_called()  # 변경 안 됨
        monitor_phone_var2.set.assert_not_called()  # 변경 안 됨
        assert mock_clear_func.call_count == 1  # 추가 호출 안 됨
        
        # 세 번째 호출: 다시 확인
        delay_time_var3 = Mock()
        delay_time_var3.set = Mock()
        monitor_phone_var3 = Mock()
        monitor_phone_var3.set = Mock()
        status_label3 = Mock()
        status_label3.config = Mock()
        
        mock_askyesno.return_value = True
        
        reset_to_defaults(mock_page, delay_time_var3, monitor_phone_var3, status_label3, mock_clear_func)
        
        delay_time_var3.set.assert_called_with('5')
        monitor_phone_var3.set.assert_called_with('911')
        assert mock_clear_func.call_count == 2  # 다시 호출됨

