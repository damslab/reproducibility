require(graphics)
require(Matrix)
options(warn = -1)

pdf(file="exp_10b.pdf",
    width=4.5, height=4.0, family="serif", pointsize=14)
#par(mar=c(3.5, 4, 2.5, 2) + 0.1)

data11 = rowMeans(matrix(as.matrix(read.table("..//results//respcanb_kdd_sk.dat", sep="\t"))[,3],1,3,byrow=TRUE))
data12 = rowMeans(matrix(as.matrix(read.table("..//results//respcanb_kdd.dat", sep="\t"))[,3],1,3,byrow=TRUE))
data13 = rowMeans(matrix(as.matrix(read.table("..//results//respcanb_kdd_reuse.dat", sep="\t"))[,3],1,3,byrow=TRUE))

data21 = rowMeans(matrix(as.matrix(read.table("..//results//respcanb_aps_sk.dat", sep="\t"))[,3],1,3,byrow=TRUE))
data22 = rowMeans(matrix(as.matrix(read.table("..//results//respcanb_aps.dat", sep="\t"))[,3],1,3,byrow=TRUE))
data23 = rowMeans(matrix(as.matrix(read.table("..//results//respcanb_aps_reuse.dat",sep="\t"))[,3],1,3,byrow=TRUE))


data = matrix(0, 3, 2)
data[1,1] = data11/1000
data[2,1] = data12/1000
data[3,1] = data13/1000

data[1,2] = data21/1000
data[2,2] = data22/1000
data[3,2] = data23/1000

plot_colors <- c("red","orange", "cornflowerblue")

barplot( data, 
         space = c(0,1),
         xlab = "", 
         ylab = "",
         col=plot_colors,
         ylim = c(0,90),
         #log = "y",
         axes = FALSE, 
         names.arg = c("KDD 98", "APS"),
         args.legend = list(x="topright", bty="n", bty="n", ncol=1, cex=1.0, x.intersp=0.5),
         legend.text = c("SKlearn", "Base", "LIMA"),
         beside = TRUE,
         cex.names = 1.0,
         line = -0.7
)

#abline(v = 7.8) #vertical line seperator between groups
axis(2, las=2) # horizontal y axis
mtext(2, text="Execution Time [s]",line=2.8) 
#mtext(1, text="Number of Rows [Thousands]",line=2) 

box()	

dev.off() 

