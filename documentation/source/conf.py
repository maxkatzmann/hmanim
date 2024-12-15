# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

# Add the hmanim package to the Python path
sys.path.insert(0, os.path.abspath("../../../"))
sys.path.insert(0, os.path.abspath("../../../"))

project = "HManim"
copyright = "2024, Maximilian Katzmann"
author = "Maximilian Katzmann"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "manim.utils.docbuild.manim_directive",
    "manim.utils.docbuild.autocolor_directive",
    "manim.utils.docbuild.autoaliasattr_directive",
]

templates_path = ["_templates"]
exclude_patterns = []

# Hide the "module" prefix in the documentation
add_module_names = False


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
