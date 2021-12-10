require(graphics)
require(Matrix)

pdf(file="plots/Experiment4a.pdf",
  width=5, height=4.0, family="serif", pointsize=14)

points = as.vector(2^seq(0,9));
input = as.matrix(read.table("results/Experiment4a_times.dat", sep=",")[3])
data = colMeans(matrix(input, 3, 60))/1000
data2 = data[1:10];
data1 = data[11:20];

plot_colors <- c("orange","black")

plot(   points, data2,     
        type="o",           
        pch=25, 
        cex=1.1,
        col=plot_colors[1],              
        ylim = c(0,1500),   
        xlab="",     
        ylab="",         
        axes=FALSE,    
        bg=plot_colors[1],
        log="x",
        lwd=1.1, 
        lty=1
  )


axis(2, las=2) # horizontal y axis
axis(1, las=1, at=points, labels=c("1","2","4","8","16","32","64","128","256","512"))      # horizontal x axis
mtext(2, text="Execution Time [s]",line=2.7) 
mtext(1, text="Hybrid TP/DP Block Size [# Slices]",line=2) 

lines(points, data1[1:10], type="o", pch=17, lty=1, lwd=1.1, col=plot_colors[2], bg=plot_colors[2], cex=1.0)

segments(16,0,16,570, lty=2, lwd=1.1)
text(16,690,"default")

box()	

legend( "top",
       c("USCensus","Covtype"), col=plot_colors, pt.bg=plot_colors,
       pch=c(25,17), lty=c(1), lwd=c(1.1), bty="n");

dev.off() 
