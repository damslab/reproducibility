#!/usr/bin/env python
import os

from sklearn.linear_model import LogisticRegressionCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from activedetect.loaders.csv_loader import CSVLoader
from sklearn.ensemble import RandomForestClassifier
from activedetect.experiments.Experiment import Experiment
from sklearn import preprocessing
import sys
"""
Example Experiment Script
"""
data = sys.argv[1]
label = sys.argv[2]
output =  sys.argv[3]


dataName = data
baseline = output
dataIn = "/home/ssiddiqi/papers/cleaning/experiments/pipelines/data/" + dataName+"/train.csv"
dataInTest = "/home/ssiddiqi/papers/cleaning/experiments/pipelines/data/" + dataName+"/test.csv"
if not os.path.exists(baseline):
    os.makedirs(baseline)


if __name__ == '__main__':

    c = CSVLoader(delimiter=",", header=True)
    # # # load training data
    loadedData = c.loadFile(dataIn)
    #all but the last column are features
    features = [l[0:-1] for l in loadedData]
    print(features[1:5])
    #last column is a label, turn into a float
    le = preprocessing.LabelEncoder()
    trainY = [l[-1] for l in loadedData]
    print("train y")
    print(trainY[1:10])
    le.fit(trainY)
    labels = le.transform(trainY)
    print("labels")
    print(labels[1:25])
    
    
    # # # load test data
    loadTest = c.loadFile(dataInTest)
    testX =  [l[0:-1] for l in loadTest]
    testY = [l[-1] for l in loadTest]
    testY = le.transform(testY)

    e = Experiment(features, labels, LogisticRegression(multi_class='multinomial', solver='newton-cg', penalty='l2', tol=1e-4, max_iter=1000), baseline, testX, testY)
    e.runAllAccuracy()
    print "train dim: rows * cols"
    print len(features)
    print len(features[0])
