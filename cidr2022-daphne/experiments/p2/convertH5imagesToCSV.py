#!/usr/bin/env python3

import h5py
import numpy as np
import pandas as pd
import sys
import os

mtd_prefix = """ 
{
    "data_type": "matrix",
    "value_type": "double",
"""

mtd_suffix = """     
    "format": "csv",
    "header": false,
    "sep": ","
}
"""

if len(sys.argv) < 3:
    print("usage: " + sys.argv[0] + " <in-file> <dataset> [NCHW] [nomean]")
    sys.exit()
    
convert_to_nchw = False
if "NCHW" in sys.argv: 
    convert_to_nchw = True

remove_mean = False
if "nomean" in sys.argv:
    remove_mean = True

input_file = sys.argv[1]
dataset = sys.argv[2]

out_file = input_file[:-3] + "_" + dataset
if dataset != "label":
    if convert_to_nchw:
        out_file += "_NCHW"
    else:
        out_file += "NHWC"
    if remove_mean:
        out_file += "_nomean"
    
out_file += ".csv"

fid = h5py.File(input_file,'r')
print('Datasets in \''+input_file+'\':')
print(fid.keys())

print('Loading ' + dataset + '...')
ds = np.array(fid[dataset])
print(ds.shape)
if remove_mean:
    ds_mean = np.mean(ds, axis=0)
    ds -= ds_mean
    
if ds.ndim > 2:
    if convert_to_nchw:
        print("converting to NCHW")
        ds = np.moveaxis(ds, -1, 1)
    ds = ds.reshape(ds.shape[0], ds.shape[1] * ds.shape[2] * ds.shape[3])
    print("reshaped to " + str(ds.shape))
else:
    print("ndim: " + str(ds.ndim))
    
df = pd.DataFrame(ds)
df.to_csv(out_file, index=False, header=False)

meta= str(ds.shape[0]) + "," + str(ds.shape[1]) + ",1,f32,\n"
mtd = mtd_prefix + "    \"rows\": " +  str(ds.shape[0]) + ",\n    \"cols\": " +  str(ds.shape[1]) + "," + mtd_suffix

with open(out_file + ".meta", 'w') as f:
    f.write(meta)

with open(out_file + ".mtd", 'w') as f:
    f.write(mtd)
