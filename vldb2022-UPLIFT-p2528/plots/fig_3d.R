require(graphics)
require(Matrix)

pdf(file="fig_3d.pdf",
    width=4.8, height=4.0, family="serif", pointsize=14)
#par(mar=c(3.5, 4, 2.5, 2) + 0.1)

data = matrix(0, 4, 8)
data[1,] = rowMeans(matrix(as.matrix(read.table("..//results//rowpart_RC_dmlAll.dat", 
          sep="\t"))[,1],8,3,byrow=TRUE))
data[2,] = rowMeans(matrix(as.matrix(read.table("..//results//rowpart_BinH_dmlAll.dat", 
          sep="\t"))[,1],8,3,byrow=TRUE))
data[3,] = rowMeans(matrix(as.matrix(read.table("..//results//rowpart_BinW_dmlAll.dat", 
          sep="\t"))[,1],8,3,byrow=TRUE))
data[4,] = rowMeans(matrix(as.matrix(read.table("..//results//rowpart_FH_dmlAll.dat", 
          sep="\t"))[,1],8,3,byrow=TRUE))

data = data/1000
#print(data)

plot_colors <- c("orange","cornflowerblue","grey30","red")

b = barplot( data, 
         space = c(0,1),
         xlab = "", 
         ylab = "",
         col=plot_colors,
         ylim = c(0,58),
         axes = FALSE, 
         names.arg = c("1","2","4","8","16","32","64","128"),
         args.legend = list(x=39,y=60, bty="n", bty="n", ncol=2, cex=1.0, 
           x.intersp=0.4, text.width=4),
         legend.text = c("RC","BinH","BinW","FH"),
         beside = TRUE,
         cex.names = 1.0,
         line = -0.7
)
#print(b) #prints the coordinates of each bar in each group
axis(2, las=2) # horizontal y axis
mtext(2, text="Execution Time [s]",line=2.8) 
mtext(side=1, line=1.2 ,c("2","4","8","16","32","64","128","256"), at=c(3,8,13,18,23,28,33,38))
#text(x=18, y=30, labels="1,2 -> 128,256")
text(x=17.2, y=25, labels="Opt.")

box()	

dev.off() 

