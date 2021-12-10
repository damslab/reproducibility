#!/bin/bash

# Compile the paper
pdflatex -interaction=batchmode SIGMOD2021
bibtex SIGMOD2021 > /dev/null
pdflatex -interaction=batchmode SIGMOD2021
pdflatex -interaction=batchmode SIGMOD2021

# Rename and move to the main folder
cp SIGMOD2021.pdf ../rdm32_repro.pdf

