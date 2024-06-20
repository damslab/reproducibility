INSTALL_DIR="${PWD}"

set -eo pipefail

echo "Generating SSB data..."
cd ssb-dbgen
./dbgen -v -s 100
cd ..
mkdir -p data/ssb
mv ssb-dbgen/*.tbl data/ssb
sed -i"" -e "s|PATHVAR|${INSTALL_DIR}/data/ssb|" ./duckdb-polr/benchmark/ssb/init/load.sql
sed -i"" -e "s|PATHVAR|${INSTALL_DIR}/data/ssb|" ./duckdb-polr/benchmark/ssb-skew/init/load.sql

echo "Loading JOB data... [DuckDB]"
rm -rf duckdb-polr/duckdb_benchmark_data
mkdir -p duckdb-polr/duckdb_benchmark_data
cat duckdb-polr/benchmark/imdb_plan_cost/init/schema.sql | duckdb-polr/build/release/duckdb duckdb-polr/duckdb_benchmark_data/imdb.duckdb
cat duckdb-polr/benchmark/imdb_plan_cost/init/load.sql | duckdb-polr/build/release/duckdb duckdb-polr/duckdb_benchmark_data/imdb.duckdb
echo "Loading SSB data... [DuckDB]"
cat duckdb-polr/benchmark/ssb/init/load.sql | duckdb-polr/build/release/duckdb duckdb-polr/duckdb_benchmark_data/ssb.duckdb
echo "Loading SSB-skew data... [DuckDB]"
cat duckdb-polr/benchmark/ssb-skew/init/load.sql | duckdb-polr/build/release/duckdb duckdb-polr/duckdb_benchmark_data/ssb-skew.duckdb
rm -rf data
