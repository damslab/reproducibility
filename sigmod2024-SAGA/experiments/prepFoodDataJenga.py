# read and classify the dataset
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing

data = "../data/Food_Inspections.csv"
def prepareFood(data):
    df = pd.read_csv(data, header=0, sep=",", encoding="latin-1")
    df.drop("Inspection ID", axis=1, inplace=True)
    df.drop("Inspection Date", axis=1, inplace=True)
    df.drop("Location", axis=1, inplace=True)
    df.drop("State", axis=1, inplace=True)
    df.drop("AKA Name", axis=1, inplace=True)
    df.drop("DBA Name", axis=1, inplace=True)
    df = df.dropna()
    df = df[df.Results.isin(["Pass", "Fail"])]
    df = df[df.City.isin(["CHICAGO"])]
    df = df[df.Risk.isin(["Risk 1 (High)", "Risk 2 (Medium)"])]
    df = df[df["Inspection Type"].isin(["Complaint", "License", "Consultation", "Canvass"])]
    df = df[df["Facility Type"].isin(["Restaurant", "Bakery", "School", "Grocery Store", "Liquor"])]
    df = df.groupby('Address').filter(lambda x: len(x) > 10)
    df.drop("City", axis=1, inplace=True)
    df = df.applymap(lambda s: s.lower() if type(s) == str else s)
    return df



if __name__ == '__main__':
    df = prepareFood(data)