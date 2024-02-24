#!/bin/bash

genPlot() {
  Rscript $1.R
  pdfcrop $1.pdf $1.pdf
}

genPlot fig_3a
genPlot fig_3b
genPlot fig_3c
genPlot fig_3d

genPlot fig_4a
genPlot fig_4b
genPlot fig_4c
genPlot fig_4d
genPlot fig_4f
genPlot fig_4g
genPlot fig_4h
./gen_fig_4e.sh

./gen_Table3.sh
