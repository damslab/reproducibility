#/bin/bash

source parameters.sh

# https://www.cs.ucr.edu/~eamonn/time_series_data_2018/
mkdir -p data/UCRTime/

# If not unpacked:
if [[ ! -f "data/UCRTime/UCRArchive_2018/DodgerLoopWeekend/DodgerLoopWeekend_TEST.tsv" ]]; then
    # If not downloaded:
    if [[ ! -f "data/UCRTime/UCRArchive_2018.zip" ]]; then
        wget -O data/UCRTime/UCRArchive_2018.zip https://www.cs.ucr.edu/~eamonn/time_series_data_2018/UCRArchive_2018.zip
    fi
    unzip -u -P someone data/UCRTime/UCRArchive_2018.zip -d data/UCRTime/
fi

export SYSDS_QUIET=1

if [[ ! -f "data/UCRTime/UCRArchive_2018/ACSF1/ACSF1_T.data.mtd" ]]; then
    for f in data/UCRTime/UCRArchive_2018/*; do

        name=${f#*2018/}
        fullName="$f/${name}_TRAIN.tsv"
        echo $fullName
        systemds code/scripts/data/UCR_tsv.dml \
            -args "$fullName" "$f/${name}_T" &
        sleep 0.5
    done
fi

wait
