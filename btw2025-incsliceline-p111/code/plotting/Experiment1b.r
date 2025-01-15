require(graphics)
require(Matrix)

pdf(file="plots/Experiment1b.pdf",
  width=7.3, height=4.5, family="serif", pointsize=14)

data0 = colMeans(read.table("results/Exp1_0.csv", sep=",")[2:10,])

data0

plot_colors <- c("orangered","orange","cornflowerblue")

barplot( data0,
         space = c(0.5, 0, 0),
         xlab = "",
         ylab = "",
         col=plot_colors,
         ylim = c(0.4,700),
         log = "y",
         axes = FALSE,
         names.arg = c("","","","","","","","","","","",""),
         args.legend = list(x="topleft", bty="n", bty="n", ncol=1),
         legend.text = c("SliceLine","IncSliceLine Init","IncSliceLine"),
         beside = TRUE,
#         line=-0.9
)

axis(1, at=c(2,5.5,9,12.5), labels=c("Adult","Covtype","KDD98","USCensus"))
axis(2, las=1,at=c(0.5,1,2,5,10,20,50,100,200,500), labels=c("0.5","1","2","5","10","20","50","100","200","500"))
mtext(2,text="Execution Time [s]",line=2.7)
mtext(1,text="Datasets",line=2.3)
text(x=1.9, y=40, labels=c("Approx"))

box()	              # box around plot
dev.off()
