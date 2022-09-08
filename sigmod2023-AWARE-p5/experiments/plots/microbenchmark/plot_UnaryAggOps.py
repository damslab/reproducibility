
import plot_util

machinesList = ["XPS-15-7590", "tango"]

small = ["colsum", "sum", "scaleshift", "divvector"]

large = ["tsmm"]

plus = ["", "+"]

for machine in machinesList:
    for p in plus:
        yticks = [ 1, 10, 100, 1000]

        for s in small:
            data = plot_util.pars(
                "plots/microbenchmark/table_"+s+p+"_"+machine+".csv")
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
                "plots/microbenchmark/table_"+l+p+"_new_"+machine+".csv")
            if data != {}:
                plot_util.plotBarPartial(
                    data, "plots/microbenchmark/ua/"+l+p+"_"+machine+".pdf", yticks)
