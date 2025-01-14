#-------------------------------------------------------------
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
#-------------------------------------------------------------

import pandas as pd
import numpy as np
import shap
import sklearn as sk
import time
import os
from sklearn.svm import SVC
import datetime
from joblib import load

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense, Dropout
from tensorflow.keras.optimizers import SGD

# for command line args
import argparse
parser=argparse.ArgumentParser(description="Run permutation shap and time it.")
parser.add_argument("--data-dir", default="../10_data/adult/", help="Path to CSV with X data.")
parser.add_argument("--data-x", default="Adult_X.csv", help="Path to CSV with X data.")
parser.add_argument("--data-y", default="Adult_y.csv", help="Path to CSV with y data.")
parser.add_argument("--model-type", default="multiLogReg", help="Model type to use.")
parser.add_argument("--result-file-name", default="python_shap_values.csv", help="File to write computed shap values to.")
parser.add_argument("--n-instances", help="Number of instances.", default=1)
parser.add_argument("--n-permutations", help="Number of permutations.", default=1)
parser.add_argument("--n-samples", help="Number of permutations.", default=100)
parser.add_argument('--silent', action='store_true', help='Don\'t print a thing.')
parser.add_argument('--just-print-t', action='store_true', help='Don\'t store, just print time at end.')
parser.add_argument('--write-t-to', default="", help='Write time to file so testscript can read it from there.')
args=parser.parse_args()


#%%
#load prepared data into dataframe

df_x = pd.read_csv(args.data_dir+args.data_x, header=None)
df_y = pd.read_csv(args.data_dir+args.data_y, header=None)


#%%
#load model
if args.model_type != "l2svm":
    model = load(args.data_dir+"models/"+args.model_type+".joblib")
    X_train, X_test, y_train, y_test = sk.model_selection.train_test_split(df_x.values, df_y.values.ravel(), test_size=0.2, random_state=42)

    if args.model_type == "fnn":
        y_train = y_train - 1
        y_test = y_test - 1
        y_pred = model.predict(X_test, verbose=0)
    else:
        y_pred = model.predict(X_test)
        
        if args.model_type == "multiLogReg":
            accuracy = sk.metrics.accuracy_score(y_test, y_pred)
            conf_matrix = sk.metrics.confusion_matrix(y_test, y_pred)
        
        if not args.silent:
            print(f"Accuracy: {accuracy}")
            print(f"Confusion Matrix:\n{conf_matrix}")
else:
    #%%
    #add faster svm function
    bias=[]
    if args.model_type == "l2svm":
        bias = np.genfromtxt(args.data_dir+"models/Census_SVM.csv", delimiter=',')
def l2svmPredict(X):
    W=bias
    n, m = X.shape
    wn = len(W)
    if m != wn:
        YRaw = np.dot(X, W[:m-1]) + W[m]
    else:
        YRaw = np.dot(X, W)
    return YRaw

#%%
#create SHAP  explainer
if not args.silent:
    print(int(args.n_permutations))
start_exp = time.time()
permutation_explainer = None

if args.model_type == "multiLogReg":
    permutation_explainer = shap.explainers.Permutation(model.predict_proba, shap.maskers.Independent(df_x.values, max_samples=int(args.n_samples)))
elif args.model_type == "l2svm":
    permutation_explainer = shap.explainers.Permutation(l2svmPredict, shap.maskers.Independent(df_x.values, max_samples=int(args.n_samples)))
elif args.model_type == "fnn":
    predict_func = lambda x: model.predict(x, verbose=0, batch_size=1028)
    permutation_explainer = shap.explainers.Permutation(predict_func, shap.maskers.Independent(df_x.values, max_samples=int(args.n_samples)))
else:
    print("Model of type "+args.model_type+" unknown.")
    exit()

#run explainer
shap_values = permutation_explainer(df_x.iloc[0:int(args.n_instances)],
                                    max_evals=2*len(df_x.iloc[1])*(int(args.n_permutations)), batch_size=10)
end_exp = time.time()
total_t=end_exp-start_exp

if not args.silent:
    print("Time:", total_t, "s")
#%%

if args.write_t_to != "":
    with open(args.write_t_to, "w") as tempfile:
        tempfile.write(str(total_t))
if args.just_print_t:
    print(str(total_t))
else:
    df_shap_values = pd.DataFrame(shap_values.values)
    df_shap_values.to_pickle(args.result_file_name)
