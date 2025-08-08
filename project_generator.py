"""
Standalone Python Project Generator

A flexible tool for generating Python projects from templates.
Can work with local templates or remote Git repositories.
"""

__version__ = "1.0.0"

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime
import json


class TemplateManager:
    """Manages project templates from various sources."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.templates_dir = Path.home() / ".python-project-generator" / "templates"
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        
        # Default templates configuration
        self.default_templates = {
            "python-skeleton": {
                "name": "Python Skeleton Project",
                "description": "Complete Python project with CLI, GUI, testing, and packaging",
                "source": "https://github.com/yourusername/python-skeleton-project.git",
                "type": "git",
                "features": ["cli", "gui", "tests", "executable", "pypi_packaging", "dev_requirements", "license", "readme", "makefile", "gitignore", "github_actions"]
            },
            "minimal-python": {
                "name": "Minimal Python Project",
                "description": "Basic Python project structure",
                "source": "local",
                "type": "builtin",
                "features": ["pypi_packaging", "tests", "license", "readme", "gitignore"]
            },
            "flask-web-app": {
                "name": "Flask Web Application",
                "description": "Flask web application with blueprints, templates, and database support",
                "source": "local",
                "type": "builtin",
                "features": ["web_framework", "database", "templates", "static_files", "tests", "pypi_packaging", "license", "readme", "gitignore", "docker"]
            },
            "fastapi-web-api": {
                "name": "FastAPI Web API",
                "description": "Modern async FastAPI application with automatic docs and validation",
                "source": "local",
                "type": "builtin",
                "features": ["web_framework", "api_docs", "async", "database", "tests", "pypi_packaging", "license", "readme", "gitignore", "docker"]
            },
            "django-web-app": {
                "name": "Django Web Application",
                "description": "Full-featured Django web application with admin and user management",
                "source": "local",
                "type": "builtin",
                "features": ["web_framework", "admin", "user_auth", "database", "templates", "static_files", "tests", "license", "readme", "gitignore"]
            },
            "data-science-project": {
                "name": "Data Science Project",
                "description": "Data science project with Jupyter notebooks, analysis scripts, and visualization",
                "source": "local",
                "type": "builtin",
                "features": ["jupyter", "data_analysis", "visualization", "notebooks", "datasets", "tests", "pypi_packaging", "license", "readme", "gitignore"]
            },
            "machine-learning-project": {
                "name": "Machine Learning Project",
                "description": "ML project template with model training, evaluation, and deployment scripts",
                "source": "local",
                "type": "builtin",
                "features": ["ml_framework", "model_training", "evaluation", "deployment", "experiments", "tests", "pypi_packaging", "license", "readme", "gitignore", "docker"]
            },
            "cli-tool": {
                "name": "Command Line Tool",
                "description": "Professional CLI tool with Click framework and comprehensive testing",
                "source": "local",
                "type": "builtin",
                "features": ["cli", "click_framework", "config_files", "logging", "tests", "pypi_packaging", "license", "readme", "gitignore"]
            },
            "python-library": {
                "name": "Python Library/Package",
                "description": "Professional Python library ready for PyPI publication",
                "source": "local",
                "type": "builtin",
                "features": ["library_structure", "api_documentation", "comprehensive_tests", "pypi_packaging", "tox", "ci_cd", "license", "readme", "gitignore", "github_actions"]
            },
            "game-development": {
                "name": "Game Development",
                "description": "Game development project with Pygame and asset management",
                "source": "local",
                "type": "builtin",
                "features": ["game_framework", "asset_management", "scenes", "sprites", "sound", "tests", "pypi_packaging", "license", "readme", "gitignore"]
            },
            "desktop-gui-app": {
                "name": "Desktop GUI Application",
                "description": "Cross-platform desktop GUI application with wxPython and packaging",
                "source": "local",
                "type": "builtin",
                "features": ["gui", "desktop_app", "menus", "dialogs", "config", "executable", "tests", "pypi_packaging", "license", "readme", "gitignore"]
            },
            "microservice": {
                "name": "Microservice",
                "description": "Microservice template with FastAPI, Docker, and health checks",
                "source": "local",
                "type": "builtin",
                "features": ["web_framework", "microservice", "health_checks", "metrics", "logging", "docker", "kubernetes", "tests", "license", "readme", "gitignore"]
            },
            "api-client-library": {
                "name": "API Client Library",
                "description": "Python library for interacting with REST APIs",
                "source": "local",
                "type": "builtin",
                "features": ["api_client", "authentication", "rate_limiting", "retries", "comprehensive_tests", "pypi_packaging", "license", "readme", "gitignore"]
            },
            "automation-scripts": {
                "name": "Automation Scripts",
                "description": "Collection of automation scripts with scheduling and monitoring",
                "source": "local",
                "type": "builtin",
                "features": ["automation", "scheduling", "monitoring", "logging", "config_files", "tests", "license", "readme", "gitignore"]
            },
            "jupyter-research": {
                "name": "Jupyter Research Project",
                "description": "Research project template with Jupyter notebooks and reproducible environment",
                "source": "local",
                "type": "builtin",
                "features": ["jupyter", "research", "reproducible_env", "data_versioning", "notebooks", "reports", "license", "readme", "gitignore"]
            }}
    
    def get_available_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get list of available templates."""
        return self.default_templates
    
    def download_template(self, template_id: str) -> Optional[Path]:
        """Download template from remote source."""
        template_config = self.default_templates.get(template_id)
        if not template_config:
            self.logger.error(f"Template {template_id} not found")
            return None
        
        if template_config["type"] == "git":
            return self._clone_git_template(template_id, template_config["source"])
        elif template_config["type"] == "builtin":
            return self._get_builtin_template(template_id)
        
        return None
    
    def _clone_git_template(self, template_id: str, git_url: str) -> Optional[Path]:
        """Clone a git repository template."""
        template_path = self.templates_dir / template_id
        
        try:
            if template_path.exists():
                # Update existing template
                self.logger.info(f"Updating template {template_id}...")
                subprocess.run(
                    ["git", "pull"],
                    cwd=template_path,
                    check=True,
                    capture_output=True
                )
            else:
                # Clone new template
                self.logger.info(f"Downloading template {template_id}...")
                subprocess.run(
                    ["git", "clone", git_url, str(template_path)],
                    check=True,
                    capture_output=True
                )
            
            return template_path
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to download template: {e}")
            return None
    
    def _get_builtin_template(self, template_id: str) -> Path:
        """Get path to builtin template."""
        # Builtin templates are generated dynamically, so return None
        # The actual generation happens in _generate_builtin_project
        return None


