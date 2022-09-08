#!/bin/bash

nr_old=$(ls archive | wc -l)
archive_old="archive/$nr_old"

nr=$((nr_old+1))
archive="archive/$nr"

mkdir $archive

cp -r code $archive
cp -r plots $archive
cp -r results $archive

# rm -r $archive/code/compression/*/lib/

cp run.sh $archive
cp setup.sh $archive
cp parameters.sh $archive
cp plot.sh $archive

# if [ -d $archive_old ]; then
#     echo "Compressing Old archive: $archive_old"
#     tar -czvf $archive_old.tar.gz $archive_old > /dev/null
#     rm -r $archive_old
# fi

echo "Clearing Results!"


rm -r results/*