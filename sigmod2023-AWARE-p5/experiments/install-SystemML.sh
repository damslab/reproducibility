#!/bin/bash

source parameters.sh

# CD over to the other path
path=$pwd

if [[ ! -d "$HOME/github/systemml" ]]; then
    echo "downloading SystemML"
    cd "$HOME/github"
    git clone git@github.com:Baunsgaard/systemds.git systemml
fi


cd ~/github/systemml
git fetch
git checkout $systemMLID >/dev/null 2>&1
git pull >/dev/null 2>&1
# Custom build to find java8 since it is needed for building systemML
./build.sh >/dev/null 2>&1

wait

printf "$HOSTNAME\tInstalled SystemML $(git rev-parse --abbrev-ref HEAD) $(git rev-parse HEAD)\n"


# CD back
cd $path
