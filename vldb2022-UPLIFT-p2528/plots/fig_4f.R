require(graphics)
require(Matrix)

pdf(file="fig_4f.pdf",
    width=4.8, height=4, family="serif", pointsize=14)
#par(mar=c(3.5, 4, 2.5, 2) + 0.1)

data2 = rowMeans(matrix(as.matrix(read.table("..//results//stringlen_dml_baseAll.dat", 
          sep="\t"))[,1],20,3,byrow=TRUE))
data1 = rowMeans(matrix(as.matrix(read.table("..//results//stringlen_skAll.dat", 
          sep="\t"))[,1],20,3,byrow=TRUE))
data3 = rowMeans(matrix(as.matrix(read.table("..//results//stringlen_dmlAll.dat", 
          sep="\t"))[,1],20,3,byrow=TRUE))

# Take range 50 to 500. Drop remaining.
data1 = matrix(data1, nrow=10, byrow=TRUE)[,2]
data2 = matrix(data2, nrow=10, byrow=TRUE)[,2]
data3 = matrix(data3, nrow=10, byrow=TRUE)[,2]

speedup = matrix(0, 2, 10)
speedup[1,] = data2/data3
speedup[2,] = data1/data3
print(speedup)

points = as.matrix(seq(50, 500, 50));
plot_colors <- c("red","orange","cornflowerblue")

plot(   points, data1/1000,     
        type="o",           
        pch=16, 
        cex=1.1,
        col=plot_colors[1],              
        ylim = c(1,270),   
        xlab="",     
        ylab="",         
        axes=FALSE,    
        bg=plot_colors[1],
        log="",
        lwd=1.1, 
        lty=1
)


axis(2, las=2) # horizontal y axis
axis(1, las=1, at=c(100,200,300,400,500), cex.axis=1.0)     # horizontal x axis
mtext(2, text="Execution Time [s]",line=2.8) 
mtext(1, text="T13 (#Characters in Each Entry)",line=2) 

lines(points, data2/1000, type="o", pch=15, lty=1, lwd=1.1, col=plot_colors[2], bg=plot_colors[2], cex=1.0)
lines(points, data3/1000, type="o", pch=17, lty=1, lwd=1.1, col=plot_colors[3], bg=plot_colors[3], cex=1.0)

box()	

legend( x=310, y=265, text.width=c(80),
        c("SKlearn","Base","UPLIFT"), col=plot_colors, cex=1.0,
        pch=c(16,15,17), lty=c(1), lwd=c(1.1), bty="n", ncol=1, seg.len=2, x.intersp=0.3);


dev.off() 