class ProjectGenerator:
    """Generates Python skeleton projects with customizable features."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.template_manager = TemplateManager()
    
    def generate_project(
        self,
        project_name: str,
        output_dir: Path,
        template_id: str = "python-skeleton",
        features: Optional[Dict[str, bool]] = None,
        metadata: Optional[Dict[str, str]] = None
    ) -> bool:
        """
        Generate a new Python project from template.
        
        Args:
            project_name: Name of the project
            output_dir: Directory where project will be created
            template_id: ID of the template to use
            features: Dict of feature flags
            metadata: Project metadata (author, email, description, etc.)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get template
            template_path = self.template_manager.download_template(template_id)
            if not template_path:
                # Fallback to builtin generation
                return self._generate_builtin_project(project_name, output_dir, features or {}, metadata or {}, template_id)
            
            project_path = output_dir / project_name
            project_path.mkdir(parents=True, exist_ok=True)
            
            # Copy template
            self._copy_template(template_path, project_path)
            
            # Customize project
            self._customize_project(project_path, project_name, features or {}, metadata or {})
            
            self.logger.info(f"Project '{project_name}' generated successfully at {project_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to generate project: {e}")
            return False
    
    def _copy_template(self, template_path: Path, project_path: Path):
        """Copy template to project directory."""
        # Skip .git directory and other unwanted files
        ignore_patterns = {'.git', '__pycache__', '*.pyc', '.DS_Store', '.vscode', '.idea'}
        
        for item in template_path.iterdir():
            if item.name in ignore_patterns:
                continue
                
            if item.is_dir():
                shutil.copytree(item, project_path / item.name, ignore=shutil.ignore_patterns(*ignore_patterns))
            else:
                shutil.copy2(item, project_path / item.name)
    
    def _customize_project(self, project_path: Path, project_name: str, features: Dict[str, bool], metadata: Dict[str, str]):
        """Customize the project based on features and metadata."""
        package_name = self._to_package_name(project_name)
        
        # Update package names in files
        self._update_package_references(project_path, project_name, package_name, metadata)
        
        # Remove unwanted features
        self._remove_unwanted_features(project_path, features)
    
    def _update_package_references(self, project_path: Path, project_name: str, package_name: str, metadata: Dict[str, str]):
        """Update package references throughout the project."""
        replacements = {
            "skeleton": package_name,
            "Skeleton": self._to_class_name(package_name),
            "python-skeleton-project": package_name.replace('_', '-'),
            "Python Skeleton": project_name,
            "A skeleton Python project": metadata.get('description', f'A {project_name} project'),
            "Your Name": metadata.get('author', 'Your Name'),
            "your.email@example.com": metadata.get('email', 'your.email@example.com'),
            "0.1.0": metadata.get('version', '0.1.0'),
            "https://github.com/yourusername/python-skeleton-project": metadata.get('url', f'https://github.com/yourusername/{package_name.replace("_", "-")}'),
        }
        
        # Files to update
        text_files = [
            'setup.py', 'pyproject.toml', 'README.md', 'LICENSE',
            'requirements.txt', 'requirements-dev.txt', 'Makefile'
        ]
        
        # Update text files
        for file_pattern in text_files:
            for file_path in project_path.rglob(file_pattern):
                if file_path.is_file():
                    self._update_file_content(file_path, replacements)
        
        # Update Python files
        for py_file in project_path.rglob("*.py"):
            if py_file.is_file():
                self._update_file_content(py_file, replacements)
        
        # Rename skeleton directory to new package name
        src_dir = project_path / "src"
        if src_dir.exists():
            skeleton_dir = src_dir / "skeleton"
            if skeleton_dir.exists() and package_name != "skeleton":
                new_package_dir = src_dir / package_name
                skeleton_dir.rename(new_package_dir)
    
    def _update_file_content(self, file_path: Path, replacements: Dict[str, str]):
        """Update file content with replacements."""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            for old_text, new_text in replacements.items():
                content = content.replace(old_text, new_text)
            
            file_path.write_text(content, encoding='utf-8')
            
        except Exception as e:
            self.logger.warning(f"Could not update {file_path}: {e}")
    
    def _remove_unwanted_features(self, project_path: Path, features: Dict[str, bool]):
        """Remove files for unwanted features."""
        if not features.get('cli', True):
            self._remove_files(project_path, ['**/cli.py'])
        
        if not features.get('gui', True):
            self._remove_files(project_path, ['**/gui.py', '**/generator_gui.py'])
        
        if not features.get('tests', True):
            self._remove_dirs(project_path, ['tests'])
        
        if not features.get('executable', True):
            self._remove_files(project_path, ['scripts/build_executable.py', '**/build_executable.py'])
        
        if not features.get('dev_requirements', True):
            self._remove_files(project_path, ['requirements-dev.txt'])
        
        if not features.get('license', True):
            self._remove_files(project_path, ['LICENSE'])
        
        if not features.get('readme', True):
            self._remove_files(project_path, ['README.md'])
        
        if not features.get('makefile', True):
            self._remove_files(project_path, ['Makefile'])
        
        if not features.get('gitignore', True):
            self._remove_files(project_path, ['.gitignore'])
        
        if not features.get('github_actions', True):
            self._remove_dirs(project_path, ['.github'])
    
    def _remove_files(self, project_path: Path, patterns: List[str]):
        """Remove files matching patterns."""
        for pattern in patterns:
            for file_path in project_path.rglob(pattern):
                if file_path.is_file():
                    file_path.unlink()
                    self.logger.debug(f"Removed file: {file_path}")
    
    def _remove_dirs(self, project_path: Path, dir_names: List[str]):
        """Remove directories."""
        for dir_name in dir_names:
            dir_path = project_path / dir_name
            if dir_path.exists() and dir_path.is_dir():
                shutil.rmtree(dir_path)
                self.logger.debug(f"Removed directory: {dir_path}")
    
    def _generate_builtin_project(self, project_name: str, output_dir: Path, features: Dict[str, bool], metadata: Dict[str, str], template_id: str = "minimal-python") -> bool:
        """Generate a project using builtin templates."""
        try:
            project_path = output_dir / project_name
            package_name = self._to_package_name(project_name)
            
            # Create basic structure
            project_path.mkdir(parents=True, exist_ok=True)
            
            # Generate based on template type
            if template_id == "flask-web-app":
                return self._generate_flask_template(project_path, project_name, package_name, features, metadata)
            elif template_id == "fastapi-web-api":
                return self._generate_fastapi_template(project_path, project_name, package_name, features, metadata)
            elif template_id == "django-web-app":
                return self._generate_django_template(project_path, project_name, package_name, features, metadata)
            elif template_id == "data-science-project":
                return self._generate_data_science_template(project_path, project_name, package_name, features, metadata)
            elif template_id == "machine-learning-project":
                return self._generate_ml_template(project_path, project_name, package_name, features, metadata)
            elif template_id == "cli-tool":
                return self._generate_cli_tool_template(project_path, project_name, package_name, features, metadata)
            elif template_id == "python-library":
                return self._generate_library_template(project_path, project_name, package_name, features, metadata)
            elif template_id == "game-development":
                return self._generate_game_template(project_path, project_name, package_name, features, metadata)
            elif template_id == "desktop-gui-app":
                return self._generate_desktop_gui_template(project_path, project_name, package_name, features, metadata)
            elif template_id == "microservice":
                return self._generate_microservice_template(project_path, project_name, package_name, features, metadata)
            elif template_id == "api-client-library":
                return self._generate_api_client_template(project_path, project_name, package_name, features, metadata)
            elif template_id == "automation-scripts":
                return self._generate_automation_template(project_path, project_name, package_name, features, metadata)
            elif template_id == "jupyter-research":
                return self._generate_jupyter_research_template(project_path, project_name, package_name, features, metadata)
            else:
                # Default minimal template
                return self._generate_minimal_template(project_path, project_name, package_name, features, metadata)
            
        except Exception as e:
            self.logger.error(f"Failed to generate builtin project: {e}")
            return False
    
    def _create_basic_init(self, src_dir: Path, project_name: str, metadata: Dict[str, str]):
        """Create basic __init__.py file."""
        content = f'''"""
{metadata.get('description', f'A {project_name} project')}
"""

__version__ = "{metadata.get('version', '0.1.0')}"
__author__ = "{metadata.get('author', 'Your Name')}"
__email__ = "{metadata.get('email', 'your.email@example.com')}"
'''
        (src_dir / "__init__.py").write_text(content)
    
    def _create_basic_core(self, src_dir: Path, project_name: str, package_name: str, metadata: Dict[str, str]):
        """Create basic core module."""
        class_name = self._to_class_name(package_name)
        content = f'''"""
Core module for {project_name}.
"""


class {class_name}:
    """Main application class."""
    
    def __init__(self):
        self.name = "{project_name}"
        self.version = "{metadata.get('version', '0.1.0')}"
    
    def run(self):
        """Run the application."""
        print(f"Hello from {{self.name}} v{{self.version}}!")
        return 0
'''
        (src_dir / "core.py").write_text(content)
    
    def _create_basic_cli(self, src_dir: Path, project_name: str, package_name: str, metadata: Dict[str, str]):
        """Create basic CLI module."""
        content = f'''"""
Command-line interface for {project_name}.
"""

import argparse
import sys
from .core import {self._to_class_name(package_name)}


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="{metadata.get('description', f'A {project_name} CLI')}")
    parser.add_argument('--version', action='version', version='{metadata.get("version", "0.1.0")}')
    
    args = parser.parse_args()
    
    app = {self._to_class_name(package_name)}()
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
'''
        (src_dir / "cli.py").write_text(content)
    
    def _create_basic_tests(self, project_path: Path, package_name: str):
        """Create basic test structure."""
        tests_dir = project_path / "tests"
        tests_dir.mkdir(exist_ok=True)
        
        (tests_dir / "__init__.py").write_text("# Tests package")
        
        test_content = f'''"""
Basic tests for {package_name}.
"""

from {package_name}.core import {self._to_class_name(package_name)}


def test_creation():
    """Test that the main class can be created."""
    app = {self._to_class_name(package_name)}()
    assert app is not None


def test_run():
    """Test that the app can run."""
    app = {self._to_class_name(package_name)}()
    result = app.run()
    assert result == 0
'''
        (tests_dir / "test_core.py").write_text(test_content)
    
    def _create_basic_setup(self, project_path: Path, project_name: str, package_name: str, metadata: Dict[str, str]):
        """Create basic setup files."""
        # setup.py
        setup_content = f'''from setuptools import setup, find_packages

setup(
    name="{package_name.replace('_', '-')}",
    version="{metadata.get('version', '0.1.0')}",
    author="{metadata.get('author', 'Your Name')}",
    author_email="{metadata.get('email', 'your.email@example.com')}",
    description="{metadata.get('description', f'A {project_name} project')}",
    packages=find_packages(where="src"),
    package_dir={{"": "src"}},
    python_requires=">=3.8",
    entry_points={{
        "console_scripts": [
            "{package_name.replace('_', '-')}-cli={package_name}.cli:main",
        ],
    }},
)
'''
        (project_path / "setup.py").write_text(setup_content)
        
        # requirements.txt
        (project_path / "requirements.txt").write_text("# Add your dependencies here\n")
    
    def _create_basic_readme(self, project_path: Path, project_name: str, metadata: Dict[str, str]):
        """Create basic README."""
        content = f'''# {project_name}

{metadata.get('description', f'A {project_name} project')}

## Installation

```bash
pip install -e .
```

## Usage

```python
from {self._to_package_name(project_name)} import {self._to_class_name(self._to_package_name(project_name))}

app = {self._to_class_name(self._to_package_name(project_name))}()
app.run()
```

## Author

{metadata.get('author', 'Your Name')} - {metadata.get('email', 'your.email@example.com')}
'''
        (project_path / "README.md").write_text(content)
    
    def _create_basic_gitignore(self, project_path: Path):
        """Create basic .gitignore."""
        content = '''__pycache__/
*.py[cod]
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
.pytest_cache/
.coverage
htmlcov/
.env
.venv
env/
venv/
.mypy_cache/
.DS_Store
'''
        (project_path / ".gitignore").write_text(content)
    
    def _generate_minimal_template(self, project_path: Path, project_name: str, package_name: str, features: Dict[str, bool], metadata: Dict[str, str]) -> bool:
        """Generate the minimal Python project template."""
        src_dir = project_path / "src" / package_name
        src_dir.mkdir(parents=True, exist_ok=True)
        
        # Create basic files
        self._create_basic_init(src_dir, project_name, metadata)
        self._create_basic_core(src_dir, project_name, package_name, metadata)
        
        if features.get('cli', False):
            self._create_basic_cli(src_dir, project_name, package_name, metadata)
        
        if features.get('tests', True):
            self._create_basic_tests(project_path, package_name)
        
        if features.get('pypi_packaging', True):
            self._create_basic_setup(project_path, project_name, package_name, metadata)
        
        if features.get('readme', True):
            self._create_basic_readme(project_path, project_name, metadata)
        
        if features.get('gitignore', True):
            self._create_basic_gitignore(project_path)
        
        return True
    
    def _generate_flask_template(self, project_path: Path, project_name: str, package_name: str, features: Dict[str, bool], metadata: Dict[str, str]) -> bool:
        """Generate a Flask web application template."""
        # Create app structure
        app_dir = project_path / package_name
        app_dir.mkdir(parents=True, exist_ok=True)
        
        # Create Flask app structure
        (app_dir / "__init__.py").write_text(f'''"""
{metadata.get('description', f'A {project_name} Flask application')}
"""

from flask import Flask
from .config import Config

__version__ = "{metadata.get('version', '0.1.0')}"

def create_app(config_class=Config):
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Register blueprints
    from .main import bp as main_bp
    app.register_blueprint(main_bp)
    
    return app
''')
        
        # Create config
        (app_dir / "config.py").write_text(f'''"""
Configuration for {project_name}.
"""

import os
from pathlib import Path

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    
class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    
class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    
config = {{
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}}
''')
        
        # Create main blueprint
        main_dir = app_dir / "main"
        main_dir.mkdir(exist_ok=True)
        (main_dir / "__init__.py").write_text('''"""
Main blueprint for the application.
"""

from flask import Blueprint

bp = Blueprint('main', __name__)

from . import routes
''')
        
        (main_dir / "routes.py").write_text(f'''"""
Main routes for {project_name}.
"""

from flask import render_template, request, jsonify
from . import bp

@bp.route('/')
def index():
    """Home page."""
    return render_template('index.html', title='Home')

@bp.route('/api/health')
def health():
    """Health check endpoint."""
    return jsonify({{'status': 'healthy', 'app': '{project_name}'}})
''')
        
        # Create templates
        templates_dir = app_dir / "templates"
        templates_dir.mkdir(exist_ok=True)
        (templates_dir / "base.html").write_text(f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{% if title %}}{project_name} - {{{{ title }}}}{{% else %}}{project_name}{{% endif %}}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{{{{ url_for('main.index') }}}}">{project_name}</a>
        </div>
    </nav>
    
    <main class="container mt-4">
        {{% block content %}}{{% endblock %}}
    </main>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
