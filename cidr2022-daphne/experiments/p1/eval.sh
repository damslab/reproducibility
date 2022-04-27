#!/bin/bash

# TODO More reasonable script verbosity.

#******************************************************************************
# Utility functions
#******************************************************************************

function print_help () {
    # TODO Use the real defaults (as defined before the argument parsing) here.
    echo "Usage: $0 [-h] [-q QUERY] [-s STEP] [-e STEP] [-sf N] [-r N] [--withoutDaphne] [--withoutMDBTF]"
    echo ""
    echo "Optional arguments:"
    echo "  -h, --help         Print this help message and exit."
    echo "  -q, --queryNo      The query variant to execute, default: 'a'."
    echo "  -s, --start        The start step of the experiments, default: 'setup'."
    echo "  -e, --end          The end step of the experiments, default: 'run'."
    echo "  -sf, --scaleFactor The TPC-H scale factor, default: 1."
    echo "  -r, --repetitions  The number of repetitions of all time measurements, default: 3."
    echo "  --withoutDaphne    Don't use Daphne, default: use it."
    echo "  --withoutMDBTF     Don't use MonetDB+TensorFlow, default: use it."
    echo ""
    echo "Steps:"
    echo "  s, setup:    Download, build, install things."
    echo "  g, generate: Generate, preprocess, load TPC-H data."
    echo "  r, run:      Execute pipelines in Daphne and MonetDB+TensorFlow."
    echo ""
    echo "Queries:"
    echo "  a: Returns customers plus aggregate on orders."
    echo "  b: Returns orders plus aggregate on lineitem."
}

function print_headline1 () {
    echo "################################################################"
    echo "# $1"
    echo "################################################################"
}

function print_headline2 () {
    echo "================================================================"
    echo "= $1"
    echo "================================================================"
}

#******************************************************************************
# Functions for the individual steps
#******************************************************************************

function setup () {
    print_headline1 "Setup Step"

    set -e

    cd $pathRoot

    mkdir --parents $pathSoftware

    print_headline2 "Downloading and compiling the TPC-H data generator"
    
    git clone https://github.com/electrum/tpch-dbgen.git $pathDBGen
    cd $pathDBGen
    make -j
    cd $pathRoot

    if [[ $useMDBTF ]]
    then
        print_headline2 "Downloading and compiling MonetDB"
        
        mkdir $pathMonetDB
        cd $pathMonetDB

        local versionMonetDB=11.39.17
        local fileMonetDB=MonetDB-$versionMonetDB.tar.bz2
        wget https://www.monetdb.org/downloads/sources/archive/$fileMonetDB
        tar -xvjf $fileMonetDB
        
        local pathMonetDBBuild=$pathMonetDB/MonetDB-$versionMonetDB/build
        mkdir --parents $pathMonetDBBuild
        cd $pathMonetDBBuild
        
        # TODO Think about the right flags again.
        cmake -DCMAKE_INSTALL_PREFIX=$pathMonetDBInstalled \
              -DASSERT=OFF -DSTRICT=OFF ..
        cmake --build .
        cmake --build . --target install
        
        cd $pathRoot
        
        printf "user=monetdb\npassword=monetdb" > $pathDotMonetDBFile
        
        eval $monetdbd create $pathMonetDBFarm
    fi

    set +e

    print_headline1 "Done"
}

