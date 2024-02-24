#!/bin/bash

# Figure 4a: Use case T1. Dataset Adult.
if [ "$1" = "T1" ]; then
  python3 T1_sk.py
fi

# Figure 4b: Use case T8. Dataset Home Credit Risk dataset.
if [ "$1" = "T8" ]; then
  python3 T8_sk.py
fi

# Figure 4b: Use case T5. Dataset Santander.
if [ "$1" = "T5" ]; then
  python3 T5_sk.py
fi

# Figure 4b: Use case T2. Dataset KDD 98.
if [ "$1" = "T2" ]; then
  python3 T2_sk.py
fi

# Figure 4c: Use case T3. Dataset Criteo.
if [ "$1" = "T3" ]; then
  python3 T3T4_sk.py 1
fi

# Figure 4c: Use case T4. Dataset Criteo.
if [ "$1" = "T4" ]; then
  python3 T3T4_sk.py 2
fi

# Figure 4c: Use case T6. Dataset Crypto Forcasting.
if [ "$1" = "T6" ]; then
  python3 T6T7_sk.py 1
fi

# Figure 4c: Use case T7. Dataset Crypto Forcasting.
if [ "$1" = "T7" ]; then
  python3 T6T7_sk.py 2
fi

# Figure 4c: Use case T9. Dataset Cat in Dat.
if [ "$1" = "T9" ]; then
  python3 T9_sk.py
fi

# Figure 4d: Use case T10. Dataset Aminer.
if [ "$1" = "T10" ]; then
  python3 T10_sk.py
fi

# Figure 4f: Use case T13. Dataset synthetic.
if [ "$1" = "T13" ]; then
  mv ../systemds/stringlen_skAll.dat .
fi

# Figure 4g: Use case T14. Dataset synthetic.
if [ "$1" = "T14" ]; then
  mv ../systemds/numdistinct_skAll.dat .
fi

# Figure 4h: Use case T15. Dataset Criteo.
if [ "$1" = "T15" ]; then
  python3 T15_sk.py
fi

exit
