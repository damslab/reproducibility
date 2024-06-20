#!/usr/bin/env bash

set -eo pipefail

INSTALL_DIR="${PWD}"

sudo apt update

declare -a packages=(
  "cgroup-tools" "cmake" "git" "libssl-dev" "python3-pip" "python3-venv" "wget"
)

for package in "${packages[@]}"
do
  dpkg -s "${package}" &> /dev/null
  if [ $? -ne 0 ]; then
    echo "Installing ${package}..."
    sudo apt install -y "${package}"
  fi
done

echo "Installing TeX Live"
mkdir install-tl && cd install-tl
wget -O - -- http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz | tar xzf - --strip-components=1
sudo apt install -y tex-common texinfo equivs perl-tk perl-doc
sudo ./install-tl -profile ../texlive.profile
cd ..

echo "Creating cgroups..."
sudo cgcreate -a "$USER" -t "$USER" -g cpu:/limitcpu1
sudo cgset -r cpu.cfs_quota_us=100000 limitcpu1
sudo cgcreate -a "$USER" -t "$USER" -g cpu:/limitcpu8
sudo cgset -r cpu.cfs_quota_us=800000 limitcpu8

if [[ ! -d "${INSTALL_DIR}/duckdb-polr" ]]; then
  echo "Downloading POLAR..."
  git clone https://github.com/d-justen/duckdb-polr.git
  cd duckdb-polr
  BUILD_BENCHMARK=1 BUILD_TPCH=1 BUILD_HTTPFS=1 make
  cd ..
fi

if [[ ! -d "${INSTALL_DIR}/ssb-dbgen" ]]; then
  echo "Downloading SSB DBGen..."
  git clone https://github.com/eyalroz/ssb-dbgen.git
  cd ssb-dbgen
  cmake .
  cmake --build .
  cd ..
fi

if [[ ! -d "${INSTALL_DIR}/venv" ]]; then
  echo "Creating Python Virtual Environment"
  python3 -m venv venv
  source "venv/bin/activate"
  pip install pip --upgrade > /dev/null
  pip -q install -r requirements.txt
  echo "$HOSTNAME"
fi