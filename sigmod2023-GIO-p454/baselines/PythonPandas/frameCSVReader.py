import sys

import pandas as pd


class readCSV(object):
    def __init__(self, data_file_name, cols, delim, dataType):
        self.data_file_name = data_file_name
        self.cols = cols
        self.data = None
        self.delim = delim
        self.dataType = dataType
        self.__load_data()

    def __load_data(self):
        if self.dataType is not None:
            data = pd.read_csv(self.data_file_name, sep=self.delim, header=None, usecols=self.cols, dtype=str)
        else:
            data = pd.read_csv(self.data_file_name, sep=self.delim, header=None, usecols=self.cols)
        self.data = pd.DataFrame(data)


if __name__ == "__main__":
    data_file_name = sys.argv[1]
    projection = sys.argv[2]
    projection_type = projection[0:1]
    cols = []
    delim = '\t'
    datatype = None
    if projection_type == "Q":  # Projection is for Queries
        if "yelp" in data_file_name:
            if projection == "Q1":
                cols = [0]
            elif projection == "Q2":
                cols = [0, 8, 3]
    else:  # Projection for a range start from 0
        number_of_fields = projection[1:]
        if "ReWasteF" in data_file_name:
            nof = int(number_of_fields)
            if nof == 0:
                cols = [0]
            else:
                cols = list(range(0, min(int(nof*10), 313)))
            delim = ','
            datatype = 'STRING'
        else:
            cols = list(range(0, int(number_of_fields)))
    # print(f'{projection} -- {cols}')
    readCSV(data_file_name=data_file_name, cols=cols, delim=delim, dataType=datatype)
