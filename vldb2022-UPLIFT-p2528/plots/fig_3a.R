require(graphics)
require(Matrix)

pdf(file="fig_3a.pdf",
    width=4.8, height=4, family="serif", pointsize=14)
#par(mar=c(3.5, 4, 2.5, 2) + 0.1)

data11 = rowMeans(matrix(as.matrix(read.table("..//results//res_RC_1thread.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data12 = rowMeans(matrix(as.matrix(read.table("..//results//res_RC_2thread.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data13 = rowMeans(matrix(as.matrix(read.table("..//results//res_RC_4thread.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data14 = rowMeans(matrix(as.matrix(read.table("..//results//res_RC_8thread.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data15 = rowMeans(matrix(as.matrix(read.table("..//results//res_RC_16thread.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data16 = rowMeans(matrix(as.matrix(read.table("..//results//res_RC_32thread.dat", sep="\t"))[,1],1,5,byrow=TRUE))

data21 = rowMeans(matrix(as.matrix(read.table("..//results//res_DC_1thread.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data22 = rowMeans(matrix(as.matrix(read.table("..//results//res_DC_2thread.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data23 = rowMeans(matrix(as.matrix(read.table("..//results//res_DC_4thread.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data24 = rowMeans(matrix(as.matrix(read.table("..//results//res_DC_8thread.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data25 = rowMeans(matrix(as.matrix(read.table("..//results//res_DC_16thread.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data26 = rowMeans(matrix(as.matrix(read.table("..//results//res_DC_32thread.dat", sep="\t"))[,1],1,5,byrow=TRUE))

data31 = rowMeans(matrix(as.matrix(read.table("..//results//res_FH_1thread.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data32 = rowMeans(matrix(as.matrix(read.table("..//results//res_FH_2thread.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data33 = rowMeans(matrix(as.matrix(read.table("..//results//res_FH_4thread.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data34 = rowMeans(matrix(as.matrix(read.table("..//results//res_FH_8thread.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data35 = rowMeans(matrix(as.matrix(read.table("..//results//res_FH_16thread.dat", sep="\t"))[,1],1,5,byrow=TRUE))
data36 = rowMeans(matrix(as.matrix(read.table("..//results//res_FH_32thread.dat", sep="\t"))[,1],1,5,byrow=TRUE))

data = matrix(0, 6, 3)
data[1,1] = data11/data11
data[2,1] = data11/data12
data[3,1] = data11/data13
data[4,1] = data11/data14
data[5,1] = data11/data15
data[6,1] = data11/data16
data[1,2] = data21/data21
data[2,2] = data21/data22
data[3,2] = data21/data23
data[4,2] = data21/data24
data[5,2] = data21/data25
data[6,2] = data21/data26
data[1,3] = data31/data31
data[2,3] = data31/data32
data[3,3] = data31/data33
data[4,3] = data31/data34
data[5,3] = data31/data35
data[6,3] = data31/data36
ideal = c(1,2,4,8,16,16)
print(data[,1])

points = as.matrix(c(1,2,4,8,16,32));
plot_colors <- c("orange", "cornflowerblue", "red2")

plot(   points, data[,1],     
        type="o",           
        pch=15, 
        cex=1.1,
        col=plot_colors[1],              
        ylim = c(1,17),   
        xlab="",     
        ylab="",         
        axes=FALSE,    
        bg=plot_colors[1],
        log="xy",
        lwd=1.1, 
        lty=1
)

axis(2, las=2) # horizontal y axis
axis(1, las=1, at=c(1,2,4,8,16,32), labels = c("1","2","4","8","16","32"), cex.axis=1.0)     # horizontal x axis
#axis(1, las=1, at=log(c(1,2,4,8,16,32)), labels = c("0.0","0.7","1.4","2.0","2.8","3.5"), cex.axis=1.0)     # horizontal x axis
mtext(2, text="Speed-up",line=2.3) 
mtext(1, text="#Threads",line=2) 

#lines(log(points), log(data[,2]), type="o", pch=16, lty=1, lwd=1.1, col=plot_colors[2], bg=plot_colors[2], cex=1.0)
#lines(log(points), log(data[,3]), type="o", pch=17, lty=1, lwd=1.1, col=plot_colors[3], bg=plot_colors[2], cex=1.0)
lines(points, data[,2], type="o", pch=16, lty=1, lwd=1.1, col=plot_colors[2], bg=plot_colors[2], cex=1.0)
lines(points, data[,3], type="o", pch=17, lty=1, lwd=1.1, col=plot_colors[3], bg=plot_colors[2], cex=1.0)
lines(points, ideal, type="l", lty=2, lwd=1.1)

box()	

legend( x="topleft", text.width=c(13,13),
        c("RC","DC","FH"), col=plot_colors, cex=1.0,
        pch=c(15,16,17), lty=c(1), lwd=c(1.1), bty="n", ncol=1, seg.len=2, x.intersp=0.5);
