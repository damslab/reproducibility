import sys

from scipy.io import mmread
import math


class readMM(object):
    def __init__(self, data_file_name, cols):
        self.data_file_name = data_file_name
        self.cols = cols
        self.data = None
        self.__load_data()

    def __load_data(self):
        mm = (mmread(self.data_file_name))
        #mmt = mm.todense()
        #self.data = pd.DataFrame(mmt, range(1, mmt.shape[0] + 1), range(1, mmt.shape[1] + 1))
        #self.data = self.data[self.cols]

if __name__ == "__main__":
    data_file_name = sys.argv[1]
    projection = sys.argv[2]
    projection_type = projection[0:1]
    cols = []
    if projection_type == "Q":  # Projection is for Queries
        if "graph500" in data_file_name:
            if projection == "Q1":
                cols = [1]
            elif projection == "Q2":
                cols = [1, 32, 1024, 32768, 1048576]
        elif "moliere" in data_file_name:
            if projection == "Q1":
                col = [1]
            elif projection == "Q2":
                cols = [1, 32, 1024, 32768, 1048576]
        elif "queen" in data_file_name :
            if projection == "Q1":
                cols = [1]
            elif projection == "Q2":
                cols = [1, 16, 256, 4096, 65536]

        elif "relat9" in data_file_name:
            if projection == "Q1":
                cols = [1]
            elif projection == "Q2":
                cols = [1, 16, 256, 4096, 65536]

    else:  # Projection for a range start from 0
        number_of_fields = projection[1:]
        cols = list(range(1, int(math.pow(2, int(number_of_fields)))+1))

    # projection on columns is not work in python lib
    readMM(data_file_name=data_file_name, cols=cols)
