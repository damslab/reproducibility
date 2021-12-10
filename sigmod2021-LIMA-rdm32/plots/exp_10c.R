require(graphics)
require(Matrix)

pdf(file="exp_10c.pdf",
    width=4.4, height=4.0, family="serif", pointsize=14)
#par(mar=c(3.5, 4, 2.5, 2) + 0.1)

data1 = rowMeans(matrix(as.matrix(read.table("..//results//pca_cv_tf.dat", sep="\t"))[,3],5,3,byrow=TRUE))
data2 = rowMeans(matrix(as.matrix(read.table("..//results//pca_cv_lima.dat", sep="\t"))[,3],5,3,byrow=TRUE))

points = as.matrix(c(50,100,200,300,400));
plot_colors <- c("orange","cornflowerblue")

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
axis(1, las=1, at=c(50,150,250,350), cex.axis=1.0)      # horizontal x axis
mtext(2, text="Execution Time [s]",line=2.8) 
mtext(1, text="#Rows [Thousands]",line=2) 

lines(points, data2/1000, type="o", pch=15, lty=1, lwd=1.1, col=plot_colors[2], bg=plot_colors[2], cex=1.0)

box()	

legend( "topleft", text.width=c(13,13),
        c("TF","LIMA"), col=plot_colors, cex=1.0,
        pch=c(17,15), lty=c(1), lwd=c(1.1), bty="n", ncol=1, seg.len=2, x.intersp=0.5);

dev.off() 

