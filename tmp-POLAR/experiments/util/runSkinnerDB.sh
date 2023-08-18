#!/usr/bin/env bash

BENCHMARK=$1
THREADS=$2

mkdir ../../experiment-results/4_1_endtoend/"${BENCHMARK}"/skinnerdb

bench_dir=duckdb-polr/benchmark/"${bench_dir}"/queries
if [[ "$BENCHMARK" = "imdb" ]]; then
  bench_dir=skinnerdb/imdb/queries
fi

echo -e "index all\nbench duckdb-polr/benchmark/${bench_dir}/queries experiment-results/4_1_endtoend/"${BENCHMARK}"/skinnerdb/skinnerdb-${BENCHMARK}-${THREADS}.csv\nquit" | \
  cgexec -g cpu:limitcpu"${THREADS}" \
  java -jar -Xmx32G -XX:+UseConcMarkSweepGC ../../skinnerdb/jars/Skinner.jar data/skinner"${BENCHMARK}"
