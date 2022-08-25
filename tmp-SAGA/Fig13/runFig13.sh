export JAVA_HOME=/usr/lib/jvm/java-1.11.0-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH 

pip=$1
for data in 37 74 110 147
do
  echo "executing pipeline"$pip" on "${data}
  start=$(date +%s%N)
  time -p sparkDML -debug -exec hybrid -f pipelines/pipeline${pip}.dml  -args \
     rep/EEG_${data}.bin  \
     meta/meta_EEG.csv $pathout/$data.csv 
  end=$(date +%s%N)
  echo $data'\t'$((($end-$start)/1000000)) >> time.dat
done

