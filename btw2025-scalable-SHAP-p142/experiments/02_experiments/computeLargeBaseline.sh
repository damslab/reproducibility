#!/bin/bash


instances="${1:-50}"
permutations="${2:-500}"
samples="${3:-1000}"

if [ "${SHAP_FAST_EXP}" = "1" ]; then
  echo "SHAP_FAST_EXP is set. Running with less samples and permutations to be faster."
  samples="500"
  permutations="250"
fi

echo "Computing large baseline for Adult with python for $instances instances on $permutations permutaions with $samples. Depending on the setup, this may take >6h..."
#adult
python3 ./shap-experiment-python.py --data-dir=../10_data/adult/ --data-x=Adult_X.csv --model-type=multiLogReg --n-permutations=$permutations --n-instances=$instances --n-samples=$samples  --result-file-name=../10_data/accuracy/shap-values_permutation_large_adult_linlogreg_python.csv --silent

echo "Computing large baseline for Census with python for $instances instances on $permutations permutaions with $samples. Depending on the setup, this may take >6h..."
#census
python3 ./shap-experiment-python.py --data-dir=../10_data/census/ --data-x=Census_X.csv --data-y=Census_y_corrected.csv --model-type=l2svm --n-permutations=$permutations --n-instances=$instances --n-samples=$samples  --result-file-name=../10_data/accuracy/shap-values_permutation_large_census_l2svm_python.csv --silent 