function load_data_into_monetdb () {
    eval $monetdb create $dbName
    eval $monetdb release $dbName

    # TODO This crashes: bug in MonetDB?
#    # Set MonetDB to read-only execution, just like Daphne.
#    eval $monetdb set readonly=yes $dbName

    # For efficient bulk insert, we follow the guidelines provided at:
    # - [https://www.monetdb.org/Documentation/SQLReference/DataManipulation/BulkInputOutput]
    # - [https://www.monetdb.org/Documentation/ServerAdministration/LoadingBulkData]
    # In particular:
    # - Provide an upper bound of the number of records in the CSV files.
    # - Don't use PK constraint during bulk insert, add it afterwards.
    # - Use minimal optimizer pipeline during bulk insert.

    local customerFile=$pathData/customer.csv
    local ordersFile=$pathData/orders.csv
    local lineitemFile=$pathData/lineitem.csv
    local sql="\
        CREATE SCHEMA $benchmark;\
        SET SCHEMA $benchmark;\
        \
        SET sys.optimizer = 'minimal_pipe';\
        \
        CREATE TABLE customer (\
            C_CUSTKEY    BIGINT,\
            C_NAME       BIGINT,\
            C_ADDRESS    BIGINT,\
            C_NATIONKEY  BIGINT,\
            C_PHONE      BIGINT,\
            C_ACCTBAL    DOUBLE,\
            C_MKTSEGMENT BIGINT,\
            C_COMMENT    BIGINT\
        );\
        COPY $(($scaleFactor * 150000)) RECORDS\
          INTO customer FROM '$customerFile' USING DELIMITERS ',','\\n';\
        ALTER TABLE customer ADD PRIMARY KEY (C_CUSTKEY);\
        \
        CREATE TABLE orders (\
            O_ORDERKEY      BIGINT,\
            O_CUSTKEY       BIGINT,\
            O_ORDERSTATUS   BIGINT,\
            O_TOTALPRICE    DOUBLE,\
            O_ORDERDATE     BIGINT,\
            O_ORDERPRIORITY BIGINT,\
            O_CLERK         BIGINT,\
            O_SHIPPRIORITY  BIGINT,\
            O_COMMENT       BIGINT\
        );\
        COPY $(($scaleFactor * 1500000)) RECORDS\
          INTO orders FROM '$ordersFile' USING DELIMITERS ',','\\n';\
        ALTER TABLE orders ADD PRIMARY KEY (O_ORDERKEY);";
    if [[ $queryNo = b ]]
    then
        # Note that we over-estimate the number of rows, since it is, by
        # definition, approximate.
        local sql="$sql\
            CREATE TABLE lineitem (\
                L_ORDERKEY      BIGINT,\
                L_PARTKEY       BIGINT,\
                L_SUPPKEY       BIGINT,\
                L_LINENUMBER    BIGINT,\
                L_QUANTITY      BIGINT,\
                L_EXTENDEDPRICE DOUBLE,\
                L_DISCOUNT      DOUBLE,\
                L_TAX           DOUBLE,\
                L_RETURNFLAG    BIGINT,\
                L_LINESTATUS    BIGINT,\
                L_SHIPDATE      BIGINT,\
                L_COMMITDATE    BIGINT,\
                L_RECEIPTDATE   BIGINT,\
                L_SHIPINSTRUCT  BIGINT,\
                L_SHIPMODE      BIGINT,\
                L_COMMENT       BIGINT\
            );\
            COPY $(($scaleFactor * 6100000)) RECORDS\
              INTO lineitem FROM '$lineitemFile' USING DELIMITERS ',','\\n';"
    fi
    local sql="$sql\
        SET sys.optimizer = 'default_pipe';"

    echo $sql | $mclient -d $dbName
}

function generate () {
    print_headline1 "Generate Step"

    set -e

    cd $pathRoot

    mkdir --parents $pathData

    print_headline2 "TPC-H data generation"
    cd $pathDBGen
    ./dbgen -f -s $scaleFactor -T O # orders
    ./dbgen -f -s $scaleFactor -T c # customer
    mv orders.tbl $pathData
    mv customer.tbl $pathData
    if [[ $queryNo = b ]]
    then
        ./dbgen -f -s $scaleFactor -T L # lineitem
        mv lineitem.tbl $pathData
    fi
    cd $pathRoot

    print_headline2 "TPC-H data pre-processing"
    $pathScripts/preprocess.py $pathData $queryNo

    # TODO do that?
    # print_headline2 "Deleting original .tbl-files"

    set +e

    print_headline1 "Done"
}

function run_p1_daphne () {
    $daphnec $pathScripts/p1-$queryNo.daphne --args \
             inCustomer="\"$pathData/customer.csv\"" \
             inOrders="\"$pathData/orders.csv\"" \
             inLineitem="\"$pathData/lineitem.csv\"" \
             mktSegUpper=$mktSegUpper \
             orderDateLower=$orderDateLower \
             > $pathFinalResDaphne \
             2> $pathTmp1
}

function run_p1q_mdb () {
    # Group by all customer columns. Internally, MonetDB only groups by
    # the primary key C_CUSTKEY (I verified that in the MAL plan).
    if [[ $queryNo = a ]]
    then
        local query="\
            SET SCHEMA $benchmark;\
            COPY\
                SELECT c.*, SUM(O_TOTALPRICE)\
                FROM customer c, orders\
                WHERE C_CUSTKEY = O_CUSTKEY\
                  AND C_MKTSEGMENT <= $mktSegUpper\
                  AND O_ORDERDATE >= $orderDateLower\
                GROUP BY\
                  C_CUSTKEY, C_NAME, C_ADDRESS, C_NATIONKEY, C_PHONE, C_ACCTBAL,\
                  C_MKTSEGMENT, C_COMMENT\
            INTO '$1'\
            USING DELIMITERS ',', '\\n';"
    elif [[ $queryNo = b ]]
    then
        local query="\
            SET SCHEMA $benchmark;\
            COPY\
                SELECT o.*, SUM(L_EXTENDEDPRICE)\
                FROM orders o, lineitem, customer\
                WHERE O_ORDERKEY = L_ORDERKEY\
                  AND C_CUSTKEY = O_CUSTKEY\
                  AND C_MKTSEGMENT <= $mktSegUpper\
                  AND O_ORDERDATE >= $orderDateLower\
                GROUP BY O_ORDERKEY, O_CUSTKEY, O_ORDERSTATUS, O_TOTALPRICE,\
                  O_ORDERDATE, O_ORDERPRIORITY, O_CLERK, O_SHIPPRIORITY,\
                  O_COMMENT\
            INTO '$1'\
            USING DELIMITERS ',', '\\n';"
    fi

    local start=$(timepoint)
    echo $query | $mclient -d $dbName -f $2 > /dev/null
    local end=$(timepoint)
    printf "\t$((end - start))" > $3
}

