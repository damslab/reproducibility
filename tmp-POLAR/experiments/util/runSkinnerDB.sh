#!/usr/bin/env bash

BENCHMARK=$1
THREADS=$2

bench_dir=duckdb-polr/benchmark/"${BENCHMARK}"
if [[ "$BENCHMARK" = "imdb" ]]; then
  bench_dir=skinnerdb/imdb
fi

echo -e "index all\nbench ${bench_dir}/queries experiment-results/4_1_endtoend/${BENCHMARK}/skinnerdb/skinnerdb-${THREADS}.csv\nquit" | \
  cgexec -g cpu:limitcpu"${THREADS}" \
  /usr/lib/jvm/java-1.8.0-openjdk-amd64/bin/java -jar -Xmx32G -XX:+UseConcMarkSweepGC ../../skinnerdb/jars/Skinner.jar data/skinner"${BENCHMARK}"
