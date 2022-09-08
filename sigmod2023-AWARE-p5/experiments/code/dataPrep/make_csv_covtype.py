import pandas as pd
import os

df = pd.read_csv("data/covtype/covtype.data", header=None)
df = df.drop(columns=[0])
df.to_csv("data/covtype/removecol1.csv" ,header=False, index=False)
