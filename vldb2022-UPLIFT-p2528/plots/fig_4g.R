require(graphics)
require(Matrix)

pdf(file="fig_4g.pdf",
    width=4.8, height=4, family="serif", pointsize=14)
#par(mar=c(3.5, 4, 2.5, 2) + 0.1)

data2 = rowMeans(matrix(as.matrix(read.table("..//results//numdistinct_dml_baseAll.dat", 
          sep="\t"))[,1],10,3,byrow=TRUE))
data1 = rowMeans(matrix(as.matrix(read.table("..//results//numdistinct_skAll.dat", 
          sep="\t"))[,1],10,3,byrow=TRUE))
data3 = rowMeans(matrix(as.matrix(read.table("..//results//numdistinct_dmlAll.dat", 
          sep="\t"))[,1],10,3,byrow=TRUE))

speedup = matrix(0, 2, 10)
speedup[1,] = data2/data3
speedup[2,] = data1/data3
print(speedup)

points = as.matrix(seq(100000, 1000000, 100000));
plot_colors <- c("red","orange","cornflowerblue")

plot(   points, data1/1000,     
        type="o",           
        pch=16, 
        cex=1.1,
        col=plot_colors[1],              
        ylim = c(1,620),   
        xlab="",     
        ylab="",         
        axes=FALSE,    
        bg=plot_colors[1],
        log="",
        lwd=1.1, 
        lty=1
)


axis(2, las=2) # horizontal y axis
axis(1, las=1, at=c(200000,400000,600000,800000,1000000), 
    labels = c("200K","400K","600K","800K","1M"), cex.axis=1.0)     # horizontal x axis
mtext(2, text="Execution Time [s]",line=2.8) 
mtext(1, text="T14 (#Distinct Items in Each Column)",line=2) 

lines(points, data2/1000, type="o", pch=15, lty=1, lwd=1.1, col=plot_colors[2], bg=plot_colors[2], cex=1.0)
lines(points, data3/1000, type="o", pch=17, lty=1, lwd=1.1, col=plot_colors[3], bg=plot_colors[3], cex=1.0)

box()	

legend( x=650000, y=570, text.width=c(13),
        c("SKlearn","Base","UPLIFT"), col=plot_colors, cex=1.0,
        pch=c(16,15,17), lty=c(1), lwd=c(1.1), bty="n", ncol=1, seg.len=2, x.intersp=0.3);


dev.off() 

