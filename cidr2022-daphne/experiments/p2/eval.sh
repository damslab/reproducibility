#!/usr/bin/env bash

TIMESTAMP=$(date --iso-8601)
TIMESTAMP=$TIMESTAMP-$(date +%H%M)

# printf "under construction\n"
# exit
export CUDA_DEVICE_ORDER="PCI_BUS_ID"
#export CUDA_VISIBLE_DEVICES="6,7"
export CUDA_VISIBLE_DEVICES="0"
# export CUDA_VISIBLE_DEVICES=""

#export TF_XLA_FLAGS="--tf_xla_auto_jit=2"

#export TF_XLA_FLAGS="--tf_xla_auto_jit=2 --tf_xla_cpu_global_jit"
#export XLA_FLAGS='--xla_dump_to=./xla-gen-out --xla_dump_hlo_as_dot --xla_dump_hlo_pass_re=forward-allocation --xla_hlo_graph_sharding_color'
# this segfaulted
#export TF_GPU_ALLOCATOR=cuda_malloc_async
# export TF_FORCE_GPU_ALLOW_GROWTH=1
export TF_CPP_MIN_LOG_LEVEL=3

useDAPHNE=""
useSYSDS=""
useSYSDSP=""
useTF=""
useTFXLA=""
TF_EAGER=eager
visualize=""

MODEL_CSV=$P2_DATA_DIR/$P2_MODEL_CSV
MODEL_H5=$P2_DATA_DIR/$P2_MODEL_H5
IMAGES=$P2_DATA_DIR/$P2_TESTING_DATA_CSV
LABELS=$P2_DATA_DIR/$P2_TESTING_LABELS_CSV

pathRuntimeDAPHNE=$P2_RESULTS/DAPHNE_runtimes.csv
pathRuntimeSYSDS=$P2_RESULTS/SYSDS_runtimes.csv
pathRuntimeSYSDSP=$P2_RESULTS/SYSDSP_runtimes.csv
pathRuntimeTF=$P2_RESULTS/TF_runtimes.csv
pathRuntimeTFXLA=$P2_RESULTS/TFXLA_runtimes.csv

# default rep val
repetitions=3

# -----------------------------------------------------------------------------
# Parsing
# -----------------------------------------------------------------------------

while [[ $# -gt 0 ]]
do
    key="$1"
    case $key in
        -r|--repetitions)
            repetitions=$2
            shift
            ;;
        --daphne)
            useDAPHNE="y"
            ;;
        --sysds)
            useSYSDS="y"
            ;;
        --sysdsp)
            useSYSDSP="y"
            ;;
        --tf)
            useTF="y"
            ;;
        --tfxla)
            useTFXLA="y"
            ;;
        --vis)
            visualize="y"
            ;;
        *)
            printf "unknown option: $key\n"
            exit 1
            ;;
    esac
    shift
done

function setup () {
    mkdir -p $P2_RESULTS
    printf "P2_BATCHSIZE=$P2_BATCHSIZE\n" >> $P2_RESULTS/configuration.txt
    printf "IMAGES=$IMAGES\n" >> $P2_RESULTS/configuration.txt    
}

function timepoint () {
    date +%s%N
}

