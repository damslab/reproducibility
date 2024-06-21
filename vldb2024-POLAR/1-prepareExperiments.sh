#!/usr/bin/env bash

if [ $# -eq 0 ];
then
  echo "Preparing experiments with third-party system installation ENABLED."
else
  echo "Preparing experiments with third-party system installation DISABLED."
fi

if [ $# -eq 0 ];
then
  source scripts/installSystemsDependencies.sh
  source scripts/installSystems.sh
  source scripts/loadBenchmarkData.sh
else
  source scripts/installSystemsDependencies.sh duckdb-only
  source scripts/installSystems.sh duckdb-only
  source scripts/loadBenchmarkData.sh duckdb-only
fi
