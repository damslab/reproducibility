 #Client mode spark-submit script
export SPARK_HOME=../spark-3.2.1-bin-hadoop3.2
export HADOOP_CONF_DIR=/home/hadoop/hadoop-3.3.1/etc/hadoop


$SPARK_HOME/bin/spark-submit \
     --master yarn \
     --deploy-mode client \
     --driver-memory 110g \
     --num-executors 2 \
     --conf spark.driver.extraJavaOptions="-Xms110g -Xmn11g -Dlog4j.configuration=file:$HOME/TaskParallelExperiments/log4j.properties" \
     --conf spark.ui.showConsoleProgress=true \
     --conf spark.executor.heartbeatInterval=100s \
     --conf spark.network.timeout=512s \
     --executor-memory 105g \
     --executor-cores 32 \
      file:$HOME/TaskParallelExperiments/SystemDS.jar \
      -config  file:$HOME/TaskParallelExperiments/SystemDS-config.xml \
     "$@" 