#!/usr/bin/env python3
"""
Simple runner script for the Python Project Generator.
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from generator_gui import main
except ImportError as e:
    print(f"Error importing generator: {e}")
    print("Make sure wxPython is installed: pip install wxpython")
    sys.exit(1)

if __name__ == "__main__":
    print("Starting Python Project Generator...")
    sys.exit(main()) 