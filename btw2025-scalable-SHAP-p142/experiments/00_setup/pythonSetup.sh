#!/bin/bash

# Ensure the script exits on any error
set -e

# Directory for the virtual environment
VENV_DIR="${1:-../python-venv}"  # Default to 'python-venv' if no argument is provided

# Check if Python is available
if ! command -v python3 &> /dev/null; then
  echo "Python3 is not installed or not in PATH. Please install it first."
  exit 1
fi

# Create the virtual environment
echo "Creating virtual environment in directory: $VENV_DIR"
python3 -m venv "$VENV_DIR"

# Activate the virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Check if the virtual environment was successfully activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
  echo "Failed to activate the virtual environment. Please check the setup."
  exit 1
else
  echo "Virtual environment successfully activated at: $VIRTUAL_ENV"
fi

echo "Installing required packages."
pip install "numpy<=1.24.3" pandas scipy scikit-learn tensorflow shap
