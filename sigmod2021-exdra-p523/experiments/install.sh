#!/bin/bash

# Load in the machine locations and settings in general
source parameters.sh

# Make address iterable including main and localhost:
address=(${address[@]} $main "localhost")

installStringJava='printf "$(hostname)   \tInstalled $(git rev-parse --abbrev-ref HEAD) $(git rev-parse HEAD)\n";'
setenvString='export JAVA_HOME="/usr/lib/jvm/java-1.8.0-openjdk-amd64"; export PATH=$JAVA_HOME/bin:$PATH;'
# Install systemds java
for index in ${!address[*]}; do
    ssh -T ${address[$index]} "
        mkdir -p reproducibility;
        cd reproducibility;
        [ ! -d 'systemds' ] && git clone https://github.com/apache/systemds.git > /dev/null 2>&1;
        cd systemds;
        $setenvString
        git ls-files -z | xargs -0 rm > /dev/null 2>&1;
        git checkout -- . > /dev/null 2>&1;
        git clean -fdx > /dev/null 2>&1;
        git checkout $systemdsHash > /dev/null 2>&1;
        mvn clean package -P distribution | grep '[INFO] BUILD';
        $installStringJava" &
    # Make python venv:
    ssh -T ${address[$index]} "
        mkdir -p $remoteDir;
        cd $remoteDir;
        rm -fr code;
        python3 -m venv $VENV_PATH;
        " &
done
wait

# transfer requirements txt.
for index in ${!address[*]}; do
    rsync -avhq -e ssh requirements.txt ${address[$index]}:$remoteDir &
done
wait

installStringPython='printf "$(hostname)   \tInstalled Python Dependencies\n";'
# Install systemds python (dependent on the java install)
for index in ${!address[*]}; do
    # Make dirs on all sites.
    ssh -T ${address[$index]} "
        mkdir -p ${remoteDir};
        cd ${remoteDir};
        mkdir -p code;
        mkdir -p hprof;
        mkdir -p results;" &
    # Install python dependencies and systemds
    ssh -T ${address[$index]} "
        cd ${remoteDir};
        source 'python_venv/bin/activate';
        pip install -q -r requirements.txt > /dev/null 2>&1;
        cd ~/reproducibility/systemds/src/main/python;
        python create_python_dist.py > /dev/null 2>&1;
        pip install . > /dev/null 2>&1;
        $installStringPython" &
done
wait

# Synchronize code
for index in ${!address[*]}; do
    rsync -avhq -e ssh code/* ${address[$index]}:$remoteDir/code &
done
wait
