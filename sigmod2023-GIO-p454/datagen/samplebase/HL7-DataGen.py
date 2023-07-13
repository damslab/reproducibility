
import os
import sys

class HL7DataGen(object):
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

        for i in range(1, int(count/1024)+1):
            for l in self.lines:
                print(l.strip(), file=dataFile)

        dataFile.close()


if __name__ == '__main__':
    inFileName = sys.argv[1]
    outFileName = sys.argv[2]
    nrows = int(sys.argv[3])
    dg = HL7DataGen(inFileName=inFileName, outFileName=outFileName)
    dg.generateData(nrows)
