#!/bin/bash

# Figure 4a: Use case T1. Dataset Adult.
if [ "$1" = "T1" ]; then
  abspath="$(cd "$(dirname "../../datasets/adult.data")"; pwd)/$(basename "../../datasets/adult.data")"
  python3 T1_spark.py $abspath
fi

# Table 3: Use case T2. Dataset KDD 98.
if [ "$1" = "T2" ]; then
  python3 T2_spark.py all
  python3 T2_spark.py 1
fi

# Table 3: Use case T3. Dataset Criteo.
if [ "$1" = "T3" ]; then
  abspath="$(cd "$(dirname "../../datasets/criteo_day21_10M")"; pwd)/$(basename "../../datasets/criteo_day21_10M")"
  python3 T3_spark.py $abspath all
  python3 T3_spark.py $abspath 1
fi

# Table 3: Use case T9. Dataset Cat in Dat.
if [ "$1" = "T9" ]; then
  python3 T9_spark.py all
  python3 T9_spark.py 1
fi

# Figure 4h: Use case T15. Dataset Criteo.
if [ "$1" = "T15" ]; then
  abspath="$(cd "$(dirname "../../datasets/criteo_day21_5M_cleaned")"; pwd)/$(basename "../../datasets/criteo_day21_5M_cleaned")"
  python3 T15_spark.py $abspath
fi

exit
