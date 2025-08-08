# Changelog

All notable changes to the Python Project Generator will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-XX

### Added
- **Multiple Template Options**: Added 15+ project templates including:
  - Minimal Python project
  - Flask web application
  - FastAPI web API
  - Django web application
  - Data science project with Jupyter notebooks
  - Machine learning project
  - CLI tool with Click framework
  - Python library for PyPI
  - Game development with Pygame
  - Desktop GUI application with wxPython
  - Microservice template
  - API client library
  - Automation scripts
  - Jupyter research project

- **Modern Packaging Setup**: 
  - Comprehensive `pyproject.toml` configuration
  - Updated `setup.py` with proper metadata
  - `MANIFEST.in` for file inclusion
  - Build scripts and development tools

- **Professional Project Structure**: Each template includes:
  - Proper package structure with `src/` layout
  - Comprehensive testing setup
  - Documentation templates
  - Configuration files
  - Dependency management
  - Entry points for CLI/GUI usage

- **Enhanced GUI Interface**: 
  - wxPython-based GUI with multiple tabs
  - Template selection with descriptions
  - Feature customization options
  - Project metadata input
  - Live preview of project structure
  - Output logging and status updates

- **Robust CLI Interface**:
  - Command-line tool with argument parsing
  - Template listing functionality
  - Customizable project generation
  - Verbose logging options

- **Development Tools**:
  - Comprehensive test suite
  - Code quality tools (black, flake8, mypy)
  - Build automation scripts
  - CI/CD configuration templates

### Changed
- Upgraded minimum Python version to 3.8+
- Improved error handling and logging
- Enhanced template customization system
- Better file organization and structure

### Technical Details
- **Dependencies**: wxPython 4.2+, modern Python packaging tools
- **Testing**: pytest-based test suite with coverage
- **Code Quality**: Black formatting, flake8 linting, mypy type checking
- **Documentation**: Sphinx-ready documentation structure
- **Packaging**: Modern Python packaging standards with pyproject.toml

### Installation
```bash
pip install python-project-generator
```

### Usage
```bash
# GUI mode
python-project-generator-gui

# CLI mode
python-project-generator my_project --template flask-web-app --author "Your Name"
``` 