#!/usr/bin/env bash

if [ $# -eq 0 ];
then
  echo "Preparing experiments with third-party system installation ENABLED."
else
  echo "Preparing experiments with third-party system installation DISABLED."
fi

source installDependenciesDuckDB.sh
if [ $# -eq 0 ];
then
  source installDependenciesThirdParty.sh
fi

source loadBenchmarkDataDuckDB.sh
if [ $# -eq 0 ];
then
  source loadBenchmarkDataThirdParty.sh
fi