function run_p1_mdbtf () {
    run_p1q_mdb $1 csv $pathTmp1
    eval $pathScripts/p1.py $queryNo train _ _ _ _ $1 $2 999 999 2>> $pathTmp1
}

function run_p1_py_stored () {
    local queryEngine=$1
    local pathQueryRes=$2
    local pathFinalRes=$3
    eval $pathScripts/p1.py $queryNo query $queryEngine \
        $pathData/customer.csv $pathData/orders.csv $pathData/lineitem.csv \
        $pathQueryRes _ $mktSegUpper $orderDateLower \
        2> $pathTmp1
    eval $pathScripts/p1.py $queryNo train _ \
        _ _ _ \
        $pathQueryRes $pathFinalRes 999 999 \
        2> $pathTmp2
}

function run_p1_py_direct () {
    local queryEngine=$1
    local pathFinalRes=$2
    eval $pathScripts/p1.py $queryNo both $queryEngine \
        $pathData/customer.csv $pathData/orders.csv $pathData/lineitem.csv \
        _ $pathFinalRes $mktSegUpper $orderDateLower \
        2> $pathTmp1
}

function timepoint () {
    date +%s%N
}

function start_monetdb_daemon () {
    printf "Starting MonetDB daemon... " >&2
    eval $monetdbd start $pathMonetDBFarm
    printf "done.\n" >&2
}

function stop_monetdb_daemon () {
    printf "Stopping MonetDB daemon... " >&2
    eval $monetdbd stop $pathMonetDBFarm
    printf "done.\n" >&2
}

function delete_db_in_monetdb_if () {
    set +e # continue if destruction fails
    eval $monetdb destroy -f $dbName
    set -e
}

function set_monetdb_db_flags () {
    eval $monetdb stop $dbName

    # TODO Change to multi-threaded.
    # Set MonetDB to single-threaded execution, just like Daphne (currently).
    eval $monetdb set nthreads=1 $dbName
    # Set MonetDB to read-only execution, just like Daphne.
    eval $monetdb set readonly=yes $dbName

    eval $monetdb start $dbName
}

