"""Sphinx configuration for SpinCirc."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
project = "SpinCirc"
author = "Meshal Alawein"
copyright = "2026, Meshal Alawein"
release = version = "1.0.0"
extensions = [
    "sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx.ext.intersphinx",
    "myst_parser", "sphinx_copybutton",
]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "DEBT.md", "INDEX.md", "README.md", "adr/**", "architecture/topology.md", "deployment.md", "operations/**"]
source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
html_theme = "sphinx_rtd_theme"
html_static_path = []
autodoc_default_options = {"members": True, "member-order": "bysource"}
intersphinx_mapping = {"python": ("https://docs.python.org/3/", None)}
myst_enable_extensions = ["colon_fence", "linkify"]
