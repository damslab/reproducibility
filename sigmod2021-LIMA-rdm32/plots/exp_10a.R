require(graphics)
require(Matrix)
options(warn = -1)

pdf(file="exp_10a.pdf",
    width=4.4, height=4.0, family="serif", pointsize=14)
#par(mar=c(3.5, 4, 2.5, 2) + 0.1)

data11 = rowMeans(matrix(as.matrix(read.table("..//results//resautoen.dat", sep="\t"))[,4],1,3,byrow=TRUE))
data12 = rowMeans(matrix(as.matrix(read.table("..//results//resautoen_reuse.dat", sep="\t"))[,4],1,3,byrow=TRUE))
data13 = rowMeans(matrix(as.matrix(read.table("..//results//resautoen_tfg.dat", sep="\t"))[,4],1,3,byrow=TRUE))
data14 = rowMeans(matrix(as.matrix(read.table("..//results//resautoen_tf.dat",sep="\t"))[,4],1,3,byrow=TRUE))
data15 = rowMeans(matrix(as.matrix(read.table("..//results//resautoen_tfg_xla.dat", sep="\t"))[,4],1,3,byrow=TRUE))

data21 = rowMeans(matrix(as.matrix(read.table("..//results//respcacvkdd.dat", sep="\t"))[,3],1,3,byrow=TRUE))
data22 = rowMeans(matrix(as.matrix(read.table("..//results//respcacvkdd_reuse.dat", sep="\t"))[,3],1,3,byrow=TRUE))
data23 = rowMeans(matrix(as.matrix(read.table("..//results//respcacvkdd_tfg.dat", sep="\t"))[,3],1,3,byrow=TRUE))
data24 = rowMeans(matrix(as.matrix(read.table("..//results//respcacvkdd_tf.dat",sep="\t"))[,3],1,3,byrow=TRUE))
data25 = rowMeans(matrix(as.matrix(read.table("..//results//respcacvkdd_tfg_xla.dat", sep="\t"))[,3],1,3,byrow=TRUE))
data26 = rowMeans(matrix(as.matrix(read.table("..//results//respcacvkdd_helix.dat", sep="\t"))[,3],1,3,byrow=TRUE))


data = matrix(0, 6, 2)
data[1,1] = data11/1000
data[2,1] = data12/1000
data[3,1] = data13/1000
data[4,1] = data14/1000
data[5,1] = data15/1000

data[1,2] = data21/1000
data[2,2] = data22/1000
data[3,2] = data23/1000
data[4,2] = data24/1000
data[5,2] = data25/1000
data[6,2] = data24/1000

plot_colors <- c("orange","cornflowerblue","red", "grey90", "gray50", "grey10")

barplot( data, 
         space = c(0,0.5),
         xlab = "", 
         ylab = "",
         col=plot_colors,
         ylim = c(0,930),
         #log = "y",
         axes = FALSE, 
         names.arg = c("Autoencoder", "PCACV"),
         args.legend = list(x="topright", bty="n", bty="n", ncol=1, cex=1.0, x.intersp=0.3, text.width=3.6),
         legend.text = c("Base", "LIMA", "TF-G", "TF", "TF-XLA", "Coarse"),
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

