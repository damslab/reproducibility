require(graphics)
require(Matrix)

pdf(file="plots/Experiment3a.pdf",
  width=4.5, height=4.0, family="serif", pointsize=14)

datasets = c("Adult", "Covtype", "USCensus", "KDD98")
plot_colors <- c("orangered", "black", "orange", "cornflowerblue")

data = matrix(0, 5, 7); #dataset x params
data[1,] = as.matrix(c(0.36,0.68,0.84,0.92,0.96,0.98,0.99))

for(i in 1:(nrow(data)-1)) {
  for(j in 1:ncol(data)) {
    fname = paste("results/Experiment3_",datasets[i],"_a",data[1,j],".dat",sep="")
    if( file.exists(fname) ) {
      data[i+1,j] = as.matrix(read.table(fname, sep=","))[1,1]
    }
    else {
      print(paste(fname," does not exist"))
    }
  }
}

data[1,] = 1-data[1,]

plot(   data[1,], data[5,],     
        type="o",           
        pch=19, 
        cex=1.1,
        col=plot_colors[4],              
        ylim = c(0,25),
        xlab="",     
        ylab="",         
        axes=FALSE,    
        bg=plot_colors[4],
        log="x",
        lwd=1.1, 
        lty=1
  )


axis(2, las=2) 
axis(1, las=1, at=c(0.01,0.02,0.04,0.08,0.16,0.32,0.64), 
      labels=c("0.99",".98",".96",".92",".84",".68",".36"))    
mtext(2, text="Top-1 Slice Score", line=2.3) 
mtext(1, text=expression(paste("Weight Parameter ",alpha)), line=2) 

lines(data[1,2:7], data[2,2:7], type="o", pch=15, lty=1, lwd=1.1, col=plot_colors[1], bg=plot_colors[1], cex=1.0)
lines(data[1,2:7], data[3,2:7], type="o", pch=17, lty=1, lwd=1.1, col=plot_colors[2], bg=plot_colors[2], cex=1.0)
lines(data[1,2:7], data[4,2:7], type="o", pch=25, lty=1, lwd=1.1, col=plot_colors[3], bg=plot_colors[3], cex=1.0)

box()	

legend( "topright",
       c("USCensus","Adult", "KDD98", "Covtype"), col=plot_colors[c(3,1,4,2)], 
       pch=c(25,15,19,17), lty=c(1), lwd=c(1.1), bty="n", pt.bg=plot_colors[c(3,1,4,2)]);

text(0.02, 9, expression(paste(sigma," = 0.01n")))

dev.off() 
