

import pandas as pd 

y = pd.read_csv("data/kdd98/cup98tar.csv",on_bad_lines="skip")
x = pd.read_csv("data/kdd98/cup98val.csv",on_bad_lines="skip")

z = pd.merge(x, y, on="CONTROLN").drop(['CONTROLN', "TARGET_B"], axis=1)

z.to_csv("data/kdd98/cup98valj.csv",index=False)