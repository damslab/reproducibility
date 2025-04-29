import pandas as pd
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

dummy_spec = data.columns[[i-1 for i in spec["dummycode"]]]
dummy_enc = pd.get_dummies(data, dtype=float, columns=dummy_spec, sparse=True)


print(dummy_enc.shape)
print(f"endTime: {time.time() - t1} sec")