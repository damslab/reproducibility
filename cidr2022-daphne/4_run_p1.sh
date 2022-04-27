#!/usr/bin/env bash

source resources/env.sh
if [ ! -f $SANDBOX ]; then
  echo "Error: Singularity image" $SANDBOX "does not exist. Please run 1_setup_env.sh to build it (root or fakeroot privileges required)"
  exit
fi

singularity run $SANDBOX "cd $DAPHNE_ROOT; git reset --hard; git checkout 549b05660f9bea874765135f4c5c4af67f843ac2; rm -rf build; ./build.sh 2>&1 | tee $WORK_DIR/logs/p1-build-daphne-log.txt"

singularity run $SANDBOX "P1_ROOT/eval.sh -e s 2>&1 | tee $WORK_DIR/logs/p1-run-setup-$(date --iso-8601)-log.txt"

singularity run $SANDBOX "P1_ROOT/eval.sh  -s g -e g -sf 10 -q a 2>&1 | tee $WORK_DIR/logs/p1-run-datagen-$(date --iso-8601)-log.txt"

singularity run $SANDBOX "P1_ROOT/eval.sh   -s r -sf 10 -q a -r $P1_REPETITIONS 2>&1 | tee $WORK_DIR/logs/p1-run-datagen-$(date --iso-8601)-log.txt"

singularity run $SANDBOX \
    "python3 $P1_ROOT/visualize.py artifacts 10 a 2>&1 | tee $WORK_DIR/logs/p1-run-vis-$(date --iso-8601)-log.txt"