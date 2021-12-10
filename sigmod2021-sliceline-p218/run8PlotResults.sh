#!/bin/bash

# This script plots all obtained results (located in results/*) via R. The 
# outputs are placed into plots/* and the mapping of pdf filenames to figures 
# in the paper is as follows:
#   - Experiment1a.pdf --> Figure 3a
#   - Experiment1b.pdf --> Figure 3b (runtime)
#   - Experiment2a.pdf --> Figure 4a
#   - Experiment2b.pdf --> Figure 4b
#   - Experiment3a.pdf --> Figure 5a
#   - Experiment3b.pdf --> Figure 5b
#   - Experiment4a.pdf --> Figure 6b (runtime)
#   - Experiment4b.pdf --> Figure 6a (runtime)
#   - Experiment5a.pdf --> Figure 7a (runtime)
#   - Experiment5b.pdf --> Figure 7b (runtime)
#   - results/Experiment6.out  --> Table 2 (runtime)
#   - results/Experiment4b.dat --> R comparison Text

Rscript exp/plotting/Experiment1a.r;
Rscript exp/plotting/Experiment1b.r;

Rscript exp/plotting/Experiment2a.r;
Rscript exp/plotting/Experiment2b.r;

Rscript exp/plotting/Experiment3a.r;
Rscript exp/plotting/Experiment3b.r;

Rscript exp/plotting/Experiment4a.r;
Rscript exp/plotting/Experiment4b.r;

Rscript exp/plotting/Experiment5a.r;
Rscript exp/plotting/Experiment5b.r;
