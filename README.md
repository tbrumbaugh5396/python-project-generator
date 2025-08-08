# Python Project Generator

A standalone GUI tool for generating customizable Python project skeletons from templates.

## Features

- 🎨 **Beautiful GUI Interface** - Intuitive wxPython-based interface
- 📁 **Multiple Templates** - Support for different project templates
- ⚙️ **Customizable Features** - Select exactly what you need
- 🔄 **Template Management** - Download and manage templates from Git repositories
- 📦 **Professional Structure** - Generate production-ready Python projects
- 🚀 **Ready to Deploy** - Projects ready for PyPI and development

## Installation

### Method 1: Direct Installation (Recommended)

```bash
pip install wxpython
python generator_gui.py
```

### Method 2: Install as Package

```bash
pip install -e .
python-project-generator-gui
```

## Usage

### GUI Application

Launch the GUI application:

```bash
python generator_gui.py
```

Or if installed as a package:

```bash
python-project-generator-gui
```

### Command Line

Use the command-line interface:

```bash
python project_generator.py
```

## How It Works

1. **Choose Template**: Select from available project templates
2. **Configure Project**: Fill in project details (name, author, description, etc.)
3. **Select Features**: Choose which features to include
4. **Generate**: Click generate to create your project

## Available Templates

### Python Skeleton Project
- Complete Python project structure
- CLI and GUI interfaces
- Unit testing framework
- PyPI packaging setup
- Executable building scripts
- Comprehensive documentation

### Minimal Python Project
- Basic Python project structure
- Essential files only
- Quick start for simple projects

## Features You Can Select

- ✅ **Command Line Interface (CLI)** - argparse-based CLI
- ✅ **Graphical User Interface (GUI)** - wxPython GUI
- ✅ **Unit Tests** - pytest framework and sample tests
- ✅ **Executable Building** - PyInstaller scripts
- ✅ **PyPI Packaging** - setup.py, pyproject.toml
- ✅ **Development Requirements** - Testing and code quality tools
- ✅ **License File** - Multiple license options
- ✅ **README.md** - Comprehensive documentation
- ✅ **Makefile** - Common development tasks
- ✅ **`.gitignore`** - Python-specific ignore rules
- ✅ **GitHub Actions** - CI/CD workflow

## Template Sources

The generator can work with:

- **Git Repositories**: Clone templates from GitHub, GitLab, etc.
- **Local Templates**: Use local template directories
- **Built-in Templates**: Minimal templates included with the generator

## Configuration

Templates are managed in `~/.python-project-generator/templates/`.

To add custom templates, modify the `default_templates` configuration in `project_generator.py`.

## Generated Project Structure

```
your_project/
├── src/
│   └── your_project/
│       ├── __init__.py
│       ├── core.py
│       ├── cli.py          # If CLI selected
│       └── gui.py          # If GUI selected
├── tests/                  # If tests selected
│   ├── __init__.py
│   └── test_core.py
├── scripts/                # If executable selected
│   └── build_executable.py
├── .github/workflows/      # If GitHub Actions selected
│   └── ci.yml
├── setup.py               # If PyPI packaging selected
├── pyproject.toml         # If PyPI packaging selected
├── requirements.txt
├── requirements-dev.txt   # If dev requirements selected
├── Makefile              # If Makefile selected
├── .gitignore            # If gitignore selected
├── LICENSE               # If license selected
└── README.md             # If README selected
```

## Requirements

- Python 3.8+
- wxPython 4.2+
- Git (for template downloads)

## Development

### Running from Source

```bash
git clone <this-repository>
cd python-project-generator
pip install wxpython
python generator_gui.py
```

### Installing in Development Mode

```bash
pip install -e .
```

## Packaging and Distribution

The Python Project Generator is professionally packaged and ready for distribution.

### Building from Source

1. **Clone the repository**:
```bash
git clone https://github.com/python-project-generator/python-project-generator.git
cd python-project-generator
```

2. **Install development dependencies**:
```bash
pip install -r requirements-dev.txt
```

3. **Run tests**:
```bash
python3 scripts.py test
```

4. **Build the package**:
```bash
python3 scripts.py build
```

### Development Workflow

```bash
# Format code
python3 scripts.py format

# Run linting
python3 scripts.py lint

# Run all checks and build
python3 scripts.py all

# Install in development mode
python3 scripts.py install
```

### Package Structure

```
python-project-generator/
├── project_generator.py      # Main generator logic
├── generator_gui.py          # wxPython GUI interface
├── run.py                   # Entry point script
├── setup.py                 # Legacy packaging config
├── pyproject.toml           # Modern packaging config
├── MANIFEST.in              # Package file inclusion rules
├── scripts.py               # Build automation script
├── requirements.txt         # Runtime dependencies
├── requirements-dev.txt     # Development dependencies
├── tests/                   # Test suite
│   ├── __init__.py
│   └── test_project_generator.py
├── LICENSE                  # MIT license
├── CHANGELOG.md            # Version history
└── README.md               # This file
```

### Entry Points

The package provides multiple entry points:

- **GUI Application**: `python-project-generator-gui` or `pyproj-gen-gui`
- **CLI Tool**: `python-project-generator` or `pyproj-gen`

### Dependencies

- **Runtime**: wxPython 4.2+
- **Development**: pytest, black, flake8, mypy, build tools
- **Python**: 3.8+ required

## Examples

### Creating a Full-Featured Project

1. Launch the GUI: `python generator_gui.py`
2. Select "Python Skeleton Project" template
3. Fill in project details:
   - Name: "my_awesome_project"
   - Author: "Your Name"
   - Email: "your@email.com"
   - Description: "An awesome Python project"
4. Select desired features (CLI, GUI, tests, etc.)
5. Choose output directory
6. Click "Generate Project"

### Quick Minimal Project

For a simple project with just the basics:

1. Select "Minimal Python Project" template
2. Fill in basic info
3. Keep default features (tests, packaging, README)
4. Generate

## Customization

### Adding Custom Templates

1. Add template configuration to `project_generator.py`:

```python
"my-template": {
    "name": "My Custom Template",
    "description": "A custom project template",
    "source": "https://github.com/myuser/my-template.git",
    "type": "git",
    "features": ["cli", "tests", "packaging"]
}
```

2. Templates will be automatically downloaded when selected

### Template Structure

Templates should follow this structure:

```
template/
├── src/
│   └── {{package_name}}/
│       ├── __init__.py
│       └── core.py
├── setup.py
├── README.md
└── requirements.txt
```

Use placeholder strings that will be replaced:
- `{{package_name}}` - Package name
- `{{project_name}}` - Project display name
- `{{author}}` - Author name
- `{{email}}` - Author email
- etc.

## Troubleshooting

### wxPython Installation Issues

**macOS:**
```bash
pip install -U wxpython
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install libgtk-3-dev libwebkitgtk-3.0-dev
pip install wxpython
```

**Windows:**
```bash
pip install wxpython
```

### Template Download Issues

- Ensure Git is installed and accessible
- Check internet connection
- Verify template repository URL

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

- Create an issue on GitHub for bugs or feature requests
- Check the documentation for usage instructions
- Review examples for common use cases 