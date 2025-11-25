"""
Test Script for SafeHome Camera Module
=======================================
Simple test script to verify the camera module functionality.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add the project directory to the path
project_path = Path(__file__).parent
if str(project_path) not in sys.path:
    sys.path.insert(0, str(project_path))

from src.controllers.camera_controller import CameraController
from src.models.camera import SafeHomeCamera
from src.utils.exceptions import CameraNotFoundError, CameraDisabledError


def test_camera_controller() -> None:
    """Test the CameraController functionality."""
    print("=" * 60)
    print("SafeHome Camera Module Test (Team Style)")
    print("=" * 60)
    
    # Create a camera controller
    print("\n1. Creating CameraController...")
    controller = CameraController()
    print(f"   {controller}")
    
    # Add cameras
    print("\n2. Adding cameras...")
    cam1_id = controller.add_camera(100, 200)
    print(f"   Added camera {cam1_id} at (100, 200)")
    
    cam2_id = controller.add_camera(300, 400)
    print(f"   Added camera {cam2_id} at (300, 400)")
    
    cam3_id = controller.add_camera(500, 600)
    print(f"   Added camera {cam3_id} at (500, 600)")
    
    print(f"   Total cameras: {controller.get_total_camera_number()}")
    
    # Get all camera info
    print("\n3. Getting all camera info...")
    all_info = controller.get_all_camera_info()
    for info in all_info:
        print(f"   Camera {info['id']}: location={info['location']}, "
              f"enabled={info['enabled']}, pan={info['pan_angle']}, "
              f"zoom={info['zoom_level']}")
    
    # Enable cameras
    print("\n4. Enabling cameras...")
    controller.enable_cameras([cam1_id, cam2_id])
    print(f"   Enabled cameras {cam1_id} and {cam2_id}")
    
    # Set password for a camera
    print("\n5. Setting password for camera 1...")
    controller.set_camera_password(cam1_id, "secure123")
    print("   Password set successfully")
    
    # Validate password
    print("\n6. Validating password...")
    is_valid = controller.validate_camera_password(cam1_id, "secure123")
    print(f"   Password 'secure123': {'Valid' if is_valid else 'Invalid'}")
    
    is_valid = controller.validate_camera_password(cam1_id, "wrong")
    print(f"   Password 'wrong': {'Valid' if is_valid else 'Invalid'}")
    
    # Control a camera
    print("\n7. Controlling camera (zoom and pan)...")
    camera = controller.get_camera_by_id(cam1_id)
    print(f"   Initial state: pan={camera.get_pan_angle()}, zoom={camera.get_zoom_level()}")
    
    # Zoom in
    controller.control_single_camera(cam1_id, CameraController.CONTROL_ZOOM_IN)
    print(f"   After zoom in: zoom={camera.get_zoom_level()}")
    
    # Pan right
    controller.control_single_camera(cam1_id, CameraController.CONTROL_PAN_RIGHT)
    print(f"   After pan right: pan={camera.get_pan_angle()}")
    
    # Pan left
    controller.control_single_camera(cam1_id, CameraController.CONTROL_PAN_LEFT)
    print(f"   After pan left: pan={camera.get_pan_angle()}")
    
    # Test camera limits
    print("\n8. Testing camera limits...")
    camera = controller.get_camera_by_id(cam2_id)
    # Try to zoom to maximum
    print(f"   Initial zoom: {camera.get_zoom_level()}")
    for i in range(10):
        if not camera.zoom_in():
            print(f"   Reached max zoom: {camera.get_zoom_level()}")
            break
    
    # Try to pan to maximum right
    print(f"   Initial pan: {camera.get_pan_angle()}")
    for i in range(10):
        if not camera.pan_right():
            print(f"   Reached max pan right: {camera.get_pan_angle()}")
            break
    
    # Test validation
    print("\n9. Testing validation...")
    try:
        camera.validate()
        print("   Camera validation: PASS")
    except Exception as e:
        print(f"   Camera validation: FAIL ({e})")
    
    # Enable all cameras
    print("\n10. Enabling all cameras...")
    controller.enable_all_cameras()
    enabled_count = sum(1 for info in controller.get_all_camera_info() if info['enabled'])
    print(f"   Enabled cameras: {enabled_count}/{controller.get_total_camera_number()}")
    
    # Disable all cameras
    print("\n11. Disabling all cameras...")
    controller.disable_all_cameras()
    enabled_count = sum(1 for info in controller.get_all_camera_info() if info['enabled'])
    print(f"   Enabled cameras: {enabled_count}/{controller.get_total_camera_number()}")
    
    # Test exception handling
    print("\n12. Testing exception handling...")
    try:
        controller.get_camera_by_id(999)
    except CameraNotFoundError as e:
        print(f"   CameraNotFoundError caught: {e}")
    
    camera3 = controller.get_camera_by_id(cam3_id)
    camera3.disable()
    try:
        camera3.display_view()
    except CameraDisabledError as e:
        print(f"   CameraDisabledError caught: {e}")
    
    # Delete a camera
    print("\n13. Deleting camera 3...")
    success = controller.delete_camera(cam3_id)
    print(f"   Delete {'successful' if success else 'failed'}")
    print(f"   Total cameras: {controller.get_total_camera_number()}")
    
    # Display final state
    print("\n14. Final camera info...")
    all_info = controller.get_all_camera_info()
    for info in all_info:
        print(f"   Camera {info['id']}: location={info['location']}, "
              f"enabled={info['enabled']}, pan={info['pan_angle']}, "
              f"zoom={info['zoom_level']}, has_password={info['has_password']}")
    
    # Cleanup
    print("\n15. Cleaning up...")
    controller.cleanup()
    print("   Cleanup complete")
    
    print("\n" + "=" * 60)
    print("All tests completed successfully!")
    print("=" * 60)


def test_individual_camera() -> None:
    """Test individual SafeHomeCamera functionality."""
    print("\n" + "=" * 60)
    print("Individual Camera Test (Team Style)")
    print("=" * 60)
    
    # Create a camera
    print("\n1. Creating SafeHomeCamera...")
    camera = SafeHomeCamera(1, 100, 200)
    print(f"   {camera}")
    
    # Test getters
    print("\n2. Testing getters...")
    print(f"   ID: {camera.get_id()}")
    print(f"   Location: {camera.get_location()}")
    print(f"   Enabled: {camera.is_enabled()}")
    print(f"   Has Password: {camera.has_password()}")
    print(f"   Pan Angle: {camera.get_pan_angle()}")
    print(f"   Zoom Level: {camera.get_zoom_level()}")
    
    # Enable camera
    print("\n3. Enabling camera...")
    camera.enable()
    print(f"   Enabled: {camera.is_enabled()}")
    
    # Set password
    print("\n4. Setting password...")
    camera.set_password("test123")
    print(f"   Has Password: {camera.has_password()}")
    print(f"   Password: {camera.get_password()}")
    
    # Test controls when enabled
    print("\n5. Testing controls...")
    print(f"   Zoom in: {camera.zoom_in()}")
    print(f"   Zoom: {camera.get_zoom_level()}")
    print(f"   Pan right: {camera.pan_right()}")
    print(f"   Pan: {camera.get_pan_angle()}")
    
    # Test validation
    print("\n6. Testing validation...")
    try:
        camera.validate()
        print("   Validation: PASS")
    except Exception as e:
        print(f"   Validation: FAIL ({e})")
    
    # Disable and test
    print("\n7. Disabling camera...")
    camera.disable()
    print(f"   Enabled: {camera.is_enabled()}")
    print(f"   Zoom in (should fail): {camera.zoom_in()}")
    
    # Cleanup
    print("\n8. Cleaning up...")
    camera.cleanup()
    print("   Cleanup complete")
    
    print("\n" + "=" * 60)
    print("Individual camera test completed!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_camera_controller()
        test_individual_camera()
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
