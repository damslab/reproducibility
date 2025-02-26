#!/bin/bash

# Submit jobs that already have their own .slurm files with proper configuration

# List of job files to submit
job_files=("unstructured_prunning.slurm" "structured_prunning.slurm")

# Iterate through each job file and submit it
for job_file in "${job_files[@]}"; do
  if [ -f "$job_file" ]; then
    echo "Submitting $job_file..."
    sbatch "$job_file"
  else
    echo "Error: $job_file not found! Skipping."
  fi
done

echo "Job submission process completed!"