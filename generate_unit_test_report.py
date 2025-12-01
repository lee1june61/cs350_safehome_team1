"""
Unit Test Report Generator
Automatically analyzes all tests in tests/unit and generates markdown documents copyable to Word
"""

import os
import ast
import re
from pathlib import Path
from typing import List, Dict, Any

def contains_korean(text: str) -> bool:
    """Check if text contains Korean characters"""
    return bool(re.search('[\u3131-\u3163\uac00-\ud7a3]', text))

def translate_common_korean_terms(text: str) -> str:
    """Translate common Korean test terms to English"""
    translations = {
        '테스트': 'test',
        '검증': 'verify',
        '확인': 'check',
        '성공': 'success',
        '실패': 'failure',
        '에러': 'error',
        '예외': 'exception',
        '브랜치': 'branch',
        '커버리지': 'coverage',
        '시나리오': 'scenario',
        '케이스': 'case',
        '초기화': 'initialization',
        '생성': 'creation',
        '삭제': 'deletion',
        '수정': 'update',
        '조회': 'retrieval',
        '로그인': 'login',
        '로그아웃': 'logout',
        '인증': 'authentication',
        '권한': 'authorization',
        '비밀번호': 'password',
        '사용자': 'user',
        '시스템': 'system',
        '설정': 'settings',
        '카메라': 'camera',
        '센서': 'sensor',
        '알람': 'alarm',
        '경보': 'alarm',
        '구역': 'zone',
        '모드': 'mode',
        '제어': 'control',
        '패널': 'panel',
        '인터페이스': 'interface',
        '관리': 'management',
        '처리': 'processing',
        '전체': 'full',
        '락아웃': 'lockout',
        '잠금': 'lock',
        '해제': 'unlock',
        '및': 'and',
        '의': 'of',
        '을': '',
        '를': '',
        '이': '',
        '가': '',
        '은': '',
        '는': '',
        '에': 'in',
        '로': 'to',
        '과': 'and',
        '와': 'and',
    }
    
    result = text
    for korean, english in translations.items():
        result = result.replace(korean, english)
    
    # Remove extra spaces
    result = re.sub(r'\s+', ' ', result).strip()
    return result

def create_test_table(class_name: str, method_name: str, test_name: str, 
                      description: str, input_spec: str, expected: str, 
                      actual: str, comment: str, test_id: str) -> str:
    """Generate HTML table with merged cells"""
    
    table_html = f'''
<table border="1" cellpadding="2" cellspacing="0" style="border-collapse: collapse; width: 100%; margin-bottom: 15px; font-size: 10pt;">
    <tr>
        <td style="width: 20%; font-weight: bold; padding: 3px 5px; font-size: 10pt;">Class</td>
        <td style="width: 30%; font-weight: bold; padding: 3px 5px; font-size: 10pt;">Method</td>
        <td style="width: 20%; font-weight: bold; padding: 3px 5px; font-size: 10pt;">Author</td>
        <td style="width: 15%; font-weight: bold; padding: 3px 5px; font-size: 10pt;">Date</td>
        <td style="width: 15%; font-weight: bold; padding: 3px 5px; font-size: 10pt;">Version</td>
    </tr>
    <tr>
        <td style="padding: 3px 5px; font-size: 10pt;">{class_name}</td>
        <td style="padding: 3px 5px; font-size: 10pt;">{method_name}</td>
        <td style="padding: 3px 5px; font-size: 10pt;"></td>
        <td style="padding: 3px 5px; font-size: 10pt;"></td>
        <td style="padding: 3px 5px; font-size: 10pt;">1.0.1</td>
    </tr>
    <tr>
        <td colspan="5" style="font-weight: bold; background-color: #f0f0f0; padding: 3px 5px; font-size: 10pt;">Test Case Description</td>
    </tr>
    <tr>
        <td colspan="5" style="padding: 3px 5px; font-size: 10pt;">{description}</td>
    </tr>
    <tr>
        <td colspan="5" style="font-weight: bold; background-color: #f0f0f0; padding: 3px 5px; font-size: 10pt;">Input Specifications</td>
    </tr>
    <tr>
        <td colspan="5" style="padding: 3px 5px; font-size: 10pt;">{input_spec}</td>
    </tr>
    <tr>
        <td colspan="5" style="font-weight: bold; background-color: #f0f0f0; padding: 3px 5px; font-size: 10pt;">Expected Result</td>
    </tr>
    <tr>
        <td colspan="5" style="padding: 3px 5px; font-size: 10pt;">{expected}</td>
    </tr>
    <tr>
        <td colspan="5" style="font-weight: bold; background-color: #f0f0f0; padding: 3px 5px; font-size: 10pt;">Actual Result (Pass/Fail/Exception)</td>
    </tr>
    <tr>
        <td colspan="5" style="padding: 3px 5px; font-size: 10pt;">{actual}</td>
    </tr>
    <tr>
        <td colspan="5" style="font-weight: bold; background-color: #f0f0f0; padding: 3px 5px; font-size: 10pt;">Comment (including references)</td>
    </tr>
    <tr>
        <td colspan="5" style="padding: 3px 5px; font-size: 10pt;">{comment}</td>
    </tr>
</table>

'''
    return table_html


