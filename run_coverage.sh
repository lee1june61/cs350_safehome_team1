# Coverage 실행 스크립트

# 1. 센서 테스트 실행 + coverage 수집
coverage run --source=src/devices/sensors -m pytest tests/unit/test_devices/test_sensor_new.py tests/unit/test_devices/test_sensor_controller_new.py -v

# 2. Coverage 리포트 출력
coverage report -m

# 3. HTML 리포트 생성 (선택사항)
# coverage html

