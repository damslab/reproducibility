require(graphics)
require(Matrix)
options(warn = -1)

pdf(file="exp_7b.pdf",
    width=4.5, height=4.0, family="serif", pointsize=14)
#par(mar=c(3.5, 4, 2.5, 2) + 0.1)

data1 = rowMeans(matrix(as.matrix(read.table("..//results//resmicromultirepeat.dat", sep="\t"))[,4],5,3,byrow=TRUE))
data2 = rowMeans(matrix(as.matrix(read.table("..//results//resmicromultirepeat_reuse.dat", sep="\t"))[,4],5,3,byrow=TRUE))
data3 = rowMeans(matrix(as.matrix(read.table("..//results//resmicromultirepeat_reuse_multilvl.dat", sep="\t"))[,4],5,3,byrow=TRUE))

points = as.matrix(c(1,5,10,15,20));
plot_colors <- c("orange","cornflowerblue", "red")

plot(   points, data1/1000,     
        type="o",           
        pch=17, 
        cex=1.1,
        col=plot_colors[1],              
        ylim = c(1,1600),   
        xlab="",     
        ylab="",         
        axes=FALSE,    
        bg=plot_colors[1],
        log="",
        lwd=1.1, 
        lty=1
)


axis(2, las=2) # horizontal y axis
axis(1, las=1, at=c(1,5,10,15,20))      # horizontal x axis
mtext(2, text="Execution Time [s]",line=2.8) 
mtext(1, text="#Repeats",line=2) 

lines(points, data2/1000, type="o", pch=16, lty=1, lwd=1.1, col=plot_colors[2], bg=plot_colors[2], cex=1.0)
lines(points, data3/1000, type="o", pch=15, lty=1, lwd=1.1, col=plot_colors[3], bg=plot_colors[3], cex=1.0)

#segments(930,105,930,565, lty=1,lwd=1.1)
segments(19.5,55,19.5,255, lty=1,lwd=1.1)

#text(x=96, y=190, labels="4.2x")
text(x=18, y=150, labels="4.6x")
text(x=16.5, y=800, labels="#Rows: 50K")
text(x=17, y=600, labels="#Cols:  1K")


box()	

legend( "topleft", text.width=c(13,13),
        c("Base","LIMA-FR", "LIMA-MLR"), col=plot_colors, cex=0.9,
        pch=c(17,16, 15), lty=c(1), lwd=c(1.1), bty="n", ncol=1, seg.len=2, x.intersp=0.5);

dev.off() 