''')
        
        (templates_dir / "index.html").write_text(f'''{{% extends "base.html" %}}

{{% block content %}}
<div class="row">
    <div class="col-md-8 mx-auto">
        <div class="jumbotron bg-light p-5 rounded">
            <h1 class="display-4">Welcome to {project_name}!</h1>
            <p class="lead">{metadata.get('description', f'A {project_name} Flask application')}</p>
            <hr class="my-4">
            <p>This is a Flask web application generated by the Python Project Generator.</p>
            <a class="btn btn-primary btn-lg" href="/api/health" role="button">Check Health</a>
        </div>
    </div>
</div>
{{% endblock %}}
''')
        
        # Create static files directory
        static_dir = app_dir / "static"
        static_dir.mkdir(exist_ok=True)
        (static_dir / "style.css").write_text('''/* Custom styles for the application */
.jumbotron {
    background-color: #f8f9fa;
}
''')
        
        # Create run script
        (project_path / "run.py").write_text(f'''#!/usr/bin/env python3
"""
Development server for {project_name}.
"""

from {package_name} import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
''')
        
        # Create requirements
        requirements = [
            "Flask>=2.3.0",
            "python-dotenv>=1.0.0"
        ]
        if features.get('database'):
            requirements.extend(["Flask-SQLAlchemy>=3.0.0", "Flask-Migrate>=4.0.0"])
        
        (project_path / "requirements.txt").write_text("\\n".join(requirements) + "\\n")
        
        # Create tests
        if features.get('tests', True):
            self._create_flask_tests(project_path, package_name)
        
        # Create other common files
        if features.get('readme', True):
            self._create_flask_readme(project_path, project_name, metadata)
        
        if features.get('gitignore', True):
            self._create_basic_gitignore(project_path)
            
        if features.get('docker'):
            self._create_flask_docker(project_path, package_name)
        
        return True
    
    def _create_flask_tests(self, project_path: Path, package_name: str):
        """Create tests for Flask application."""
        tests_dir = project_path / "tests"
        tests_dir.mkdir(exist_ok=True)
        
        (tests_dir / "__init__.py").write_text("")
        
        (tests_dir / "conftest.py").write_text(f'''"""
Test configuration for Flask app.
"""

