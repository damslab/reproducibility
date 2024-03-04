#!/bin/bash

source parameters.sh

mkdir -p results

source "python_venv/bin/activate"

#####
## DONT RUN AGAIN
# Figure 3:
# source code/Performance/scalingLoss.sh
# # Figure 16 Frame Compression size and time
# # source code/ReadWrite/datasetsRun.sh
# #Figure 17 lossless transform encode
# # source code/ReadWrite/datasetsTE.sh
# # Figure 6 + 18 Lossy transform encode size and time
######




# # Figure 21 poly  + lossy performance algorithm
# source code/e2enew/poly.sh



# # Figure 19 Base line algorithm
# source code/e2enew/regression.sh  ## settled except for replace maybe need optimization.
# source code/e2enew/classification.sh



# # Figure 20 lossy performance algorithm
# # Lossy Regression
# source code/e2enew/lossy_lm.sh
# #Lossy classification
# source code/e2enew/lossy_classification.sh

# # Figure ??? Lossy scaling # Citeo up till one day.
# source code/e2enew/lossy_scaling.sh



## Other baselines 
# source code/otherSystems/run.sh

# Figure 22 Multi spec


# Improve Crypto and Run Crit again --- fix execution criteo
# source code/ReadWrite/datasetsTElossy.sh
# source code/e2enew/algorithms.sh


# Figure 23 Multi spec Multi augment.
source code/e2enew/pipeline.sh


# source code/e2e/E2_augment.sh
# source code/e2e/E2_augment_readWrite.sh

# source code/e2e/E1.sh


# source code/e2e/E3_distributed.sh