function run_mdb_tmptbl () {
    local format=$1
    local pathQueryRes=$2
    local pathTmp=$3

    $monetdb create $dbName
    $monetdb release $dbName
    eval $monetdb set nthreads=1 $dbName
    # eval $monetdb set readonly=yes $dbName
    eval $monetdb start $dbName

    local customerFile=$pathData/customer.csv
    local ordersFile=$pathData/orders.csv
    local lineitemFile=$pathData/lineitem.csv
    local sql="\
        SET sys.optimizer = 'minimal_pipe';\
        \
        CREATE TEMPORARY TABLE customer (\
            C_CUSTKEY    BIGINT PRIMARY KEY,\
            C_NAME       BIGINT,\
            C_ADDRESS    BIGINT,\
            C_NATIONKEY  BIGINT,\
            C_PHONE      BIGINT,\
            C_ACCTBAL    DOUBLE,\
            C_MKTSEGMENT BIGINT,\
            C_COMMENT    BIGINT\
        ) ON COMMIT PRESERVE ROWS;\
        COPY $(($scaleFactor * 150000)) RECORDS\
          INTO customer FROM '$customerFile' USING DELIMITERS ',','\\n';\
        \
        CREATE TEMPORARY TABLE orders (\
            O_ORDERKEY      BIGINT PRIMARY KEY,\
            O_CUSTKEY       BIGINT,\
            O_ORDERSTATUS   BIGINT,\
            O_TOTALPRICE    DOUBLE,\
            O_ORDERDATE     BIGINT,\
            O_ORDERPRIORITY BIGINT,\
            O_CLERK         BIGINT,\
            O_SHIPPRIORITY  BIGINT,\
            O_COMMENT       BIGINT\
        ) ON COMMIT PRESERVE ROWS;\
        COPY $(($scaleFactor * 1500000)) RECORDS\
          INTO orders FROM '$ordersFile' USING DELIMITERS ',','\\n';";
    if [[ $queryNo = b ]]
    then
        # Note that we over-estimate the number of rows, since it is, by
        # definition, approximate.
        local sql="$sql\
            CREATE TEMPORARY TABLE lineitem (\
                L_ORDERKEY      BIGINT,\
                L_PARTKEY       BIGINT,\
                L_SUPPKEY       BIGINT,\
                L_LINENUMBER    BIGINT,\
                L_QUANTITY      BIGINT,\
                L_EXTENDEDPRICE DOUBLE,\
                L_DISCOUNT      DOUBLE,\
                L_TAX           DOUBLE,\
                L_RETURNFLAG    BIGINT,\
                L_LINESTATUS    BIGINT,\
                L_SHIPDATE      BIGINT,\
                L_COMMITDATE    BIGINT,\
                L_RECEIPTDATE   BIGINT,\
                L_SHIPINSTRUCT  BIGINT,\
                L_SHIPMODE      BIGINT,\
                L_COMMENT       BIGINT\
            ) ON COMMIT PRESERVE ROWS;\
            COPY $(($scaleFactor * 6100000)) RECORDS\
              INTO lineitem FROM '$lineitemFile' USING DELIMITERS ',','\\n';"
    fi
    local sql="$sql\
        SET sys.optimizer = 'default_pipe';"

    if [[ $queryNo = a ]]
    then
        local sql="$sql\
            COPY\
                SELECT c.*, SUM(O_TOTALPRICE)\
                FROM tmp.customer c, tmp.orders\
                WHERE C_CUSTKEY = O_CUSTKEY\
                  AND C_MKTSEGMENT <= $mktSegUpper\
                  AND O_ORDERDATE >= $orderDateLower\
                GROUP BY\
                  C_CUSTKEY, C_NAME, C_ADDRESS, C_NATIONKEY, C_PHONE, C_ACCTBAL,\
                  C_MKTSEGMENT, C_COMMENT\
            INTO '$pathQueryResMDBTFTmpTbl'\
            USING DELIMITERS ',', '\\n';"
    elif [[ $queryNo = b ]]
    then
        local sql="$sql\
            COPY\
                SELECT o.*, SUM(L_EXTENDEDPRICE)\
                FROM tmp.orders o, tmp.lineitem, tmp.customer\
                WHERE O_ORDERKEY = L_ORDERKEY\
                  AND C_CUSTKEY = O_CUSTKEY\
                  AND C_MKTSEGMENT <= $mktSegUpper\
                  AND O_ORDERDATE >= $orderDateLower\
                GROUP BY O_ORDERKEY, O_CUSTKEY, O_ORDERSTATUS, O_TOTALPRICE,\
                  O_ORDERDATE, O_ORDERPRIORITY, O_CLERK, O_SHIPPRIORITY,\
                  O_COMMENT\
            INTO '$pathQueryRes'\
            USING DELIMITERS ',', '\\n';"
    fi

    local start=$(timepoint)
    echo $sql | $mclient -d $dbName -f $format > /dev/null
    local end=$(timepoint)
    printf "\t$((end - start))" > $pathTmp
}

