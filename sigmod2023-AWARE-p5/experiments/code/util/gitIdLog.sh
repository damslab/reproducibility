#/bin/bash

## writes out the Git hash IDs for this repository but also for the repo in SystemDSRoot.

source parameters.sh

logGitIDs() {
    here=$(pwd)
    cd $SYSTEMDS_ROOT
    id="$(git rev-parse HEAD)"
    cd $here
    touch results/$HOSTNAME-GitID.txt
    if [ -d .git ]; then
        idexp="$(git rev-parse HEAD)"
        echo "$HOSTNAME sysds: $id papers: $idexp" | tee -a results/$HOSTNAME-GitID.txt
    else
        echo "$HOSTNAME sysds: $id" | tee -a results/$HOSTNAME-GitID.txt
    fi
}
