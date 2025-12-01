"""
SafeHome tests package bootstrap.

- Adds the project root to sys.path so `import src...` works regardless of the
  current working directory.
- Documents the layout for contributors.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
