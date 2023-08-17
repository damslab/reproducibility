#!/usr/bin/env bash

BENCHMARK=$1
THREADS=$2

echo -e "index all\nbench skinnerdb/${BENCHMARK}/queries skinnerdb-${BENCHMARK}-${THREADS}.csv\nquit" | \
  cgexec -g cpu:limitcpu"${THREADS}" \
  java -jar -Xmx32G -XX:+UseConcMarkSweepGC ../../skinnerdb/jars/Skinner.jar skinner"${BENCHMARK}"
