# import pandas as pd
# import torch
# import json
# import sys
# import time
# import numpy as np

# t1 = time.time()

# data_path = sys.argv[1]
# spec_path = sys.argv[2]
# header = (int)(sys.argv[3])
# if header == 0:
#     header = None

# with open(data_path, "r") as f:
#     spec = json.load(f)
# print(f"specTime: {time.time() - t1} sec")
# data = pd.read_csv(spec_path, header=header)
# print(f"readTime: {time.time() - t1} sec")

# dummy_spec = list(data.columns[[i - 1 for i in spec["dummycode"]]])

# rows = torch.range(0, data.shape[0], 1, dtype=torch.int64)
# ones = torch.ones([data.shape[0]], dtype=torch.double)


# tmp_tensors = []
# for col in data.columns:
#     if col in dummy_spec:
#         recoded, values = pd.factorize(data[col])
#         # pd.replace()
#         recoded = torch.tensor(recoded)

#         # print(distincts.dtype)
#         # if isinstance(distincts, (np.ndarray, np.generic)) and None in distincts:
#         # recoded.replace(-1, 0)
#         # el

#         # if pd.isna().any():
#         # recoded[recoded==-1] = 0
#         # recoded.replace(-1, 0)

#         # print(min(recoded))
#         # print(distincts)
#         # oneH = torch.nn.functional.one_hot(recoded, len(distincts))
#         # oneHS = oneH.to_sparse()

#         oneH = torch.sparse_csr_tensor(rows, recoded, ones, size=(data.shape[0], len(values)), dtype=torch.double)
#         print(oneH)
#         tmp_tensors.append(oneH)

# print(f"BeforeCombine: {time.time() - t1} sec")
# res = torch.geom
# res = torch.cat(tmp_tensors, 1)

# print(f"endTime: {time.time() - t1} sec")
