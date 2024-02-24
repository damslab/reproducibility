import sys
import time
import numpy as np
import scipy as sp
from scipy.sparse import csr_matrix
import pandas as pd
import math
import warnings
from pyspark import StorageLevel
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType
from pyspark.ml.feature import Normalizer
from pyspark.ml.feature import StringIndexer
from pyspark.ml.feature import OneHotEncoder
from pyspark.ml import Pipeline 

# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)
warnings.filterwarnings('ignore') #cleaner, but not recommended

def readNprep(nRows, spark):
    # Read the 1M or the 10M dataset
    if nRows == 1:
      print("Reading file: criteo_day21_1M")
      path = sys.argv[1]
      criteo = spark.read.options(inferSchema='True', delimiter=',') \
               .csv(f"file:{path}")
    if nRows == 10:
      path = sys.argv[1]
      print("Reading file: criteo_day21_10M")
      criteo = spark.read.options(inferSchema='True', delimiter=',') \
               .csv(f"file:{path}")
    print(criteo.printSchema())
    print(criteo.show(5))
    criteo.persist(StorageLevel.MEMORY_ONLY)
    print((criteo.count(), len(criteo.columns)))
    print("#partitions: ", criteo.rdd.getNumPartitions())
    return criteo 

# Use Case T3 (spec1): DC(26)
def transformSparkml(criteo):
    # NOTE: one core execution is 4.4x slower than all cores execution
    outCols = ['{0}_rc'.format(out) for out in criteo.columns[14:40]]
    indexer = StringIndexer(inputCols=criteo.columns[14:40], 
            outputCols=outCols, handleInvalid="keep")
    #encoded = indexer.fit(criteo).transform(criteo)
    outCols = ['{0}_dc'.format(out) for out in indexer.getOutputCols()]
    one_hot = OneHotEncoder(dropLast=False, inputCols=indexer.getOutputCols(), outputCols=outCols)
    pipe = Pipeline(stages=[indexer, one_hot])
    encoded = pipe.fit(criteo).transform(criteo)
    #print(encoded.show(1, truncate=False))
    return encoded


nthreads_arg = sys.argv[2] #num of threads or "all"
nthreads = "*" if nthreads_arg.lower() == "all" else nthreads_arg
spark = SparkSession\
    .builder\
    .master(f"local[{nthreads}]")\
    .config("spark.driver.memory", "110g")\
    .config("spark.kryoserializer.buffer.max", "1024m")\
    .appName("CriteoBySparkML")\
    .getOrCreate()

X = readNprep(10, spark)

# The 1st call may read the dataset. Don't track the 1st call
t1 = time.time()
X_enc1 = transformSparkml(X)
print("Elapsed time for transformations via sparkml = %s sec" % (time.time() - t1))

# Average of three calls
totTime = 0
t1 = time.time()
X_enc2 = transformSparkml(X)
totTime = totTime + ((time.time() - t1) * 1000) #millisec
print("Elapsed time for transformations via sparkml = %s sec" % (time.time() - t1))

t1 = time.time()
X_enc3 = transformSparkml(X)
totTime = totTime + ((time.time() - t1) * 1000) #millisec
print("Elapsed time for transformations via sparkml = %s sec" % (time.time() - t1))

t1 = time.time()
X_enc4 = transformSparkml(X)
totTime = totTime + ((time.time() - t1) * 1000) #millisec
print("Elapsed time for transformations via sparkml = %s sec" % (time.time() - t1))

print("Average elapsed time = %s millisec" % (totTime/3))
if nthreads_arg.lower() == "all":
    filename = "Tab3_T3_spark.dat"
else:
    filename = "Tab3_T3_spark1T.dat"
avgTime = round((totTime/3)/1000, 1) #sec
with open(filename, "w") as file:
    file.write(str(avgTime))
