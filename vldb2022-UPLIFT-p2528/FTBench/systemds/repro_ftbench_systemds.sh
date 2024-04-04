#!/bin/bash

# Figure 4a: Use case T1. Dataset Adult.
if [ "$1" = "T1" ]; then
  ./config partransform stop
  ./runjava -f T1.dml -stats
  mv adult_dml.dat adult_dml_base.dat
  ./config partransform start
  ./runjava -f T1.dml -stats
fi

# Figure 4b: Use case T8. Dataset Home Credit Risk dataset.
if [ "$1" = "T8" ]; then
  ./config partransform stop
  ./runjava -f T8.dml -stats
  mv homecredit_dml.dat homecredit_dml_base.dat
  ./config partransform start
  ./runjava -f T8.dml -stats
fi

# Figure 4b: Use case T5. Dataset Santander.
if [ "$1" = "T5" ]; then
  ./config partransform stop
  ./runjava -f T5.dml -stats
  mv santander_dml.dat santander_dml_base.dat
  ./config partransform start
  ./runjava -f T5.dml -stats
fi

# Figure 4b: Use case T2. Dataset KDD 98.
if [ "$1" = "T2" ]; then
  ./config partransform stop
  ./runjava -f T2.dml -stats
  mv kdd_dml.dat kdd_dml_base.dat
  ./config partransform start
  ./runjava -f T2.dml -stats
fi

# Figure 4c: Use case T3. Dataset Criteo.
if [ "$1" = "T3" ]; then
  ./config partransform stop
  ./runjava -f T3.dml -stats
  mv criteo10M_s1_dml.dat criteo10M_s1_dml_base.dat
  mv Tab3_T3_dml.dat Tab3_T3_base.dat
  ./config partransform start
  ./runjava -f T3.dml -stats
  mv Tab3_T3_dml.dat Tab3_T3_uplift.dat
fi

# Figure 4c: Use case T4. Dataset Criteo.
if [ "$1" = "T4" ]; then
  ./config partransform stop
  ./runjava -f T4.dml -stats
  mv criteo10M_s2_dml.dat criteo10M_s2_dml_base.dat
  ./config partransform start
  ./runjava -f T4.dml -stats
fi

# Figure 4c: Use case T6. Dataset Crypto Forcasting.
if [ "$1" = "T6" ]; then
  ./config partransform stop
  ./runjava -f T6T7.dml -args 1 -stats
  mv crypto_s1_dml.dat crypto_s1_dml_base.dat
  ./config partransform start
  ./runjava -f T6T7.dml -args 1 -stats
fi

# Figure 4c: Use case T7. Dataset Crypto Forcasting.
if [ "$1" = "T7" ]; then
  ./config partransform stop
  ./runjava -f T6T7.dml -args 2 -stats
  mv crypto_s2_dml.dat crypto_s2_dml_base.dat
  ./config partransform start
  ./runjava -f T6T7.dml -args 2 -stats
fi

# Figure 4c: Use case T9. Dataset Cat in Dat.
if [ "$1" = "T9" ]; then
  ./config partransform stop
  ./runjava -f T9.dml -stats
  mv catindat_dml.dat catindat_dml_base.dat 
  mv Tab3_T9_dml.dat Tab3_T9_base.dat
  ./config partransform start
  ./runjava -f T9.dml -stats
  mv Tab3_T9_dml.dat Tab3_T9_uplift.dat
fi

# Figure 4c: Use case T12. Dataset synthetic.
if [ "$1" = "T12" ]; then
  ./config partransform stop
  ./runjava -f T12.dml -stats
  mv batch_dml.dat batch_dml_base.dat 
  ./config partransform start
  ./runjava -f T12.dml -stats
fi

# Figure 4d: Use case T10. Dataset Aminer.
if [ "$1" = "T10" ]; then
  ./config partransform stop
  ./runjava -f T10.dml -stats
  mv bagfwords_dml.dat bagfwords_dml_base.dat 
  ./config partransform start
  ./runjava -f T10.dml -stats
fi

# Figure 4d: Use case T11. Dataset Aminer.
if [ "$1" = "T11" ]; then
  ./config partransform stop
  ./config parop stop
  ./runjava -f T11.dml -stats
  mv embedding_dml.dat embedding_dml_base.dat 
  ./config partransform start
  ./config parop start
  ./runjava -f T11.dml -stats
fi

# Figure 4f: Use case T13. Dataset synthetic.
if [ "$1" = "T13" ]; then
  ./runT13.sh
fi

# Figure 4g: Use case T14. Dataset synthetic.
if [ "$1" = "T14" ]; then
  ./runT14.sh
fi

# Figure 4h: Use case T15. Dataset Criteo.
if [ "$1" = "T15" ]; then
  ./config partransform stop
  ./runjava -f T15.dml -stats
  mv featureeng_dml.dat featureeng_dml_base.dat 
  ./config partransform start
  ./runjava -f T15.dml -stats
fi


rm *.mtd

exit
