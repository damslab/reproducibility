#!/usr/bin/env bash

BENCHMARK=$1
THREADS=$2

bench_dir=$BENCHMARK
if [[ "$BENCHMARK" = "imdb" ]]; then
  bench_dir="imdb_plan_cost"
fi

echo -e "index all\nbench duckdb-polr/benchmark/${bench_dir}/queries skinnerdb-${BENCHMARK}-${THREADS}.csv\nquit" | \
  cgexec -g cpu:limitcpu"${THREADS}" \
  java -jar -Xmx32G -XX:+UseConcMarkSweepGC ../../skinnerdb/jars/Skinner.jar skinner"${BENCHMARK}"
