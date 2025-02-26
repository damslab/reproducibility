#!/bin/bash

# Define the first set of parameters
strategies=('structured')
imagenet_subset_list=('' 'animals' 'clothes' 'food' 'veggies' 'fruits' 'traffic')
# imagenet_subset_list=('traffic')

# Path to the Python script
python_script="/app/llm_adapt_serving/src/structured_pruning.py"
# Directory where the files are located
directory="/app/llm_adapt_serving/data/artifacts"

# Nested for loop
for subset in "${imagenet_subset_list[@]}"; do
    # Check if the file exists
    file_path="${directory}/${subset}_prunning_results.csv"
    if [ -e "$file_path" ]; then
        echo "File $file_path exists. Deleting it."
        rm "$file_path"
        echo "File deleted."
    else
        echo "File $file_path does not exist."
    fi
    for strategy in "${strategies[@]}"; do
        for p in $(seq 0.1 0.1 1.0); do
            echo "Running Python script with parameters: $strategy, $p, $subset"
            
            python "$python_script" "$strategy" "$p" "$subset"
        done
    done
done

echo "All combinations completed!"