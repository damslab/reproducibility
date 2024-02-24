require(graphics)
require(Matrix)

pdf(file="fig_4b.pdf",
    width=4.8, height=4.0, family="serif", pointsize=14)
#par(mar=c(3.5, 4, 2.5, 2) + 0.1)

data = matrix(0, 3, 3)
data[2,1] = rowMeans(matrix(as.matrix(read.table("..//results//homecredit_dml_base.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data[2,2] = rowMeans(matrix(as.matrix(read.table("..//results//santander_dml_base.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data[2,3] = rowMeans(matrix(as.matrix(read.table("..//results//kdd_dml_base.dat", sep="\t"))[,1],1,5,byrow=TRUE))

data[3,1] = rowMeans(matrix(as.matrix(read.table("..//results//homecredit_dml.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data[3,2] = rowMeans(matrix(as.matrix(read.table("..//results//santander_dml.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data[3,3] = rowMeans(matrix(as.matrix(read.table("..//results//kdd_dml.dat", sep="\t"))[,1],1,5,byrow=TRUE))

data[1,1] = rowMeans(matrix(as.matrix(read.table("..//results//homecredit_sk.dat", sep="\t"))[,1],1,3,byrow=TRUE))
data[1,2] = rowMeans(matrix(as.matrix(read.table("..//results//santander_sk.dat", sep="\t"))[,1],1,3,byrow=TRUE))
data[1,3] = rowMeans(matrix(as.matrix(read.table("..//results//kdd_sk.dat", sep="\t"))[,1],1,3,byrow=TRUE))

speedup = matrix(0, 2, 3)
speedup[1,] = data[2,]/data[3,]
speedup[2,] = data[1,]/data[3,]
print(speedup)

data = data/1000

plot_colors <- c("red","orange","cornflowerblue")

barplot( data, 
         space = c(0,1),
         xlab = "", 
         ylab = "",
         col=plot_colors,
         ylim = c(0,8.8),
         #log = "y",
         axes = FALSE, 
         names.arg = c("T8","T5","T2"),
         args.legend = list(x="topleft", bty="n", bty="n", ncol=1, cex=1.0, 
           x.intersp=0.5, text.width=2.6),
         legend.text = c("SKlearn", "Base", "UPLIFT"),
         beside = TRUE,
         cex.names = 1.0,
         line = -0.7
)

#abline(v = 7.8) #vertical line seperator between groups
axis(2, las=2) # horizontal y axis
mtext(2, text="Execution Time [s]",line=2) 
#mtext(1, text="Number of Rows [Thousands]",line=2) 

box()	

dev.off() 

