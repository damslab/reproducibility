import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
import json
import sys
import time 

t1 = time.time()

data_path = sys.argv[1]
spec_path = sys.argv[2]
header = (int) (sys.argv[3])
delim = sys.argv[4]
if(delim == "t"):
    delim = "\t"
if header == 0:
    header = None

with open(data_path, 'r') as f:
    spec = json.load(f)
print(f"specTime: {time.time() - t1} sec")
data = pd.read_csv(spec_path, header=header, delimiter= delim)
print(f"readTime: {time.time() - t1} sec")

dummy_spec = list(data.columns[[i-1 for i in spec["dummycode"]]])

col_trasformer = ColumnTransformer([
    ("onehot", OneHotEncoder(sparse_output=True), dummy_spec)], 
    remainder=StandardScaler())
res = col_trasformer.fit_transform(data)
# print(res.shape)
print(f"endTime: {time.time() - t1} sec")
