import argparse
import os

import numpy as np


numprint = "\\numprint{"
end = "}"


def makeBytes(v):

    if v > 1000000000:
        vf = v / 1000000000.0
        return "{0}{1:0.2f}{2} GB".format(numprint, vf, end)
    elif v > 1000000:
        vf = v / 1000000.0
        return "{0}{1:0.2f}{2} MB".format(numprint, vf, end)
    elif v > 1000:
        vf = v / 1000.0
        return "{0}{1:0.2f}{2} KB".format(numprint, vf, end)
    else:
        return "{0}{1}{2} B".format(numprint, v, end)


def formatRatio(v):
    if v > 100:
        return "{0}{1:0.0f}{2}".format(numprint, v, end)
    elif v > 10:
        return "{0}{1:0.1f}{2}".format(numprint, v, end)
    else:
        return "{0}{1:0.2f}{2}".format(numprint, v, end)


def pars(path):
    ratio = []
    sizeBlocks = []
    sparkOutSize = 0
    sparkInSize = 0
    InSizeSum = 0
    OutSizeSum = 0
    if os.path.isfile(path):
        with open(path) as f:
            for line in f:
                if "CompressionRatio" in line:
                    ratio.append(float(line[24:]))
                elif "Compressed Size" in line:
                    sizeBlocks.append(int(line[24:]))
                elif "SBCompress:" in line:
                    if " InSize:     " in line:
                        sparkInSize = int(line[29:])
                    elif "InBlockSize:   " in line:
                        InSizeSum = int(line[29:])
                    elif " OutSize:       " in line:
                        sparkOutSize = int(line[29:])
                    elif "OutBlockSize: " in line:
                        OutSizeSum = int(line[29:])

    # ratio - min - q1 - mean - q3 - max - blocks - spark - spark ratio

    if len(ratio) == 0 or sparkInSize == 0:
        return "NA", "NA", "NA"
    ratio = np.array(ratio)
    sizeBlocks = np.array(sizeBlocks)
    actualRatio = formatRatio(sparkInSize / sparkOutSize)
    # minRatio = formatRatio(min(ratio))
    # q1 = formatRatio(np.quantile(ratio, 0.25))
    # q2 = formatRatio(np.quantile(ratio, 0.5))
    # q3 = formatRatio(np.quantile(ratio, 0.75))
    # maxRatio = formatRatio(max(ratio))

    sparkOutString = makeBytes(sparkOutSize)
    sparkInString = makeBytes(sparkInSize)
    return actualRatio, sparkOutString, sparkInString

parser = argparse.ArgumentParser()
parser.add_argument("-x", "--machines", nargs="+", required=False)
args = parser.parse_args()
machinesArg = args.machines


header = """\\begin{tabular}{r|cr|cr|c}
\\toprule
          & \\multicolumn{2} {c|}{\\textbf{\\name-Mem}} & \\multicolumn{2} {c|}{\\textbf{\\name}} &                          \\\\
Blocksize & Ratio                                    & Total Size                           & Ratio & Total Size & ULA \\\\
\\midrule
"""

footer = """\\bottomrule
\end{tabular}"""
for machine in machinesArg:
    with open("plots/tables/compression_spark_" +machine+".tex", "w") as f:
        folder = "results/sparkCompression/census_enc/"+machine+"/"

        exp = ["1", "2", "16", "64", "256"]

        f.write(header)

        for x in exp:
            f.write(x + "K   \t")
            res = pars(folder + "clab" + x + "-spark.log")
            for d in res[:-1]:
                f.write(" &\t")
                f.write(d)
            res = pars(folder + "claWorkloadb" + x + "-spark.log")
            for d in res:
                f.write(" &\t")
                f.write(d)
            f.write("    \\\\\n")
        f.write(footer)

