# Please note: loadBenchmarkDataDuckDB.sh must run beforehand

set -eo pipefail

INSTALL_DIR="${PWD}"

echo "Downloading JOB data... [SkinnerDB]"
source "venv/bin/activate"
gdown "1UCXtiPvVlwzUCWxKM6ic-XqIryk4OTgE&confirm=t"
unzip imdbskinner.zip -d data

echo "Downloading JOB data... [SkinnerMT]"
mkdir -p data
gdown "1zr9pKMfK33IOlZ26YrvLpO1STi7Rzueu&confirm=t"
unzip databases.zip
rm databases.zip
mv imdb data/skinnermtimdb
rm -rf tpch-sf-10 jcch-sf-10
rm data/skinnermtimdb/config.sdb
cat <<EOT >> data/skinnermtimdb/config.sdb
PARALLEL_ALGO=DP
NR_WARMUP=1
NR_EXECUTORS=1
NR_BATCHES=120
WRITE_RESULTS=false
THREADS=8
JNI_PATH=$INSTALL_DIR/skinnermt/Filter/jniFilter.so
EOT

echo "Preparing benchmark data... [Postgres]"
mkdir -p data/imdb
mkdir -p data/ssb
mkdir -p data/ssb-skew
sed -i"" -e "s|PATHVAR|${INSTALL_DIR}|" ./experiments/util/*.sql
sed -i"" -e "s|PATHVAR|${INSTALL_DIR}/data|" ./experiments/util/skinnerdb/*.sql
cat experiments/util/export-imdb.sql | duckdb-polr/build/release/duckdb duckdb-polr/duckdb_benchmark_data/imdb.duckdb
cat experiments/util/export-ssb.sql | duckdb-polr/build/release/duckdb duckdb-polr/duckdb_benchmark_data/ssb.duckdb
cat experiments/util/export-ssb-skew.sql | duckdb-polr/build/release/duckdb duckdb-polr/duckdb_benchmark_data/ssb-skew.duckdb
sed -i"" -e "s|true|1|g" ./data/ssb/date.tbl
sed -i"" -e "s|false|0|g" ./data/ssb/date.tbl
sed -i"" -e "s|true|1|g" ./data/ssb-skew/date.tbl
sed -i"" -e "s|false|0|g" ./data/ssb-skew/date.tbl
mv data/imdb/cast_info.tbl data/imdb/cast_info.tbl.dirty
sed -i"" -e "s|\x0| |g" ./data/imdb/cast_info.tbl.dirty
iconv -f utf-8 -t utf-8 -c ./data/imdb/cast_info.tbl.dirty > ./data/imdb/cast_info.tbl
rm data/imdb/cast_info.tbl.dirty
mv data/imdb/movie_info.tbl data/imdb/movie_info.tbl.dirty
sed -i"" -e "s|\x0| |g" ./data/imdb/movie_info.tbl.dirty
iconv -f utf-8 -t utf-8 -c ./data/imdb/movie_info.tbl.dirty > ./data/imdb/movie_info.tbl
rm data/imdb/movie_info.tbl.dirty