import pytest
from {package_name} import create_app

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config.update({{
        "TESTING": True,
    }})
    return app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()
''')
        
        (tests_dir / "test_routes.py").write_text(f'''"""
Test routes for the application.
"""

def test_index(client):
    """Test the home page."""
    response = client.get('/')
    assert response.status_code == 200

def test_health(client):
    """Test the health endpoint."""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
''')
    
    def _create_flask_readme(self, project_path: Path, project_name: str, metadata: Dict[str, str]):
        """Create README for Flask application."""
        content = f'''# {project_name}

{metadata.get('description', f'A {project_name} Flask application')}

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Development Mode
```bash
python run.py
```

The application will be available at http://localhost:5000

### Environment Variables
Create a `.env` file in the project root:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///app.db
FLASK_ENV=development
```

## Testing

```bash
pip install pytest
pytest
```

## Project Structure

```
{self._to_package_name(project_name)}/
├── {self._to_package_name(project_name)}/
│   ├── __init__.py
│   ├── config.py
│   ├── main/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── templates/
│   │   ├── base.html
│   │   └── index.html
│   └── static/
│       └── style.css
├── tests/
├── run.py
└── requirements.txt
```

## Author

{metadata.get('author', 'Your Name')} - {metadata.get('email', 'your.email@example.com')}
'''
        (project_path / "README.md").write_text(content)
    
    def _create_flask_docker(self, project_path: Path, package_name: str):
        """Create Docker files for Flask application."""
        (project_path / "Dockerfile").write_text(f'''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "run.py"]
''')
        
        (project_path / "docker-compose.yml").write_text(f'''version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
    volumes:
               - .:/app
''')
    
    def _generate_fastapi_template(self, project_path: Path, project_name: str, package_name: str, features: Dict[str, bool], metadata: Dict[str, str]) -> bool:
        """Generate a FastAPI web application template."""
        # Create app structure
        app_dir = project_path / package_name
        app_dir.mkdir(parents=True, exist_ok=True)
        
        # Main application
        (app_dir / "__init__.py").write_text(f'''"""
{metadata.get('description', f'A {project_name} FastAPI application')}
"""

__version__ = "{metadata.get('version', '0.1.0')}"
''')
        
        (app_dir / "main.py").write_text(f'''"""
Main FastAPI application for {project_name}.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="{project_name}",
    description="{metadata.get('description', f'A {project_name} FastAPI application')}",
    version="{metadata.get('version', '0.1.0')}"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    app: str
    version: str

class Item(BaseModel):
    """Example item model."""
    id: Optional[int] = None
    name: str
    description: Optional[str] = None

# In-memory storage (replace with database)
items_db: List[Item] = []

@app.get("/", tags=["root"])
async def read_root():
    """Welcome endpoint."""
    return {{"message": "Welcome to {project_name}!"}}

@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        app="{project_name}",
        version="{metadata.get('version', '0.1.0')}"
    )

@app.get("/items", response_model=List[Item], tags=["items"])
async def read_items():
    """Get all items."""
    return items_db

@app.post("/items", response_model=Item, tags=["items"])
async def create_item(item: Item):
    """Create a new item."""
    item.id = len(items_db) + 1
    items_db.append(item)
    return item

@app.get("/items/{{item_id}}", response_model=Item, tags=["items"])
async def read_item(item_id: int):
    """Get a specific item."""
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
''')
        
        # Create requirements
        requirements = [
            "fastapi>=0.104.0",
            "uvicorn[standard]>=0.24.0",
            "pydantic>=2.4.0"
        ]
        if features.get('database'):
            requirements.extend(["sqlalchemy>=2.0.0", "alembic>=1.12.0"])
        
        (project_path / "requirements.txt").write_text("\\n".join(requirements) + "\\n")
        
        # Create run script
        (project_path / "run.py").write_text(f'''#!/usr/bin/env python3
"""
Development server for {project_name}.
"""

import uvicorn
from {package_name}.main import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
''')
        
        # Tests
        if features.get('tests', True):
            tests_dir = project_path / "tests"
            tests_dir.mkdir(exist_ok=True)
            (tests_dir / "__init__.py").write_text("")
            
            (tests_dir / "test_main.py").write_text(f'''"""
Tests for {project_name} FastAPI application.
"""

from fastapi.testclient import TestClient
from {package_name}.main import app

client = TestClient(app)

def test_read_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_create_and_read_item():
    """Test item creation and retrieval."""
    # Create item
    item_data = {{"name": "Test Item", "description": "Test Description"}}
    response = client.post("/items", json=item_data)
    assert response.status_code == 200
    created_item = response.json()
    assert created_item["name"] == "Test Item"
    assert "id" in created_item
    
    # Read item
    item_id = created_item["id"]
    response = client.get(f"/items/{{item_id}}")
    assert response.status_code == 200
    assert response.json() == created_item
''')
        
        # README
        if features.get('readme', True):
            (project_path / "README.md").write_text(f'''# {project_name}

{metadata.get('description', f'A {project_name} FastAPI application')}

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
python run.py
```