function run () {
    print_headline1 "Run Step"
    echo "mktSegUpper: $mktSegUpper, orderDateLower: $orderDateLower"

    set -e

    cd $pathRoot

    local params=msu${mktSegUpper}_odl${orderDateLower}
    local nameDaphne=Daphne_$params
    local nameMDBTFPreloaded=MDBTF_preloaded_$params
    local nameMDBTFScratch=MDBTF_scratch_$params
    local nameMDBTFTmpTbl=MDBTF_tmptbl_$params
    local namePDTFStored=PDTF_stored_$params
    local namePDTFDirect=PDTF_direct_$params
    local nameDDBTFStored=DDBTF_stored_$params
    local nameDDBTFDirect=DDBTF_direct_$params

    mkdir --parents $pathResults
    local pathFinalResDaphne=$pathResults/final_$nameDaphne.csv
    local pathQueryResMDBTFPreloaded=$pathResults/query_$nameMDBTFPreloaded.csv
    local pathFinalResMDBTFPreloaded=$pathResults/final_$nameMDBTFPreloaded.csv
    local pathQueryResMDBTFScratch=$pathResults/query_$nameMDBTFScratch.csv
    local pathFinalResMDBTFScratch=$pathResults/final_$nameMDBTFScratch.csv
    local pathQueryResMDBTFTmpTbl=$pathResults/query_$nameMDBTFTmpTbl.csv
    local pathFinalResMDBTFTmpTbl=$pathResults/final_$nameMDBTFTmpTbl.csv
    local pathQueryResPDTFStored=$pathResults/query_$namePDTFStored.csv
    local pathFinalResPDTFStored=$pathResults/final_$namePDTFStored.csv
    local pathFinalResPDTFDirect=$pathResults/final_$namePDTFDirect.csv
    local pathQueryResDDBTFStored=$pathResults/query_$nameDDBTFStored.csv
    local pathFinalResDDBTFStored=$pathResults/final_$nameDDBTFStored.csv
    local pathFinalResDDBTFDirect=$pathResults/final_$nameDDBTFDirect.csv

    mkdir --parents $pathRuntimes
    local pathRuntimeDaphne=$pathRuntimes/$nameDaphne.csv
    local pathRuntimeMDBTFPreloaded=$pathRuntimes/$nameMDBTFPreloaded.csv
    local pathRuntimeMDBTFScratch=$pathRuntimes/$nameMDBTFScratch.csv
    local pathRuntimeMDBTFTmpTbl=$pathRuntimes/$nameMDBTFTmpTbl.csv
    local pathRuntimePDTFStored=$pathRuntimes/$namePDTFStored.csv
    local pathRuntimePDTFDirect=$pathRuntimes/$namePDTFDirect.csv
    local pathRuntimeDDBTFStored=$pathRuntimes/$nameDDBTFStored.csv
    local pathRuntimeDDBTFDirect=$pathRuntimes/$nameDDBTFDirect.csv
    local header="system\trepIdx\truntime [ns]"

    # Since DAPHNE uses OpenBLAS, but we want to use DAPHNE single-threaded or
    # with its built-in multi-threading here.
    export OPENBLAS_NUM_THREADS=1

    # Such that TensorFlow does not use CUDA/GPU.
    export CUDA_VISIBLE_DEVICES=""

    if [[ $useDaphne ]]
    then
        # ---------------------------------------------------------------------
        # Pipeline P1 in Daphne
        # ---------------------------------------------------------------------
        print_headline2 "Running pipeline P1 in Daphne"

        printf "$header\truntime load [ns]\truntime query [ns]\truntime cast [ns]\truntime train+save [ns]\n" > $pathRuntimeDaphne

        cd $pathDaphne

        for repIdx in $(seq $repetitions)
        do
            printf "repetition $repIdx... "

            local start=$(timepoint)
            run_p1_daphne
            local end=$(timepoint)

            printf "Daphne\t$repIdx\t$(($end - $start))$(<$pathTmp1)\n" >> $pathRuntimeDaphne

            printf "done.\n"
        done
        cd $pathRoot
    fi

    if [[ $useMDBTF ]]
    then
#        # ---------------------------------------------------------------------
#        # Pipeline P1 in MonetDB + TensorFlow (pre-loaded data)
#        # ---------------------------------------------------------------------
#
#        print_headline2 "Running pipeline P1 in MonetDB+TensorFlow (pre-loaded data)"
#
#        printf "$header\truntime load+query [ns]\truntime load+query+isave [ns]\truntime pyload1 [s]\truntime pyload2 [s]\truntime iload [s]\truntime cast [s]\truntime train+save [s]\n" > $pathRuntimeMDBTFPreloaded
#
#        start_monetdb_daemon
#        delete_db_in_monetdb_if
#        load_data_into_monetdb
#        set_monetdb_db_flags
#
#        # Warm up MonetDB by executing the query a couple of times.
#        for repIdx in $(seq 3)
#        do
#            # Ensure that MonetDB does not complain about exisiting file.
#            rm -f $pathQueryResMDBTFPreloaded
#
#            run_p1_mdbtf $pathQueryResMDBTFPreloaded $pathFinalResMDBTFPreloaded
#        done
#
#        for repIdx in $(seq $repetitions)
#        do
#            printf "repetition $repIdx... "
#
#            # Ensure that MonetDB does not complain about exisiting file.
#            rm -f $pathQueryResMDBTFPreloaded
#
#            local start=$(timepoint)
#            run_p1_mdbtf $pathQueryResMDBTFPreloaded $pathFinalResMDBTFPreloaded
#            local end=$(timepoint)
#
#            # Ensure that MonetDB does not complain about exisiting file.
#            rm -f $pathQueryResMDBTFPreloaded
#
#            # Measure the runtime without producing a result output.
#            run_p1q_mdb $pathQueryResMDBTFPreloaded trash $pathTmp2
#
#            printf "MonetDB+TF (pre-loaded data)\t$repIdx\t$(($end - $start))$(<$pathTmp2)$(<$pathTmp1)\n" >> $pathRuntimeMDBTFPreloaded
#
#            printf "done.\n"
#        done
#        
#        stop_monetdb_daemon

#        # ---------------------------------------------------------------------
#        # Pipeline P1 in MonetDB + TensorFlow (from scratch)
#        # ---------------------------------------------------------------------
#
#        print_headline2 "Running pipeline P1 in MonetDB+TensorFlow (from scratch)"
#
#        printf "$header\truntime createdb [ns]\truntime load+query [ns]\truntime load+query+isave [ns]\truntime pyload1 [s]\truntime pyload2 [s]\truntime iload [s]\truntime cast [s]\truntime train+save [s]\n" > $pathRuntimeMDBTFScratch
#
#        start_monetdb_daemon
#        delete_db_in_monetdb_if
#
#        for repIdx in $(seq $repetitions)
#        do
#            printf "repetition $repIdx... "
#
#            # Ensure that MonetDB does not complain about exisiting file.
#            rm -f $pathQueryResMDBTFScratch
#
#            local start=$(timepoint)
#
#            local startCreate=$(timepoint)
#            load_data_into_monetdb
#            local endCreate=$(timepoint)
#            set_monetdb_db_flags
#            run_p1_mdbtf $pathQueryResMDBTFScratch $pathFinalResMDBTFScratch
#
#            local end=$(timepoint)
#
#            # Ensure that MonetDB does not complain about exisiting file.
#            rm -f $pathQueryResMDBTFScratch
#
#            # Measure the runtime without producing a result output.
#            run_p1q_mdb $pathQueryResMDBTFScratch trash $pathTmp2
#
#            delete_db_in_monetdb_if
#
#            printf "MonetDB+TF (from scratch)\t$repIdx\t$(($end - $start))\t$(($endCreate - $startCreate))$(<$pathTmp2)$(<$pathTmp1)\n" >> $pathRuntimeMDBTFScratch
#
#            printf "done.\n"
#        done
#
#        stop_monetdb_daemon

        # ---------------------------------------------------------------------
        # Pipeline P1 in MonetDB + TensorFlow (temporary table)
        # ---------------------------------------------------------------------

        print_headline2 "Running pipeline P1 in MonetDB+TensorFlow (temporary table)"

        printf "$header\truntime load+query [ns]\truntime load+query+isave [ns]\truntime pyload1 [s]\truntime pyload2 [s]\truntime iload [s]\truntime cast [s]\truntime train+save [s]\n" > $pathRuntimeMDBTFTmpTbl

        start_monetdb_daemon
        delete_db_in_monetdb_if

        for repIdx in $(seq $repetitions)
        do
            printf "repetition $repIdx... "

            # Ensure that MonetDB does not complain about exisiting file.
            rm -f $pathQueryResMDBTFTmpTbl

            local start=$(timepoint)
            run_mdb_tmptbl csv $pathQueryResMDBTFTmpTbl $pathTmp1
            $pathScripts/p1.py $queryNo train _ _ _ _ $pathQueryResMDBTFTmpTbl $pathFinalResMDBTFTmpTbl 999 999 2>> $pathTmp1
            local end=$(timepoint)

            delete_db_in_monetdb_if

            # Ensure that MonetDB does not complain about exisiting file.
            rm -f $pathQueryResMDBTFTmpTbl

            # Measure the runtime without producing a result output.
            run_mdb_tmptbl trash $pathQueryResMDBTFTmpTbl $pathTmp2

            delete_db_in_monetdb_if

            printf "MonetDB+TF (temporary table)\t$repIdx\t$(($end - $start))$(<$pathTmp2)$(<$pathTmp1)\n" >> $pathRuntimeMDBTFTmpTbl

            printf "done.\n"
        done

        stop_monetdb_daemon

#        # ---------------------------------------------------------------------
#        # Pipeline P1 in Pandas + TensorFlow (stored intermediate)
#        # ---------------------------------------------------------------------
#
#        print_headline2 "Running pipeline P1 in Pandas+TensorFlow (stored intermediate)"
#
#        printf "$header\truntime pyload1a [s]\truntime load [s]\truntime query [s]\truntime isave [s]\truntime pyload1b [s]\truntime pyload2b [s]\truntime iload [s]\truntime cast [s]\truntime train+save [s]\n" > $pathRuntimePDTFStored
#
#        for repIdx in $(seq $repetitions)
#        do
#            printf "repetition $repIdx... "
#
#            local start=$(timepoint)
#            run_p1_py_stored pandas $pathQueryResPDTFStored $pathFinalResPDTFStored
#            local end=$(timepoint)
#
#            printf "Pandas+TF (stored intermediate)\t$repIdx\t$(($end - $start))$(<$pathTmp1)$(<$pathTmp2)\n" >> $pathRuntimePDTFStored
#
#            printf "done.\n"
#        done

        # ---------------------------------------------------------------------
        # Pipeline P1 in Pandas + TensorFlow (direct handover)
        # ---------------------------------------------------------------------

        print_headline2 "Running pipeline P1 in Pandas+TensorFlow (direct handover)"

        printf "$header\truntime pyload1 [s]\truntime pyload2 [s]\truntime load [s]\truntime query [s]\truntime cast [s]\truntime train+save [s]\n" > $pathRuntimePDTFDirect

        for repIdx in $(seq $repetitions)
        do
            printf "repetition $repIdx... "

            local start=$(timepoint)
            run_p1_py_direct pandas $pathFinalResPDTFDirect
            local end=$(timepoint)

            printf "Pandas+TF (direct handover)\t$repIdx\t$(($end - $start))$(<$pathTmp1)\n" >> $pathRuntimePDTFDirect

            printf "done.\n"
        done

#        # ---------------------------------------------------------------------
#        # Pipeline P1 in DuckDB + TensorFlow (stored intermediate)
#        # ---------------------------------------------------------------------
#
#        print_headline2 "Running pipeline P1 in DuckDB+TensorFlow (stored intermediate)"
#
#        printf "$header\truntime pyload1a [s]\truntime pyload2a [s]\truntime load [s]\truntime query [s]\truntime isave [s]\truntime pyload1b [s]\truntime pyload3b [s]\truntime iload [s]\truntime cast [s]\truntime train+save [s]\n" > $pathRuntimeDDBTFStored
#
#        for repIdx in $(seq $repetitions)
#        do
#            printf "repetition $repIdx... "
#
#            local start=$(timepoint)
#            run_p1_py_stored duckdb $pathQueryResDDBTFStored $pathFinalResDDBTFStored
#            local end=$(timepoint)
#
#            printf "DuckDB+TF (stored intermediate)\t$repIdx\t$(($end - $start))$(<$pathTmp1)$(<$pathTmp2)\n" >> $pathRuntimeDDBTFStored
#
#            printf "done.\n"
#        done

        # ---------------------------------------------------------------------
        # Pipeline P1 in DuckDB + TensorFlow (direct handover)
        # ---------------------------------------------------------------------

        print_headline2 "Running pipeline P1 in DuckDB+TensorFlow (direct handover)"

        printf "$header\truntime pyload1 [s]\truntime pyload2 [s]\truntime pyload3 [s]\truntime load [s]\truntime query [s]\truntime cast [s]\truntime train+save [s]\n" > $pathRuntimeDDBTFDirect

        for repIdx in $(seq $repetitions)
        do
            printf "repetition $repIdx... "

            local start=$(timepoint)
            run_p1_py_direct duckdb $pathFinalResDDBTFDirect
            local end=$(timepoint)

            printf "DuckDB+TF (direct handover)\t$repIdx\t$(($end - $start))$(<$pathTmp1)\n" >> $pathRuntimeDDBTFDirect

            printf "done.\n"
        done
    fi

    if [[ $useDaphne ]] && [[ $useMDBTF ]]
    then
        print_headline2 "Comparing results of Daphne and MonetDB+TensorFlow"
        local compare=$pathScripts/compareFinalResult.py

        # We check result values originating from columns that underwent
        # one-hot encoding in the ML part less strictly, because they are more
        # prone to numerical instability.
        if [[ $queryNo = a ]]
        then
            # 2 cols not one-hot-encoded, 1->x25, 2 not, 1->x5, 1 not
            local specialTolerance="$(seq -s , 2 26),$(seq -s , 29 33) 2.0"
        elif [[ $queryNo = b ]]
        then
            # 1 col not one-hot-encoded, 1->x3, 2 not, 1->x5, 3 not
            local specialTolerance="$(seq -s , 1 3),$(seq -s , 6 10) 2.0"
        fi

#        $compare $pathFinalResDaphne $pathFinalResMDBTFPreloaded $specialTolerance
#        $compare $pathFinalResDaphne $pathFinalResMDBTFScratch   $specialTolerance
        $compare $pathFinalResDaphne $pathFinalResMDBTFTmpTbl    $specialTolerance
#        $compare $pathFinalResDaphne $pathFinalResPDTFStored     $specialTolerance
        $compare $pathFinalResDaphne $pathFinalResPDTFDirect     $specialTolerance
#        $compare $pathFinalResDaphne $pathFinalResDDBTFStored    $specialTolerance
        $compare $pathFinalResDaphne $pathFinalResDDBTFDirect    $specialTolerance
    fi

    set +e

    print_headline1 "Done"
}

