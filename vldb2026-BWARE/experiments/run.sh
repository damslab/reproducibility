#!/bin/bash

source parameters.sh

mkdir -p results

source "python_venv/bin/activate"

# Figure 3:
# source code/Performance/scalingLoss.sh
# # Figure 16 Frame Compression size and time
# # source code/ReadWrite/datasetsRun.sh
# #Figure 17 lossless transform encode
# source code/ReadWrite/datasetsTE.sh
# # Figure 6 + 18 Lossy transform encode size and time





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
# source code/e2enew/pipeline.sh

# Figure 24 Word embedding experiment
# source code/wordemb/run.sh



# echo "BWARE"
# rm -rf results/power/BWARE
# sudo /home/baunsgaard/Programs/jdk17/bin/java -Xmx900g -Xms900g -Xmn90g -Dspark.driver.extraJavaOptions="-Xms64g -Xmn64g -Dlog4j.configuration=file:code/logging/log4j-compression.properties" -Dspark.executor.extraJavaOptions="-Dlog4j.configuration=file:code/logging/log4j-compression.properties" -Dspark.executor.heartbeatInterval=100s -Dspark.executor.instances=2 -Dspark.default.parallelism=2 -Dspark.default.cores=2 -Dspark.executor.memory=64g -XX:+UseNUMA             -javaagent:/home/baunsgaard/Programs/joularjx/joularjx-3.0.0.jar   -Dlog4j.configuration=file:code/logging/log4j-compression.properties   --add-modules=jdk.incubator.vector   -jar /home/baunsgaard/github/systemds/target/systemds-3.3.0-SNAPSHOT.jar   -f code/e2enew/regress_lm_pipeline.dml   -exec singlenode   -config code/conf/TAWAb16.xml   -stats 100 -debug -exec singlenode -seed 333 -args data/kdd98/cup98lrn.csv.cla code/scripts/specs/kdd > results/power/BWARE.log 2>&1
# mv joularjx-result results/power/BWARE


# echo "AWARE"
# rm -rf results/power/AWARE
# sudo /home/baunsgaard/Programs/jdk17/bin/java -Xmx900g -Xms900g -Xmn90g -Dspark.driver.extraJavaOptions="-Xms64g -Xmn64g -Dlog4j.configuration=file:code/logging/log4j-compression.properties" -Dspark.executor.extraJavaOptions="-Dlog4j.configuration=file:code/logging/log4j-compression.properties" -Dspark.executor.heartbeatInterval=100s -Dspark.executor.instances=2 -Dspark.default.parallelism=2 -Dspark.default.cores=2 -Dspark.executor.memory=64g -XX:+UseNUMA            -javaagent:/home/baunsgaard/Programs/joularjx/joularjx-3.0.0.jar   -Dlog4j.configuration=file:code/logging/log4j-compression.properties   --add-modules=jdk.incubator.vector   -jar /home/baunsgaard/github/systemds/target/systemds-3.3.0-SNAPSHOT.jar   -f code/e2enew/regress_lm_pipeline.dml   -exec singlenode   -config code/conf/AWAb16.xml   -stats 100 -debug -exec singlenode -seed 333 -args data/kdd98/cup98lrn.csv.cla code/scripts/specs/kdd > results/power/AWARE.log 2>&1
# mv joularjx-result results/power/AWARE

# echo "ULA"
# rm -rf results/power/ULA
# sudo /home/baunsgaard/Programs/jdk17/bin/java -Xmx900g -Xms900g -Xmn90g -Dspark.driver.extraJavaOptions="-Xms64g -Xmn64g -Dlog4j.configuration=file:code/logging/log4j-compression.properties" -Dspark.executor.extraJavaOptions="-Dlog4j.configuration=file:code/logging/log4j-compression.properties" -Dspark.executor.heartbeatInterval=100s -Dspark.executor.instances=2 -Dspark.default.parallelism=2 -Dspark.default.cores=2 -Dspark.executor.memory=64g -XX:+UseNUMA       -javaagent:/home/baunsgaard/Programs/joularjx/joularjx-3.0.0.jar   -Dlog4j.configuration=file:code/logging/log4j-compression.properties   --add-modules=jdk.incubator.vector   -jar /home/baunsgaard/github/systemds/target/systemds-3.3.0-SNAPSHOT.jar   -f code/e2enew/regress_lm_pipeline.dml   -exec singlenode   -config code/conf/ULAb16.xml   -stats 100 -debug -exec singlenode -seed 333 -args data/kdd98/cup98lrn.csv.cla code/scripts/specs/kdd > results/power/ULA.log 2>&1
# mv joularjx-result results/power/ULA

## old?
# source code/e2e/E2_augment.sh
# source code/e2e/E2_augment_readWrite.sh
# source code/e2e/E1.sh
# source code/e2e/E3_distributed.sh