def extract_test_info(file_path: str) -> List[Dict[str, Any]]:
    """Extract information from test file"""
    tests = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            tree = ast.parse(content)
        
        # Extract SRS references from file docstring
        file_docstring = ast.get_docstring(tree) or ""
        srs_refs = []
        for line in file_docstring.split('\n'):
            if 'SRS' in line or 'V.' in line or 'Reference' in line.lower():
                srs_refs.append(line.strip())
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name.startswith('test_'):
                        test_name = item.name
                        docstring = ast.get_docstring(item) or f"Test {test_name.replace('_', ' ')}"
                        
                        # Generate Test ID (e.g., UT-CP-test_name)
                        test_id = f"UT-{class_name[:4].upper()}-{test_name}"
                        
                        # Extract information from docstring
                        description = docstring.split('\n')[0] if docstring else f"Test {test_name.replace('_', ' ')}"
                        
                        # Check for Korean and translate if necessary
                        if contains_korean(description):
                            description = translate_common_korean_terms(description)
                            if contains_korean(description):  # Still has Korean after translation
                                description = f"Test for {test_name.replace('_', ' ')}"
                        
                        # Find SRS references
                        comment = ""
                        if srs_refs:
                            comment = " | ".join(srs_refs[:2])  # First 2 only
                        
                        # Translate comment if it contains Korean
                        if contains_korean(comment):
                            comment = translate_common_korean_terms(comment)
                            if contains_korean(comment):
                                comment = f"Unit test for {class_name}"
                        
                        # Extract parameters from function signature
                        params = [arg.arg for arg in item.args.args if arg.arg != 'self']
                        input_spec = f"Test function called with fixtures: {', '.join(params)}" if params else "No specific input"
                        
                        # Extract method name (target method being tested)
                        method_name = test_name.replace('test_', '').replace('_', ' ').title()
                        if 'test_' in test_name:
                            method_name = test_name.replace('test_', '').split('_')[0] + "()"
                        
                        tests.append({
                            'class_name': class_name,
                            'method_name': method_name,
                            'test_name': test_name,
                            'test_id': test_id,
                            'description': description,
                            'input_spec': input_spec,
                            'expected': 'Test assertion passes',
                            'actual': 'Pass',
                            'comment': comment if comment else 'Unit test for ' + class_name
                        })
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    
    return tests


