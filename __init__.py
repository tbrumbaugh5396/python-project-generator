"""
Python Project Generator

A standalone GUI tool for generating customizable Python project skeletons from templates.
"""

__version__ = "1.0.0"
__author__ = "Python Project Generator Team"
__email__ = "support@python-project-generator.com"

# Import main classes and functions for easy access
from .project_generator import ProjectGenerator, TemplateManager
from .generator_gui import ProjectGeneratorApp

__all__ = [
    "ProjectGenerator",
    "TemplateManager", 
    "ProjectGeneratorApp"
] 