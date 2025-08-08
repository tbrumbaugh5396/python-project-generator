#!/usr/bin/env python3
"""
Python Project Generator - Main Module Entry Point

This module allows the Python Project Generator to be run as a module:
    python -m python_project_generator

By default, it launches the GUI application. Use --cli flag for CLI mode.
"""

import sys
import argparse
from pathlib import Path

# Add current directory to Python path to find modules
current_dir = Path(__file__).parent.absolute()
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

def main():
    """Main entry point for module execution."""
    parser = argparse.ArgumentParser(
        description="Python Project Generator - Create customizable Python project skeletons",
        prog="python -m python_project_generator"
    )
    parser.add_argument(
        "--cli", 
        action="store_true", 
        help="Launch CLI interface instead of GUI"
    )
    parser.add_argument(
        "--gui", 
        action="store_true", 
        help="Launch GUI interface (default)"
    )
    parser.add_argument(
        "--version", 
        action="version", 
        version="Python Project Generator 1.0.0"
    )
    
    # Parse only known args to allow CLI args to pass through
    args, remaining = parser.parse_known_args()
    
    # Determine which interface to launch
    if args.cli:
        # Launch CLI interface
        from .project_generator import main as cli_main
        
        # Restore remaining args for CLI parsing
        sys.argv = [sys.argv[0]] + remaining
        return cli_main()
    
    else:
        # Launch GUI interface (default)
        try:
            import wx
            from .generator_gui import ProjectGeneratorApp
            
            app = ProjectGeneratorApp()
            app.MainLoop()
            return 0
            
        except ImportError as e:
            print("Error: GUI dependencies not available.")
            print("Please install wxPython: pip install wxpython")
            print(f"Details: {e}")
            print("\nAlternatively, use the CLI interface:")
            print("python -m python_project_generator --cli --help")
            return 1
        except Exception as e:
            print(f"Error launching GUI: {e}")
            print("\nTry using the CLI interface:")
            print("python -m python_project_generator --cli --help")
            return 1


if __name__ == "__main__":
    sys.exit(main()) 