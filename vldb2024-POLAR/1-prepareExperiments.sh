#!/usr/bin/env bash

if [ $# -eq 0 ];
then
  echo "Preparing experiments with third-party system installation ENABLED."
else
  echo "Preparing experiments with third-party system installation DISABLED."
fi

./installDependenciesDuckDB.sh
if [ $# -eq 0 ];
then
  ./installDependenciesThirdParty.sh
fi

./loadBenchmarkDataDuckDB.sh
if [ $# -eq 0 ];
then
 ./loadBenchmarkDataThirdParty.sh
fi
