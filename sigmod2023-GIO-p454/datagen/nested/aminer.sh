#!/usr/bin/env bash


in_path=$1
sample_nrows=$2
out_path=$3

#echo "1. AMiner Author Data Gen Started ..."
#time java -Xms1g -Xmx30g -cp  ./target/nesteddbmodel-1.0-SNAPSHOT-jar-with-dependencies.jar\
#      at.tugraz.aminer.AminerAuthorDataGen $in_path $out_path $sample_nrows
#echo "1. AMiner Author Data Gen Finished ..."


#echo "2. AMiner Author Example Gen Started ..."
#time java -Xms1g -Xmx14g -cp  ./target/nesteddbmodel-1.0-SNAPSHOT-jar-with-dependencies.jar\
#      at.tugraz.aminer.AminerAuthorExampleGen $in_path $out_path $sample_nrows
#echo "2. AMiner Author Example Gen Finished ..."


#echo "3. AMiner Paper Data Gen Started ..."
#time java -Xms1g -Xmx30g -cp  ./target/nesteddbmodel-1.0-SNAPSHOT-jar-with-dependencies.jar\
#      at.tugraz.aminer.AminerPaperDataGen $in_path $out_path $sample_nrows
#echo "3. AMiner Paper Data Gen Finished ..."

echo "4. AMiner Paper Example Gen Started ..."
time java -Xms1g -Xmx30g -cp  ./target/nesteddbmodel-1.0-SNAPSHOT-jar-with-dependencies.jar\
      at.tugraz.aminer.AminerPaperExampleGen $in_path $out_path $sample_nrows
echo "4. AMiner Paper Example Gen Finished ..."