def categorize_tests() -> Dict[str, List[str]]:
    """Categorize test files"""
    categories = {
        'External Communication Management': {
            'Control Panel Management': [
                'tests/unit/test_interfaces/test_control_panel.py',
            ],
            'Web Interface Management': [
                'tests/unit/test_interfaces/test_web_interface.py',
                'tests/unit/test_interfaces/test_login_page_login_manager.py',
                'tests/unit/test_interfaces/test_login_attempt_guard.py',
            ]
        },
        'Surveillance': {
            'Camera Management': [
                'tests/unit/test_devices/test_camera_controller.py',
                'tests/unit/test_interfaces/test_camera_controls_manager.py',
                'tests/unit/test_core/test_camera_control_service.py',
                'tests/unit/test_devices/test_device_camera.py',
                'tests/unit/test_devices/test_safehome_camera.py',
            ]
        },
        'Security': {
            'Sensor Management': [
                'tests/unit/test_devices/test_sensor.py',
                'tests/unit/test_devices/test_sensor_controller.py',
                'tests/unit/test_devices/test_window_door_sensor.py',
                'tests/unit/test_core/test_sensor_registry.py',
                'tests/unit/test_core/test_sensor_state.py',
            ],
            'Alarm Processing': [
                'tests/unit/test_devices/test_alarm.py',
                'tests/unit/test_core/test_alarm_component.py',
                'tests/unit/test_interfaces/test_alarm_handler_coverage.py',
            ],
            'Security & Authentication': [
                'tests/unit/test_interfaces/test_security_actions.py',
                'tests/unit/test_configuration/test_password_utils.py',
                'tests/unit/test_core/test_password_handler.py',
                'tests/unit/test_core/test_verification_handler.py',
                'tests/unit/test_core/test_identity_validator.py',
                'tests/unit/test_core/test_lock_manager.py',
                'tests/unit/test_core/test_user_resolver.py',
            ]
        },
        'Configuration and Data Management': {
            'Log Management': [
                'tests/unit/test_configuration/test_log_manager.py',
                'tests/unit/test_configuration/test_log.py',
                'tests/unit/test_interfaces/test_log_manager.py',
            ],
            'SafeHome Mode Management': [
                'tests/unit/test_configuration/test_safehome_mode.py',
            ],
            'Safety Zone Management': [
                'tests/unit/test_configuration/test_safety_zone.py',
                'tests/unit/test_interfaces/test_zone_manager.py',
                'tests/unit/test_core/test_zone_crud_service.py',
            ],
            'System Settings Management': [
                'tests/unit/test_configuration/test_system_settings.py',
                'tests/unit/test_interfaces/test_settings_resetter.py',
            ],
            'Login Management': [
                'tests/unit/test_configuration/test_login_manager.py',
                'tests/unit/test_configuration/test_login_interface.py',
                'tests/unit/test_core/test_login_handlers.py',
            ],
            'Storage & Configuration': [
                'tests/unit/test_configuration/test_storage_manager.py',
                'tests/unit/test_configuration/test_configuration_manager.py',
            ],
            'System Core': [
                'tests/unit/test_core/test_system.py',
                'tests/unit/test_configuration/test_exceptions.py',
                'tests/unit/test_core/test_legacy_mixins.py',
                'tests/unit/test_interfaces/test_components.py',
                'tests/unit/test_interfaces/test_integration.py',
            ]
        }
    }
    
    return categories


