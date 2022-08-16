from smac.scenario.scenario import Scenario
import autosklearn.metrics
import pandas as pd
from sklearn.metrics import accuracy_score
import sys
import os
from autosklearn.experimental.askl2 import AutoSklearn2Classifier
from smac.optimizer.smbo import SMBO
from smac.runhistory.runhistory import RunInfo, RunValue

os.environ["OPENBLAS_NUM_THREADS"] = "8"

dataName = sys.argv[1]
t = sys.argv[2]
sep=","

train="../autosklearn/clean/"+dataName+"/train.csv"
test="../autosklearn/clean/"+dataName+"/test.csv"

if __name__ == '__main__':


	print("reading data from: "+train)
	print("started: "+dataName+" with "+str(t))
	# SMAC scenario object
	scenario_dict = {
		"run_obj": "quality",  # we optimize quality (alternative to runtime)
		"deterministic": True,
		"limit_resources": True,  # Uses pynisher to limit memory and runtime
		"cutoff": 3,  # runtime limit for the target algorithm
		}

	loadedDataTrain = pd.read_csv(train, na_values={"", " ", "?"}, header=0, sep=sep)
	loadedDataTest = pd.read_csv(test, na_values={"", " ", "?"}, header=0, sep=sep)

	loadedDataTrain.info()
    
	loadedDataTrain[[col for col in loadedDataTrain.columns if loadedDataTrain[col].dtypes == object]] =\
	loadedDataTrain[[col for col in loadedDataTrain.columns if loadedDataTrain[col].dtypes == object]].astype('category')

	loadedDataTrain.info()
    
	loadedDataTest[[col for col in loadedDataTest.columns if loadedDataTest[col].dtypes == object]] =\
	loadedDataTest[[col for col in loadedDataTest.columns if loadedDataTest[col].dtypes == object]].astype('category')
	loadedDataTest.info()
    
	print("data loaded")
	X_train, y_train = loadedDataTrain.iloc[:, :-1], loadedDataTrain.iloc[:, [-1]]
	X_test, y_test = loadedDataTest.iloc[:, :-1], loadedDataTest.iloc[:, [-1]]
	print("splits made")
	model =  AutoSklearn2Classifier(time_left_for_this_task=int(t)*60, per_run_time_limit=1200, memory_limit=100000, n_jobs=16,\
    max_models_on_disc=10, smac_scenario_args=scenario_dict)
	print("model constructed")
	# perform the search
	model.fit(X_train, y_train)
	print("model fit")
	# summarize
	print(model.sprint_statistics())
	# evaluate best model
	y_hat = model.predict(X_test)
	acc = accuracy_score(y_test, y_hat)
	print("Accuracy: %.3f" % acc)
	ensemble_dict = model.show_models()
	print("-----------------------show models------------------------")
	print(ensemble_dict)
    
