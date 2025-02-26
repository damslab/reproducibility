#!/bin/bash
#SBATCH -A rabl
#SBATCH --job-name=unstructured_pruning
#SBATCH --mail-user=ricardo.salazardiaz@hpi.de
#SBATCH --mail-type=ALL
#SBATCH --time=5-00:00:00
#SBATCH --mem=150G
#SBATCH --ntasks=1 # Define task count
#SBATCH --nodes=1 # Define node count
#SBATCH --cpus-per-task=64 # Define cpu core count per task 
#SBATCH --partition magic # partition
#SBATCH --nodelist=cx[17-32]

# HDFS folder:
ulimit -n 65536

enroot start -m /hpi/fs00/home/ricardo.salazardiaz/llm-adapt-serving:/app/llm_adapt_serving \
             -m /hpi/fs00/share/fg/rabl/ricardo.salazardiaz/data:/app/llm_adapt_serving/data  \
            --rw rsd8914+llm_adpt_serving+latest python /app/llm_adapt_serving/src/unstructured_pruning.py

