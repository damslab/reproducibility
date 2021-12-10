require(graphics)
require(Matrix)
options(warn = -1)

pdf(file="exp_9d.pdf",
    width=4.5, height=4.0, family="serif", pointsize=14)
#par(mar=c(3.5, 4, 2.5, 2) + 0.1)

data1 = rowMeans(matrix(as.matrix(read.table("..//results//resenswp.dat", sep="\t"))[,4],5,3,byrow=TRUE))
data2 = rowMeans(matrix(as.matrix(read.table("..//results//resenswp_reuse.dat", sep="\t"))[,4],5,3,byrow=TRUE))

points = as.matrix(c(1,2,3,4,5));
plot_colors <- c("orange","cornflowerblue")

plot(   points, data1/1000,     
        type="o",           
        pch=17, 
        cex=1.1,
        col=plot_colors[1],              
        ylim = c(1,720),   
        xlab="",     
        ylab="",         
        axes=FALSE,    
        bg=plot_colors[1],
        log="",
        lwd=1.1, 
        lty=1
)


axis(2, las=2) # horizontal y axis
axis(1, las=1, at=c(1,2,3,4,5), cex.axis=1.0)      # horizontal x axis
mtext(2, text="Execution Time [s]",line=2.8) 
mtext(1, text="#Weights [Thousands]",line=2) 

lines(points, data2/1000, type="o", pch=15, lty=1, lwd=1.1, col=plot_colors[2], bg=plot_colors[2], cex=1.0)

box()	

legend( "topleft", text.width=c(13,13),
        c("Base","LIMA"), col=plot_colors, cex=1.0,         # cex to reduce text size (default=1)
        pch=c(17,15), lty=c(1), lwd=c(1.1), bty="n", ncol=1, seg.len=2, x.intersp=0.5);

dev.off() 

