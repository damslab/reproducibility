#!/bin/bash

mkdir -p archive
nr_old=$(ls archive | wc -l)
archive_old="archive/$nr_old"

nr=$((nr_old+1))
archive="archive/$nr"

mkdir $archive

cp -r code $archive
cp -r plots $archive
cp -r results $archive

cp run.sh $archive
cp setup.sh $archive

echo "Clearing Results!"

rm -rf results/*
