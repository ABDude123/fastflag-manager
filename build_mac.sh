#!/bin/bash

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
pip install pillow flask

# Create DMG resources
python scripts/create_background.py
python scripts/create_icons.py

# Create .app bundle
python setup.py py2app

# Sign the app
./scripts/codesign.sh

# Create DMG installer
./scripts/create_dmg.sh

# Prepare release
python scripts/prepare_release.py

# Clean up
deactivate