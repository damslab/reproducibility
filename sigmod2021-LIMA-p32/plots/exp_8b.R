require(graphics)
require(Matrix)
options(warn = -1)

pdf(file="exp_8b.pdf",
    width=4.5, height=4.0, family="serif", pointsize=14)
#par(mar=c(3.5, 4, 2.5, 2) + 0.1)

data11 = rowMeans(matrix(as.matrix(read.table("..//results//resmicroevic_auto.dat", sep="\t"))[,4],1,3,byrow=TRUE))
data12 = rowMeans(matrix(as.matrix(read.table("..//results//resmicroevic_auto_lru.dat", sep="\t"))[,4],1,3,byrow=TRUE))
data13 = rowMeans(matrix(as.matrix(read.table("..//results//resmicroevic_auto_cs.dat", sep="\t"))[,4],1,3,byrow=TRUE))
data14 = rowMeans(matrix(as.matrix(read.table("..//results//resmicroevic_auto_dh.dat", sep="\t"))[,4],1,3,byrow=TRUE))
data15 = rowMeans(matrix(as.matrix(read.table("..//results//resmicroevic_auto_inf.dat", sep="\t"))[,4],1,3,byrow=TRUE))

data21 = rowMeans(matrix(as.matrix(read.table("..//results//resmicroevic_stplm.dat", sep="\t"))[,4],1,3,byrow=TRUE))
data22 = rowMeans(matrix(as.matrix(read.table("..//results//resmicroevic_stplm_lru.dat", sep="\t"))[,4],1,3,byrow=TRUE))
data23 = rowMeans(matrix(as.matrix(read.table("..//results//resmicroevic_stplm_cs.dat", sep="\t"))[,4],1,3,byrow=TRUE))
data24 = rowMeans(matrix(as.matrix(read.table("..//results//resmicroevic_stplm_dh.dat", sep="\t"))[,4],1,3,byrow=TRUE))
data25 = rowMeans(matrix(as.matrix(read.table("..//results//resmicroevic_stplm_inf.dat", sep="\t"))[,4],1,3,byrow=TRUE))

data = matrix(0, 5, 2)
data[1,1] = data11[1:1]/1000
data[2,1] = data12[1:1]/1000
data[3,1] = data13[1:1]/1000
data[4,1] = data14[1:1]/1000
data[5,1] = data15[1:1]/1000
data[1,2] = data21[1:1]/1000
data[2,2] = data22[1:1]/1000
data[3,2] = data23[1:1]/1000
data[4,2] = data24[1:1]/1000
data[5,2] = data25[1:1]/1000

plot_colors <- c("orange","gray90","cornflowerblue","red","gray10")

barplot( data, 
         space = c(0,1.5),
         xlab = "", 
         ylab = "",
         col=plot_colors,
         ylim = c(0,615),
         #log = "y",
         axes = FALSE, 
         names.arg = c("Mini-batch", "StepLM"),
         args.legend = list(x="topleft", bty="n", bty="n", ncol=1, x.intersp=0.5),
         legend.text = c("Base", "LRU", "C&S", "DAG-Height", "Infinite"),
         beside = TRUE,
         line = -0.7
)


#abline(v = 7.8) #vertical line seperator between groups
axis(2, las=2,) # horizontal y axis
mtext(2, text="Execution Time [s]",line=2.8) 


box()	

dev.off() 

