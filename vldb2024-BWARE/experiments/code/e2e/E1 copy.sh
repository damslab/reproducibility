# Read Compressed matrix vs read binary matrix into algrotihm

logstart="results/e2e"
SYSTEMDS_STANDALONE_OPTS_BASE="$SYSTEMDS_STANDALONE_OPTS"

echo "code/e2e/E1.sh"

run() {
    alg=$1
    conf="code/conf/$2.xml"
    mode=$3

    shift 3

    logDir="$logstart/$alg/$conf/$mode/$HOSTNAME"
    mkdir -p "$logDir/perf"

    IFS="_"
    lname="$*"
    lname="${lname//'/'/'-'}"
    log="$logDir/$lname.log"
    profile="$logDir/perf/$lname.html"
    IFS=" "
    echo $log $alg $conf $mode
    export SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE -agentpath:$HOME/Programs/profiler/lib/libasyncProfiler.so=start,event=cpu,file=$profile"

    rm -fr $log

    perf stat -d -d -d \
        systemds \
        code/e2e/$alg.dml \
        -config $conf \
        -stats 100 -debug \
        -exec $mode \
        -seed $seed \
        -args $* \
        >>$log 2>&1
        # -explain \

    export SYSTEMDS_STANDALONE_OPTS="$SYSTEMDS_STANDALONE_OPTS_BASE"
}

# rows=1430000 # Guarantee that we get 1Mil rows.
# rows=14300000 # Guarantee that we get 10Mil rows.
# rows=143000000 # Guarantee that we get 100Mil rows.
# rows=("1430000 14300000 143000000")

# for row in $rows; do
#     for xml in $xmls; do
#         run GenV2 $xml $mode $row 250 0 4 tmp/e2e/X.bin tmp/e2e/Y.bin tmp/e2e/Xt.bin tmp/e2e/Yt.bin binary
#         run GenV2 $xml $mode $row 250 0 4 tmp/e2e/X.cbin tmp/e2e/Y.cbin tmp/e2e/Xt.cbin tmp/e2e/Yt.cbin compressed

#         run PCA $xml $mode tmp/e2e/X.bin $row
#         run PCA $xml $mode tmp/e2e/X.cbin $row
#         run kmeans $xml $mode tmp/e2e/X.bin $row
#         run kmeans $xml $mode tmp/e2e/X.cbin $row
#         run mLogReg $xml $mode tmp/e2e/X.bin tmp/e2e/Y.bin tmp/e2e/Xt.bin tmp/e2e/Yt.bin $row
#         run mLogReg $xml $mode tmp/e2e/X.cbin tmp/e2e/Y.cbin tmp/e2e/Xt.cbin tmp/e2e/Yt.cbin $row
#         run L2SVM $xml $mode tmp/e2e/X.bin tmp/e2e/Y.bin tmp/e2e/Xt.bin tmp/e2e/Yt.bin $row
#         run L2SVM $xml $mode tmp/e2e/X.cbin tmp/e2e/Y.cbin tmp/e2e/Xt.cbin tmp/e2e/Yt.cbin $row
#         run lmCG $xml $mode tmp/e2e/X.bin tmp/e2e/Y.bin tmp/e2e/Xt.bin tmp/e2e/Yt.bin 3 $row
#         run lmCG $xml $mode tmp/e2e/X.cbin tmp/e2e/Y.cbin tmp/e2e/Xt.cbin tmp/e2e/Yt.cbin 3 $row
#         run lmDS $xml $mode tmp/e2e/X.bin tmp/e2e/Y.bin tmp/e2e/Xt.bin tmp/e2e/Yt.bin 3 $row
#         run lmDS $xml $mode tmp/e2e/X.cbin tmp/e2e/Y.cbin tmp/e2e/Xt.cbin tmp/e2e/Yt.cbin 3 $row

#     done
# done
# mode="hybrid"

# xmls=("ULAb1 ULAb16 CLAb1 CLAb16 AWAb1 AWAb16")

spec="code/scripts/specs/adult_spec2.json"
input="data/adult/adult.csv"

