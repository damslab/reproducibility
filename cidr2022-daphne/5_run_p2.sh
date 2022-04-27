#!/usr/bin/env bash

source resources/env.sh
if [ ! -f $SANDBOX ]; then
  echo "Error: Singularity image" $SANDBOX "does not exist. Please run 1_setup_env.sh to build it (root or fakeroot privileges required)"
  exit
fi

singularity run --nv --bind $CUDA11_PATH:/usr/local/cuda $SANDBOX \
    "cd $DAPHNE_ROOT; git checkout p2-alpha; git apply $BASE_DIR/resources/0000-daphne-build_sh.patch; rm -rf build; \
     ./build.sh 2>&1 | tee $WORK_DIR/logs/p2-build-daphne-cuda-log.txt"

singularity run --nv --bind "$CUDA11_PATH":/usr/local/cuda $SANDBOX \
    "$P2_ROOT/eval.sh --daphne --repetitions $P2_REPETITIONS 2>&1 | tee $WORK_DIR/logs/p2-run-daphne-$(date --iso-8601)-log.txt"

singularity run --nv --bind "$CUDA10_PATH":/usr/local/cuda $SANDBOX \
    "$P2_ROOT/eval.sh --sysds --repetitions $P2_REPETITIONS 2>&1 | tee $WORK_DIR/logs/p2-run-sysds-$(date --iso-8601)-log.txt"

singularity run --nv --bind "$CUDA10_PATH":/usr/local/cuda $SANDBOX \
    "$P2_ROOT/eval.sh --sysdsp --repetitions $P2_REPETITIONS 2>&1 | tee $WORK_DIR/logs/p2-run-sysdsp-$(date --iso-8601)-log.txt"

singularity run --nv --bind "$CUDA11_PATH":/usr/local/cuda $SANDBOX \
    "$P2_ROOT/eval.sh --tf --repetitions $P2_REPETITIONS 2>&1 | tee $WORK_DIR/logs/p2-run-tf-$(date --iso-8601)-log.txt"

singularity run --nv --bind "$CUDA11_PATH":/usr/local/cuda $SANDBOX \
    "$P2_ROOT/eval.sh --tfxla --repetitions $P2_REPETITIONS 2>&1 | tee $WORK_DIR/logs/p2-run-tfxla-$(date --iso-8601)-log.txt"

singularity run $SANDBOX \
    "$P2_ROOT/eval.sh --vis 2>&1 | tee $WORK_DIR/logs/p2-run-vis-$(date --iso-8601)-log.txt"