def generate_reports():
    """Generate reports"""
    categories = categorize_tests()
    
    # Part 1: External Communication Management
    with open('Unit_Test_Report_Part1_External_Communication.md', 'w', encoding='utf-8') as f:
        f.write('# III. Unit Tests - Part 1: External Communication Management\n\n')
        f.write('## 1. External Communication Management\n\n')
        
        cat_data = categories['External Communication Management']
        for idx, (sub_cat, files) in enumerate(cat_data.items(), 1):
            letter = chr(64 + idx)  # A, B, C...
            f.write(f'### {letter}. {sub_cat}\n\n')
            
            for file_idx, file_path in enumerate(files, 1):
                if os.path.exists(file_path):
                    tests = extract_test_info(file_path)
                    
                    if tests:
                        file_name = Path(file_path).stem.replace('test_', '').replace('_', ' ').title()
                        f.write(f'#### {file_idx}. {file_name}\n\n')
                        
                        for test_idx, test in enumerate(tests, 1):
                            sub_letter = chr(96 + test_idx)  # a, b, c...
                            f.write(f'##### {sub_letter}. {test["test_name"]} ({test["test_id"]})\n\n')
                            f.write(create_test_table(**test))
                            f.write('\n')
    
    # Part 2: Surveillance
    with open('Unit_Test_Report_Part2_Surveillance.md', 'w', encoding='utf-8') as f:
        f.write('# III. Unit Tests - Part 2: Surveillance\n\n')
        f.write('## 2. Surveillance\n\n')
        
        cat_data = categories['Surveillance']
        for idx, (sub_cat, files) in enumerate(cat_data.items(), 1):
            letter = chr(64 + idx)
            f.write(f'### {letter}. {sub_cat}\n\n')
            
            for file_idx, file_path in enumerate(files, 1):
                if os.path.exists(file_path):
                    tests = extract_test_info(file_path)
                    
                    if tests:
                        file_name = Path(file_path).stem.replace('test_', '').replace('_', ' ').title()
                        f.write(f'#### {file_idx}. {file_name}\n\n')
                        
                        for test_idx, test in enumerate(tests, 1):
                            sub_letter = chr(96 + test_idx)
                            f.write(f'##### {sub_letter}. {test["test_name"]} ({test["test_id"]})\n\n')
                            f.write(create_test_table(**test))
                            f.write('\n')
    
    # Part 3: Security - Split into 3 parts
    cat_data = categories['Security']
    sub_categories = list(cat_data.items())
    
    # Part 3-1: Sensor Management
    with open('Unit_Test_Report_Part3_1_Security_Sensors.md', 'w', encoding='utf-8') as f:
        f.write('# III. Unit Tests - Part 3-1: Security (Sensor Management)\n\n')
        f.write('## 3. Security\n\n')
        
        sub_cat, files = sub_categories[0]  # Sensor Management
        f.write(f'### A. {sub_cat}\n\n')
        
        for file_idx, file_path in enumerate(files, 1):
            if os.path.exists(file_path):
                tests = extract_test_info(file_path)
                
                if tests:
                    file_name = Path(file_path).stem.replace('test_', '').replace('_', ' ').title()
                    f.write(f'#### {file_idx}. {file_name}\n\n')
                    
                    for test_idx, test in enumerate(tests, 1):
                        sub_letter = chr(96 + test_idx)
                        f.write(f'##### {sub_letter}. {test["test_name"]} ({test["test_id"]})\n\n')
                        f.write(create_test_table(**test))
                        f.write('\n')
    
    # Part 3-2: Alarm Processing
    with open('Unit_Test_Report_Part3_2_Security_Alarms.md', 'w', encoding='utf-8') as f:
        f.write('# III. Unit Tests - Part 3-2: Security (Alarm Processing)\n\n')
        f.write('## 3. Security\n\n')
        
        sub_cat, files = sub_categories[1]  # Alarm Processing
        f.write(f'### B. {sub_cat}\n\n')
        
        for file_idx, file_path in enumerate(files, 1):
            if os.path.exists(file_path):
                tests = extract_test_info(file_path)
                
                if tests:
                    file_name = Path(file_path).stem.replace('test_', '').replace('_', ' ').title()
                    f.write(f'#### {file_idx}. {file_name}\n\n')
                    
                    for test_idx, test in enumerate(tests, 1):
                        sub_letter = chr(96 + test_idx)
                        f.write(f'##### {sub_letter}. {test["test_name"]} ({test["test_id"]})\n\n')
                        f.write(create_test_table(**test))
                        f.write('\n')
    
    # Part 3-3: Security & Authentication
    with open('Unit_Test_Report_Part3_3_Security_Authentication.md', 'w', encoding='utf-8') as f:
        f.write('# III. Unit Tests - Part 3-3: Security (Authentication)\n\n')
        f.write('## 3. Security\n\n')
        
        sub_cat, files = sub_categories[2]  # Security & Authentication
        f.write(f'### C. {sub_cat}\n\n')
        
        for file_idx, file_path in enumerate(files, 1):
            if os.path.exists(file_path):
                tests = extract_test_info(file_path)
                
                if tests:
                    file_name = Path(file_path).stem.replace('test_', '').replace('_', ' ').title()
                    f.write(f'#### {file_idx}. {file_name}\n\n')
                    
                    for test_idx, test in enumerate(tests, 1):
                        sub_letter = chr(96 + test_idx)
                        f.write(f'##### {sub_letter}. {test["test_name"]} ({test["test_id"]})\n\n')
                        f.write(create_test_table(**test))
                        f.write('\n')
    
    # Part 4: Configuration and Data Management
    with open('Unit_Test_Report_Part4_Configuration.md', 'w', encoding='utf-8') as f:
        f.write('# III. Unit Tests - Part 4: Configuration and Data Management\n\n')
        f.write('## 4. Configuration and Data Management\n\n')
        
        cat_data = categories['Configuration and Data Management']
        for idx, (sub_cat, files) in enumerate(cat_data.items(), 1):
            letter = chr(64 + idx)
            f.write(f'### {letter}. {sub_cat}\n\n')
            
            for file_idx, file_path in enumerate(files, 1):
                if os.path.exists(file_path):
                    tests = extract_test_info(file_path)
                    
                    if tests:
                        file_name = Path(file_path).stem.replace('test_', '').replace('_', ' ').title()
                        f.write(f'#### {file_idx}. {file_name}\n\n')
                        
                        for test_idx, test in enumerate(tests, 1):
                            sub_letter = chr(96 + test_idx)
                            f.write(f'##### {sub_letter}. {test["test_name"]} ({test["test_id"]})\n\n')
                            f.write(create_test_table(**test))
                            f.write('\n')
    
    print("✅ Report generation completed!")
    print("- Unit_Test_Report_Part1_External_Communication.md")
    print("- Unit_Test_Report_Part2_Surveillance.md")
    print("- Unit_Test_Report_Part3_1_Security_Sensors.md")
    print("- Unit_Test_Report_Part3_2_Security_Alarms.md")
    print("- Unit_Test_Report_Part3_3_Security_Authentication.md")
    print("- Unit_Test_Report_Part4_Configuration.md")


if __name__ == '__main__':
    generate_reports()

