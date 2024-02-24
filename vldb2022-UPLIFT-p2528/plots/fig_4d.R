require(graphics)
require(Matrix)

pdf(file="fig_4d.pdf",
    width=4.8, height=4.0, family="serif", pointsize=14)
#par(mar=c(3.5, 4, 2.5, 2) + 0.1)

data = matrix(0, 4, 2)
data[3,1] = rowMeans(matrix(as.matrix(read.table("..//results//bagfwords_dml.dat", 
          sep="\t"))[,1],1,3,byrow=TRUE))
data[3,2] = rowMeans(matrix(as.matrix(read.table("..//results//embedding_dml.dat", 
          sep="\t"))[,1],1,3,byrow=TRUE))
data[2,1] = rowMeans(matrix(as.matrix(read.table("..//results//bagfwords_dml_base.dat", 
          sep="\t"))[,1],1,3,byrow=TRUE))
data[2,2] = rowMeans(matrix(as.matrix(read.table("..//results//embedding_dml_base.dat", 
          sep="\t"))[,1],1,3,byrow=TRUE))
data[4,1] = rowMeans(matrix(as.matrix(read.table("..//results//bagfwords_keras.dat", 
          sep="\t"))[,1],1,3,byrow=TRUE))
data[4,2] = rowMeans(matrix(as.matrix(read.table("..//results//embedding_keras.dat", 
          sep="\t"))[,1],1,3,byrow=TRUE))
data[1,1] = rowMeans(matrix(as.matrix(read.table("..//results//bagfwords_sk.dat", 
          sep="\t"))[,1],1,3,byrow=TRUE))
data[1,2] = NA

speedup = matrix(0, 3, 2)
speedup[1,] = data[2,]/data[3,]
speedup[2,] = data[1,]/data[3,]
speedup[3,] = data[4,]/data[3,]
print(speedup)

data = data/1000

plot_colors <- c("red","orange","cornflowerblue","grey30")

barplot( data, 
         space = c(0,0),
         xlab = "", 
         ylab = "",
         col=plot_colors,
         ylim = c(0,380),
         #log = "y",
         axes = FALSE, 
         names.arg = c("T10", "T11"),
         args.legend = list("topright", bty="n", bty="n", ncol=1, cex=1.0, 
           x.intersp=0.4, text.width=1.6),
         legend.text = c("SKlearn", "Base", "UPLIFT", "Keras"),
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

