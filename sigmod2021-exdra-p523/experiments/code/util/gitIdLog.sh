#/bin/bash

## writes out the Git hash IDs for this repository but also for the repo in SystemDSRoot.
logGitIDs() {
    here=$(pwd)
    cd $SYSTEMDS_ROOT
    id="$(git rev-parse HEAD)"
    cd $here
    if [[ -d .git ]]; then
        idexp="$(git rev-parse HEAD)"
        echo "sysds: $id papers: $idexp" | tee -a results/$HOSTNAME-GitID.txt
    else
        echo "sysds: $id" | tee -a results/$HOSTNAME-GitID.txt
    fi
}
