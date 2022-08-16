import autosklearn.classification
import autosklearn.metrics
import pandas as pd
from sklearn.metrics import accuracy_score
import sys

dataName = sys.argv[1]
sep=","

train="clean/"+dataName+"/train.csv"
test="clean/"+dataName+"/test.csv"
if __name__ == '__main__':
	print("started: "+dataName+" 200")
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
	model =  autosklearn.classification.AutoSklearnClassifier(time_left_for_this_task=200*60, per_run_time_limit=1200, n_jobs=16, memory_limit=100000)
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
  