function run () {
    local header="system\trepIdx\truntime [ns]\n"

    if [[ $useDAPHNE ]]; then
        cd $P2_ROOT
        printf "$header" > $pathRuntimeDAPHNE
        printf "$header" > $P2_RESULTS/DAPHNE-dataload.csv
        printf "$header" > $P2_RESULTS/DAPHNE-scoring.csv

        printf " --- Starting Daphne scoring at $(date) \n "
        for repIdx in $(seq $repetitions)
        do
            printf "$(date) repetition $repIdx...\n "

            local start=$(timepoint)

            $DAPHNE_ROOT/build/bin/daphnec p2.daphne --args libdir="$DAPHNE_ROOT/build/src/runtime/local/kernels" \
              cuda=1 images=\""$IMAGES\"" labels=\""$LABELS\"" \
              batch_size=$P2_BATCHSIZE model=\""$MODEL_CSV\""  | tee $P2_RESULTS/DAPHNE-output-$repIdx.txt
              
            local end=$(timepoint)

            printf "DAPHNE\t$repIdx\t$(($end - $start))\n" >> $pathRuntimeDAPHNE

            printf "DAPHNE\t$repIdx\t$(grep -i data $P2_RESULTS/DAPHNE-output-$repIdx.txt | cut -d "=" -f 2 | cut -d "n" -f 1)\n" \
              >> $P2_RESULTS/DAPHNE-dataload.csv

            printf "DAPHNE\t$repIdx\t$(grep -i inference $P2_RESULTS/DAPHNE-output-$repIdx.txt | cut -d "=" -f 2 | cut -d "n" -f 1)\n" \
              >> $P2_RESULTS/DAPHNE-scoring.csv
              
            printf "done.\n"
        done
        cd $P2_ROOT
    fi
    
    if [[ $useSYSDS ]]; then
        cd $P2_ROOT
        printf "$header" > $pathRuntimeSYSDS
        printf "$header" > $P2_RESULTS/SYSDS-dataload.csv
        printf "$header" > $P2_RESULTS/SYSDS-scoring.csv

        printf " --- Starting SystemDS scoring at $(date)\n "
        for repIdx in $(seq $repetitions)
        do
            printf "$(date) repetition $repIdx...\n "

            local start=$(timepoint)

            CONFIG_FILE=$P2_ROOT/SystemDS-config.xml SYSDS_QUIET=1 CUDA_PATH=/usr/local/cuda \
              $BASE_DIR/resources/systemds $P2_ROOT/p2.dml -nvargs images=$IMAGES model=$MODEL_CSV \
              labels=$LABELS batch_size=$P2_BATCHSIZE -gpu | tee $P2_RESULTS/SYSDS-output-$repIdx.txt

            local end=$(timepoint)

            printf "SYSDS\t$repIdx\t$(($end - $start))\n" >> $pathRuntimeSYSDS

            printf "SYSDS\t$repIdx\t$(grep -i data $P2_RESULTS/SYSDS-output-$repIdx.txt | cut -d "=" -f 2 | cut -d "n" -f 1)\n" \
              >> $P2_RESULTS/SYSDS-dataload.csv
              
            printf "SYSDS\t$repIdx\t$(grep -i inference $P2_RESULTS/SYSDS-output-$repIdx.txt | cut -d "=" -f 2 | cut -d "n" -f 1)\n" \
              >> $P2_RESULTS/SYSDS-scoring.csv
              
            printf "done.\n"
        done
        cd $P2_ROOT
    fi
    
    if [[ $useSYSDSP ]]; then
        cd $P2_ROOT
        printf "$header" > $pathRuntimeSYSDSP
        printf "$header" > $P2_RESULTS/SYSDSP-dataload.csv
        printf "$header" > $P2_RESULTS/SYSDSP-scoring.csv

        printf " --- Starting SystemDS scoring at $(date)\n "
        for repIdx in $(seq $repetitions)
        do
            printf "$(date) repetition $repIdx...\n "

            local start=$(timepoint)

            CONFIG_FILE=$P2_ROOT/SystemDS-config-par-io.xml SYSDS_QUIET=1 CUDA_PATH=/usr/local/cuda \
              $BASE_DIR/resources/systemds $P2_ROOT/p2.dml -nvargs images=$IMAGES model=$MODEL_CSV \
              labels=$LABELS batch_size=$P2_BATCHSIZE -gpu | tee $P2_RESULTS/SYSDSP-output-$repIdx.txt

            local end=$(timepoint)

            printf "SYSDSP\t$repIdx\t$(($end - $start))\n" >> $pathRuntimeSYSDSP

            printf "SYSDSP\t$repIdx\t$(grep -i data $P2_RESULTS/SYSDSP-output-$repIdx.txt | cut -d "=" -f 2 | cut -d "n" -f 1)\n" \
              >> $P2_RESULTS/SYSDSP-dataload.csv
              
            printf "SYSDSP\t$repIdx\t$(grep -i inference $P2_RESULTS/SYSDSP-output-$repIdx.txt | cut -d "=" -f 2 | cut -d "n" -f 1)\n" \
              >> $P2_RESULTS/SYSDSP-scoring.csv
              
            printf "done.\n"
        done
        cd $P2_ROOT
    fi

    if [[ $useTF ]]; then
        printf " --- Starting Tensorflow scoring at $(date)\n "
        printf "$header" > $pathRuntimeTF
        printf "$header" > $P2_RESULTS/TF-dataload.csv
        printf "$header" > $P2_RESULTS/TF-scoring.csv
        
        for repIdx in $(seq $repetitions)
        do
            printf "$(date) repetition $repIdx...\n "

            local start=$(timepoint)

            python3 $P2_ROOT/resnet20-scoring.py dataset=sen2 batch_size=$P2_BATCHSIZE images=$IMAGES labels=$LABELS \
              model=$MODEL_H5 $TF_EAGER | tee $P2_RESULTS/TF-output-$repIdx.txt

            local end=$(timepoint)

            printf "TF\t$repIdx\t$(($end - $start))\n" >> $pathRuntimeTF

            printf "TF\t$repIdx\t$(grep -i data $P2_RESULTS/TF-output-$repIdx.txt | cut -d "=" -f 2 | cut -d "n" -f 1)\n" \
              >> $P2_RESULTS/TF-dataload.csv

            printf "TF\t$repIdx\t$(grep -i inference $P2_RESULTS/TF-output-$repIdx.txt | cut -d "=" -f 2 | cut -d "n" -f 1)\n" \
              >> $P2_RESULTS/TF-scoring.csv
            printf "done.\n"
        done
        cd $P2_ROOT
    fi
    
    if [[ $useTFXLA ]]; then

        printf "$header" > $pathRuntimeTFXLA
        printf "$header" > $P2_RESULTS/TFXLA-dataload.csv
        printf "$header" > $P2_RESULTS/TFXLA-scoring.csv

        printf " --- Starting Tensorflow XLA scoring at $(date)\n "
        for repIdx in $(seq $repetitions)
        do
            printf "$(date) repetition $repIdx...\n "

            local start=$(timepoint)

            python3 $P2_ROOT/resnet20-scoring.py xla batch_size=$P2_BATCHSIZE dataset=sen2 batch_size=$P2_BATCHSIZE images=$IMAGES \
              labels=$LABELS model=$MODEL_H5 $TF_EAGER | tee $P2_RESULTS/TFXLA-output-$repIdx.txt

            local end=$(timepoint)

            printf "TFXLA\t$repIdx\t$(($end - $start))\n" >> $pathRuntimeTFXLA

            printf "TFXLA\t$repIdx\t$(grep -i data $P2_RESULTS/TFXLA-output-$repIdx.txt | cut -d "=" -f 2 | cut -d "n" -f 1)\n" \
              >> $P2_RESULTS/TFXLA-dataload.csv

            printf "TFXLA\t$repIdx\t$(grep -i inference $P2_RESULTS/TFXLA-output-$repIdx.txt | cut -d "=" -f 2 | cut -d "n" -f 1)\n" \
              >> $P2_RESULTS/TFXLA-scoring.csv
              
            printf "done.\n"
        done
        cd $P2_ROOT
    fi
}

setup
run
if [[ $visualize ]]; then
  python3 $P2_ROOT/visualize-p2.py $P2_RESULTS | tee $P2_RESULTS/visualize-output.txt
fi
date
