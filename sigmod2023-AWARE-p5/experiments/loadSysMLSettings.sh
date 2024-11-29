#!/bin/bash

if [[ ! -d "/usr/lib/jvm/java-8-openjdk-amd64" ]]; then 
    echo "failed to load java 8 path."
    exit -1
fi

JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64"
PATH="/usr/lib/jvm/java-8-openjdk-amd64/bin":$PATH

export HADOOP_HOME=/home/hadoop/hadoop-2.7.7
export JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64"
export SPARK_HOME="$HOME/spark-2.4.7-bin-hadoop2.7"

export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export HADOOP_CLASSPATH="${JAVA_HOME}/lib/tools.jar"

export PATH="$JAVA_HOME/bin:$PATH"
export PATH="$SPARK_HOME/bin:$PATH"