API will be available at http://localhost:8000

## Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

```bash
pip install pytest httpx
pytest
```

## Author

{metadata.get('author', 'Your Name')} - {metadata.get('email', 'your.email@example.com')}
''')
        
        if features.get('gitignore', True):
            self._create_basic_gitignore(project_path)
            
        if features.get('docker'):
            self._create_fastapi_docker(project_path, package_name)
        
        return True
    
    def _create_fastapi_docker(self, project_path: Path, package_name: str):
        """Create Docker files for FastAPI application."""
        (project_path / "Dockerfile").write_text('''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
''')
    
    def _generate_data_science_template(self, project_path: Path, project_name: str, package_name: str, features: Dict[str, bool], metadata: Dict[str, str]) -> bool:
        """Generate a data science project template."""
        # Create structure
        (project_path / "data" / "raw").mkdir(parents=True, exist_ok=True)
        (project_path / "data" / "processed").mkdir(parents=True, exist_ok=True)
        (project_path / "notebooks").mkdir(exist_ok=True)
        (project_path / "reports").mkdir(exist_ok=True)
        (project_path / "src" / package_name).mkdir(parents=True, exist_ok=True)
        
        # Main module
        (project_path / "src" / package_name / "__init__.py").write_text(f'''"""
{metadata.get('description', f'A {project_name} data science project')}
"""

