#!/bin/bash

# This script is run after the devcontainer is created.

# Install Python Development Tools
pip install pipx
pipx install pre-commit
pipx install ruff

# Install pre-commit hooks
pre-commit install
pre-commit install --hook-type commit-msg

# Create Virtual Environment and Install Python Packages
python -m venv venv
venv/bin/pip install --upgrade pip
venv/bin/pip install pip-tools
venv/bin/pip-sync requirements.txt dev-requirements.txt
