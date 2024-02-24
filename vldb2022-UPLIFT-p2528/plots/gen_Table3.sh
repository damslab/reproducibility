#!/bin/bash

# Read numbers from files
n11=$(cat ../results/Tab3_T2_spark.dat)
n12=$(cat ../results/Tab3_T2_spark1T.dat)
n13=$(cat ../results/Tab3_T2_dask.dat)
n14=$(cat ../results/Tab3_T2_sk.dat)
n15=$(cat ../results/Tab3_T2_base.dat)
n16=$(cat ../results/Tab3_T2_uplift.dat)
n21=$(cat ../results/Tab3_T3_spark.dat)
n22=$(cat ../results/Tab3_T3_spark1T.dat)
n23=$(cat ../results/Tab3_T3_dask.dat)
n24=$(cat ../results/Tab3_T3_sk.dat)
n25=$(cat ../results/Tab3_T3_base.dat)
n26=$(cat ../results/Tab3_T3_uplift.dat)
n31=$(cat ../results/Tab3_T9_spark.dat)
n32=$(cat ../results/Tab3_T9_spark1T.dat)
n34=$(cat ../results/Tab3_T9_sk.dat)
n35=$(cat ../results/Tab3_T9_base.dat)
n36=$(cat ../results/Tab3_T9_uplift.dat)

# Specify the output file
output_file="Table_3.table"

# Print the table and save to a file
{
  echo "    |   Spark   |   Spark1T   |   Dask   |   SKlearn   |   Base   |   UPLIFT   |"
  echo "--------------------------------------------------------------------------------"
  echo "T2  |   $n11    |     $n12    |   $n13   |     $n14    |   $n15   |    $n16    |"
  echo "T3  |   $n21    |     $n22    |   $n23   |     $n24    |   $n25  |    $n26   |"
  echo "T9  |   $n31     |     $n32    |    NA     |     $n34    |   $n35   |    $n36    |"
} > "$output_file"

echo "Table saved to $output_file"
