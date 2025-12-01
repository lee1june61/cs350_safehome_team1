"""Tests for LogManager (interfaces/pages) - 브랜치 커버리지 향상"""

import pytest
from unittest.mock import Mock

from src.interfaces.pages.log_manager import LogManager


class TestLogManager:
    """LogManager의 모든 브랜치를 커버하는 테스트"""
    
    @pytest.fixture
    def mock_page(self):
        """Mock page instance"""
        page = Mock()
        page.send_to_system = Mock()
        return page
    
    @pytest.fixture
    def mock_widgets(self):
        """Mock tkinter widgets"""
        treeview = Mock()
        treeview.get_children = Mock(return_value=[])
        treeview.delete = Mock()
        treeview.insert = Mock(return_value='item1')
        treeview.item = Mock(return_value={'tags': ('normal',)})
        treeview.tag_configure = Mock()
        
        status_label = Mock()
        status_label.config = Mock()
        status_label.cget = Mock(return_value="")
        
        return treeview, status_label
    
    @pytest.fixture
    def log_manager(self, mock_page, mock_widgets):
        """Create LogManager instance"""
        treeview, status_label = mock_widgets
        return LogManager(mock_page, treeview, status_label)
    
    # 2-1 패턴: if/elif/elif - event 타입별 태그 브랜치
    def test_load_log_entries_success_with_intrusion_event(self, log_manager, mock_page, mock_widgets):
        """load_log_entries 성공 - INTRUSION 이벤트 (alert 태그)"""
        treeview, status_label = mock_widgets
        mock_page.send_to_system.return_value = {
            'success': True,
            'data': [
                {'timestamp': '2024-01-01 10:00:00', 'event': 'INTRUSION', 'detail': 'Motion detected'}
            ]
        }
        
        log_manager.load_log_entries()
        
        # insert가 'alert' 태그와 함께 호출되었는지 확인
        treeview.insert.assert_called_once()
        call_kwargs = treeview.insert.call_args[1]
        assert 'alert' in call_kwargs['tags']
        status_label.config.assert_called_with(text="Showing 1 entries")
    
    def test_load_log_entries_success_with_panic_event(self, log_manager, mock_page, mock_widgets):
        """load_log_entries 성공 - PANIC 이벤트 (alert 태그)"""
        treeview, status_label = mock_widgets
        mock_page.send_to_system.return_value = {
            'success': True,
            'data': [
                {'timestamp': '2024-01-01 11:00:00', 'event': 'PANIC', 'detail': 'Panic button pressed'}
            ]
        }
        
        log_manager.load_log_entries()
        
        call_kwargs = treeview.insert.call_args[1]
        assert 'alert' in call_kwargs['tags']
    
    def test_load_log_entries_success_with_arm_event(self, log_manager, mock_page, mock_widgets):
        """load_log_entries 성공 - ARM 이벤트 (armed 태그)"""
        treeview, status_label = mock_widgets
        mock_page.send_to_system.return_value = {
            'success': True,
            'data': [
                {'timestamp': '2024-01-01 12:00:00', 'event': 'ARM', 'detail': 'System armed'}
            ]
        }
        
        log_manager.load_log_entries()
        
        call_kwargs = treeview.insert.call_args[1]
        assert 'armed' in call_kwargs['tags']
    
    def test_load_log_entries_success_with_arm_zone_event(self, log_manager, mock_page, mock_widgets):
        """load_log_entries 성공 - ARM_ZONE 이벤트 (armed 태그)"""
        treeview, status_label = mock_widgets
        mock_page.send_to_system.return_value = {
            'success': True,
            'data': [
                {'timestamp': '2024-01-01 13:00:00', 'event': 'ARM_ZONE', 'detail': 'Zone 1 armed'}
            ]
        }
        
        log_manager.load_log_entries()
        
        call_kwargs = treeview.insert.call_args[1]
        assert 'armed' in call_kwargs['tags']
    
    def test_load_log_entries_success_with_disarm_event(self, log_manager, mock_page, mock_widgets):
        """load_log_entries 성공 - DISARM 이벤트 (disarmed 태그)"""
        treeview, status_label = mock_widgets
        mock_page.send_to_system.return_value = {
            'success': True,
            'data': [
                {'timestamp': '2024-01-01 14:00:00', 'event': 'DISARM', 'detail': 'System disarmed'}
            ]
        }
        
        log_manager.load_log_entries()
        
        call_kwargs = treeview.insert.call_args[1]
        assert 'disarmed' in call_kwargs['tags']
    
    def test_load_log_entries_success_with_disarm_zone_event(self, log_manager, mock_page, mock_widgets):
        """load_log_entries 성공 - DISARM_ZONE 이벤트 (disarmed 태그)"""
        treeview, status_label = mock_widgets
        mock_page.send_to_system.return_value = {
            'success': True,
            'data': [
                {'timestamp': '2024-01-01 15:00:00', 'event': 'DISARM_ZONE', 'detail': 'Zone 2 disarmed'}
            ]
        }
        
        log_manager.load_log_entries()
        
        call_kwargs = treeview.insert.call_args[1]
        assert 'disarmed' in call_kwargs['tags']
    
    def test_load_log_entries_success_with_unknown_event(self, log_manager, mock_page, mock_widgets):
        """load_log_entries 성공 - 알 수 없는 이벤트 (normal 태그 - else 브랜치)"""
        treeview, status_label = mock_widgets
        mock_page.send_to_system.return_value = {
            'success': True,
            'data': [
                {'timestamp': '2024-01-01 16:00:00', 'event': 'SYSTEM_START', 'detail': 'System started'}
            ]
        }
        
        log_manager.load_log_entries()
        
        call_kwargs = treeview.insert.call_args[1]
        assert 'normal' in call_kwargs['tags']
    
    def test_load_log_entries_success_with_multiple_events(self, log_manager, mock_page, mock_widgets):
        """load_log_entries 성공 - 여러 이벤트 (모든 브랜치 동시 테스트)"""
        treeview, status_label = mock_widgets
        mock_page.send_to_system.return_value = {
            'success': True,
            'data': [
                {'timestamp': '2024-01-01 10:00:00', 'event': 'INTRUSION', 'detail': 'Motion'},
                {'timestamp': '2024-01-01 11:00:00', 'event': 'ARM', 'detail': 'Armed'},
                {'timestamp': '2024-01-01 12:00:00', 'event': 'DISARM', 'detail': 'Disarmed'},
                {'timestamp': '2024-01-01 13:00:00', 'event': 'LOGIN', 'detail': 'User logged in'},
            ]
        }
        
        log_manager.load_log_entries()
        
        assert treeview.insert.call_count == 4
        status_label.config.assert_called_with(text="Showing 4 entries")
    
    def test_load_log_entries_success_with_empty_data(self, log_manager, mock_page, mock_widgets):
        """load_log_entries 성공 - 빈 데이터"""
        treeview, status_label = mock_widgets
        mock_page.send_to_system.return_value = {
            'success': True,
            'data': []
        }
        
        log_manager.load_log_entries()
        
        treeview.insert.assert_not_called()
        status_label.config.assert_called_with(text="Showing 0 entries")
    
    # 2-1 패턴: if/else - success 실패 브랜치
    def test_load_log_entries_failure_branch(self, log_manager, mock_page, mock_widgets):
        """load_log_entries 실패 브랜치 (if res.get('success'): False)"""
        treeview, status_label = mock_widgets
        mock_page.send_to_system.return_value = {'success': False}
        
        log_manager.load_log_entries()
        
        treeview.insert.assert_not_called()
        status_label.config.assert_called_with(text="Failed to load log")
    
    # 추가: 기존 항목이 있을 때 clear 동작 확인
    def test_load_log_entries_clears_existing_items(self, log_manager, mock_page, mock_widgets):
        """load_log_entries가 기존 항목을 먼저 삭제하는지 확인"""
        treeview, status_label = mock_widgets
        treeview.get_children.return_value = ['old_item1', 'old_item2']
        mock_page.send_to_system.return_value = {
            'success': True,
            'data': [
                {'timestamp': '2024-01-01 10:00:00', 'event': 'ARM', 'detail': 'New entry'}
            ]
        }
        
        log_manager.load_log_entries()
        
        # delete가 각 기존 항목에 대해 호출되었는지 확인
        assert treeview.delete.call_count == 2
        treeview.delete.assert_any_call('old_item1')
        treeview.delete.assert_any_call('old_item2')
    
    # 추가: 데이터 누락 시 기본값 처리
    def test_load_log_entries_with_missing_fields(self, log_manager, mock_page, mock_widgets):
        """load_log_entries - 필드가 누락된 경우 기본값 사용"""
        treeview, status_label = mock_widgets
        mock_page.send_to_system.return_value = {
            'success': True,
            'data': [
                {},  # 모든 필드 누락
                {'event': 'ARM'}  # timestamp, detail 누락
            ]
        }
        
        log_manager.load_log_entries()
        
        assert treeview.insert.call_count == 2
        # get() 메서드로 기본값 '-'를 사용하므로 에러 없이 처리됨
    
    # clear_log_display 테스트
    def test_clear_log_display_removes_all_items(self, log_manager, mock_widgets):
        """clear_log_display가 모든 항목을 삭제하는지 확인"""
        treeview, status_label = mock_widgets
        treeview.get_children.return_value = ['item1', 'item2', 'item3']
        
        log_manager.clear_log_display()
        
        assert treeview.delete.call_count == 3
        treeview.delete.assert_any_call('item1')
        treeview.delete.assert_any_call('item2')
        treeview.delete.assert_any_call('item3')
        status_label.config.assert_called_with(text="Log cleared from display")
    
    def test_clear_log_display_when_empty(self, log_manager, mock_widgets):
        """clear_log_display - 이미 비어있는 경우"""
        treeview, status_label = mock_widgets
        treeview.get_children.return_value = []
        
        log_manager.clear_log_display()
        
        treeview.delete.assert_not_called()
        status_label.config.assert_called_with(text="Log cleared from display")