# *****************************************************************************
# Some configuration
# *****************************************************************************

benchmark=tpch

# -----------------------------------------------------------------------------
# Steps of this script's execution.
# -----------------------------------------------------------------------------

stepSetup=1
stepGenerate=2
stepRun=3
declare -A stepMap=(
    [s]=$stepSetup
    [setup]=$stepSetup
    [g]=$stepGenerate
    [generate]=$stepGenerate
    [r]=$stepRun
    [run]=$stepRun
)

# *****************************************************************************
# Argument parsing
# *****************************************************************************

# -----------------------------------------------------------------------------
# Defaults
# -----------------------------------------------------------------------------

queryNo=a
startStep=$stepSetup
endStep=$stepRun
scaleFactor=1
useDaphne="1"
useMDBTF="1"
repetitions=3

# -----------------------------------------------------------------------------
# Parsing
# -----------------------------------------------------------------------------

while [[ $# -gt 0 ]]
do
    key="$1"
    case $key in
        -h|--help)
            print_help
            exit 0
            ;;
        -q|--queryNo)
            queryNo=$2
            shift
            ;;
        -s|--start)
            if [[ ${stepMap[$2]+_} ]]
            then
                startStep=${stepMap[$2]}
                shift
            else
                printf "unknown step: $2\n"
                exit 1
            fi
            ;;
        -e|--end)
            if [[ ${stepMap[$2]+_} ]]
            then
                endStep=${stepMap[$2]}
                shift
            else
                printf "unknown step: $2\n"
                exit 1
            fi
            ;;
        -sf|--scaleFactor)
            scaleFactor=$2
            shift
            ;;
        -r|--repetitions)
            repetitions=$2
            shift
            ;;
        --withoutDaphne)
            useDaphne=""
            ;;
        --withoutMDBTF)
            useMDBTF=""
            ;;
        *)
            printf "unknown option: $key\n"
            exit 1
            ;;
    esac
    shift
