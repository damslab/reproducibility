#!/bin/bash

# Read numbers from files
n11=$(cat ../results/4e_T2_Base.dat)
n12=$(cat ../results/4e_T2_Scale.dat)
n13=$(cat ../results/4e_T2_udf.dat)
n21=$(cat ../results/4e_T4_Base.dat)
n22=$(cat ../results/4e_T4_Scale.dat)
n23=$(cat ../results/4e_T4_udf.dat)
n31=$(cat ../results/4e_T4s_Base.dat)
n32=$(cat ../results/4e_T4s_Scale.dat)
n33=$(cat ../results/4e_T4s_udf.dat)

# Specify the output file
output_file="fig_4e.table"

# Print the table and save to a file
{
  echo "    |    Base    |    Scale    |  Scale-UDF  |"
  echo "-----------------------------------------------"
  echo "T2  |    $n11    |     $n12    |     $n13    |"
  echo "T4  |    $n21    |     $n22    |     $n23    |"
  echo "T4* |    $n31    |     $n32    |     $n33    |"
} > "$output_file"

echo "Table saved to $output_file"
