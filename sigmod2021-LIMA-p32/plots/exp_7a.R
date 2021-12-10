require(graphics)
require(Matrix)
options(warn = -1)

pdf(file="exp_7a.pdf",
    width=4.5, height=4.0, family="serif", pointsize=14)

data1 = rowMeans(matrix(as.matrix(read.table("..//results//resmicrotsmm.dat", sep="\t"))[,4],10,2,byrow=TRUE))
data2 = rowMeans(matrix(as.matrix(read.table("..//results//resmicrotsmm_preuse.dat", sep="\t"))[,4],10,2,byrow=TRUE))
data3 = rowMeans(matrix(as.matrix(read.table("..//results//resmicrotsmm_preuse_comp.dat", sep="\t"))[,4],10,2,byrow=TRUE))

points = as.matrix(c(10,20,30,40,50,60,70,80,90,100));
plot_colors <- c("orange","cornflowerblue", "red")

plot(   points, data1/1000,     
        type="o",           
        pch=17, 
        cex=1.1,
        col=plot_colors[1],              
        ylim = c(1,600),   
        xlab="",     
        ylab="",         
        axes=FALSE,    
        bg=plot_colors[1],
        log="",
        lwd=1.1, 
        lty=1
)


axis(2, las=2) # horizontal y axis
axis(1, las=1, at=c(10,25,50,75,100))      # horizontal x axis
mtext(2, text="Execution Time [s]",line=2.8) 
mtext(1, text="#Rows [Thousands]",line=2) 

lines(points, data2/1000, type="o", pch=16, lty=1, lwd=1.1, col=plot_colors[2], bg=plot_colors[2], cex=1.0)
lines(points, data3/1000, type="o", pch=15, lty=1, lwd=1.1, col=plot_colors[3], bg=plot_colors[3], cex=1.0)

text(x=96, y=190, labels="4.2x")
text(x=97, y=70, labels="41x")

data1[10]/data2[10]
data1[10]/data3[10]


box()	

legend( "topleft", text.width=c(13,13),
        c("Base","LIMA","LIMA-CA"), col=plot_colors, cex=1.0,
        pch=c(17,16,15), lty=c(1), lwd=c(1.1), bty="n", ncol=1, seg.len=2, x.intersp=0.5);

dev.off() 

