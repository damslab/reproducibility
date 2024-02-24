import sys
import time
import numpy as np
import scipy as sp
import pandas as pd
import math
import warnings
from pyspark.sql import SparkSession
from pyspark import StorageLevel
from pyspark.ml.feature import Normalizer
from pyspark.ml.feature import StringIndexer, StandardScaler
from pyspark.ml.feature import OneHotEncoder, VectorAssembler
from pyspark.ml.feature import QuantileDiscretizer 
from pyspark.sql.types import StringType, DoubleType
from pyspark.ml import Pipeline 

# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)
warnings.filterwarnings('ignore') #cleaner, but not recommended

def readNprep():
    # Read and isolate target and training data
    kdd = pd.read_csv("../../datasets/KDD98.csv", delimiter=",", header=None)
    print(kdd.head())
    kddX = kdd.iloc[:,0:469]
    kddX = kddX.drop([0], axis=0)
    kddX = kddX.replace(r'\s+',np.nan,regex=True).replace('',np.nan)
    # Replace NAs with before/after entries
    kddX.fillna(method='pad', inplace=True)
    kddX.fillna(method='bfill', inplace=True)

    # Cast categorical columns that have numbers to float first, 
    # to avoid mix of int and float type strings (5, 5.0), which
    # increases # distinct values in a column
    st = [23,24,*range(28,42),195,196,197,*range(362,384),*range(412,434)]
    #kddX[st] = kddX[st].astype(float).astype(str)

    # Set dtype float for numeric columns and str from categorical
    # The default dtype for all columns is object at this point 
    fl = [4,7,16,26,*range(43,50),53,*range(75,195),*range(198,361),407,409,410,411,*range(434,469)]
    kddX[fl] = kddX[fl].astype(float)
    cat = kddX.select_dtypes(exclude=np.float64).columns
    kddX[cat] = kddX[cat].astype(str)
    #print(kddX.info())
    kddX_df = spark.createDataFrame(kddX)
    print("#partitions: ", kddX_df.rdd.getNumPartitions())
    kddX_df.persist(StorageLevel.MEMORY_ONLY)
    print((kddX.count(), len(kddX.columns)))
    return kddX_df

def transform(kddX):
    # Seperate out the numeric, categorical inputs
    numeric_df = kddX.select([f.name for f in kddX.schema.fields if isinstance(f.dataType, DoubleType)])
    cat_df = kddX.select([f.name for f in kddX.schema.fields if isinstance(f.dataType, StringType)])
    # Run them through binning and scaling
    outCols = ['{0}_bin'.format(out) for out in numeric_df.columns]
    #newCols = outCols
    binner = QuantileDiscretizer(inputCols=numeric_df.columns, 
            outputCols=outCols, numBuckets=5)
    binned = binner.fit(numeric_df).transform(numeric_df)
    #print(binned.show(1))
    assembler = VectorAssembler(inputCols=binner.getOutputCols(), outputCol='features', handleInvalid="keep")
    assembled = assembler.transform(binned)
    scaler = StandardScaler(inputCol='features', outputCol='scaledFeatures',
            withStd=True, withMean=False)
    scaled = scaler.fit(assembled).transform(assembled)
    # Recode and dummycode the categorical features
    outCols = ['{0}_rc'.format(out) for out in cat_df.columns]
    newCols = outCols
    indexer = StringIndexer(inputCols=cat_df.columns, outputCols=outCols)
    indexed = indexer.fit(cat_df).transform(cat_df)
    outCols = ['{0}_dc'.format(out) for out in indexer.getOutputCols()]
    newCols = newCols + outCols
    one_hot = OneHotEncoder(dropLast=False, inputCols=indexer.getOutputCols(), 
            outputCols=outCols)
    encoded = one_hot.fit(indexed).transform(indexed)
    # Assemble the encoded columns for the normalizer
    assembler = VectorAssembler(inputCols=newCols, outputCol='features', handleInvalid="keep")
    assembled = assembler.transform(encoded)
    # Apply StandardScaler on all features
    scaler = StandardScaler(inputCol='features', outputCol='scaledFeatures',
            withStd=True, withMean=False)
    scaled = scaler.fit(assembled).transform(assembled)
    #print(scaled.show(1))
    return scaled