# run PCA ULAb1 hybrid $input $spec 
# run PCA ULAb1 hybrid $input $spec -explain
# run PCA ULAb1 singlenode $input $spec
# run PCA CLAb1 hybrid $input $spec -explain
# run PCA CLAb1 singlenode $input $spec -explain
# run PCA ULAb1 singlenode $input $spec -explain
# run PCA TCLAb1 singlenode $input $spec -explain
# run PCA CLAb1 hybrid $input $spec "-explain"
# run PCA AWAb1 hybrid $input $spec 

# run kmeans ULAb1 singlenode $input $spec -explain
# run kmeans CLAb1 singlenode $input $spec -explain
# run kmeans TCLAb1 singlenode $input $spec -explain


input="data/cat/train.csv"
# input="data/cat/train_1.csv"
input2="data/cat/test.csv"
# input2="data/cat/test_1.csv"
spec="code/scripts/specs/catindat_spec1.json"

# run lmDS ULAb1 singlenode $input $spec
spec="code/scripts/specs/catindat_spec2.json"
# run lmDS ULAb1 singlenode $input $spec 
spec="code/scripts/specs/catindat_spec3.json"
# run lmDS ULAb1 singlenode $input $spec 
spec="code/scripts/specs/catindat_specD.json"
# spec="code/scripts/specs/catindat_specNM.json"
# run lmDS ULAb1 singlenode $input $spec $input2 -explain
# run kaggle_lm ULAb1 singlenode $input $spec $input2 300000 catPred.csv
# run kaggle_lm AWAb1 singlenode $input $spec $input2 300000 catPred.csv

# run kaggle_lm ULAb1 singlenode $input $spec $input2 300000 catPred.csv
# run reformat ULAb1 singlenode $input $input.bin binary
# run reformat ULAb1 singlenode $input2 $input2.bin binary
# run kaggle_lm ULAb1 singlenode $input.bin $spec $input2.bin 300000 catPred.csv

# run reformat ULAb1 singlenode $input $input.cla compressed
# run reformat ULAb1 singlenode $input2 $input2.cla compressed
# run kaggle_lm ULAb1 singlenode $input.cla $spec $input2.cla 300000 catPred.csv


# run kaggle_lm TCLAb1 singlenode $input $spec $input2 300000 catPred.csv
# run kaggle_wlm ULAb1 singlenode $input $spec $input2 300000 catPred.csv
# run kaggle_l2svm ULAb1 singlenode $input $spec $input2 300000 catPred.csv
# run kaggle_glm ULAb1 singlenode $input $spec $input2 300000 catPred.csv
# run kaggle_mlg ULAb1 singlenode $input $spec $input2 300000 catPred.csv
# run kaggle_lasso ULAb1 singlenode $input $spec $input2 300000 catPred.csv
# run kaggle_ensemble_lm ULAb1 singlenode $input $spec $input2 300000 catPred.csv


input="data/softdefect/train.csv"
input2="data/softdefect/test.csv"
spec="code/scripts/specs/softdefect_spec1.json"
# run kaggle_lm ULAb1 singlenode $input $spec $input2 101763 softPred.csv
# run kaggle_lasso ULAb1 singlenode $input $spec $input2 101763 softPred.csv
# run kaggle_mlg ULAb1 singlenode $input $spec $input2 101763 softPred.csv
# run kaggle_l2svm ULAb1 singlenode $input $spec $input2 101763 softPred.csv
# run kaggle_glm ULAb1 singlenode $input $spec $input2 101763 softPred.csv
spec="code/scripts/specs/softdefect_spec2.json"
# run kaggle_decisionTree ULAb1 singlenode $input $spec $input2 101763 softPred.csv
# run kaggle_decisionTree TCLAb1 singlenode $input $spec $input2 101763 softPred.csv
# run kaggle_randomForest ULAb1 singlenode $input $spec $input2 101763 softPred.csv
# run kaggle_randomForest TCLAb1 singlenode $input $spec $input2 101763 softPred.csv


input="data/criteo/day_0_1000.tsv"
input="data/criteo/day_0_10000.tsv"
input2="data/criteo/day_23_10000.tsv"
# spec="code/scripts/specs/criteo_fe2.json"
spec="code/scripts/specs/criteo_full.json"
# spec="code/scripts/specs/criteo_Hash100.json"
# input="data/criteo/day_0_1000000.tsv"
# input="data/criteo/day_0_3000000.tsv"
# input="data/criteo/day_0_10000000.tsv"

