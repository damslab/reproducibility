require(graphics)
require(Matrix)

pdf(file="fig_3b.pdf",
    width=4.8, height=4, family="serif", pointsize=14)
#par(mar=c(3.5, 4, 2.5, 2) + 0.1)

dataRC = rowMeans(matrix(as.matrix(read.table("..//results//res_RC_rows_dmlAll.dat", sep="\t"))[,1],9,7,byrow=TRUE))
dataDC = rowMeans(matrix(as.matrix(read.table("..//results//res_DC_rows_dmlAll.dat", sep="\t"))[,1],9,7,byrow=TRUE))
dataFH = rowMeans(matrix(as.matrix(read.table("..//results//res_FH_rows_dmlAll.dat", sep="\t"))[,1],9,7,byrow=TRUE))
dataRCBase = rowMeans(matrix(as.matrix(read.table("..//results//res_RC_rows_baseAll.dat", sep="\t"))[,1],9,7,byrow=TRUE))
dataDCBase = rowMeans(matrix(as.matrix(read.table("..//results//res_DC_rows_baseAll.dat", sep="\t"))[,1],9,7,byrow=TRUE))
dataFHBase= rowMeans(matrix(as.matrix(read.table("..//results//res_FH_rows_baseAll.dat", sep="\t"))[,1],9,7,byrow=TRUE))

data = matrix(0, 9, 3)
data[,1] = dataRCBase/dataRC
data[,2] = dataDCBase/dataDC
data[,3] = dataFHBase/dataFH

#ideal = c(1,1,1,1,1,1,1,1,1)
print(data)

points = as.matrix(c(500,1500,5000,15000,50000,150000,500000,1500000,5000000));
plot_colors <- c("orange", "cornflowerblue", "red2")

plot(   points, data[,1],     
        type="o",           
        pch=15, 
        cex=1.1,
        col=plot_colors[1],              
        ylim = c(0.2,17.2),   
        xlab="",     
        ylab="",         
        axes=FALSE,    
        bg=plot_colors[1],
        log="xy",
        lwd=1.1, 
        lty=1
)

axis(2, las=2) # horizontal y axis
axis(1, las=1, at=c(1500,15000,150000,1500000), 
    labels = c("1.5K","15K","150K","1.5M"), cex.axis=1.0)     # horizontal x axis
mtext(2, text="Speed-up",line=2.3) 
mtext(1, text="#Rows",line=2) 

lines(points, data[,2], type="o", pch=16, lty=1, lwd=1.1, col=plot_colors[2], bg=plot_colors[2], cex=1.0)
lines(points, data[,3], type="o", pch=17, lty=1, lwd=1.1, col=plot_colors[3], bg=plot_colors[2], cex=1.0)
#lines(points, ideal, type="l", lty=2, lwd=1.1)
abline(h=1.0, type="l", lty=2, lwd=1.1)
text(x=18000, y=0.72, labels="Single-threaded")
abline(v=135000, type="l", lty=2, lwd=1.1)
text(x=90000, y=3.0, labels="L3")
text(x=70000, y=2.0, labels="limit")

box()	

#legend( x=500000,y=4, text.width=c(13,13),
#        c("RC","DC","FH"), col=plot_colors, cex=1.0,
#        pch=c(15,16,17), lty=c(1), lwd=c(1.1), bty="n", ncol=1, seg.len=2, x.intersp=0.5);
legend( "topleft", text.width=0.5,
        c("RC","DC","FH"), col=plot_colors, cex=1.0,
        pch=c(15,16,17), lty=c(1), lwd=c(1.1), bty="n", ncol=2, seg.len=2, x.intersp=0.5);
