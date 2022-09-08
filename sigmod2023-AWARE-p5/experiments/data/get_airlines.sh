#/bin/bash

# Change directory to data.
if [[ pwd != *"data"* ]]; then
    cd "data"
fi

mkdir -p airlines

# Download file if not already downloaded.
if [[ ! -f "airlines/airlines.zip" ]]; then
    # echo "airlines file already downloaded"
# else
    # https://www.transtats.bts.gov/OT_Delay/OT_DelayCause1.asp?pn=1
    # https://dataverse.harvard.edu/dataset.xhtml;jsessionid=fe17cc149e3d39ae7da34fa0acc7?persistentId=doi%3A10.7910%2FDVN%2FHG7NV7&version=&q=&fileTypeGroupFacet=&fileAccess=&fileSortField=date
    wget -nv -O airlines/airlines.zip https://dataverse.harvard.edu/api/access/datafiles/1375005,1375004,1375003,1375002,1375001,1375000,1374999,1374998,1374997,1374996,1374995,1374994,1374993,1374929,1374928,1374927,1374926,1374925,1374923,1374922,1374918,1374917,1374930,1374931,1374932,1374933?gbrecs=true
    echo "Download complete"
fi

if [[ ! -f "airlines/airports.csv" ]]; then
    # echo "airlines file already unzipped"
# else
    cd airlines
    unzip airlines.zip
    cd ..
fi

if [[ -f "airlines/1987.csv.bz2" ]]; then
    cd airlines
    mkdir -p years
    for x in {1987..2008}; do
        if [[ -f "$x.csv.bz2" ]]; then
            bzip2 -d $x.csv.bz2 && echo "Uncompressed $x" && mv $x.csv years/ &
        fi
    done
    cd ..
    wait
fi

if [[ ! -d "airlines/sample" ]]; then

    cd airlines
    mkdir -p sample
    for x in {2007..2008}; do
        sed '1d' years/$x.csv > sample/$x.csv &
    done
    cd ..
    wait
fi

cd ..

if [[ ! -d "data/airlines/train_airlines.data" ]]; then
    systemds code/dataPrep/saveTrainAirlines.dml
fi

echo "Airlines Setup Done"
