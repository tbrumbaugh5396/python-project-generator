#!/usr/bin/env python3
"""
python_project_generator package entry point

Allows: python -m python_project_generator [--gui|--cli]
"""

import sys
import argparse


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Python Project Generator - Create customizable Python project skeletons",
        prog="python -m python_project_generator",
    )
    parser.add_argument("--cli", action="store_true", help="Launch CLI interface instead of GUI")
    parser.add_argument("--gui", action="store_true", help="Launch GUI interface (default)")
    parser.add_argument("--version", action="version", version="Python Project Generator 1.0.0")

    args, remaining = parser.parse_known_args()

    if args.cli:
        # CLI
        try:
            from . import project_generator as cli_mod
        except Exception:
            try:
                import project_generator as cli_mod  # type: ignore
            except Exception as e:
                print(f"Error loading CLI: {e}")
                return 1
        sys.argv = [sys.argv[0]] + remaining
        return cli_mod.main()

    # GUI (default)
    try:
        import wx  # type: ignore
        try:
            from . import generator_gui as gui_mod
        except Exception:
            import generator_gui as gui_mod  # type: ignore
    except Exception as e:
        print("Error: GUI dependencies not available.")
        print("Please install wxPython: pip install wxpython")
        print(f"Details: {e}")
        print("\nAlternatively, use the CLI interface:")
        print("python -m python_project_generator --cli --help")
        return 1

    app = gui_mod.ProjectGeneratorApp()
    app.MainLoop()
    return 0


if __name__ == "__main__":
    sys.exit(main())


