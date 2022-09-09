#!/bin/bash

source parameters.sh

if [[ ! -d "$VENV_PATH" ]]; then
    echo "Creating Python Virtual Enviroment"
    python3 -m venv $VENV_PATH
    source "$VENV_PATH/bin/activate"
    pip install pip --upgrade > /dev/null
fi

pip -q install -r requirements.txt  >/dev/null 2>&1 

echo "Python Venv Installed."
