#/bin/bash

#https://ailab.criteo.com/download-criteo-1tb-click-logs-dataset/

mkdir -p data/criteo/

if [[ ! -f "data/criteo/day_0.tsv" ]]; then
    echo "Go to  https://ailab.criteo.com/download-criteo-1tb-click-logs-dataset/ and download day 0"
    echo "and uncompress it and put it in 'data/criteo' relative to this path"
    exit
fi

if [[ ! -f "data/criteo/day_0_1000.tsv" ]]; then
    # https://ailab.criteo.com/download-criteo-1tb-click-logs-dataset/
    # wget https://download.wetransfer.com/eugv/4bbea9b4a54baddea549d71271a38e2c20230428071257/abaa609e0d18f95ad5c29dad106469775cf499bb/day_0.gz?cf=y&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRlZmF1bHQifQ.eyJleHAiOjE2OTQ0MzcyNjMsImlhdCI6MTY5NDQzNjY2MywiZG93bmxvYWRfaWQiOiI4MWEwNTdmZS00YTA5LTQ0ZDMtYmFkZC1mOWI1YTIxNWQyMDkiLCJzdG9yYWdlX3NlcnZpY2UiOiJzdG9ybSJ9.2bk1tF8KrEI8Iei-uzMSPCL-PCtToIujhtqXscgMMEs -O data/criteo/day_0.gz
    # gzip -d data/criteo/day_0.gz

    cd data/criteo

    head -n 1000 day_0.tsv >day_0_1000.tsv &
    head -n 10000 day_0.tsv >day_0_10000.tsv &
    head -n 100000 day_0.tsv >day_0_100000.tsv &
    head -n 300000 day_0.tsv >day_0_300000.tsv &
    head -n 1000000 day_0.tsv >day_0_1000000.tsv &
    head -n 3000000 day_0.tsv >day_0_3000000.tsv &
    head -n 10000000 day_0.tsv >day_0_10000000.tsv &
    head -n 30000000 day_0.tsv >day_0_30000000.tsv &
    head -n 100000000 day_0.tsv >day_0_100000000.tsv &
    head -n 10000 day_23.tsv >day_23_10000.tsv &

    cd ../../
fi

cd data/criteo
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":195841983}' >day_0.tsv.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":1000}' >day_0_1000.tsv.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":10000}' >day_0_10000.tsv.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":100000}' >day_0_100000.tsv.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":300000}' >day_0_300000.tsv.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":1000000}' >day_0_1000000.tsv.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":3000000}' >day_0_3000000.tsv.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":10000000}' >day_0_10000000.tsv.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":30000000}' >day_0_30000000.tsv.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":100000000}' >day_0_100000000.tsv.mtd

echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":10000}' >day_23_10000.tsv.mtd

echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":195841983}' >day_0.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":199563535}' >day_1.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":196792019}' >day_2.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":181115208}' >day_3.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":152115810}' >day_4.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":172548507}' >day_5.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":204846845}' >day_6.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":200801003}' >day_7.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":193772492}' >day_8.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":198424372}' >day_9.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":185778055}' >day_10.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":153588700}' >day_11.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":169003364}' >day_12.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":194216520}' >day_13.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":194081279}' >day_14.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":187154596}' >day_15.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":177984934}' >day_16.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":163382602}' >day_17.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":142061091}' >day_18.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":156534237}' >day_19.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":193627464}' >day_20.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":192215183}' >day_21.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":189747893}' >day_22.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":178274637}' >day_23.mtd


echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":395405518}' >days_1_1.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":592197537}' >days_1_2.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":773312745}' >days_1_3.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":925428555}' >days_1_4.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":1097977062}' >days_1_5.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":1302823907}' >days_1_6.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":1503624910}' >days_1_7.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":1697397402}' >days_1_8.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":1895821774}' >days_1_9.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":2081599829}' >days_1_10.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":2235188529}' >days_1_11.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":2404191893}' >days_1_12.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":2598408413}' >days_1_13.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":2792489692}' >days_1_14.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":2979644288}' >days_1_15.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":3157629222}' >days_1_16.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":3321011824}' >days_1_17.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":3463072915}' >days_1_18.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":3619607152}' >days_1_19.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":3813234616}' >days_1_20.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":4005449799}' >days_1_21.mtd
echo '{"data_type":"frame","format":"csv","sep":"	","header":false,"cols":40,"rows":4195197692}' >days_1_21.mtd

cd ../../
wait



