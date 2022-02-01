require(graphics)
require(Matrix)

pdf(file="plots/Experiment5a.pdf",
  width=5, height=4.0, family="serif", pointsize=14)

points = as.vector(seq(1,10));
input = as.matrix(read.table("results/Experiment5a_times.dat", sep=",")[3])
data = colMeans(matrix(input, 3, 10))/1000
data2 = data[1]*points;

plot_colors <- c("orange","black")

plot(   points, data,     
        type="o",           
        pch=25, 
        cex=1.1,
        col=plot_colors[1],              
        ylim = c(0,7300),   
        xlab="",     
        ylab="",         
        axes=FALSE,    
        bg=plot_colors[1],
        log="",
        lwd=1.1, 
        lty=1
  )


axis(2, las=2) # horizontal y axis
axis(1, las=1)      # horizontal x axis
mtext(2, text="Execution Time [s]",line=2.8) 
mtext(1, text="Row Replication Factor (x 2,458,285)",line=2) 

lines(points, data2, type="l", lty=2, lwd=1.1, col=plot_colors[2], cex=1.0)

#segments(16,0,16,570, lty=2, lwd=1.1)
text(9,900,"scale-up")

box()	

legend( "topleft",
       c("USCensus","Ideal Scaling"), col=plot_colors, pt.bg=plot_colors,
       pch=c(25,NA), lty=c(1,2), lwd=c(1.1), bty="n");

dev.off() 