__version__ = "{metadata.get('version', '0.1.0')}"
''')
        
        # Data processing module
        (project_path / "src" / package_name / "data.py").write_text('''"""
Data processing utilities.
"""

import pandas as pd
import numpy as np
from pathlib import Path

def load_data(filepath: str) -> pd.DataFrame:
    """Load data from file."""
    return pd.read_csv(filepath)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the dataset."""
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Handle missing values
    df = df.dropna()
    
    return df

def save_processed_data(df: pd.DataFrame, filepath: str) -> None:
    """Save processed data."""
    df.to_csv(filepath, index=False)
''')
        
        # Analysis module
        (project_path / "src" / package_name / "analysis.py").write_text('''"""
Data analysis utilities.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Optional

def basic_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Get basic statistics of the dataset."""
    return df.describe()

def correlation_matrix(df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
    """Calculate correlation matrix."""
    if columns:
        df = df[columns]
    return df.corr()

def plot_distribution(df: pd.DataFrame, column: str, figsize: tuple = (10, 6)) -> None:
    """Plot distribution of a column."""
    plt.figure(figsize=figsize)
    sns.histplot(df[column], kde=True)
    plt.title(f'Distribution of {column}')
    plt.show()

def plot_correlation_heatmap(df: pd.DataFrame, figsize: tuple = (12, 8)) -> None:
    """Plot correlation heatmap."""
    plt.figure(figsize=figsize)
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation Heatmap')
    plt.show()
''')
        
        # Sample notebook
        notebook_content = '''{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Data Analysis Notebook\\n",
    "\\n",
    "This notebook contains the main analysis for the project."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Import libraries\\n",
    "import pandas as pd\\n",
    "import numpy as np\\n",
    "import matplotlib.pyplot as plt\\n",
    "import seaborn as sns\\n",
    "\\n",
    "# Import project modules\\n",
    "import sys\\n",
    "sys.path.append('../src')\\n",
    "from ''' + package_name + ''' import data, analysis"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Load data\\n",
    "# df = data.load_data('../data/raw/sample.csv')"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}'''
        
        (project_path / "notebooks" / "01_exploratory_analysis.ipynb").write_text(notebook_content)
        
        # Requirements
        requirements = [
            "pandas>=2.0.0",
            "numpy>=1.24.0",
            "matplotlib>=3.7.0",
            "seaborn>=0.12.0",
            "jupyter>=1.0.0",
            "scikit-learn>=1.3.0"
        ]
        (project_path / "requirements.txt").write_text("\\n".join(requirements) + "\\n")
        
        # Basic files
        if features.get('readme', True):
            (project_path / "README.md").write_text(f'''# {project_name}

{metadata.get('description', f'A {project_name} data science project')}

## Project Structure

```
├── data/
│   ├── raw/          # Raw data files
│   └── processed/    # Processed data files
├── notebooks/        # Jupyter notebooks
├── reports/          # Generated reports
└── src/
    └── {package_name}/   # Source code
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Start Jupyter:
```bash
jupyter notebook
```

## Author

{metadata.get('author', 'Your Name')} - {metadata.get('email', 'your.email@example.com')}
''')
        
        if features.get('gitignore', True):
            self._create_basic_gitignore(project_path)
        
        return True
    
    def _generate_cli_tool_template(self, project_path: Path, project_name: str, package_name: str, features: Dict[str, bool], metadata: Dict[str, str]) -> bool:
        """Generate a CLI tool template."""
        src_dir = project_path / "src" / package_name
        src_dir.mkdir(parents=True, exist_ok=True)
        
        # Main CLI module
        (src_dir / "__init__.py").write_text(f'''"""
{metadata.get('description', f'A {project_name} CLI tool')}
"""

__version__ = "{metadata.get('version', '0.1.0')}"
''')
        
        (src_dir / "cli.py").write_text(f'''"""
