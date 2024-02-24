require(graphics)
require(Matrix)

pdf(file="fig_4c.pdf",
    width=4.8, height=4.0, family="serif", pointsize=14)
#par(mar=c(3.5, 4, 2.5, 2) + 0.1)

data = matrix(0, 4, 6)
data[2,1] = rowMeans(matrix(as.matrix(read.table("..//results//criteo10M_s1_dml_base.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data[2,2] = rowMeans(matrix(as.matrix(read.table("..//results//criteo10M_s2_dml_base.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data[2,3] = rowMeans(matrix(as.matrix(read.table("..//results//crypto_s1_dml_base.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data[2,4] = rowMeans(matrix(as.matrix(read.table("..//results//crypto_s2_dml_base.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data[2,5] = rowMeans(matrix(as.matrix(read.table("..//results//catindat_dml_base.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data[2,6] = rowMeans(matrix(as.matrix(read.table("..//results//batch_dml_base.dat", sep="\t"))[,1],1,3,byrow=TRUE))

data[3,1] = rowMeans(matrix(as.matrix(read.table("..//results//criteo10M_s1_dml.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data[3,2] = rowMeans(matrix(as.matrix(read.table("..//results//criteo10M_s2_dml.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data[3,3] = rowMeans(matrix(as.matrix(read.table("..//results//crypto_s1_dml.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data[3,4] = rowMeans(matrix(as.matrix(read.table("..//results//crypto_s2_dml.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data[3,5] = rowMeans(matrix(as.matrix(read.table("..//results//catindat_dml.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data[3,6] = rowMeans(matrix(as.matrix(read.table("..//results//batch_dml.dat", sep="\t"))[,1],1,3,byrow=TRUE))

data[1,1] = rowMeans(matrix(as.matrix(read.table("..//results//criteo10M_s1_sk.dat", sep="\t"))[,1],1,3,byrow=TRUE))
data[1,2] = rowMeans(matrix(as.matrix(read.table("..//results//criteo10M_s2_sk.dat", sep="\t"))[,1],1,3,byrow=TRUE))
data[1,3] = rowMeans(matrix(as.matrix(read.table("..//results//crypto_s1_sk.dat", sep="\t"))[,1],1,3,byrow=TRUE))
data[1,4] = rowMeans(matrix(as.matrix(read.table("..//results//crypto_s2_sk.dat", sep="\t"))[,1],1,3,byrow=TRUE))
data[1,5] = rowMeans(matrix(as.matrix(read.table("..//results//catindat_sk.dat", sep="\t"))[,1],1,3,byrow=TRUE))
data[1,6] = NA

data[4,1] = NA
data[4,2] = NA
data[4,3] = NA
data[4,4] = NA
data[4,5] = NA
data[4,6] = rowMeans(matrix(as.matrix(read.table("..//results//batch_keras.dat", sep="\t"))[,1],1,3,byrow=TRUE))

speedup = matrix(0, 3, 6)
speedup[1,] = data[2,]/data[3,]
speedup[2,] = data[1,]/data[3,]
speedup[3,] = data[4,]/data[3,]
print(speedup)

data = data/1000

plot_colors <- c("red","orange","cornflowerblue","gray30")

barplot( data, 
         space = c(0,0), #space in the group, space between 2 groups
         xlab = "", 
         ylab = "",
         col=plot_colors,
         ylim = c(0,160),
         #log = "y",
         axes = FALSE, 
         names.arg = c("T3","T4","T6","T7","T9","T12"),
         args.legend = list(x="top", bty="n", bty="n", ncol=2, 
           cex=1.0, x.intersp=0.5, text.width=5.0),
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