done

# -----------------------------------------------------------------------------
# Validation
# -----------------------------------------------------------------------------

if [[ $startStep -gt $endStep ]]
then
    printf "the start step must not come after the end step\n"
    exit 1
fi

# -----------------------------------------------------------------------------
# Setting some paths
# -----------------------------------------------------------------------------

# Root path of the experiments.
#pathRoot=$(pwd)
pathRoot=$WORK_DIR

# Paths for experimental artifacts.
#pathArtifacts=$pathRoot/artifacts
pathArtifacts=$P1_DATA_DIR
pathData=$pathArtifacts/data_sf$scaleFactor
#pathResults=$pathArtifacts/results_sf${scaleFactor}_q$queryNo
#pathRuntimes=$pathArtifacts/runtimes_sf${scaleFactor}_q$queryNo
pathResults=$P1_RESULTS/results_sf${scaleFactor}_q$queryNo
pathRuntimes=$P1_RESULTS/runtimes_sf${scaleFactor}_q$queryNo
pathTmp1=$pathArtifacts/tmp1.txt
pathTmp2=$pathArtifacts/tmp2.txt

# Path for auxiliary scripts.
#pathScripts=$pathRoot/scripts
pathScripts=$P1_ROOT

# TODO Where should they ideally be, relative to each other?
# Paths related to DAPHNE.
#pathDaphne=$pathRoot/prototype
pathDaphne=$DAPHNE_ROOT
daphnec=$pathDaphne/build/bin/daphnec
if [[ ! -d $pathDaphne ]]
then
    echo "Fatal: Expected $pathDaphne to exist. Consider creating a soft"\
         "link to the directory where your DAPHNE prototype resides."
    exit 1
