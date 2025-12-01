"""Tests for LoginAttemptGuard - 브랜치 커버리지 향상"""

import pytest
import time
from unittest.mock import Mock

from src.interfaces.pages.login_page.controllers.login_attempt_guard import LoginAttemptGuard


class TestLoginAttemptGuard:
    """LoginAttemptGuard의 모든 브랜치를 커버하는 테스트"""
    
    @pytest.fixture
    def guard(self):
        """기본 LoginAttemptGuard 인스턴스 (max_attempts=3, lock_seconds=60)"""
        return LoginAttemptGuard(max_attempts=3, lock_seconds=60)
    
    @pytest.fixture
    def guard_with_short_lock(self):
        """짧은 락 시간을 가진 LoginAttemptGuard (테스트 속도 향상)"""
        return LoginAttemptGuard(max_attempts=3, lock_seconds=2)
    
    # 기본 동작 테스트
    def test_initialization(self, guard):
        """초기화 시 기본 상태 확인"""
        assert guard.remaining_attempts() == 3
        assert guard.is_locked() == False
    
    def test_reset_attempts(self, guard):
        """reset_attempts가 상태를 초기화하는지 확인"""
        # 실패 기록
        guard.record_failure()
        assert guard.remaining_attempts() == 2
        
        # 리셋
        guard.reset_attempts()
        assert guard.remaining_attempts() == 3
        assert guard.is_locked() == False
    
    # 2-1 패턴: if/else - record_failure의 락아웃 브랜치
    def test_record_failure_not_locked_yet(self, guard):
        """record_failure - 아직 락아웃되지 않은 경우 (if self._attempts <= 0: False)"""
        # 첫 번째 실패
        should_lock = guard.record_failure()
        assert should_lock == False  # 아직 락아웃 안 됨
        assert guard.remaining_attempts() == 2
        assert guard.is_locked() == False
        
        # 두 번째 실패
        should_lock = guard.record_failure()
        assert should_lock == False
        assert guard.remaining_attempts() == 1
        assert guard.is_locked() == False
    
    def test_record_failure_triggers_lockout(self, guard):
        """record_failure - 락아웃 트리거 (if self._attempts <= 0: True)"""
        # 2번 실패 (attempts를 1로 만듦)
        guard.record_failure()
        guard.record_failure()
        assert guard.remaining_attempts() == 1
        
        # 3번째 실패 - 락아웃 발생
        should_lock = guard.record_failure()
        assert should_lock == True  # 락아웃 시작
        assert guard.remaining_attempts() == 0
        assert guard.is_locked() == True
        assert guard._started_at is not None  # 시작 시간 기록
    
    def test_record_failure_exactly_zero_attempts(self):
        """record_failure - attempts가 정확히 0이 되는 경우"""
        guard = LoginAttemptGuard(max_attempts=1, lock_seconds=60)
        
        should_lock = guard.record_failure()
        assert should_lock == True
        assert guard.remaining_attempts() == 0
        assert guard.is_locked() == True
    
    # 2-2 패턴: early return - _remaining_seconds의 None 체크
    def test_remaining_seconds_when_not_started(self, guard):
        """_remaining_seconds - started_at이 None인 경우 (if not self._started_at: 진입)"""
        # 락아웃이 시작되지 않았을 때
        remaining = guard._remaining_seconds()
        assert remaining == 0  # early return
    
    def test_remaining_seconds_when_started(self, guard_with_short_lock):
        """_remaining_seconds - started_at이 설정된 경우 (if not self._started_at: False)"""
        # 락아웃 시작
        guard_with_short_lock.record_failure()
        guard_with_short_lock.record_failure()
        guard_with_short_lock.record_failure()
        
        # 시작 직후
        remaining = guard_with_short_lock._remaining_seconds()
        assert remaining > 0
        assert remaining <= 2  # lock_seconds=2
    
    def test_remaining_seconds_after_time_passes(self, guard_with_short_lock):
        """_remaining_seconds - 시간이 지난 후"""
        # 락아웃 시작
        guard_with_short_lock.record_failure()
        guard_with_short_lock.record_failure()
        guard_with_short_lock.record_failure()
        
        # 조금 기다림
        time.sleep(0.5)
        
        remaining = guard_with_short_lock._remaining_seconds()
        assert remaining >= 0
        assert remaining < 2  # 시간이 줄어듦
    
    def test_remaining_seconds_max_function(self, guard):
        """_remaining_seconds - max(0, ...) 함수 동작 (음수가 0이 되는지)"""
        # 락아웃 시작하고 시간을 과거로 설정
        guard.record_failure()
        guard.record_failure()
        guard.record_failure()
        
        # started_at을 과거로 설정 (60초 이상 지남)
        guard._started_at = time.time() - 100
        
        remaining = guard._remaining_seconds()
        assert remaining == 0  # 음수가 아닌 0
    
    # 2-1 패턴: if - start_countdown의 early return
    def test_start_countdown_unlocks_when_time_expired(self):
        """start_countdown - 시간이 만료된 경우 (if remaining <= 0: 진입)"""
        guard = LoginAttemptGuard(max_attempts=3, lock_seconds=60)
        
        # 락아웃 시작하고 시간을 과거로 설정
        guard.record_failure()
        guard.record_failure()
        guard.record_failure()
        guard._started_at = time.time() - 100  # 100초 전 (lock_seconds=60보다 큼)
        
        schedule_fn = Mock()
        tick_fn = Mock()
        unlock_fn = Mock()
        
        guard.start_countdown(schedule_fn, tick_fn, unlock_fn)
        
        # remaining <= 0이므로 unlock_fn 호출되고 early return
        unlock_fn.assert_called_once()
        tick_fn.assert_not_called()
        schedule_fn.assert_not_called()
    
    def test_start_countdown_continues_when_time_remaining(self):
        """start_countdown - 시간이 남아있는 경우 (if remaining <= 0: False)"""
        guard = LoginAttemptGuard(max_attempts=3, lock_seconds=60)
        
        # 락아웃 시작
        guard.record_failure()
        guard.record_failure()
        guard.record_failure()
        
        schedule_fn = Mock(return_value="job123")
        tick_fn = Mock()
        unlock_fn = Mock()
        
        guard.start_countdown(schedule_fn, tick_fn, unlock_fn)
        
        # 시간이 남아있으므로 tick_fn 호출되고 다음 카운트다운 스케줄
        unlock_fn.assert_not_called()
        tick_fn.assert_called_once()
        # tick_fn에 전달된 remaining 값이 양수인지 확인
        remaining_arg = tick_fn.call_args[0][0]
        assert remaining_arg > 0
        assert remaining_arg <= 60
        
        # schedule_fn이 호출되어 다음 카운트다운 예약
        schedule_fn.assert_called_once()
        assert guard._job == "job123"
    
    # 2-1 패턴: if - _cancel의 job 존재 여부 브랜치
    def test_cancel_with_existing_job(self):
        """_cancel - job이 있는 경우 (if self._job: 진입)"""
        guard = LoginAttemptGuard(max_attempts=3, lock_seconds=60)
        
        # job 설정
        guard._job = "job456"
        
        schedule_fn = Mock()
        guard._cancel(schedule_fn)
        
        # schedule_fn이 "cancel"과 job_id로 호출됨
        schedule_fn.assert_called_once_with("cancel", "job456")
        assert guard._job is None  # job이 None으로 리셋
    
    def test_cancel_without_job(self):
        """_cancel - job이 없는 경우 (if self._job: False)"""
        guard = LoginAttemptGuard(max_attempts=3, lock_seconds=60)
        
        # job이 None인 상태
        assert guard._job is None
        
        schedule_fn = Mock()
        guard._cancel(schedule_fn)
        
        # schedule_fn이 호출되지 않아야 함
        schedule_fn.assert_not_called()
        assert guard._job is None
    
    # 2-4 패턴: start_countdown에서 _cancel 호출 확인
    def test_start_countdown_cancels_previous_job(self):
        """start_countdown - 이전 job을 취소하는지 확인"""
        guard = LoginAttemptGuard(max_attempts=3, lock_seconds=60)
        
        # 락아웃 시작
        guard.record_failure()
        guard.record_failure()
        guard.record_failure()
        
        # 기존 job 설정
        guard._job = "old_job"
        
        schedule_fn = Mock(return_value="new_job")
        tick_fn = Mock()
        unlock_fn = Mock()
        
        guard.start_countdown(schedule_fn, tick_fn, unlock_fn)
        
        # 첫 번째 호출: cancel
        # 두 번째 호출: 새로운 카운트다운 스케줄
        assert schedule_fn.call_count == 2
        first_call = schedule_fn.call_args_list[0]
        assert first_call[0] == ("cancel", "old_job")
    
    # 통합 시나리오 테스트
    def test_full_lockout_and_unlock_scenario(self, guard_with_short_lock):
        """전체 락아웃 및 잠금 해제 시나리오"""
        guard = guard_with_short_lock
        
        # 1. 초기 상태
        assert guard.remaining_attempts() == 3
        assert guard.is_locked() == False
        
        # 2. 실패 3번으로 락아웃
        guard.record_failure()
        guard.record_failure()
        should_lock = guard.record_failure()
        
        assert should_lock == True
        assert guard.is_locked() == True
        assert guard.remaining_attempts() == 0
        
        # 3. 카운트다운 시작
        schedule_fn = Mock(return_value="job")
        tick_fn = Mock()
        unlock_fn = Mock()
        
        guard.start_countdown(schedule_fn, tick_fn, unlock_fn)
        
        # 시간이 남아있으므로 tick_fn 호출
        assert tick_fn.called
        
        # 4. 시간이 지나면 unlock
        guard._started_at = time.time() - 3  # lock_seconds=2보다 길게
        guard.start_countdown(schedule_fn, tick_fn, unlock_fn)
        
        # 시간 만료로 unlock_fn 호출
        assert unlock_fn.called
        
        # 5. 리셋으로 다시 사용 가능
        guard.reset_attempts()
        assert guard.remaining_attempts() == 3
        assert guard.is_locked() == False
    
    # 엣지 케이스
    def test_custom_max_attempts_and_lock_seconds(self):
        """커스텀 max_attempts와 lock_seconds 테스트"""
        guard = LoginAttemptGuard(max_attempts=5, lock_seconds=30)
        
        assert guard.remaining_attempts() == 5
        
        # 5번 실패해야 락아웃
        for i in range(4):
            should_lock = guard.record_failure()
            assert should_lock == False
        
        should_lock = guard.record_failure()
        assert should_lock == True
        assert guard.is_locked() == True
        
        # lock_seconds=30 확인
        remaining = guard._remaining_seconds()
        assert remaining <= 30
    
    def test_multiple_resets(self, guard):
        """여러 번 리셋해도 정상 동작"""
        guard.reset_attempts()
        guard.reset_attempts()
        guard.reset_attempts()
        
        assert guard.remaining_attempts() == 3
        assert guard.is_locked() == False

