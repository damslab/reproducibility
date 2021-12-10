require(graphics)
require(Matrix)

pdf(file="plots/Experiment1b.pdf",
  width=3.7, height=4.0, family="serif", pointsize=14)

data1 = rowMeans(matrix(as.matrix(read.table("results/Experiment1_times.dat", sep=","))[,2],5,3,byrow=TRUE))

data = as.matrix(data1/1000)
data

plot_colors <- c("cornflowerblue","gray40","black","orange","orangered")

barplot( data, 
         space = c(0.5,0.5),
         xlab = "", 
         ylab = "",
         col=plot_colors,
         ylim = c(1,245),
         log = "y",
         axes = FALSE, 
         names.arg = c("Deduplication and Pruning"),
         args.legend = list(x="topleft", bty="n", bty="n", ncol=1),
         beside = TRUE,
)

legend( 0, 290,
       c("No dedup","No parents, sc, ss","No parents, sc","No parents", "All"), fill=plot_colors[5:1], 
       bty="n", x.intersp=0.7);


axis(2, las=1) 
mtext(2,text="Execution Time [s]",line=2.7) 
mtext(1,text="Configurations",line=2) 


box()	              # box around plot       
dev.off() 
