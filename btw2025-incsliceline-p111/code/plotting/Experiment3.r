require(graphics)
require(Matrix)

pdf(file="plots/Experiment3.pdf",
  width=7.3, height=4.5, family="serif", pointsize=14)

data0 = colMeans(read.table("results/Exp3.csv", sep=",")[2:5,])
X = matrix(data0, 4, 8, byrow=TRUE)
X = cbind(X[,1],X[,2],X[,8],X[,5],X[,7],X[,6],X[,4],X[,3])

X = matrix(t(X), 32, 1, byrow=TRUE)


plot_colors <- c("orangered","orange","black","slategray1","slategray2","slategray3","slategray4","cornflowerblue")

barplot( X,
         space = c(0.5, 0, 0, 0, 0, 0, 0, 0),
         xlab = "",
         ylab = "",
         col=plot_colors,
         ylim = c(0.4,1700),
         log = "y",
         axes = FALSE,
         names.arg = c("","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""),
         args.legend = list(x="topleft", bty="n", bty="n", ncol=4, cex=0.96),
         legend.text = c("SliceLine","IncSL Init","None","Score","Size","MaxScore","All Exact", "+ Approx"),
         beside = TRUE,
#         line=-0.9
)

axis(1, at=c(4.5,13,21.5,30), labels=c("Adult","Covtype","KDD98","USCensus"))
axis(2, las=1,at=c(0.5,1,2,5,10,20,50,100,200,500), labels=c("0.5","1","2","5","10","20","50","100","200","500"))
mtext(2,text="Execution Time [s]",line=2.7)
mtext(1,text="Datasets",line=2.3)

box()	              # box around plot
dev.off()

