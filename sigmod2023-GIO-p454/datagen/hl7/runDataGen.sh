#!/bin/bash

seed_data=HL7-Message-Sample-Anonymised.dat
out_path=../../data/message-hl7.dat
nrows=10240000

python3 HL7-DataGen.py $seed_data $out_path $nrows