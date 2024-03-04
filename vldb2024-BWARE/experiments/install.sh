#/bin/bash

here=$pwd

if [[ ! -d "python_venv" ]]; then
    echo "Creating Python Virtual Enviroment on $HOSTNAME"

    python3 -m venv python_venv

    source "python_venv/bin/activate"
    pip install -r requirements.txt
fi

source parameters.sh

if [[ ! -d "$HOME/github/systemds/src" ]]; then
    cd ~/github
    rm -rf systemds
    git clone git@github.com:Baunsgaard/systemds.git
    cd systemds
    mvn clean package
    cd $here
    echo $pwd
fi

mkdir -p $HOME/Programs

if [[ ! -d $HOME/Programs/profiler ]]; then
    cd $HOME/Programs
    if [[ ! -f async-profiler-2.10-linux-x64.tar.gz ]]; then
        wget https://github.com/async-profiler/async-profiler/releases/download/v2.10/async-profiler-2.10-linux-x64.tar.gz
    fi
    tar -xvzf async-profiler-2.10-linux-x64.tar.gz
    ln -s async-profiler-2.10-linux-x64/ profiler
    cd $here
fi

# build systemds
cd ~/github/systemds
git fetch
if [[ "$HOSTNAME" = "XPS-15-7590" ]]; then
    echo "Laptop!"
else 
    git checkout $SYSDS_BRANCH
fi
mvn clean package | grep BUILD
cd $here

# hdfs dfs -put code/scripts/specs/* code/scripts/specs/.
