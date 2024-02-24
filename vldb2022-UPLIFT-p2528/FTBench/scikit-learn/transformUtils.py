import json
import numpy as np
import pandas as pd
import sys
import time
import scipy as sp
from scipy.sparse import csr_matrix
import pandas as pd
import math
import warnings
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn import preprocessing

def getTransformSpec(X, filename):
    # Deserialize the transform spec
    fullfile = "../systemds/specs/" + filename
    specFile = open(fullfile, "r")
    spec = json.loads(specFile.read())

    # Read column list for individual encoders
    rc = spec.get('recode')
    dc = spec.get('dummycode')
    fh = spec.get('hash')
    bins = []
    methods = []
    numbins = []
    # TODO: support column specific methods and numbins
    equiWidth = True
    binCount = 0;
    if (spec.get('bin')):
        for bin in spec['bin']:
            bins.append(bin.get('id'))
            methods.append(bin.get('method'))
            numbins.append(bin.get('numbins'))
        equiWidth = True if methods[0] == "equi-width" else False
        binCount = numbins[0]

    bins = [i-1 for i in bins]
    # Union the columns lists for categorical encoders
    # NOTE: DC list may contain binned columns 
    catEncode = []
    if fh:
        fh = [i-1 for i in fh]
        catEncode = catEncode + fh
    if rc:
        rc = [i-1 for i in rc]   #convert to 0-based indices
        catEncode = catEncode + rc
    if dc:
        dc = [i-1 for i in dc]
        catEncode = catEncode + dc
    # Sort and remove duplicates
    catEncode = list(set(sorted(catEncode)))
    # Get categorical column list by subtracting binned from catEncode
    catCols = list(set(catEncode) - set(bins))
    # Passthrough list = all columns - (numeric + categorical)
    pt = list(set(range(0,len(X.columns))) - set(catCols + bins))
    return {'rc':rc, 'dc':dc, 'fh':fh, 'bins':bins, 'method':equiWidth, 'numbin':binCount, 'cat':catCols, 'pt':pt}


# Define custom transformer for FeatureUnion
class ColumnSelector(BaseEstimator, TransformerMixin):
    """Select only specified columns."""
    def __init__(self, columns):
        self.columns = columns
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return X[self.columns]

def transformFUnion(X, specfile, resultfile, scale=False, save=True):
    # TODO: Fuse json parsing and building pipeline to avoid passing many lists across
    encoders = getTransformSpec(X, specfile)
    timeres = np.zeros(3)
    # Cast to right datatypes
    X[encoders['bins']] = X[encoders['bins']].astype(float)
    X[encoders['cat']] = X[encoders['cat']].astype(str)

    t1 = time.time()
    # Passthrough transformation -- convert to float
    print("Passthrough columns: %s" % encoders['pt'])
    X[encoders['pt']] = X[encoders['pt']].astype(float)
    # Record the passthrough time only once
    #timeres = timeres + ((time.time() - t1) * 1000) #millisec

    # Seperate numeric inputs
    numeric = list(X.select_dtypes(include=np.float64).columns)
    num_pipe = Pipeline([
            ('selector', ColumnSelector(numeric)),
    ])
    # Build the numeric pipeline
    if scale:
        norm = preprocessing.StandardScaler()
        num_pipe.steps.append(['normalize', norm])

    bins = encoders['bins']
    isBin = True if bins else False   #False if empty
    if isBin:
        isBinDC = True if encoders['dc'] and all(elem in encoders['dc'] for elem in bins) else False
        #isBinDC = False
        #if encoders['dc']:
        #    isBinDC = all(elem in encoders['dc'] for elem in bins)
        strategy = 'uniform' if encoders['method'] else 'quantile'
        postBin = 'onehot' if isBinDC else 'ordinal'
        nbins = encoders['numbin']
        bin_en = preprocessing.KBinsDiscretizer(n_bins=nbins, strategy=strategy, encode=postBin)
        num_pipe.steps.append(['biner', bin_en])

    print(num_pipe)

    # Seperate categorical features
    categorical = list(X.select_dtypes(exclude=np.float64).columns)
    dc = encoders['dc']
    isDC = True if dc else False   #False if empty
    rc = encoders['rc']
    isRC = True if rc else False   #False if empty
    # Define categorical pipeline (one_hot)
    # TODO: feature hashing
    cat_pipe = Pipeline([
            ('selector', ColumnSelector(categorical)),
    ])
    # Below code assums all cat cols are for RC or DC
    # TODO: support mixed encoders
    if isDC:
        one_hot = preprocessing.OneHotEncoder()
        cat_pipe.steps.append(['onehot', one_hot])
    elif isRC:
        recode = preprocessing.OrdinalEncoder()
        cat_pipe.steps.append(['recode', recode])

    if scale:
        norm = preprocessing.StandardScaler(with_mean=False)
        cat_pipe.steps.append(['normalize', norm])

    print(cat_pipe)

    # Wrap the pipelines in a FeatureUnion 
    # Note: n_jobs = -1 means 'All CPUs'
    preprocessor = FeatureUnion([
            ('num', num_pipe),
            ('cat', cat_pipe)
    ], n_jobs=1, verbose=True)

    # Run fit_transform 3 times and record time
    if save:
        for i in range(3):
            t1 = time.time()
            transformed = preprocessor.fit_transform(X) #sparse
            timeres[i] = timeres[i] + ((time.time() - t1) * 1000) #millisec
        print(np.shape(transformed))
        print("Elapsed time for transformations using FeatureUnion in millsec")
        print(timeres)
        resfile = resultfile
        np.savetxt(resfile, timeres, delimiter="\t", fmt='%f')
    else:
        t1 = time.time()
        transformed = preprocessor.fit_transform(X) #sparse
        print("Elapsed time for Transform = %s sec" % (time.time() - t1))

    # Return the transformed data
    return transformed 



