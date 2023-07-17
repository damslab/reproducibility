
import os
import sys

class ADFDataGen(object):
    def __init__(self, inFileName, outFileName):
        self.inFileName = inFileName
        self.outFileName = outFileName
        self.lines = self.loadSampleData()    

    def loadSampleData(self):
        with open(os.path.join(sys.path[0], self.inFileName), "r", encoding='latin-1') as file:
            lines = file.readlines()
            return lines
        
    def generateData(self, count):
        dataFile = open(self.outFileName, 'w')

        for i in range(1, int(count/5000)+1):
            for l in self.lines:
                print(l.strip(), file=dataFile)
            print("\n", file=dataFile)    

        dataFile.close()


if __name__ == '__main__':
    inFileName = sys.argv[1]
    outFileName = sys.argv[2]
    nrows = int(sys.argv[3])
    dg = ADFDataGen(inFileName=inFileName, outFileName=outFileName)
    dg.generateData(nrows)
