require(graphics)
require(Matrix)

pdf(file="plots/Experiment1a.pdf",
  width=7.3, height=4.5, family="serif", pointsize=14)

data0 = colMeans(read.table("results/Exp1_1.csv", sep=",")[2:10,])

plot_colors <- c("orangered","orange","cornflowerblue")

barplot( data0,
         space = c(0.5, 0, 0),
         xlab = "",
         ylab = "",
         col=plot_colors,
         ylim = c(1,700),
         log = "y",
         axes = FALSE,
         names.arg = c("","","","","","","","","","","",""),
         args.legend = list(x="topleft", bty="n", bty="n", ncol=1),
         legend.text = c("SliceLine","IncSliceLine Init","IncSliceLine"),
         beside = TRUE,
#         line=-0.9
)

axis(1, at=c(2,5.5,9,12.5), labels=c("Adult","Covtype","KDD98","USCensus"))
axis(2, las=1)
mtext(2,text="Execution Time [s]",line=2.7)
mtext(1,text="Datasets",line=2.3)


box()	              # box around plot
dev.off()
