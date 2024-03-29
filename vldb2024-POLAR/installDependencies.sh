#!/usr/bin/env bash

INSTALL_DIR="${PWD}"

sudo apt update
sudo add-apt-repository ppa:deadsnakes/ppa

declare -a packages=(
  "cgroup-tools" "git" "libssl-dev" "openjdk-8-jre-headless" "openjdk-16-jre-headless" "postgresql-12" "python3-pip" "software-properties-common" "texlive-full" "unzip"
)

for package in "${packages[@]}"
do
  dpkg -s "${package}" &> /dev/null
  if [ $? -ne 0 ]; then
    echo "Installing ${package}..."
    sudo apt install "${package}"
  fi
done

echo "Starting Postgres..."
sudo systemctl start postgresql.service

echo "Creating cgroups..."
sudo cgcreate -a "$USER" -t "$USER" -g cpu:/limitcpu1
sudo cgset -r cpu.cfs_quota_us=100000 limitcpu1
sudo cgcreate -a "$USER" -t "$USER" -g cpu:/limitcpu8
sudo cgset -r cpu.cfs_quota_us=800000 limitcpu8

if [[ ! -d "${INSTALL_DIR}/duckdb-polr" ]]; then
  echo "Downloading POLAR..."
  git clone https://github.com/d-justen/duckdb-polr.git
  cd duckdb-polr
  BUILD_BENCHMARK=1 BUILD_TPCH=1 BUILD_HTTPFS=1 make -j
  cd ..
fi

if [[ ! -d "${INSTALL_DIR}/ssb-dbgen" ]]; then
  echo "Downloading SSB DBGen..."
  git clone https://github.com/eyalroz/ssb-dbgen.git
  cd ssb-dbgen
  cmake .
  cmake --build .
  echo "Generating SSB data..."
  ./dbgen -v -s 100
  cd ..
  mkdir -p data/ssb
  mv ssb-dbgen/*.tbl data/ssb
  sed -i"" -e "s|PATHVAR|${INSTALL_DIR}/data/ssb|" ./duckdb-polr/benchmark/ssb/init/load.sql
  sed -i"" -e "s|PATHVAR|${INSTALL_DIR}/data/ssb|" ./duckdb-polr/benchmark/ssb-skew/init/load.sql
fi

echo "Loading JOB data..."
rm -rf duckdb-polr/duckdb_benchmark_data
mkdir -p duckdb-polr/duckdb_benchmark_data
cat duckdb-polr/benchmark/imdb_plan_cost/init/schema.sql | duckdb-polr/build/release/duckdb duckdb-polr/duckdb_benchmark_data/imdb.duckdb
cat duckdb-polr/benchmark/imdb_plan_cost/init/load.sql | duckdb-polr/build/release/duckdb duckdb-polr/duckdb_benchmark_data/imdb.duckdb
echo "Loading SSB data..."
cat duckdb-polr/benchmark/ssb/init/load.sql | duckdb-polr/build/release/duckdb duckdb-polr/duckdb_benchmark_data/ssb.duckdb
echo "Loading SSB-skew data..."
cat duckdb-polr/benchmark/ssb-skew/init/load.sql | duckdb-polr/build/release/duckdb duckdb-polr/duckdb_benchmark_data/ssb-skew.duckdb
rm -rf data
mkdir -p data/imdb
mkdir -p data/ssb
mkdir -p data/ssb-skew

echo "Preparing benchmark data for third-party systems..."
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

if [[ ! -d "${INSTALL_DIR}/venv" ]]; then
  echo "Creating Python Virtual Environment"
  python3 -m venv venv
  source "venv/bin/activate"
  pip install pip --upgrade > /dev/null
  pip -q install -r requirements.txt
  pip install --upgrade --no-cache-dir gdown
  echo "$HOSTNAME"
fi

if [[ ! -d "${INSTALL_DIR}/skinnerdb" ]]; then
  echo "Downloading SkinnerDB..."
  git clone https://github.com/cornelldbgroup/skinnerdb.git
  gdown "1UCXtiPvVlwzUCWxKM6ic-XqIryk4OTgE&confirm=t"
  unzip imdbskinner.zip -d data
  rm imdbskinner.zip
fi

if [[ ! -d "${INSTALL_DIR}/skinnermt" ]]; then
  echo "Downloading SkinnerMT"
  gdown "1CU0sJlR-GvSBKzzfJO-CyaFlM_PmN4Tb&confirm=t"
  gdown "1zr9pKMfK33IOlZ26YrvLpO1STi7Rzueu&confirm=t"
  unzip skinnermt.zip
  rm skinnermt.zip
  unzip databases.zip
  rm databases.zip
  mkdir -p data
  mv imdb data/skinnermtimdb
  rm data/skinnermtimdb/config.sdb
  rm -rf tpch-sf-10 jcch-sf-10
  mkdir build
  cd build
  git clone https://github.com/efficient/libcuckoo
  cd libcuckoo
  cmake -DCMAKE_INSTALL_PREFIX=../install -DBUILD_EXAMPLES=1 -DBUILD_TESTS=1 .
  make all
  make install
  cd ../../skinnermt/Filter
  g++ -std=c++11 -lpthread -shared -fPIC -O3 jniFilter.cpp -o jniFilter.so -I../../build/install/include/
  cd ../..
  cat <<EOT >> data/skinnermtimdb/config.sdb
PARALLEL_ALGO=DP
NR_WARMUP=1
NR_EXECUTORS=1
NR_BATCHES=120
WRITE_RESULTS=false
THREADS=8
JNI_PATH=$INSTALL_DIR/skinnermt/Filter/jniFilter.so
EOT
  cd "${INSTALL_DIR}"
fi
