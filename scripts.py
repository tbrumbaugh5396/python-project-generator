#!/usr/bin/env python3
"""
Build script for the Python Project Generator.
Handles building, testing, and packaging operations.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description=""):
    """Run a command and handle errors."""
    if description:
        print(f"🔄 {description}...")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False

def clean_build():
    """Clean build artifacts."""
    print("🧹 Cleaning build artifacts...")
    
    patterns = [
        "build",
        "dist", 
        "*.egg-info",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".tox",
        ".coverage"
    ]
    
    for pattern in patterns:
        for path in Path(".").rglob(pattern):
            if path.exists():
                if path.is_dir():
                    shutil.rmtree(path)
                    print(f"  Removed directory: {path}")
                else:
                    path.unlink()
                    print(f"  Removed file: {path}")

def run_tests():
    """Run the test suite."""
    return run_command("python3 -m pytest tests/ -v", "Running tests")

def run_linting():
    """Run code linting."""
    success = True
    
    # Run flake8
    if not run_command("python3 -m flake8 .", "Running flake8"):
        success = False
    
    # Run mypy
    if not run_command("python3 -m mypy .", "Running mypy"):
        success = False
    
    return success

def format_code():
    """Format code with black."""
    return run_command("python3 -m black .", "Formatting code with black")

def build_package():
    """Build the package."""
    return run_command("python3 -m build", "Building package")

def install_dev_dependencies():
    """Install development dependencies."""
    return run_command("pip install -r requirements-dev.txt", "Installing dev dependencies")

def install_package():
    """Install package in development mode."""
    return run_command("pip install -e .", "Installing package in development mode")

def main():
    """Main build script."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Build script for Python Project Generator")
    parser.add_argument("action", choices=[
        "clean", "test", "lint", "format", "build", "install-dev", "install", "all"
    ], help="Action to perform")
    
    args = parser.parse_args()
    
    success = True
    
    if args.action == "clean":
        clean_build()
    
    elif args.action == "test":
        success = run_tests()
    
    elif args.action == "lint":
        success = run_linting()
    
    elif args.action == "format":
        success = format_code()
    
    elif args.action == "build":
        clean_build()
        success = build_package()
    
    elif args.action == "install-dev":
        success = install_dev_dependencies()
    
    elif args.action == "install":
        success = install_package()
    
    elif args.action == "all":
        clean_build()
        success &= install_dev_dependencies()
        success &= format_code()
        success &= run_linting()
        success &= run_tests()
        success &= build_package()
    
    if success:
        print("✅ Build completed successfully!")
        return 0
    else:
        print("❌ Build failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 