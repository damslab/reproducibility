require(graphics)
require(Matrix)
options(warn = -1)

pdf(file="exp_9b.pdf",
    width=4.5, height=4.0, family="serif", pointsize=14)
#par(mar=c(3.5, 4, 2.5, 2) + 0.1)

data1 = rowMeans(matrix(as.matrix(read.table("..//results//resexample_parfor.dat", sep="\t"))[,4],10,3,byrow=TRUE))
data2 = rowMeans(matrix(as.matrix(read.table("..//results//resexample_parfor_reuse.dat", sep="\t"))[,4],10,3,byrow=TRUE))

data3 = rowMeans(matrix(as.matrix(read.table("..//results//resexample.dat", sep="\t"))[,4],10,3,byrow=TRUE))
data4 = rowMeans(matrix(as.matrix(read.table("..//results//resexample_reuse.dat", sep="\t"))[,4],10,3,byrow=TRUE))


points = as.matrix(c(100,200,300,400,500,600,700,800,900,1000));
plot_colors <- c("orange","gray10","cornflowerblue","red")

plot(   points, data3/1000,     
        type="o",           
        pch=17, 
        cex=1.1,
        col=plot_colors[1],              
        ylim = c(1,250),   
        xlab="",     
        ylab="",         
        axes=FALSE,    
        bg=plot_colors[1],
        log="",
        lwd=1.1, 
        lty=1
)


axis(2, las=2) # horizontal y axis
axis(1, las=1, at=c(200,400,600,800,1000), cex.axis = 1.0)      # horizontal x axis
mtext(2, text="Execution Time [s]",line=2.5) 
mtext(1, text="#Rows [Thousands]",line=2) 

lines(points, data1/1000, type="o", pch=18, lty=1, lwd=1.1, col=plot_colors[2], bg=plot_colors[2], cex=1.0)
lines(points, data4/1000, type="o", pch=15, lty=1, lwd=1.1, col=plot_colors[3], bg=plot_colors[3], cex=1.0)
lines(points, data2/1000, type="o", pch=16, lty=1, lwd=1.1, col=plot_colors[4], bg=plot_colors[4], cex=1.0)

segments(915,16,915,182, lty=1,lwd=1.1)
segments(921,20,921,52, lty=1,lwd=1.1)

text(x=980, y=35.5, labels="2.6x")
text(x=830, y=100, labels="12.4x")


data1[10]/data2[10]
data3[10]/data4[10]
data4[10]/data2[10]

box()	

legend( "topleft", text.width=c(13,13),
        c("Base","Base-P","LIMA","LIMA-P"), col=plot_colors, cex=1.0,
        pch=c(17,18,15,16), lty=c(1), lwd=c(1.1), bty="n", ncol=1, seg.len=2, x.intersp=0.5);

dev.off() 

