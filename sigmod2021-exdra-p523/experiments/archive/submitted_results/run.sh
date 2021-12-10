#/bin/bash

source parameters.sh

source code/util/gitIdLog.sh

logGitIDs

date +%T

./setup.sh

source "$VENV_PATH/bin/activate" 

# ./code/other.sh
./code/localExp.sh
# ./code/distributedExpNew.sh


date +%T

deactivate

printf '\a'
sleep 0.2
printf '\a'
sleep 0.1
printf '\a'
sleep 0.2
printf '\a'
sleep 0.4
printf '\a'
sleep 0.4
printf '\a'
