 #Client mode spark-submit script
export SPARK_HOME=../spark-3.2.1-bin-hadoop3.2
export HADOOP_CONF_DIR=/home/hadoop/hadoop-3.3.1/etc/hadoop
export HOME=/home/ssiddiqi

$SPARK_HOME/bin/spark-submit \
     --master yarn \
     --deploy-mode client \
     --driver-memory 70g \
     --num-executors 6 \
     --conf spark.driver.extraJavaOptions="-Xms70g -Xmn700m -Dlog4j.configuration=file:$HOME/SAGA/log4j.properties" \
     --conf spark.ui.showConsoleProgress=true \
     --conf spark.executor.heartbeatInterval=100s \
     --conf spark.network.timeout=51200s \
     --conf spark.executor.memoryOverhead=10000 \
     --executor-memory 105g \
     --executor-cores 32 \
      file:$HOME/SAGA/SystemDS.jar \
      -config  SystemDS-config.xml \
     "$@" 