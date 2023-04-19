#!/bin/bash

# clean original plots
rm -rf plots/*;

cd explocal/sigmod
make clean
make