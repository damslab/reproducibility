#!/usr/bin/env bash

set -e

./1_setup_env.sh
./2_setup_p2_data.sh
./3_run_microbenchmarks.sh
./4_run_p1.sh
./5_run_p2.sh

set +e