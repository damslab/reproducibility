#!/usr/bin/env bash

BENCHMARK=$1
THREADS=$2

install_dir=$PWD
bench_dir="${install_dir}/duckdb-polr/benchmark/${BENCHMARK}"
if [[ "$BENCHMARK" = "imdb" ]]; then
  bench_dir="${install_dir}/data/skinnermtimdb"
fi

sed -i"" -e "s|.*THREADS.*|THREADS=${THREADS}|" "${install_dir}/data/skinnermt${BENCHMARK}/config.sdb"
cd "${install_dir}/skinnermt/scripts"

echo -e "index all\nbench ${bench_dir}/queries ${install_dir}/experiment-results/4_1_endtoend/${BENCHMARK}/skinnermt/skinnermt-${THREADS}.csv\nquit" | \
  cgexec -g cpu:limitcpu"${THREADS}" \
  /usr/lib/jvm/java-1.16.0-openjdk-amd64/bin/java -jar \
  -XX:+UnlockExperimentalVMOptions -XX:+UseEpsilonGC -XX:+AlwaysPreTouch -Xmx200G -Xms200G \
  Skinner.jar "${install_dir}/data/skinnermt${BENCHMARK}"

cd $install_dir