fi

# Paths related to third-party software.
pathSoftware=$pathRoot/software

# Paths related to the TPC-H data generator.
pathDBGen=$pathSoftware/tpch-dbgen

# Paths related to MonetDB.
pathMonetDB=$pathSoftware/MonetDB
pathMonetDBInstalled=$pathMonetDB/monetdb
monetdbd=$pathMonetDBInstalled/bin/monetdbd
monetdb=$pathMonetDBInstalled/bin/monetdb
mclient=$pathMonetDBInstalled/bin/mclient
pathMonetDBFarm=$pathMonetDB/monetdbfarm
pathDotMonetDBFile=$pathRoot/.monetdb
dbName=${benchmark}_sf${scaleFactor}
if [[ $useMonetDB ]]
then
    export DOTMONETDBFILE=$pathDotMonetDBFile
fi

# *****************************************************************************
# Execution of the selected steps
# *****************************************************************************

if [[ $useMDBTF ]]
then
    # Stop the MonetDB daemon if it is still running.
    stop_monetdb_daemon
fi

if [[ $startStep -le $stepSetup ]] && [[ $stepSetup -le $endStep ]]
then
    setup
fi

if [[ $startStep -le $stepGenerate ]] && [[ $stepGenerate -le $endStep ]]
then
    generate
fi

if [[ $startStep -le $stepRun ]] && [[ $stepRun -le $endStep ]]
then
    # C_MKTSEGMENT has values in the interval [0, 4].
    # O_ORDERDATE has values in the interval [19920101, 19980802].
    if [[ $queryNo = a ]]
    then
        orderDateLower=19950802 # consider the last three years
        for mktSegUpper in 0 2 4 # to vary the query's selectivity
        do
            run
        done
    elif [[ $queryNo = b ]]
    then
        # Varying both predicates to vary the query's selectivity.

        # One market segment, last six months.
        mktSegUpper=0
        orderDateLower=19980202
        run

        # Three market segments, last three years.
        mktSegUpper=2
        orderDateLower=19950802
        run

        # All five market segments, last six years.
        mktSegUpper=4
        orderDateLower=19920802
        run
    fi
fi