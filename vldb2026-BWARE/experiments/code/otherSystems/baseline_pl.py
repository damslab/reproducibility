import polars as pl
import json
import sys
import time 

t1 = time.time()


data_path = sys.argv[1]
spec_path = sys.argv[2]
header = (bool) (sys.argv[3])
header = (int) (sys.argv[3])
delim = sys.argv[4]
if(delim == "t"):
    delim = "\t"
header = header != 0


with open(data_path, 'r') as f:
    spec = json.load(f)
print(f"specTime: {time.time() - t1} sec")
data = pl.read_csv(spec_path, has_header=header, separator=delim)
print(f"readTime: {time.time() - t1} sec")

dummy_spec = [data.columns[x-1] for x in spec["dummycode"]]
dummy_enc = data.to_dummies(columns=dummy_spec)

print(f"endTime: {time.time() - t1} sec")


print(dummy_enc[0,0], dummy_enc[dummy_enc.shape[0]-1,dummy_enc.shape[1] -1 ])
print(f"extra: {time.time() - t1} sec")