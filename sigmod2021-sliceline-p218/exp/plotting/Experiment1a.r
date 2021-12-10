require(graphics)
require(Matrix)

pdf(file="plots/Experiment1a.pdf",
  width=5, height=4.0, family="serif", pointsize=14)

data1 = as.matrix(read.table("results/Experiment1_p1.dat", sep=","))[,2]
data2 = as.matrix(read.table("results/Experiment1_p2.dat", sep=","))[,2]
data3 = as.matrix(read.table("results/Experiment1_p3.dat", sep=","))[,2]
data4 = as.matrix(read.table("results/Experiment1_p4.dat", sep=","))[,2]
data5 = as.matrix(read.table("results/Experiment1_p5.dat", sep=","))[,2]

points = as.vector(seq(1:10));
plot_colors <- c("cornflowerblue","gray40","black","orange","orangered")

plot(   points, data3,     
        type="o",           
        pch=19, 
        cex=1.1,
        col=plot_colors[3],              
        ylim = c(0.5,3500000),   
        xlab="",     
        ylab="",         
        axes=FALSE,    
        bg=plot_colors[3],
        log="y",
        lwd=1.1, 
        lty=1
  )


axis(2, las=2, at=c(1,10,100,1000,1e4,1e5,1e6), labels=c("1","10","100","1000","1e4","1e5","1e6")) # horizontal y axis
axis(1, las=1)      # horizontal x axis
mtext(2, text="# Enumerated Slices",line=2.7) 
mtext(1, text="Lattice Level L",line=2) 

lines(points[1:4], data5, type="o", pch=15, lty=1, lwd=1.1, col=plot_colors[5], bg=plot_colors[5], cex=1.0)
lines(points[1:4], data4, type="o", pch=15, lty=1, lwd=1.1, col=plot_colors[4], bg=plot_colors[4], cex=1.0)
lines(points[1:8], data2, type="o", pch=25, lty=1, lwd=1.1, col=plot_colors[2], bg=plot_colors[2], cex=1.0)
lines(points[1:8], data1[1:8], type="o", pch=17, lty=1, lwd=1.1, col=plot_colors[1], bg=plot_colors[1], cex=1.0)

box()	

legend( "topright",
       c("No dedup","No parents, sc, ss"), col=plot_colors[5:4], 
       pch=c(15,15), lty=c(1), lwd=c(1.1), bty="n");

legend( 1.5, 600,
       c("No parents, sc","No parents", "All"), col=plot_colors[3:1], pt.bg=plot_colors[3:1], 
       pch=c(19,25,17), lty=c(1), lwd=c(1.1), bty="n");

dev.off() 
