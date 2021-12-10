require(graphics)
require(Matrix)

pdf(file="plots/Experiment3b.pdf",
  width=4.5, height=4.0, family="serif", pointsize=14)

datasets = c("Adult", "Covtype", "USCensus", "KDD98")
plot_colors <- c("orangered", "black", "orange", "cornflowerblue")

data = matrix(0, 5, 7); #dataset x params
data[1,] = as.matrix(c(0.36,0.68,0.84,0.92,0.96,0.98,0.99))

for(i in 1:(nrow(data)-1)) {
  for(j in 1:ncol(data)) {
    fname = paste("results/Experiment3_",datasets[i],"_a",data[1,j],".dat",sep="")
    if( file.exists(fname) ) {
      data[i+1,j] = as.matrix(read.table(fname, sep=","))[1,4]
    }
    else {
      print(paste(fname," does not exist"))
    }
  }
}

data[1,] = 1-data[1,]

print(data)

plot(   data[1,], data[5,],     
        type="o",           
        pch=19, 
        cex=1.1,
        col=plot_colors[4],              
        ylim = c(1,2e6),
        xlab="",     
        ylab="",         
        axes=FALSE,    
        bg=plot_colors[4],
        log="xy",
        lwd=1.1, 
        lty=1
  )


axis(2, las=2,at=c(1,10,100,1000,1e4,1e5,1e6), labels=c("1","10","100","1000","1e4","1e5","1e6")) 
axis(1, las=1, at=c(0.01,0.02,0.04,0.08,0.16,0.32,0.64), 
      labels=c("0.99",".98",".96",".92",".84",".68",".36"))    
mtext(2, text="Top-1 Slice Size", line=2.7) 
mtext(1, text=expression(paste("Weight Parameter ",alpha)), line=2) 

lines(data[1,2:7], data[2,2:7], type="o", pch=15, lty=1, lwd=1.1, col=plot_colors[1], bg=plot_colors[1], cex=1.0)
lines(data[1,2:7], data[3,2:7], type="o", pch=17, lty=1, lwd=1.1, col=plot_colors[2], bg=plot_colors[2], cex=1.0)
lines(data[1,2:7], data[4,2:7], type="o", pch=25, lty=1, lwd=1.1, col=plot_colors[3], bg=plot_colors[3], cex=1.0)

box()	

legend( "bottomright",
       c("USCensus","Adult", "KDD98", "Covtype"), col=plot_colors[c(3,1,4,2)], 
       pch=c(25,15,19,17), lty=c(1), lwd=c(1.1), bty="n", ncol=2, pt.bg=plot_colors[c(3,1,4,2)]);

text(0.32, 1000, expression(paste(sigma," = 0.01n")))

dev.off() 
