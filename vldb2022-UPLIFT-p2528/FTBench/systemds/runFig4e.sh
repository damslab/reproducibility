#!/bin/bash

mv kdd_dml.dat kdd_tmp_dat #save before rerunning T2
mv criteo10M_s2_dml.dat criteo10M_s2_tmp.dat #same before rerunning T4
./config partransform start
./runjava -f T2.dml -stats
./runjava -f T4.dml -stats
./runjava -f T4_star.dml -stats
mv 4e_T2_Base.dat 4e_T2_Scale.dat
cp 4e_T2_Scale.dat Tab3_T2_uplift.dat
mv 4e_T4_Base.dat 4e_T4_Scale.dat
mv 4e_T4s_Base.dat 4e_T4s_Scale.dat
./runjava -f T2_udf.dml -stats
./runjava -f T4_udf.dml -stats
./runjava -f T4_star_udf.dml -stats
./config partransform stop
./runjava -f T2.dml -stats
cp 4e_T2_Base.dat Tab3_T2_base.dat
./runjava -f T4.dml -stats
./runjava -f T4_star.dml -stats
./config partransform start
mv kdd_tmp_dat kdd_dml.dat #restore T2 result
mv criteo10M_s2_tmp.dat criteo10M_s2_dml.dat #restore T4 result

