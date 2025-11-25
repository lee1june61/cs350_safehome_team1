"""SafeHome Control Panel package.

Refactored control panel following modern development practices:
- SOLID principles
- Separation of concerns
- MVP pattern
- Testable architecture

Structure:
- models/: Data models and state definitions
- views/: UI components (presentation layer)
- controllers/: Business logic coordinators (presenters)
- services/: Business logic services
- utils/: Utility functions
- config/: Configuration constants
"""

from .main import SafeHomeControlPanel

__all__ = ["SafeHomeControlPanel"]
