#!/bin/bash

# This script plots all obtained results (located in results/*) via R. The
# outputs are placed into plots/* and the mapping of pdf filenames to figures
# in the paper is as follows:
#   - Experiment1a.pdf --> Figure 3
#   - Experiment1b.pdf --> Figure 4
#   - Experiment2a1.pdf --> Figure 5a
#   - Experiment2a2.pdf --> Figure 5b
#   - Experiment2a3.pdf --> Figure 5c
#   - Experiment2a4.pdf --> Figure 5d
#   - Experiment2c1.pdf --> Figure 6a
#   - Experiment2c2.pdf --> Figure 6b
#   - Experiment2b.pdf --> Figure 7
#   - Experiment3.pdf --> Figure 8

Rscript code/plotting/Experiment1a.r;
Rscript code/plotting/Experiment1b.r;

Rscript code/plotting/Experiment2a1.r;
Rscript code/plotting/Experiment2a2.r;
Rscript code/plotting/Experiment2a3.r;
Rscript code/plotting/Experiment2a4.r;

Rscript code/plotting/Experiment2c1.r;
Rscript code/plotting/Experiment2c2.r;

Rscript code/plotting/Experiment2b.r;

Rscript code/plotting/Experiment3.r;

