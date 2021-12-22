"""Sphinx configuration."""
from datetime import datetime


project = "Human Readable"
author = "staticdev"
copyright = f"{datetime.now().year}, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]
autodoc_typehints = "description"
html_theme = "furo"
