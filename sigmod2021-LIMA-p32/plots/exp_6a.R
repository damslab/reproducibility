require(graphics)
require(Matrix)
options(warn = -1)

pdf(file="exp_6a.pdf",
    width=4.5, height=4.0, family="serif", pointsize=14)

data1 = rowMeans(matrix(as.matrix(read.table("..//results//reslinTime.dat", sep="\t"))[,4],7,3,byrow=TRUE))
data2 = rowMeans(matrix(as.matrix(read.table("..//results//reslinTime_lineage.dat", sep="\t"))[,4],7,3,byrow=TRUE))
data3 = rowMeans(matrix(as.matrix(read.table("..//results//reslinTime_reuse.dat", sep="\t"))[,4],7,3,byrow=TRUE))
data4 = rowMeans(matrix(as.matrix(read.table("..//results//reslinTime_dedup.dat", sep="\t"))[,4],7,3,byrow=TRUE))

data = matrix(0, 4, 7)
data[1,] = data1/1000
data[2,] = data2/1000
data[3,] = data3/1000
data[4,] = data4/1000

line1 <- c("2","8","32","128","512","2048")
#line2 <- c("1M","250K","62K","15K","4K","976","244")
#names <- paste(line1, line2, sep="\n")

points = as.matrix(c(10,20,30,40,50,60,70));
plot_colors <- c("orange","cornflowerblue", "gray90","gray10")

barplot( data[,1:6], 
         space = c(0,2),
         xlab = "", 
         ylab = "",
         col=plot_colors,
         ylim = c(0,330),
         #log = "y",
         axes = FALSE, 
         names.arg = line1,
         args.legend = list(x="topright", bty="n", bty="n", ncol=2, x.intersp=0.5),
         legend.text = c("Base", "LT","LTP", "LTD"),
         beside = TRUE,
         line = -0.7,
)


axis(2, las=2) # horizontal y axis
mtext(2, text="Execution Time [s]",line=2.5) 
mtext(1, text="Bachsize (#Rows x 784)", line=1.3)

text(x=30.3, y=200, labels="#Rows: 2M")
text(x=29.2, y=150, labels="#Ops/Iter:  40")

box()	

dev.off() 

