#!/bin/bash

data_root="$(pwd)/data"
tmpdata_root="$(pwd)/tmpdata"

# clean-up
rm -rf "$data_root/aminer-author-json.dat"
rm -rf "$data_root/aminer-paper-json.dat"
rm -rf "$data_root/message-hl7.dat"
rm -rf "$data_root/autolead-xml.dat"
rm -rf "$data_root/yelp-json.dat"

in_aminer_author="$data_root/aminer-author.dat"
in_aminer_paper="$data_root/aminer-paper.dat"
in_yelp_business="$tmpdata_root/yelp_academic_dataset_business.json"
in_yelp_checkin="$tmpdata_root/yelp_academic_dataset_checkin.json"
in_yelp_review="$tmpdata_root/yelp_academic_dataset_review.json"
in_yelp_user="$tmpdata_root/yelp_academic_dataset_user.json"

hl7_sample_data=HL7-Message-Sample-Anonymised.dat
adf_sample_data=ADF-Sample.dat

hl7_out_path=../../data/message-hl7.dat
adf_out_path=../../data/autolead-xml.dat

hl7_nrows=10240000
adf_nrows=10000000


# Sample-base Data Gene (HL7 and ADF)
#####################

cd datagen/samplebase
./setup.sh

# HL7 (Custom format)
python3 HL7-DataGen.py $hl7_sample_data $hl7_out_path $hl7_nrows

# ADF (XML)
python3 ADF-DataGen.py $adf_sample_data $adf_out_path $adf_nrows


# Generate AMiner (JSON), Yelp (JSON), and Yelp (CSV)
####################################################
cd ../nested
mvn clean compile assembly:single

rm -rf nested.jar # clean-up
mv target/nested-1.0-SNAPSHOT-jar-with-dependencies.jar nested.jar
rm -rf target 

# Aminer-Author (JSON):
$CMD -cp  ./nested.jar at.tugraz.aminer.AminerAuthorDataGen $in_aminer_author $data_root

# Aminer-Paper (JSON):
$CMD -cp  ./nested.jar at.tugraz.aminer.AminerPaperDataGen $in_aminer_paper $in_aminer_author $data_root

# Yelp (JSON):
$CMD -cp  ./nested.jar at.tugraz.yelp.YelpDataGen $in_yelp_business $in_yelp_checkin $in_yelp_review $in_yelp_user $data_root