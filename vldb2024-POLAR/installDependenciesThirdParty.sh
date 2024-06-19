#!/usr/bin/env bash

declare -a packages=(
  "openjdk-8-jre-headless" "openjdk-16-jre-headless" "postgresql-12" "software-properties-common" "unzip"
)

for package in "${packages[@]}"
do
  dpkg -s "${package}" &> /dev/null
  if [ $? -ne 0 ]; then
    echo "Installing ${package}..."
    sudo apt install -y "${package}"
  fi
done

sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

echo "Starting Postgres..."
sudo systemctl start postgresql.service

if [[ ! -d "${INSTALL_DIR}/skinnerdb" ]]; then
  echo "Downloading SkinnerDB..."
  git clone https://github.com/cornelldbgroup/skinnerdb.git
fi

if [[ ! -d "${INSTALL_DIR}/skinnermt" ]]; then
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