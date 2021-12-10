#!/bin/bash

genPlot() {
  Rscript $1.R
  pdfcrop $1.pdf $1.pdf
}

genPlot exp_6a
genPlot exp_6b
genPlot exp_7a
genPlot exp_7b
genPlot exp_8a
genPlot exp_8b

genPlot exp_9a
genPlot exp_9b
genPlot exp_9c
genPlot exp_9d
genPlot exp_9e
genPlot exp_9f

genPlot exp_10a
genPlot exp_10b
genPlot exp_10c
genPlot exp_10d

