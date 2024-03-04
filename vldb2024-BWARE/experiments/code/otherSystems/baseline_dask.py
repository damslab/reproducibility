# import pandas as pd
import dask.dataframe as dd
import dask_ml.preprocessing as dp
from dask_ml.compose import ColumnTransformer
import json
import sys
import time 
import pandas as pd

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

dummy_spec = data.columns[[i-1 for i in spec["dummycode"]]]

cat = dp.Categorizer(columns=dummy_spec)
data = cat.fit_transform(data)
print(data.shape)

dc = dp.DummyEncoder(columns=dummy_spec)
res = dc.fit_transform(data)

print(res.shape)
print(f"endTime: {time.time() - t1} sec")