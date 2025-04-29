
import sys

def parseAndPrint(file):
   with open(file, "r") as f:
      for l in f: 
         split = l.split(",")
         print(",".join(split[:469]) + ","+split[471] )

parseAndPrint(sys.argv[1])