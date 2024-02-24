require(graphics)
require(Matrix)

pdf(file="fig_4h.pdf",
    width=4.8, height=4.0, family="serif", pointsize=14)
#par(mar=c(3.5, 4, 2.5, 2) + 0.1)

data = matrix(0, 2, 4)
data[,1] = rowMeans(matrix(as.matrix(read.table("..//results//featureeng_spark.dat", sep="\t"))[,1],2,3,byrow=TRUE))
data[,2] = rowMeans(matrix(as.matrix(read.table("..//results//featureeng_sk.dat", sep="\t"))[,1],2,3,byrow=TRUE))
data[,3] = rowMeans(matrix(as.matrix(read.table("..//results//featureeng_dml_base.dat", sep="\t"))[,1],2,3,byrow=TRUE))
data[,4] = rowMeans(matrix(as.matrix(read.table("..//results//featureeng_dml.dat", sep="\t"))[,1],2,3,byrow=TRUE))

speedup = matrix(0, 3, 1)
speedup[1,1] = data[1,1]/data[1,4]
speedup[2,1] = data[1,2]/data[1,4]
speedup[3,1] = data[1,3]/data[1,4]
print(speedup)

data = data/1000
print(data)

plot_colors <- c("orange","cornflowerblue")

barplot( data, 
         space = c(0.2,0.2,0.2,0.2),
         xlab = "", 
         ylab = "",
         col=plot_colors,
         ylim = c(0,960),
         axes = FALSE, 
         names.arg = c("Spark","Sklearn","Base","UPLIFT"),
         args.legend = list(x="topright", bty="n", bty="n", ncol=1, cex=1.0, 
           x.intersp=0.5, text.width=2.6),
         legend.text = c("Transformations", "NaiveBayes"),
         #beside = TRUE,
         cex.names = 1.0,
         line = -0.7
)

#abline(v = 7.8) #vertical line seperator between groups
axis(2, las=2) # horizontal y axis
mtext(2, text="Execution Time [s]",line=2.8) 
#mtext(1, text="Number of Rows [Thousands]",line=2) 

box()	

dev.off() 

