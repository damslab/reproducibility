import sys
import time
import numpy as np
import pandas as pd
import math
import warnings
import sklearn
from pyspark.sql import SparkSession
from pyspark import StorageLevel
from pyspark.ml.feature import FeatureHasher
from pyspark.ml.feature import StringIndexer
from pyspark.ml.feature import OneHotEncoder
from pyspark.ml import Pipeline 

# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)
warnings.filterwarnings('ignore') #cleaner, but not recommended

def readNprep(scaleFactor=1):
    # Read,isolate target and combine training and test data
    train = pd.read_csv("~/datasets/catindattrain.csv", delimiter=",", header=None)
    train = train.iloc[1:,:] #remove header
    train.drop(24, axis=1, inplace=True); #remove target
    train = train.replace(r'\s+',np.nan,regex=True).replace('',np.nan)
    train.fillna(method="ffill", inplace=True)
    train.fillna(method="bfill", inplace=True)
    st = [*range(0,24)]
    train[st] = train[st].astype(str)
    # Augment by repeating
    trainList = [train for i in range(1, scaleFactor+1)]
    catindat_pd = pd.concat(trainList, ignore_index=True)
    print(catindat_pd.head())
    # Convert to spar dataframe
    catindat_sp = spark.createDataFrame(catindat_pd)
    catindat_sp.persist(StorageLevel.MEMORY_ONLY)
    print((catindat_sp.count(), len(catindat_sp.columns)))
    print(catindat_sp.printSchema())
    print(catindat_sp.show(5))
    print("#partitions: ", catindat_sp.rdd.getNumPartitions())
    return catindat_sp 

def featureHashingSp(X, ncol):
    t1 = time.time()
    #outCols = ['{0}_rc'.format(out) for out in X.columns]
    #indexer = StringIndexer(inputCols=X.columns, outputCols=outCols, handleInvalid="keep")
    #outCols = ['{0}_dc'.format(out) for out in indexer.getOutputCols()]
    #one_hot = OneHotEncoder(dropLast=False, inputCols=indexer.getOutputCols(), outputCols=outCols)
    #pipe = Pipeline(stages=[indexer, one_hot])
    #encoded = pipe.fit(X).transform(X)
    # NOTE: RC+DC takes 11 sec w/ 32 cores and 21 sec with 1 core
    # In sklearn DC takes similar 22 sec.
    
    hasher = FeatureHasher(numFeatures=ncol, inputCols=X.columns, outputCol="features")
    encoded = hasher.transform(X)
    print(encoded.show(1, truncate=False))
    print("Elapsed time for transformations via sparkml = %s sec" % (time.time() - t1))
    return encoded



spark = SparkSession\
    .builder\
    .master("local[*]")\
    .config("spark.driver.memory", "110g")\
    .config("spark.kryoserializer.buffer.max", "1024m")\
    .config("spark.sql.execution.arrow.pyspark.enabled", "true")\
    .appName("CriteoBySparkML")\
    .getOrCreate()

X = readNprep(scaleFactor=10)
X_enc1 = featureHashingSp(X, 24000)
X_enc2 = featureHashingSp(X, 24000)
X_enc3 = featureHashingSp(X, 24000)
X_enc3 = featureHashingSp(X, 24000)
