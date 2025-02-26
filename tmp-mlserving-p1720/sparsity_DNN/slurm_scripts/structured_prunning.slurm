#!/bin/bash
#SBATCH -A rabl
#SBATCH --job-name=structured_pruning
#SBATCH --mail-user=ricardo.salazardiaz@hpi.de
#SBATCH --mail-type=ALL
#SBATCH --time=5-00:00:00
#SBATCH --mem=300G
#SBATCH --ntasks=1 # Define task count
#SBATCH --nodes=1 # Define node count
#SBATCH --cpus-per-task=64 # Define cpu core count per task 
#SBATCH --partition sorcery # partition
#SBATCH --nodelist=gx01
#SBATCH --gpus=1


# HDFS folder:
ulimit -n 65536

# Directory where the files are located
directory="/app/llm_adapt_serving/data/artifacts"

# Check if the file exists
file_path="${directory}/prunning_results.csv"
if [ -e "$file_path" ]; then
    echo "File $file_path exists. Deleting it."
    rm "$file_path"
    echo "File deleted."
else
    echo "File $file_path does not exist."
fi


enroot start -m /hpi/fs00/home/ricardo.salazardiaz/llm-adapt-serving:/app/llm_adapt_serving \
             -m /hpi/fs00/share/fg/rabl/ricardo.salazardiaz/data:/app/llm_adapt_serving/data  \
            --rw rsd8914+llm_adapt_serving+latest bash /app/llm_adapt_serving/slurm_scripts/structured_pruning.sh

