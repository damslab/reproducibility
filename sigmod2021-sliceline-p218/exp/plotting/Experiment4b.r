require(graphics)
require(Matrix)

pdf(file="plots/Experiment4b.pdf",
  width=3.7, height=4.0, family="serif", pointsize=14)

input = as.matrix(read.table("results/Experiment4b_times.dat", sep=",")[3])
data = colMeans(matrix(input, 3, 4))/1000

data1 = data #data[c(35,15,25,5)]

plot_colors <- c("cornflowerblue","orange","black","orangered")

barplot( data1, 
         space = c(0.1,0.1),
         xlab = "", 
         ylab = "",
         col=plot_colors,
         ylim = c(1,900),
         log = "y",
         axes = FALSE, 
         cex.names=0.96,
         names.arg = c("KDD","USC","Cov","Adu"),
         args.legend = list(x="topleft", bty="n", bty="n", ncol=1),
         beside = TRUE,
)

axis(2, las=1) 
mtext(2,text="Execution Time [s]",line=2.7) 
mtext(1,text="Datasets",line=2) 

text(3.6,400,"maxL = 3")


box()	              # box around plot       
dev.off() 
