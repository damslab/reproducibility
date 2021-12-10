#/bin/bash

source parameters.sh

address=(${address[@]} $main "localhost")

for index in ${!address[*]}; do
    rsync -avhq -e ssh ${address[$index]}:$remoteDir/results/. results/ &
    rsync -avhq -e ssh ${address[$index]}:$remoteDir/hprof/. hprof/ &
done

wait

./plots/makePlots.sh
