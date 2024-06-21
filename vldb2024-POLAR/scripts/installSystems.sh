#!/usr/bin/env bash

set -o pipefail

INSTALL_DIR="${PWD}"

#### THIRD-PARTY SYSTEMS ###

if [ $# -eq 0 ];
then
  if [[ ! -d "${INSTALL_DIR}/skinnerdb" ]]; then
    echo "Downloading SkinnerDB..."
    git clone https://github.com/cornelldbgroup/skinnerdb.git
  fi

  if [[ ! -d "${INSTALL_DIR}/skinnermt" ]]; then
    source "venv/bin/activate"
    pip install gdown
    pip install --upgrade gdown
    echo "Downloading SkinnerMT"
    gdown "1CU0sJlR-GvSBKzzfJO-CyaFlM_PmN4Tb&confirm=t"
    unzip skinnermt.zip
    rm skinnermt.zip
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
    cd "${INSTALL_DIR}"
  fi
fi

#### DUCKDB ###

if [[ ! -d "${INSTALL_DIR}/duckdb-polr" ]]; then
  echo "Downloading POLAR..."
  git clone https://github.com/d-justen/duckdb-polr.git
  cd duckdb-polr
  BUILD_BENCHMARK=1 BUILD_TPCH=1 BUILD_HTTPFS=1 make
  cd ..
fi
