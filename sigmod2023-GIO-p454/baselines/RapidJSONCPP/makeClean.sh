#!/usr/bin/env bash
# clean last cmake files and the run "make clean" and make
echo "start to compiling the project"
echo "------------------------------"

rm -rf CMakeFiles
rm -rf cmake_install.cmake
rm -rf CMakeCache.txt
rm -rf Makefile
rm -rf RapidJSONCPP.cbp
rm -rf bin
cmake .
make clean
make -j12