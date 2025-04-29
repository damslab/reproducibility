#!/bin/bash

export HADOOP_HOME=/home/hadoop/hadoop-3.3.1
export JAVA_HOME="/usr/lib/jvm/java-1.11.0-openjdk-amd64"
export SPARK_HOME="$HOME/spark-3.2.0-bin-hadoop3.2"

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
