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

def readNprep(spark):
    # Read and isolate target and training data
    adult = spark.read.options(inferSchema='True', delimiter=',') \
               .csv("file:/home/aphani/datasets/adult.data")
    adult.persist(StorageLevel.MEMORY_ONLY)
    print(adult.printSchema())
    print(adult.show(5))
    return adult 

def transform(adult):
    # Seperate out the numeric, categorical inputs
    numeric_df = adult.select([f.name for f in adult.schema.fields if isinstance(f.dataType, DoubleType)])
    cat_df = adult.select([f.name for f in adult.schema.fields if isinstance(f.dataType, StringType)])
    # Bin the numerical columns
    outCols = ['{0}_bin'.format(out) for out in numeric_df.columns]
    binner = QuantileDiscretizer(inputCols=numeric_df.columns, outputCols=outCols, numBuckets=5)
    # Recode and dummycode the categorical features
    outCols = ['{0}_rc'.format(out) for out in cat_df.columns]
    indexer = StringIndexer(inputCols=cat_df.columns, outputCols=outCols)
    inCols = binner.getOutputCols() + indexer.getOutputCols() 
    outCols = ['{0}_dc'.format(out) for out in inCols]
    one_hot = OneHotEncoder(dropLast=False, inputCols=inCols, outputCols=outCols)
    # Make a pipeline and apply
    pipe = Pipeline(stages=[binner, indexer, one_hot])
    encoded = pipe.fit(adult).transform(adult)
    return encoded

spark = SparkSession\
    .builder\
    .master("local[*]")\
    .config("spark.driver.memory", "110g")\
    .config("spark.kryoserializer.buffer.max", "1024m")\
    .appName("CriteoBySparkML")\
    .getOrCreate()
spark.sparkContext.setLogLevel('ERROR')

X = readNprep(spark)

# The 1st call may read the dataset. Don't count the 1st call
t1 = time.time()
X_prep1 = transform(X)
print("Elapsed time for transformations via sparkml = %s sec" % (time.time() - t1))

# Average of three calls
totTime = 0
t1 = time.time()
X_prep2 = transform(X)
totTime = totTime + ((time.time() - t1) * 1000) #millisec
print("Elapsed time for transformations via sparkml = %s sec" % (time.time() - t1))

t1 = time.time()
X_prep3 = transform(X)
totTime = totTime + ((time.time() - t1) * 1000) #millisec
print("Elapsed time for transformations via sparkml = %s sec" % (time.time() - t1))

t1 = time.time()
X_prep4 = transform(X)
totTime = totTime + ((time.time() - t1) * 1000) #millisec
print("Elapsed time for transformations via sparkml = %s sec" % (time.time() - t1))

print("Average elapsed time = %s millisec" % (totTime/3))


