require(graphics)
require(Matrix)
options(warn = -1)

pdf(file="exp_6b.pdf",
    width=4.5, height=4.0, family="serif", pointsize=14)

data1 = rowMeans(matrix(as.matrix(read.table("..//results//reslinMem.dat", sep="\t"))[,1],6,3,byrow=TRUE))
data2 = rowMeans(matrix(as.matrix(read.table("..//results//reslinMem_lineage.dat", sep="\t"))[,1],6,3,byrow=TRUE))
data3 = rowMeans(matrix(as.matrix(read.table("..//results//reslinMem_dedup.dat", sep="\t"))[,1],6,3,byrow=TRUE))

data = matrix(0, 3, 6)
data[1,] = data1/(1024*1024)
data[2,] = data2/(1024*1024)
data[3,] = data3/(1024*1024)

line1 <- c("2","4","8","128","512","2048")

plot_colors <- c("orange","cornflowerblue", "gray10")

barplot( data, 
         space = c(0,2.5),
         xlab = "", 
         ylab = "",
         col=plot_colors,
         ylim = c(0,65),
         #log = "y",
         axes = FALSE, 
         names.arg = line1,
         args.legend = list(x="topleft", bty="n", bty="n", ncol=3, x.intersp=0.5),
         legend.text = c("Base", "LT", "LTD"),
         beside = TRUE,
         line = -0.7,
)


axis(2, las=2) # horizontal y axis
mtext(2, text="Memory [MB]",line=2.2) 
mtext(1, text="Bachsize (#Rows x 784)", line=1.3)

text(x=21.3, y=42, labels="#Rows: 20K")
text(x=20.2, y=33, labels="#Ops/Iter:   40")

box()	

dev.off() 

