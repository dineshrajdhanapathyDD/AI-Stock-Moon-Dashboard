#!/bin/bash
echo "=== Stock Moon Dashboard Build Script ==="
echo "Python version:"
python3 --version
echo "Pip version:"
pip3 --version
echo "Installing Python dependencies..."
pip3 install -r requirements.txt --user
echo "Build completed successfully!"