CLI for {project_name}.
"""

import click
import logging
from pathlib import Path
from . import __version__

logger = logging.getLogger(__name__)

@click.group()
@click.version_option(version=__version__)
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.pass_context
def cli(ctx, verbose):
    """
    {metadata.get('description', f'A {project_name} CLI tool')}
    """
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    
    # Configure logging
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format='%(levelname)s: %(message)s')

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file')
@click.pass_context
def process(ctx, input_file, output):
    """Process an input file."""
    click.echo(f"Processing {{input_file}}...")
    
    # Add your processing logic here
    result = f"Processed {{input_file}}"
    
    if output:
        Path(output).write_text(result)
        click.echo(f"Result saved to {{output}}")
    else:
        click.echo(result)

@cli.command()
@click.pass_context
def info(ctx):
    """Show information about the tool."""
    click.echo(f"{project_name} v{{__version__}}")
    click.echo(f"Author: {metadata.get('author', 'Your Name')}")

if __name__ == '__main__':
    cli()
''')
        
        # Requirements
        requirements = [
            "click>=8.1.0",
            "colorama>=0.4.6"
        ]
        (project_path / "requirements.txt").write_text("\\n".join(requirements) + "\\n")
        
        # Setup.py for CLI entry point
        (project_path / "setup.py").write_text(f'''from setuptools import setup, find_packages

setup(
    name="{package_name.replace('_', '-')}",
    version="{metadata.get('version', '0.1.0')}",
    packages=find_packages(where="src"),
    package_dir={{"": "src"}},
    install_requires=[
        "click>=8.1.0",
        "colorama>=0.4.6",
    ],
    entry_points={{
        "console_scripts": [
            "{package_name.replace('_', '-')}={package_name}.cli:cli",
        ],
    }},
    python_requires=">=3.8",
    author="{metadata.get('author', 'Your Name')}",
    author_email="{metadata.get('email', 'your.email@example.com')}",
    description="{metadata.get('description', f'A {project_name} CLI tool')}",
)
''')
        
        if features.get('tests', True):
            tests_dir = project_path / "tests"
            tests_dir.mkdir(exist_ok=True)
            (tests_dir / "__init__.py").write_text("")
            (tests_dir / "test_cli.py").write_text(f'''"""
