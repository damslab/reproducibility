#!/bin/bash
# HDFS directory to upload the folder to
HDFS_DIR="/user/hadoop/scalable-shap"
LOCAL_FOLDER="../10_data"

# Check if HDFS is available
hdfs dfs -ls / &> /dev/null
if [[ $? -eq 0 ]]; then
  echo "HDFS is available."

  # Create the target HDFS directory if it doesn't exist
  hdfs dfs -test -d "$HDFS_DIR"
  if [[ $? -ne 0 ]]; then
    echo "HDFS directory $HDFS_DIR does not exist. Creating it..."
    hdfs dfs -mkdir -p "$HDFS_DIR"
    if [[ $? -ne 0 ]]; then
      echo "Failed to create HDFS directory $HDFS_DIR. Exiting."
      exit 1
    fi
  fi

  # Upload the folder to HDFS recursively
  echo "Uploading folder $LOCAL_FOLDER to $HDFS_DIR..."
  hdfs dfs -put -f "$LOCAL_FOLDER" "$HDFS_DIR"
  if [[ $? -eq 0 ]]; then
    echo "Folder uploaded successfully to $HDFS_DIR."
  else
    echo "Failed to upload the folder to HDFS."
    exit 1
  fi
else
  echo "HDFS is not available. Please check your HDFS setup."
  exit 1
fi
