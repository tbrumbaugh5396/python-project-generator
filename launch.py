#!/usr/bin/env python3
"""
Launcher script for Python Project Generator
This can be run from within the package directory.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to Python path so we can import the package
current_dir = Path(__file__).parent.absolute()
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# Import and run the main module
try:
    from importlib import import_module
    module_name = current_dir.name
    main_module = import_module(f"{module_name}.__main__")
    sys.exit(main_module.main())
except Exception as e:
    print(f"Error launching Python Project Generator: {e}")
    print("\nAlternatively, run from the parent directory:")
    print(f'cd "{parent_dir}"')
    print(f'python3 -m "{module_name}"')
    sys.exit(1) 