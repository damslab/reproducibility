require(graphics)
require(Matrix)

pdf(file="crypto_time.pdf",
    width=4.8, height=4, family="serif", pointsize=14)

data1 = rowMeans(matrix(as.matrix(read.table("crypto_time.dat", 
          sep="\t"))[,1],4,3,byrow=TRUE))


points = as.matrix(c(0,30,40,90));
plot_colors <- c("orange")

plot(   points, data1,     
        type="o",           
        pch=16, 
        cex=1.1,
        col=plot_colors[1],              
        ylim = c(1,2500),   
        xlab="",     
        ylab="",         
        axes=FALSE,    
        bg=plot_colors[1],
        log="",
        lwd=1.1, 
        lty=1
)


axis(2, las=2) # horizontal y axis
axis(1, las=1, at=c(0,30,40,90), cex.axis=1.0)     # horizontal x axis
mtext(2, text="Execution Time [ms]",line=2.8) 
mtext(1, text="Sparsity",line=2) 

text(x=15, y=400, labels="R2 Value: 0.94 - 0.89")

box()	

#legend( x=310, y=265, text.width=c(80),
#        c("SKlearn","Base","UPLIFT"), col=plot_colors, cex=1.0,
#        pch=c(16,15,17), lty=c(1), lwd=c(1.1), bty="n", ncol=1, seg.len=2, x.intersp=0.3);


dev.off() 