Tests for {project_name} CLI.
"""

from click.testing import CliRunner
from {package_name}.cli import cli

def test_cli_info():
    """Test the info command."""
    runner = CliRunner()
    result = runner.invoke(cli, ['info'])
    assert result.exit_code == 0
    assert "{project_name}" in result.output
''')
        
        if features.get('readme', True):
            (project_path / "README.md").write_text(f'''# {project_name}

{metadata.get('description', f'A {project_name} CLI tool')}

## Installation

```bash
pip install -e .
```

## Usage

```bash
{package_name.replace('_', '-')} --help
{package_name.replace('_', '-')} info
{package_name.replace('_', '-')} process input.txt -o output.txt
```

## Author

{metadata.get('author', 'Your Name')} - {metadata.get('email', 'your.email@example.com')}
''')
        
        if features.get('gitignore', True):
            self._create_basic_gitignore(project_path)
        
        return True
    
    # Stub implementations for remaining templates
    def _generate_django_template(self, project_path: Path, project_name: str, package_name: str, features: Dict[str, bool], metadata: Dict[str, str]) -> bool:
        """Generate Django template (stub - falls back to minimal)."""
        return self._generate_minimal_template(project_path, project_name, package_name, features, metadata)
    
    def _generate_ml_template(self, project_path: Path, project_name: str, package_name: str, features: Dict[str, bool], metadata: Dict[str, str]) -> bool:
        """Generate ML template (stub - falls back to minimal)."""
        return self._generate_minimal_template(project_path, project_name, package_name, features, metadata)
    
    def _generate_library_template(self, project_path: Path, project_name: str, package_name: str, features: Dict[str, bool], metadata: Dict[str, str]) -> bool:
        """Generate library template (stub - falls back to minimal)."""
        return self._generate_minimal_template(project_path, project_name, package_name, features, metadata)
    
    def _generate_game_template(self, project_path: Path, project_name: str, package_name: str, features: Dict[str, bool], metadata: Dict[str, str]) -> bool:
        """Generate game template (stub - falls back to minimal)."""
        return self._generate_minimal_template(project_path, project_name, package_name, features, metadata)
    
    def _generate_desktop_gui_template(self, project_path: Path, project_name: str, package_name: str, features: Dict[str, bool], metadata: Dict[str, str]) -> bool:
        """Generate desktop GUI template (stub - falls back to minimal)."""
        return self._generate_minimal_template(project_path, project_name, package_name, features, metadata)
    
    def _generate_microservice_template(self, project_path: Path, project_name: str, package_name: str, features: Dict[str, bool], metadata: Dict[str, str]) -> bool:
        """Generate microservice template (stub - falls back to minimal)."""
        return self._generate_minimal_template(project_path, project_name, package_name, features, metadata)
    
    def _generate_api_client_template(self, project_path: Path, project_name: str, package_name: str, features: Dict[str, bool], metadata: Dict[str, str]) -> bool:
        """Generate API client template (stub - falls back to minimal)."""
        return self._generate_minimal_template(project_path, project_name, package_name, features, metadata)
    
    def _generate_automation_template(self, project_path: Path, project_name: str, package_name: str, features: Dict[str, bool], metadata: Dict[str, str]) -> bool:
        """Generate automation template (stub - falls back to minimal)."""
        return self._generate_minimal_template(project_path, project_name, package_name, features, metadata)
    
    def _generate_jupyter_research_template(self, project_path: Path, project_name: str, package_name: str, features: Dict[str, bool], metadata: Dict[str, str]) -> bool:
        """Generate Jupyter research template (stub - falls back to minimal)."""
        return self._generate_minimal_template(project_path, project_name, package_name, features, metadata)
    
    def _to_package_name(self, project_name: str) -> str:
        """Convert project name to valid Python package name."""
        return project_name.lower().replace('-', '_').replace(' ', '_')
    
    def _to_class_name(self, package_name: str) -> str:
        """Convert package name to class name."""
        return ''.join(word.capitalize() for word in package_name.split('_'))


def setup_logging(level: str = "INFO") -> None:
    """Set up logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()]
    )


def main():
    """
    Main CLI entry point for the project generator.
    """
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="Python Project Generator CLI")
    parser.add_argument("project_name", help="Name of the project to create")
    parser.add_argument("-o", "--output", default=".", help="Output directory (default: current directory)")
    parser.add_argument("-t", "--template", default="minimal-python", help="Template to use (default: minimal-python)")
    parser.add_argument("--author", help="Author name")
    parser.add_argument("--email", help="Author email")
    parser.add_argument("--description", help="Project description")
    parser.add_argument("--version", default="0.1.0", help="Initial version (default: 0.1.0)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    parser.add_argument("--list-templates", action="store_true", help="List available templates")
    
    args = parser.parse_args()
    
    # Set up logging
    level = "DEBUG" if args.verbose else "INFO"
    setup_logging(level)
    
    generator = ProjectGenerator()
    
    # List templates if requested
    if args.list_templates:
        templates = generator.template_manager.get_available_templates()
        print("Available templates:")
        for template_id, template_info in templates.items():
            print(f"  {template_id}: {template_info['name']}")
            print(f"    {template_info['description']}")
        return 0
    
    # Generate project
    metadata = {
        "author": args.author or "Your Name",
        "email": args.email or "your.email@example.com",
        "description": args.description or f"A {args.project_name} project",
        "version": args.version,
    }
    
    # Default features for CLI usage
    features = {
        "cli": True,
        "tests": True,
        "pypi_packaging": True,
        "readme": True,
        "gitignore": True,
        "license": True,
    }
    
    print(f"Generating project '{args.project_name}' using template '{args.template}'...")
    
    result = generator.generate_project(
        project_name=args.project_name,
        output_dir=Path(args.output),
        template_id=args.template,
        features=features,
        metadata=metadata
    )
    
    if result:
        print("✅ Project generated successfully!")
        project_path = Path(args.output) / args.project_name
        print(f"📁 Location: {project_path.absolute()}")
        print("\nNext steps:")
        print(f"  cd '{project_path}'")
        print("  pip install -e .")
        return 0
    else:
        print("❌ Project generation failed!")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main()) 