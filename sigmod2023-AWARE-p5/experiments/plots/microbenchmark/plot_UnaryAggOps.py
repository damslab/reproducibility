import plot_util

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-x", "--machines", nargs="+", required=False)
args = parser.parse_args()
machinesList = args.machines


small = ["colsum", "sum", "scaleshift", "divvector"]

large = ["tsmm"]

plus = ["", "+"]

for machine in machinesList:
    for p in plus:
        yticks = [ 1, 10, 100, 1000]

        for s in small:
            data = plot_util.pars(
                "plots/microbenchmark/tab/table_"+s+p+"_"+machine+".csv")
            if data != {}:
                plot_util.plotBarPartial(
                    data, "plots/microbenchmark/ua/"+s+p+"_"+machine+".pdf", yticks)
        # data = plot_util.pars(
        #     "plots/microbenchmark/table_colsum"+p+"_"+machine+".csv")
        # if data != {}:
        #     plot_util.plotBarPartial(
        #         data, "plots/microbenchmark/ua/colsum"+p+"_"+machine+".pdf", yticks)

        # data = plot_util.pars(
        #     "plots/microbenchmark/table_sum"+p+"_"+machine+".csv")
        # if data != {}:
        #     plot_util.plotBarPartial(
        #         data, "plots/microbenchmark/ua/sum"+p+"_"+machine+".pdf", yticks)

        # data = plot_util.pars(
        #     "plots/microbenchmark/table_sum+"+p+"_"+machine+".csv")
        # if data != {}:
        #     plot_util.plotBarPartial(
        #         data, "plots/microbenchmark/ua/sum+"+p+"_"+machine+".pdf", yticks)

        yticks = [10, 100, 1000, 10000, 100000]
        for l in large:
            data = plot_util.pars(
                "plots/microbenchmark/tab/table_"+l+p+"_new_"+machine+".csv")
            if data != {}:
                plot_util.plotBarPartial(
                    data, "plots/microbenchmark/ua/"+l+p+"_"+machine+".pdf", yticks)
