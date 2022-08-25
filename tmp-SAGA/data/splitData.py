import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split


dataName = sys.argv[1]
dataIn = sys.argv[2]

if not os.path.exists(dataName):
    os.makedirs(dataName)
    
if __name__ == '__main__':
    headSym = 0
    loadedDataTest = pd.read_csv(dataIn, na_values={"?", "", " ", "NA"}, header=headSym, encoding='latin-1', sep=',')

    X = loadedDataTest.iloc[:, :-1]
    y = loadedDataTest.iloc[:, [-1]]
    trainset_features, test_features, trainset_labels, test_labels = train_test_split(X, y, test_size=0.3, random_state=1,
                                                                                       # stratify=y
                                                                                      )

    df2 = pd.DataFrame(test_features)
    df2['class'] = test_labels
    df2.to_csv(out+"/test.csv", index=False, header=True, sep=",", encoding='utf-8')


    df = pd.DataFrame(trainset_features)
    df['class'] = trainset_labels

    X1  = df.iloc[:, :-1]
    y1 = df.iloc[:, [-1]]
    train_features, val_features, train_labels, val_labels = train_test_split(X1, y1, test_size=0.3, random_state=1,
                                                                             # stratify=y1
                                                                              )
    df3 = pd.DataFrame(train_features)
    df3['class'] = train_labels

    df4 = pd.DataFrame(val_features)
    df4['class'] = val_labels

    df5 = df3.append(df4)
    df5.to_csv(out+"/train.csv", index=False, header=True, sep=",", encoding='utf-8')

