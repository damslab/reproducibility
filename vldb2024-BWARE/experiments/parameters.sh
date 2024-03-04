#!/bin/bash

export SYSTEMDS_ROOT="$HOME/github/systemds"
export PATH="$SYSTEMDS_ROOT/bin:$PATH"
export LOG4JPROP='code/logging/log4j-compression.properties'

export SYSDS_QUIET=1
export SYSDS_DISTRIBUTED=0
export SYSDS_BRANCH="origin/RMMIdentity2"

if [ "$HOSTNAME" = "XPS-15-7590" ]; then
	export SYSTEM_THREADS="16"
	export SYSTEMDS_STANDALONE_OPTS="-Xmx25g -Xms25g -Xmn2500m \
			-Dspark.driver.extraJavaOptions=\"-Xms1g -Xmn1g -Dlog4j.configuration=file:$LOG4JPROP\" \
			-Dspark.executor.extraJavaOptions=\"-Dlog4j.configuration=file:$LOG4JPROP\" \
			-Dspark.executor.heartbeatInterval=100s \
			-Dspark.executor.instances=2 \
			-Dspark.default.parallelism=2 \
			-Dspark.default.cores=2 \
			-Dspark.executor.memory=1g \
		"
elif [ "$HOSTNAME" = "dams-su1" ]; then
	export SYSTEM_THREADS="128"
	export SYSTEMDS_STANDALONE_OPTS="-Xmx900g -Xms900g -Xmn90g \
			-Dspark.driver.extraJavaOptions=\"-Xms64g -Xmn64g -Dlog4j.configuration=file:$LOG4JPROP\" \
			-Dspark.executor.extraJavaOptions=\"-Dlog4j.configuration=file:$LOG4JPROP\" \
			-Dspark.executor.heartbeatInterval=100s \
			-Dspark.executor.instances=2 \
			-Dspark.default.parallelism=2 \
			-Dspark.default.cores=2 \
			-Dspark.executor.memory=64g \
		"
	export SYSTEMDS_DISTRIBUTED_OPTS="\
			--master yarn \
			--deploy-mode client \
			--driver-memory 1000g \
			--conf spark.driver.extraJavaOptions=\"-Xms1000g -Xmn100g -Dlog4j.configuration=file:$LOG4JPROP\" \
			--conf spark.executor.extraJavaOptions=\"-Dlog4j.configuration=file:$LOG4JPROP\" \
			--conf spark.executor.heartbeatInterval=100s \
			--files $LOG4JPROP \
			--conf spark.network.timeout=512s \
			--num-executors 8 \
			--executor-memory 200g \
			--executor-cores 48 \
		"
elif [[ "$HOSTNAME" == *"dams-so0"* ]]; then
	export SYSTEM_THREADS="48"
	export SYSTEMDS_STANDALONE_OPTS="-Xmx250g -Xms250g -Xmn25g \
			-Dspark.driver.extraJavaOptions=\"-Xms10g -Xmn10g -Dlog4j.configuration=file:$LOG4JPROP\" \
			-Dspark.executor.extraJavaOptions=\"-Dlog4j.configuration=file:$LOG4JPROP\" \
			-Dspark.executor.heartbeatInterval=100s \
			-Dspark.executor.instances=2 \
			-Dspark.default.parallelism=2 \
			-Dspark.default.cores=2 \
			-Dspark.executor.memory=1g \
		"
	export SYSTEMDS_DISTRIBUTED_OPTS="\
			--master yarn \
			--deploy-mode client \
			--driver-memory 200g \
			--conf spark.driver.extraJavaOptions=\"-Xms200g -Xmn20g -Dlog4j.configuration=file:$LOG4JPROP\" \
			--conf spark.executor.extraJavaOptions=\"-Dlog4j.configuration=file:$LOG4JPROP\" \
			--conf spark.executor.heartbeatInterval=100s \
			--files $LOG4JPROP \
			--conf spark.network.timeout=512s \
			--num-executors 8 \
			--executor-memory 200g \
			--executor-cores 48 \
		"
else
	echo "unknown machine please add"
	exit -1
fi

if [ -d ~/intel ] && [ -d ~/intel/bin ] && [ -f ~/intel/bin/compilervars.sh ]; then
	. ~/intel/bin/compilervars.sh intel64
fi

export VENV_PATH="python_venv"
source "$VENV_PATH/bin/activate"
export remoteDir="papers/2023-vldb-CAFE/experiments/"
export remotes=("su1")

seed=333

### Cleanup tmp
rm -rf /tmp/systemds
