
# * **MCAR** Missing completely at random
# * **MAR** Missing at random - corruption is conditioned on other column

# In[1
import random

import pandas as pd
import numpy as np
from jenga.corruptions.generic import MissingValues


from src.jenga.basis import TabularCorruption
from src.jenga.corruptions import generic


def foodInspectionMissing(data, missingness):
    for i in np.arange(0.0, 0.7, 0.1):
        df = pd.read_csv(data)
        df['License #'] = MissingValues(column='License #', fraction=i, missingness=missingness).transform(df)['License #']
        df['Facility Type'] = MissingValues(column='Facility Type', fraction=i, missingness=missingness).transform(df)['Facility Type']
        df['Risk'] = MissingValues(column='Risk', fraction=i, missingness=missingness).transform(df)['Risk']
        df['Address'] = MissingValues(column='Address', fraction=i, missingness=missingness).transform(df)['Address']
        df['Zip'] = MissingValues(column='Zip', fraction=i, missingness=missingness).transform(df)['Zip']
        df['Inspection Type'] = MissingValues(column='Inspection Type', fraction=i, missingness=missingness).transform(df)['Inspection Type']
        df['Latitude'] = MissingValues(column='Latitude', fraction=i, missingness=missingness).transform(df)['Latitude']
        df['Longitude'] = MissingValues(column='Longitude', fraction=i, missingness=missingness).transform(df)['Longitude']
        df.to_csv("Food/"+str(missingness.lower())+"/food_"+str(missingness.lower())+"_"+str(i)+".csv", sep=',', index=False, header=True)
        print("file name: ", "Food/food_"+str(missingness.lower())+"_"+str("%.1f" %i)+".csv")


def foodInspectionVFD(data, missingness):
    for i in np.arange(0.0, 0.6, 0.1):
        df = pd.read_csv(data)
        df['Zip'] = MissingValues(column='Zip', fraction=i, missingness=missingness).transform(df)['Zip']
        df.to_csv("Food/vfd/food_vfd_"+str("%.1f" % i)+".csv", sep=',', index=False, header=True)
        print("file name: ", "Food/vfd/food_vfd_"+str(i)+".csv")


from jenga.corruptions.numerical import GaussianNoise

def foodInspectionGaussianNoise(data, missingness):
    for i in np.arange(0.0, 0.7, 0.1):
        df = pd.read_csv(data)
        df['Latitude'] = GaussianNoise(column='Latitude', fraction=i, sampling=missingness).transform(df)['Latitude']
        df['Longitude'] = GaussianNoise(column='Longitude', fraction=i, sampling=missingness).transform(df)['Longitude']
        df.to_csv("Food/GN/"+str(missingness.lower())+"/food_gn_"+str("%.1f" % i)+".csv", sep=',', index=False, header=True)
        print("file name: ", "Food/GN/"+str(missingness.lower())+"/food_GN_"+str("%.2f" % i)+".csv")

from jenga.corruptions.numerical import Scaling

def foodInspectionScaling(data, missingness):
    for i in np.arange(0.0, 0.5, 0.1):
        df = pd.read_csv(data)
        df['Latitude'] = Scaling(column='Latitude', fraction=i, sampling=missingness).transform(df)['Latitude']
        df['Longitude'] = Scaling(column='Longitude', fraction=i, sampling=missingness).transform(df)['Longitude']
        df.to_csv("Food/scale/"+str(missingness.lower())+"/food_scale_"+str("%.1f" % i)+".csv", sep=',', index=False, header=True)
        print("file name: ", "Food/scale/"+str(missingness.lower())+"/food_scale_"+str(i)+".csv")


from jenga.corruptions.generic import SwappedValues

def foodInspectionSwap(data, missingness):
    for i in np.arange(0.0, 0.5, 0.1):
        df = pd.read_csv(data)
        df['License #'] = SwappedValues(column='License #', fraction=i, sampling=missingness, swap_with="Facility Type").transform(df)['License #']
        df['Zip'] = SwappedValues(column='Zip', fraction=i, sampling=missingness, swap_with="Address").transform(df)['Zip']
        df.to_csv("Food/swap/"+str(missingness.lower())+"/food_swap_"+str("%.1f" % i)+".csv", sep=',', index=False, header=True)
        print("file name: ", "Food/swap/"+str(missingness.lower())+"/food_swap_"+str(i)+".csv")

# we randomly picks the column and introduce an error in it
# but we make sure that all five categories of errors are introduced
from jenga.corruptions.generic import CategoricalShift
def allErrors(data):
    for i in np.arange(0.4, 0.6, 0.1):
        df = pd.read_csv(data)
        cols = df.columns.tolist()
        numeric_cols, non_numeric_cols = CategoricalShift.get_dtype(None, df)
        numeric_cols.remove("Zip")
        print(numeric_cols)
        catCol = random.choice(non_numeric_cols)
        numCol = random.choice(numeric_cols)
        print(numCol)

        # 2. apply missing MCAR and MAR
        anyCol = random.choice(cols)
        cols.remove(anyCol)
        missingness = random.choice(["MAR", "MCAR"])
        df[anyCol] = MissingValues(column=anyCol, fraction=i, missingness=missingness).transform(df)[
            anyCol]
        # 3. apply GN errors
        numCol = random.choice(numeric_cols)
        missingness = random.choice(["MAR", "MCAR"])
        df[numCol] = GaussianNoise(column=numCol, fraction=i, sampling=missingness).transform(df)[
            numCol]
        # 4. violate functional dependency
        anyCol = random.choice(cols)
        cols.remove(anyCol)
        missingness = "MAR"
        df[anyCol] = MissingValues(column=anyCol, fraction=i, missingness=missingness).transform(df)[
            anyCol]

        df.to_csv("Food/allErrors/food_ae_"+str(i)+".csv", sep=',', index=False, header=True)
        print("file name: ", "Food/allErrors/food_ae_"+str(i)+".csv")





# print(df.isna().sum())
if __name__ == '__main__':
    foodInspectionVFD("D:/Workspace/Dataset/foodInsp.csv", "MAR")
    foodInspectionMissing("D:/Workspace/Dataset/foodInsp.csv", "MCAR")
    foodInspectionMissing("D:/Workspace/Dataset/foodInsp.csv", "MAR")
    foodInspectionGaussianNoise("D:/Workspace/Dataset/foodInsp.csv", "MAR")
    foodInspectionGaussianNoise("D:/Workspace/Dataset/foodInsp.csv", "MCAR")
    foodInspectionSwap("D:/Workspace/Dataset/foodInsp.csv", "MCAR")
    foodInspectionSwap("D:/Workspace/Dataset/foodInsp.csv", "MAR")
    foodInspectionScaling("D:/Workspace/Dataset/foodInsp.csv", "MAR")
    foodInspectionScaling("D:/Workspace/Dataset/foodInsp.csv", "MCAR")
    allErrors("D:/Workspace/Dataset/foodInsp.csv")