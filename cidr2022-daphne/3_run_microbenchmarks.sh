#!/usr/bin/env bash

source resources/env.sh
if [ ! -f $SANDBOX ]; then
  echo "Error: Singularity image" $SANDBOX "does not exist. Please run 1_setup_env.sh to build it (root or fakeroot privileges required)"
  exit
fi

singularity run $SANDBOX "cd $DAPHNE_ROOT; git reset --hard; git checkout 4d6db3c7bbf29cff89004cc55d1852836469302b; rm -rf build; ./build.sh 2>&1 | tee $WORK_DIR/logs/build-daphne-log.txt"

singularity run $SANDBOX "experiments/microbenchmarks/microeval.sh --lm --kmeans --check 2>&1 | tee $WORK_DIR/logs/run-mb-check-$(date --iso-8601)-log.txt"

singularity run $SANDBOX "experiments/microbenchmarks/microeval.sh  --lm --kmeans --run -r $MB_REPETITIONS 2>&1 | tee $WORK_DIR/logs/run-mb-runs-$(date --iso-8601)-log.txt"

singularity run $SANDBOX \
    "python3 experiments/microbenchmarks/visualize.py 1 1 $MB_RESULTS 2>&1 | tee $WORK_DIR/logs/run-mb-vis-$(date --iso-8601)-log.txt"
