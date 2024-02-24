require(graphics)
require(Matrix)

pdf(file="fig_4a.pdf",
    width=4.8, height=4.0, family="serif", pointsize=14)
#par(mar=c(3.5, 4, 2.5, 2) + 0.1)

data = matrix(0, 7, 1)
data[7,1] = rowMeans(matrix(as.matrix(read.table("..//results//adult_keras.dat", sep="\t"))[,1],1,3,byrow=TRUE))
data[6,1] = rowMeans(matrix(as.matrix(read.table("..//results//adult_keras_np.dat", sep="\t"))[,1],1,3,byrow=TRUE))
data[2,1] = rowMeans(matrix(as.matrix(read.table("..//results//adult_dml_base.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data[1,1] = rowMeans(matrix(as.matrix(read.table("..//results//adult_sk.dat", sep="\t"))[,1],1,3,byrow=TRUE))
data[3,1] = rowMeans(matrix(as.matrix(read.table("..//results//adult_dml.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data[4,1] = rowMeans(matrix(as.matrix(read.table("..//results//adult_spark.dat", sep="\t"))[,1],1,3,byrow=TRUE))
data[5,1] = rowMeans(matrix(as.matrix(read.table("..//results//adult_dask.dat", sep="\t"))[,1],1,3,byrow=TRUE))

speedup = matrix(0, 4, 1)
speedup[1,] = data[2,]/data[3,]
speedup[2,] = data[1,]/data[3,]
speedup[3,] = data[5,]/data[3,]
speedup[4,] = data[4,]/data[3,]
print(speedup)

data = data/1000

plot_colors <- c("red","orange","cornflowerblue","brown","green4","grey0","grey30")

barplot( data, 
         space = c(0,1),
         xlab = "", 
         ylab = "",
         col=plot_colors,
         ylim = c(0.01,13.50),
         log = "y",
         axes = FALSE, 
         names.arg = c("T1"),
         args.legend = list(x=5.0,y=20.0, bty="n", bty="n", ncol=2, cex=1.0, 
           x.intersp=0.4, text.width=1.3),
         legend.text = c("SKlearn", "Base", "UPLIFT", "Spark", "Dask", "KerasNp", "Keras"),
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

