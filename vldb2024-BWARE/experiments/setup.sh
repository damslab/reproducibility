#/bin/bash

source parameters



if [[ ! -d "python_venv" ]]; then
    # Install systemds python environment if not already installed.
    # this also install the system on the remotes defined in parameters.sh
    ./install.sh
fi