# run reformat ULAb1 singlenode $input $input.bin binary
# run reformat ULAb1 singlenode $input2 $input2.bin binary

# run criteo_lm ULAb1 singlenode $input $spec $input2 CritPred
# run criteo_lm TCLAb1 singlenode $input $spec $input2 CritPred
# run criteo_lm TAWAb1 singlenode $input $spec $input2 CritPred

input="data/criteo/day_0_1000.tsv"

run criteo_kmeans ULAb1 singlenode $input $spec
run criteo_kmeans TULAb1 singlenode $input $spec
run criteo_kmeans TCLAb1 singlenode $input $spec
run criteo_kmeans TAWAb1 singlenode $input $spec

run criteo_kmeans10 ULAb1 singlenode $input $spec
run criteo_kmeans10 TULAb1 singlenode $input $spec
run criteo_kmeans10 TCLAb1 singlenode $input $spec
run criteo_kmeans10 TAWAb1 singlenode $input $spec

input="data/criteo/day_0_10000.tsv"

# run criteo_pca ULAb1 singlenode $input code/scripts/specs/criteo_fe3.json
# run criteo_pca TULAb1 singlenode $input code/scripts/specs/criteo_fe3.json
# run criteo_pca TCLAb1 singlenode $input code/scripts/specs/criteo_fe3.json
# run criteo_pca TAWAb1 singlenode $input code/scripts/specs/criteo_fe3.json

run criteo_kmeans ULAb1 singlenode $input $spec
run criteo_kmeans TULAb1 singlenode $input $spec
run criteo_kmeans TCLAb1 singlenode $input $spec
run criteo_kmeans TAWAb1 singlenode $input $spec

run criteo_kmeans10 ULAb1 singlenode $input $spec
run criteo_kmeans10 TULAb1 singlenode $input $spec
run criteo_kmeans10 TCLAb1 singlenode $input $spec
run criteo_kmeans10 TAWAb1 singlenode $input $spec

input="data/criteo/day_0_100000.tsv"


# run criteo_pca ULAb1 singlenode $input code/scripts/specs/criteo_Hash100.json
# run criteo_pca TULAb1 singlenode $input code/scripts/specs/criteo_Hash100.json
# run criteo_pca TCLAb1 singlenode $input code/scripts/specs/criteo_Hash100.json
# run criteo_pca TAWAb1 singlenode $input code/scripts/specs/criteo_Hash100.json

# run criteo_pca ULAb1 singlenode $input $spec
# run criteo_pca TULAb1 singlenode $input $spec
# run criteo_pca TCLAb1 singlenode $input $spec
# run criteo_pca TAWAb1 singlenode $input $spec

run criteo_kmeans ULAb1 singlenode $input $spec
run criteo_kmeans TULAb1 singlenode $input $spec
run criteo_kmeans TCLAb1 singlenode $input $spec
run criteo_kmeans TAWAb1 singlenode $input $spec

run criteo_kmeans10 ULAb1 singlenode $input $spec
run criteo_kmeans10 TULAb1 singlenode $input $spec
run criteo_kmeans10 TCLAb1 singlenode $input $spec
run criteo_kmeans10 TAWAb1 singlenode $input $spec


input="data/criteo/day_0_300000.tsv"

run criteo_kmeans ULAb1 singlenode $input $spec
run criteo_kmeans TULAb1 singlenode $input $spec
run criteo_kmeans TCLAb1 singlenode $input $spec
run criteo_kmeans TAWAb1 singlenode $input $spec

run criteo_kmeans10 ULAb1 singlenode $input $spec
run criteo_kmeans10 TULAb1 singlenode $input $spec
run criteo_kmeans10 TCLAb1 singlenode $input $spec
run criteo_kmeans10 TAWAb1 singlenode $input $spec

input="data/criteo/day_0_1000000.tsv"

run criteo_kmeans ULAb1 singlenode $input $spec
run criteo_kmeans TULAb1 singlenode $input $spec
run criteo_kmeans TCLAb1 singlenode $input $spec
run criteo_kmeans TAWAb1 singlenode $input $spec

run criteo_kmeans10 ULAb1 singlenode $input $spec
run criteo_kmeans10 TULAb1 singlenode $input $spec
run criteo_kmeans10 TCLAb1 singlenode $input $spec
run criteo_kmeans10 TAWAb1 singlenode $input $spec

