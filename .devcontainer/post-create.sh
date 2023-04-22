#!/bin/bash

# This script is run after the devcontainer is created.

# Install Python Development Tools
pip install pipx
pipx install pre-commit
pipx install ruff
pipx install pip-tools

# Install pre-commit hooks
pre-commit install
pre-commit install --hook-type commit-msg
