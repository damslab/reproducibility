export JAVA_HOME=/usr/lib/jvm/java-1.11.0-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH 

pip=$1
for data in 5 7 1 3 
do
  echo "executing pipeline"$pip" on "${data}
  pathout=res/pipeline${pip}/
  pathout2=res/pipeline${pip}/time/
  mkdir -p $pathout
  mkdir -p $pathout2
  echo "executing " data/rep/EEG17_${data}.bin
  start=$(date +%s%N)
  time -p ./sparkDML.sh -debug -exec hybrid -f pipelines/pipeline${pip}.dml  -args \
     hdfs://charlie.dm.isds.tugraz.at:9000/user/tmp/data/rep/EEG17_${data}.bin  \
    "hdfs://charlie.dm.isds.tugraz.at:9000/user/tmp/meta/meta_EEG.csv" $pathout/$data.csv 2>&1 > ${pathout}/${data}.txt
  end=$(date +%s%N)
  echo $data'\t'$((($end-$start)/1000000)) >> ${pathout2}/pipelinesTime.dat
done

