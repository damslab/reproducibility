#!/usr/bin/env bash

declare -a packages=(
  "cgroup-tools" "git" "libssl-dev" "pigz"
)

for package in "${packages[@]}"
do
  dpkg -s "${package}" &> /dev/null
  if [ $? -ne 0 ]; then
    echo "Installing ${package}..."
    sudo apt install "${package}"
  fi
done

echo "Creating cgroups..."
sudo cgcreate -a "$USER" -t "$USER" -g cpu:/limitcpu1
sudo cgset -r cpu.cfs_quota_us=100000 limitcpu1
sudo cgcreate -a "$USER" -t "$USER" -g cpu:/limitcpu8
sudo cgset -r cpu.cfs_quota_us=800000 limitcpu8

if [[ ! -d "$PWD/duckdb-polr" ]]; then
  echo "Downloading POLAR..."
  git clone https://github.com/d-justen/duckdb-polr.git
  cd duckdb-polr
  git checkout new
  BUILD_BENCHMARK=1 BUILD_TPCH=1 BUILD_HTTPFS=1 make -j
  cd ..
fi

if [[ ! -d "$PWD/ssb-dbgen" ]]; then
  echo "Downloading SSB DBGen..."
  git clone https://github.com/eyalroz/ssb-dbgen.git
  cd ssb-dbgen
  cmake .
  cmake --build .
  echo "Generating SSB Data..."
  ./dbgen -v -s 10
  cd ..
  mkdir -p data/ssb
  mv ssb-dbgen/*.tbl data/ssb
  pigz -v9 data/ssb/*.tbl
  sed -i.".original" -e "s|PATHVAR|`pwd`/data/ssb|" ./duckdb-polr/benchmark/ssb/init/load.sql
  sed -i.".original" -e "s|PATHVAR|`pwd`/data/ssb|" ./duckdb-polr/benchmark/ssb-skew/init/load.sql
fi

mkdir -p duckdb-polr/duckdb_benchmark_data
cat duckdb-polr/benchmark/imdb/init/load.sql | duckdb-polr/build/release/duckdb duckdb-polr/duckdb_benchmark_data/imdb.duckdb
cat duckdb-polr/benchmark/ssb/init/load.sql | duckdb-polr/build/release/duckdb duckdb-polr/duckdb_benchmark_data/ssb.duckdb
cat duckdb-polr/benchmark/ssb-skew/init/load.sql | duckdb-polr/build/release/duckdb duckdb-polr/duckdb_benchmark_data/ssb-skew.duckdb
