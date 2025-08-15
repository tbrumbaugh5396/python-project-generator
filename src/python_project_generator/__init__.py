"""
python_project_generator package

Convenience exports so users can:
    from python_project_generator import ProjectGenerator
and use module entry point:
    python -m python_project_generator --gui | --cli
"""

from typing import List

# Public metadata
__version__ = "1.0.0"
__author__ = "Python Project Generator Team"
__email__ = "support@python-project-generator.com"

# Primary APIs
from .project_generator import ProjectGenerator, TemplateManager, setup_logging  # noqa: E402

# Optional GUI export (wxPython may not be installed)
_all: List[str] = [
    "ProjectGenerator",
    "TemplateManager",
    "setup_logging",
    "__version__",
]

try:  # best-effort GUI exposure
    from .generator_gui import ProjectGeneratorApp  # type: ignore  # noqa: F401

    _all.append("ProjectGeneratorApp")
except Exception:
    # GUI not available; keep core APIs
    pass

__all__ = _all