input="data/criteo/day_0_3000000.tsv"

# run criteo_pca ULAb1 singlenode $input code/scripts/specs/criteo_Hash100.json
# run criteo_pca TULAb1 singlenode $input code/scripts/specs/criteo_Hash100.json
# run criteo_pca TCLAb1 singlenode $input code/scripts/specs/criteo_Hash100.json
# run criteo_pca TAWAb1 singlenode $input code/scripts/specs/criteo_Hash100.json

run criteo_kmeans ULAb1 singlenode $input $spec
run criteo_kmeans TULAb1 singlenode $input $spec
run criteo_kmeans TCLAb1 singlenode $input $spec
run criteo_kmeans TAWAb1 singlenode $input $spec

run criteo_kmeans10 ULAb1 singlenode $input $spec
run criteo_kmeans10 TULAb1 singlenode $input $spec
run criteo_kmeans10 TCLAb1 singlenode $input $spec
run criteo_kmeans10 TAWAb1 singlenode $input $spec

input="data/criteo/day_0_10000000.tsv"

run criteo_kmeans ULAb1 singlenode $input $spec
run criteo_kmeans TULAb1 singlenode $input $spec
run criteo_kmeans TCLAb1 singlenode $input $spec
run criteo_kmeans TAWAb1 singlenode $input $spec

run criteo_kmeans10 ULAb1 singlenode $input $spec
run criteo_kmeans10 TULAb1 singlenode $input $spec
run criteo_kmeans10 TCLAb1 singlenode $input $spec
run criteo_kmeans10 TAWAb1 singlenode $input $spec

input="data/criteo/day_0_30000000.tsv"

run criteo_kmeans ULAb1 singlenode $input $spec
run criteo_kmeans TULAb1 singlenode $input $spec
run criteo_kmeans TCLAb1 singlenode $input $spec
run criteo_kmeans TAWAb1 singlenode $input $spec

run criteo_kmeans10 ULAb1 singlenode $input $spec
run criteo_kmeans10 TULAb1 singlenode $input $spec
run criteo_kmeans10 TCLAb1 singlenode $input $spec
run criteo_kmeans10 TAWAb1 singlenode $input $spec


input="data/criteo/day_0_100000000.tsv"

run criteo_kmeans ULAb1 singlenode $input $spec
run criteo_kmeans TULAb1 singlenode $input $spec
run criteo_kmeans TCLAb1 singlenode $input $spec
run criteo_kmeans TAWAb1 singlenode $input $spec

run criteo_kmeans10 ULAb1 singlenode $input $spec
run criteo_kmeans10 TULAb1 singlenode $input $spec
run criteo_kmeans10 TCLAb1 singlenode $input $spec
run criteo_kmeans10 TAWAb1 singlenode $input $spec

input="data/criteo/day_0"

run criteo_kmeans ULAb1 singlenode $input $spec
run criteo_kmeans TULAb1 singlenode $input $spec
run criteo_kmeans TCLAb1 singlenode $input $spec
run criteo_kmeans TAWAb1 singlenode $input $spec

run criteo_kmeans10 ULAb1 singlenode $input $spec
run criteo_kmeans10 TULAb1 singlenode $input $spec
run criteo_kmeans10 TCLAb1 singlenode $input $spec
run criteo_kmeans10 TAWAb1 singlenode $input $spec

# run PCA ULAb1 singlenode $input $spec -explain

# run kmeans ULAb1 singlenode $input $spec
# run kmeans CLAb1 singlenode $input $spec 
# run kmeans TCLAb1 singlenode $input $spec


spec="code/scripts/specs/criteo_fe3.json"

# run kmeans ULAb1 singlenode $input $spec
# run kmeans TCLAb1 singlenode $input $spec




spec="code/scripts/specs/kdd_spec1.json"
input="data/kdd98/cup98val.csv"

## not really working pca with this many columns.
# run PCA ULAb1 singlenode $input $spec -explain
# run PCA TCLAb1 singlenode $input $spec -explain




spec="code/scripts/specs/santander_spec2.json"
input="data/santander/train.csv"

# run PCA ULAb1 singlenode $input $spec -explain
# run PCA CLAb1 singlenode $input $spec -explain
# run PCA TCLAb1 singlenode $input $spec -explain
