rm tracegpu2.dat
rm tracegpu2_lineage.dat
rm tracegpu2_probe.dat
rm tracegpu2_20.dat
rm tracegpu2_40.dat
rm tracegpu2_80.dat

echo "Starting microbenchmark trace1"
echo "----------------------------- "
# time calculated in milliseconds

# Vary batch size [2, 256] and reuse (0%, 20%, 40%, 80%)
# Data size = 200000 X 3*32*32

pow2() {
  # The first argument is the exponent
  echo $((2**$1))
}

for exp in {1..8..1}
do
  scale=$(pow2 $exp)
  for rep in {1..3}
  do
    echo "Batch size: $scale, repetition: $rep"
    config2 all stop
    start=$(date +%s%N)
    runjava -f lineageThroughputGPU2.dml -args $scale 0 -stats -gpu
    end=$(date +%s%N)
    echo -e $scale'\t'$((($end-$start)/1000000)) >> tracegpu2.dat

    start=$(date +%s%N)
    runjava -f lineageThroughputGPU2.dml -args $scale 0 -stats -gpu -lineage
    end=$(date +%s%N)
    echo -e $scale'\t'$((($end-$start)/1000000)) >> tracegpu2_lineage.dat

    start=$(date +%s%N)
    runjava -f lineageThroughputGPU2.dml -args $scale 0 -stats -gpu -lineage reuse_full
    end=$(date +%s%N)
    echo -e $scale'\t'$((($end-$start)/1000000)) >> tracegpu2_probe.dat

    start=$(date +%s%N)
    runjava -f lineageThroughputGPU2.dml -args $scale 0.2 -stats -gpu -lineage reuse_full
    end=$(date +%s%N)
    echo -e $scale'\t'$((($end-$start)/1000000)) >> tracegpu2_20.dat

    start=$(date +%s%N)
    runjava -f lineageThroughputGPU2.dml -args $scale 0.4 -stats -gpu -lineage reuse_full
    end=$(date +%s%N)
    echo -e $scale'\t'$((($end-$start)/1000000)) >> tracegpu2_40.dat

    start=$(date +%s%N)
    runjava -f lineageThroughputGPU2.dml -args $scale 0.8 -stats -gpu -lineage reuse_full
    end=$(date +%s%N)
    echo -e $scale'\t'$((($end-$start)/1000000)) >> tracegpu2_80.dat
  done
done

exit