def transformPipe(kddX):
    # Seperate out the numeric, categorical inputs
    numeric_df = kddX.select([f.name for f in kddX.schema.fields if isinstance(f.dataType, DoubleType)])
    cat_df = kddX.select([f.name for f in kddX.schema.fields if isinstance(f.dataType, StringType)])

    # Bin the numerical columns
    outCols = ['{0}_bin'.format(out) for out in numeric_df.columns]
    newCols = outCols
    binner = QuantileDiscretizer(inputCols=numeric_df.columns, outputCols=outCols, numBuckets=5)
    # Recode and dummycode the categorical features
    outCols = ['{0}_rc'.format(out) for out in cat_df.columns]
    newCols = newCols + outCols
    indexer = StringIndexer(inputCols=cat_df.columns, outputCols=outCols)
    #indexed = indexer.fit(cat_df).transform(cat_df)
    outCols = ['{0}_dc'.format(out) for out in indexer.getOutputCols()]
    newCols = newCols + outCols
    one_hot = OneHotEncoder(dropLast=False, inputCols=indexer.getOutputCols(), outputCols=outCols)
    # Assemble the encoded columns for the normalizer
    assembler = VectorAssembler(inputCols=newCols, outputCol='features', handleInvalid="keep")
    # Apply StandardScaler on all features
    scaler = StandardScaler(inputCol='features', outputCol='scaledFeatures',
            withStd=True, withMean=False)
    pipe = Pipeline(stages=[binner, indexer, one_hot, assembler, scaler])
    encoded = pipe.fit(kddX).transform(kddX)
    #print(encoded.show(1))
    #print(encoded.rdd.toDebugString)
    return encoded

nthreads_arg = sys.argv[1] #num of threads or "all"
nthreads = "*" if nthreads_arg.lower() == "all" else nthreads_arg
spark = SparkSession\
    .builder\
    .master(f"local[{nthreads}]")\
    .config("spark.driver.memory", "110g")\
    .config("spark.kryoserializer.buffer.max", "1024m")\
    .config("spark.sql.execution.arrow.pyspark.enabled", "true")\
    .appName("KddByMLlib")\
    .getOrCreate()
spark.sparkContext.setLogLevel('ERROR')

X = readNprep()

# The 1st call may read the dataset. Don't count the 1st call
t1 = time.time()
X_prep1 = transformPipe(X)
#X_prep1 = transform(X)
print("Elapsed time for transformations via sparkml = %s sec" % (time.time() - t1))

# Average of three calls
totTime = 0
t1 = time.time()
X_prep2 = transformPipe(X)
#X_prep2 = transform(X)
totTime = totTime + ((time.time() - t1) * 1000) #millisec
print("Elapsed time for transformations via sparkml = %s sec" % (time.time() - t1))

t1 = time.time()
X_prep3 = transformPipe(X)
#X_prep3 = transform(X)
totTime = totTime + ((time.time() - t1) * 1000) #millisec
print("Elapsed time for transformations via sparkml = %s sec" % (time.time() - t1))

t1 = time.time()
X_prep4 = transformPipe(X)
#X_prep4 = transform(X)
totTime = totTime + ((time.time() - t1) * 1000) #millisec
print("Elapsed time for transformations via sparkml = %s sec" % (time.time() - t1))

print("Average elapsed time = %s millisec" % (totTime/3))
if nthreads_arg.lower() == "all":
    filename = "Tab3_T2_spark.dat"
else:
    filename = "Tab3_T2_spark1T.dat"
avgTime = round((totTime/3)/1000, 1) #sec
with open(filename, "w") as file:
    file.write(str(avgTime))

