#!/usr/bin/env bash

declare -a packages=(
  "git" "libssl-dev" "pigz"
)

for package in "${packages[@]}"
do
  dpkg -s "${package}" &> /dev/null
  if [ $? -ne 0 ]; then
    echo "Installing ${package}..."
    sudo apt install "${package}"
  fi
done

if [[ ! -d "$PWD/duckdb-polr" ]]; then
  echo "Downloading POLAR..."
  git clone git@github.com:d-justen/duckdb-polr.git
  cd duckdb-polr
  BUILD_BENCHMARK=1 BUILD_TPCH=1 BUILD_HTTPFS=1 make -j
  cd ..
fi

if [[ ! -d "$PWD/ssb-dbgen" ]]; then
  echo "Downloading SSB DBGen..."
  git clone git@github.com:eyalroz/ssb-dbgen.git
  cd ssb-dbgen
  cmake .
  cmake --build .
  echo "Generating SSB Data..."
  ./dbgen -v -s 10
  cd ..
  mkdir -p data/ssb
  mv ssb-dbgen/*.tbl data/ssb
  pigz -v9 data/ssb/*.tbl
  sed -i "s|PATHVAR|`pwd`/data/ssb|" ./duckdb-polr/benchmark/ssb/init/load.sql
  sed -i "s|PATHVAR|`pwd`/data/ssb|" ./duckdb-polr/benchmark/ssb-skew/init/load.sql
fi


