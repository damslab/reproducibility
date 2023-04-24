
import plot_util
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-x", "--machines", nargs="+", required=False)
args = parser.parse_args()
machinesList = args.machines

plus = ["", "+"]

tech = ["plus"]

for machine in machinesList:
    for p in plus:
        for t in tech:
            yticks = [1, 10, 100, 1000, 10000, 100000]
            data = plot_util.pars("plots/microbenchmark/tab/table_scalar_"+t+p+"_"+machine+".csv")
            if data != {}:
                plot_util.plotBarPartial(data, "plots/microbenchmark/sc/"+t+p+"_"+machine+".pdf", yticks)

            # data = plot_util.pars("plots/microbenchmark/table_scalar_plus_tango.csv")
            # if data != {}:
            #     plot_util.plotBar(data, "plots/microbenchmark/sc/scalar_plus_tango.pdf",yticks)

            # yticks = [0.1, 1, 10, 100, 1000, 10000, 100000]
            # data = plot_util.pars("plots/microbenchmark/table_scalar_mult_XPS-15-7590.csv")
            # if data != {}:
            #     plot_util.plotBar(data, "plots/microbenchmark/sc/scalar_mult_XPS.pdf",yticks)

            # data = plot_util.pars("plots/microbenchmark/table_scalar_mult_tango.csv")
            # if data != {}:
            #     plot_util.plotBar(data, "plots/microbenchmark/sc/scalar_mult_tango.pdf",yticks)
