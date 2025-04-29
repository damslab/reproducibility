#/bin/bash


source parameters.sh

pip install wheel >> /dev/null
pip install kaggle >> /dev/null

./code/scripts/data/Criteo.sh &
./code/scripts/data/Adult.sh &
./code/scripts/data/KDD98.sh &
./code/scripts/data/UCRTime.sh & 
./code/scripts/data/Crypto.sh &
./code/scripts/data/CatInDat.sh &
./code/scripts/data/HomeCredit.sh &
./code/scripts/data/Salaries.sh & 
./code/scripts/data/Santader.sh &
./code/scripts/data/SoftDefects.sh &

wait