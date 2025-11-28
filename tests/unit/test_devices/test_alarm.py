"""
test_alarm.py
Unit tests for Alarm class (실제 구현 기준)
"""

import pytest
from unittest.mock import Mock, patch
from src.devices.alarm import Alarm


class TestAlarm:
    """Alarm 클래스 테스트"""
    
    @pytest.fixture
    def alarm(self):
        """Alarm fixture"""
        return Alarm(alarm_id=1, xCoord=150, yCoord=300)
    
    def test_initialization(self, alarm):
        """알람 초기화 테스트"""
        assert alarm.id == 1
        assert alarm.xCoord == 150
        assert alarm.yCoord == 300
        assert alarm.status is False  # 초기 상태는 꺼짐
    
    def test_initialization_with_defaults(self):
        """기본값으로 알람 초기화 테스트"""
        alarm = Alarm(alarm_id=5)
        assert alarm.id == 5
        assert alarm.xCoord == 0
        assert alarm.yCoord == 0
        assert alarm.status is False
    
    # getID 테스트
    def test_get_id(self, alarm):
        """getID() 메서드 테스트"""
        assert alarm.getID() == 1
    
    def test_get_id_different_id(self):
        """다른 ID로 getID() 테스트"""
        alarm = Alarm(alarm_id=99)
        assert alarm.getID() == 99
    
    # getLocation 테스트
    def test_get_location(self, alarm):
        """getLocation() 메서드 테스트"""
        location = alarm.getLocation()
        assert location == [150, 300]
        assert isinstance(location, list)
        assert len(location) == 2
    
    def test_get_location_default(self):
        """기본 위치로 getLocation() 테스트"""
        alarm = Alarm(alarm_id=1)
        location = alarm.getLocation()
        assert location == [0, 0]
    
    # setLocation 테스트
    def test_set_location(self, alarm):
        """setLocation() 메서드 테스트"""
        alarm.setLocation(500, 600)
        assert alarm.xCoord == 500
        assert alarm.yCoord == 600
        assert alarm.getLocation() == [500, 600]
    
    def test_set_location_negative(self, alarm):
        """음수 좌표로 setLocation() 테스트"""
        alarm.setLocation(-100, -200)
        assert alarm.xCoord == -100
        assert alarm.yCoord == -200
    
    # isRinging 테스트
    def test_is_ringing_initial_state(self, alarm):
        """초기 상태에서 isRinging() 테스트"""
        assert alarm.isRinging() is False
    
    def test_is_ringing_when_active(self, alarm):
        """알람이 울릴 때 isRinging() 테스트"""
        alarm.status = True
        assert alarm.isRinging() is True
    
    def test_is_ringing_when_stopped(self, alarm):
        """알람이 멈췄을 때 isRinging() 테스트"""
        alarm.status = True
        alarm.status = False
        assert alarm.isRinging() is False
    
    # ring 테스트
    def test_ring_activate(self, alarm):
        """ring(True)로 알람 활성화 테스트"""
        alarm.ring(True)
        assert alarm.status is True
        assert alarm.isRinging() is True
    
    def test_ring_deactivate(self, alarm):
        """ring(False)로 알람 비활성화 테스트"""
        alarm.ring(True)  # 먼저 활성화
        alarm.ring(False)  # 비활성화
        assert alarm.status is False
        assert alarm.isRinging() is False
    
    def test_ring_multiple_times(self, alarm):
        """ring() 여러 번 호출 테스트"""
        alarm.ring(True)
        alarm.ring(True)  # 이미 울리는 중
        assert alarm.status is True
        
        alarm.ring(False)
        alarm.ring(False)  # 이미 멈춤
        assert alarm.status is False
    
    # starting 테스트
    def test_starting_correct_id(self, alarm):
        """올바른 ID로 starting() 테스트"""
        result = alarm.starting(1)
        assert result is True
        assert alarm.status is True
        assert alarm.isRinging() is True
    
    def test_starting_wrong_id(self, alarm):
        """잘못된 ID로 starting() 테스트"""
        result = alarm.starting(999)
        assert result is False
        assert alarm.status is False  # 상태 변화 없음
    
    def test_starting_already_ringing(self, alarm):
        """이미 울리는 중에 starting() 테스트"""
        alarm.starting(1)  # 첫 번째 시작
        result = alarm.starting(1)  # 두 번째 시작
        assert result is True
        assert alarm.status is True
    
    # ending 테스트
    def test_ending_correct_id(self, alarm):
        """올바른 ID로 ending() 테스트"""
        alarm.starting(1)  # 먼저 시작
        result = alarm.ending(1)
        assert result is True
        assert alarm.status is False
        assert alarm.isRinging() is False
    
    def test_ending_wrong_id(self, alarm):
        """잘못된 ID로 ending() 테스트"""
        alarm.starting(1)  # 먼저 시작
        result = alarm.ending(999)
        assert result is False
        assert alarm.status is True  # 상태 변화 없음
    
    def test_ending_not_ringing(self, alarm):
        """울리지 않을 때 ending() 테스트"""
        result = alarm.ending(1)
        assert result is True
        assert alarm.status is False
    
    # 통합 시나리오 테스트
    def test_intrusion_scenario(self, alarm):
        """침입 감지 시나리오 테스트"""
        # 초기 상태
        assert alarm.isRinging() is False
        
        # 침입 감지로 알람 시작
        result = alarm.starting(1)
        assert result is True
        assert alarm.isRinging() is True
        
        # 사용자가 알람 종료
        result = alarm.ending(1)
        assert result is True
        assert alarm.isRinging() is False
    
    def test_false_alarm_scenario(self, alarm):
        """오작동 시나리오 테스트"""
        # 알람 울림
        alarm.ring(True)
        assert alarm.isRinging() is True
        
        # 즉시 종료
        alarm.ring(False)
        assert alarm.isRinging() is False
    
    def test_location_change_while_ringing(self, alarm):
        """알람이 울리는 중 위치 변경 테스트"""
        alarm.starting(1)
        alarm.setLocation(999, 888)
        
        assert alarm.isRinging() is True  # 여전히 울림
        assert alarm.getLocation() == [999, 888]  # 위치는 변경됨
    
    def test_multiple_alarms_different_ids(self):
        """여러 알람 독립 동작 테스트"""
        alarm1 = Alarm(alarm_id=1, xCoord=100, yCoord=200)
        alarm2 = Alarm(alarm_id=2, xCoord=300, yCoord=400)
        
        # alarm1만 시작
        alarm1.starting(1)
        
        assert alarm1.isRinging() is True
        assert alarm2.isRinging() is False
        
        # alarm2 시작
        alarm2.starting(2)
        
        assert alarm1.isRinging() is True
        assert alarm2.isRinging() is True
        
        # alarm1만 종료
        alarm1.ending(1)
        
        assert alarm1.isRinging() is False
        assert alarm2.isRinging() is True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
