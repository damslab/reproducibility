#!/usr/bin/env python3

import h5py
import numpy as np
import pandas as pd
import os
import sys

if len(sys.argv) < 2:
    print("usage: " + sys.argv[0] + " <in-file>")
    sys.exit()
    
input_file = sys.argv[1]
export_dir = input_file[:-3] + "_hdf2csv"

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

def visit_func(name, node) :
    #print ('Full object pathname is:', node.name)
    if isinstance(node, h5py.Group) :
        return
        #print ('Object:', name, 'is a Group\n')
    elif isinstance(node, h5py.Dataset) :
        data = np.array(node)
        #print("ndim=" + str(data.ndim) + " shape=" + str(data.shape))
        node_split = node.name.split('/')
        fname=node_split[-2:][0]
        suffix = node_split[-1:][0].split(':')[0]
        filename = fname + "_" + suffix + ".csv"
        if data.ndim == 4:
            data = np.moveaxis(data, -1, 1) # nhwc -> nchw
            data = data.reshape(data.shape[1], data.shape[0] * data.shape[2] * data.shape[3])
            metadata = str(data.shape[0]) + "," + str(data.shape[1]) + ",1,f32,\n"
            mtd = mtd_prefix + "    \"rows\": " +  str(data.shape[0]) + ",\n    \"cols\": " +  str(data.shape[1]) + "," + mtd_suffix
            #print(fname)
        elif data.ndim == 2:
                metadata = str(data.shape[0]) + "," + str(data.shape[1]) + ",1,f32,\n"
                mtd = mtd_prefix + "    \"rows\": " +  str(data.shape[0]) + ",\n    \"cols\": " +  str(data.shape[1]) + "," + mtd_suffix
        else:
            #data = data.reshape(data.shape[0], 1)
            #print(name)
            #print(data.shape)
            if "dense" in name:
                data = data.reshape(1,data.shape[0])
                metadata = "1," + str(data.shape[1]) + ",1,f32,\n"
                mtd = mtd_prefix + "    \"rows\": 1" + ",\n    \"cols\": " +  str(data.shape[1]) + "," + mtd_suffix
            else:
                metadata = str(data.shape[0]) + ",1,1,f32,\n"
                mtd = mtd_prefix + "    \"rows\": " +  str(data.shape[0]) + ",\n    \"cols\": " +  str(1) + ",\n" + mtd_suffix

        #data.tofile(os.path.join(export_dir,filename), sep = ',')
        pd.DataFrame(data).to_csv(os.path.join(export_dir,filename), index=False, header=False)
        with open(os.path.join(export_dir, filename + ".meta"), 'w') as f:
            f.write(metadata)
        
        with open(os.path.join(export_dir, filename + ".mtd"), 'w') as f:
            f.write(mtd)
        #print(metadata + "    " + str(node.dtype))
    else :
        print ('Object:', name, 'is an unknown type\n')

export_dir = os.path.join("./", export_dir)
if not os.path.exists(export_dir):  # os.path.join() for making a full path safely
    print(export_dir)
    os.makedirs(os.path.join(export_dir))  # If not create the directory, inside their home directory
else:
    print("Export directory already exists. Stopping.")
    sys.exit()
    
with h5py.File(input_file, 'r') as h5r:     
    #h5r.visititems(visit_func)
    h5r["model_weights"].visititems(visit_func)
