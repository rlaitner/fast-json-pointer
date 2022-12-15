# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import re

project = 'Fast JSON Pointer'
copyright = '2022, Tristan Sweeney'
author = 'Tristan Sweeney'

# The full version, including alpha/beta/rc tags.
release = re.sub('^v', '', os.popen('git describe --tags').read().strip())
# The short X.Y version.
version = release

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx_toolbox.github',
    'sphinx_toolbox.sidebar_links',
]

github_username = 'slowAPI'
github_repository = 'fast-json-pointer'

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
