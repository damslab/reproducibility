#!/bin/bash

# Load in the machine locations and settings in general
source experiments/parameters.sh

# Make address iterable including main and localhost:
address=(${address[@]} $main "localhost")

# for each location verify setup:
for index in ${!address[*]}; do
    echo "alias: ${address[$index]}"
    ssh ${address[$index]} '
        echo "$HOSTNAME"; 
        java -version; 
        if [ -d "/usr/lib/jvm/java-1.8.0-openjdk-amd64" ]; then
            echo "Java 1.8 exists"
        else
            echo "----------------------"
            echo "Java 1.8 is Missing!!!"
            echo "----------------------"
        fi;
        mvn -version; 
        git --version; 
        python3 --version;
        '
    echo "  "
done

