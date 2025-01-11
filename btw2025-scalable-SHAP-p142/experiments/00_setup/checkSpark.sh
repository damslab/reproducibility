#!/bin/bash
set -e
echo "Checking if spark is available..."


if command -v "$SPARK_HOME"/bin/spark-submit &> /dev/null; then
    echo "Apache Spark is installed."
    exit 0
else
    echo "Apache Spark is not installed. Please install Spark to run distributed experiments."
    exit 1
fi

