#!/bin/bash

./plots/makePlots.sh

cp plots/pdfs/workers.pdf ../paper/figures/workers.pdf
cp plots/pdfs/workersSSL.pdf ../paper/figures/workersSSL.pdf
cp plots/pdfs/mlsystems.pdf ../paper/figures/mlsystems.pdf
cp plots/pdfs/workersPL.pdf ../paper/figures/workersPL.pdf

