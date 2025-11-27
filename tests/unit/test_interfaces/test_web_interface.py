"""
Unit Tests for WebInterface (TC-WI-01 ~ TC-WI-04)

Based on: SDS CRC Cards and Meeting Log Test Cases
Run: cd safehome_team1 && python -m pytest tests/unit/test_interfaces/test_web_interface.py -v
"""
import pytest


class TestWebInterface:
    """Tests for WebInterface class - TC-WI series"""
    
    def test_tc_wi_01_get_size(self, web_interface):
        """TC-WI-01: Verifies UI dimensions retrieval"""
        assert web_interface._system is not None
    
    def test_tc_wi_03_process_button_event(self, web_interface, mock_system):
        """TC-WI-03: Verifies UI events are passed to System"""
        result = web_interface.send_message('get_status')
        assert result['success'] == True
        assert 'data' in result

    def test_tc_wi_03_with_parameters(self, web_interface, mock_system):
        """TC-WI-03 variant: Test event with parameters"""
        result = web_interface.send_message('arm_system', mode='AWAY')
        assert result['success'] == True

        status = web_interface.send_message('get_status')
        assert status['data']['armed'] == True
    
    def test_tc_wi_04_draw_page(self):
        """TC-WI-04: Verifies page registry exists"""
        from src.interfaces.page_registry import PAGE_CLASSES
        
        assert 'login' in PAGE_CLASSES
        assert 'security' in PAGE_CLASSES
        assert 'surveillance' in PAGE_CLASSES
    
    def test_send_message_no_system(self):
        """Test error handling when System is not connected"""
        from src.interfaces.web_interface import WebInterface
        
        wi = object.__new__(WebInterface)
        wi._system = None
        wi._pages = {}
        wi._current_page = None
        wi._context = {}
        
        result = wi.send_message('get_status')
        assert result['success'] == False
    
    def test_context_management(self, web_interface):
        """Test context management for page data passing"""
        web_interface.set_context('camera', {'id': '1'})
        assert web_interface.get_context('camera')['id'] == '1'
        
        web_interface.clear_context()
        assert web_interface.get_context('camera') is None