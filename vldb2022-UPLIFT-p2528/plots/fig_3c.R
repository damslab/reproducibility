require(graphics)
require(Matrix)

pdf(file="fig_3c.pdf",
    width=4.8, height=4, family="serif", pointsize=14)
#par(mar=c(3.5, 4, 2.5, 2) + 0.1)

RC = rowMeans(matrix(as.matrix(read.table("..//results//res_RC_breakdown.dat", sep="\t"))[,1],4,3,byrow=TRUE))
RCBase = rowMeans(matrix(as.matrix(read.table("..//results//res_RC_breakdown_base.dat", sep="\t"))[,1],4,3,byrow=TRUE))
DC = rowMeans(matrix(as.matrix(read.table("..//results//res_DC_breakdown.dat", sep="\t"))[,1],4,3,byrow=TRUE))
DCBase = rowMeans(matrix(as.matrix(read.table("..//results//res_DC_breakdown_base.dat", sep="\t"))[,1],4,3,byrow=TRUE))
binRC = rowMeans(matrix(as.matrix(read.table("..//results//res_BIN-RC_breakdown.dat", sep="\t"))[,1],4,3,byrow=TRUE))
binRCBase = rowMeans(matrix(as.matrix(read.table("..//results//res_BIN-RC_breakdown_base.dat", sep="\t"))[,1],4,3,byrow=TRUE))

data = matrix(0, 4, 6)
data[,1] = t(RC)/1000
data[,2] = t(RCBase)/1000
data[,3] = t(DC)/1000
data[,4] = t(DCBase)/1000
data[,5] = t(binRC)/1000
data[,6] = t(binRCBase)/1000

plot_colors <- c("cornflowerblue","grey30","red2","orange")

plt = barplot( data,
         space = c(0,0,1,0,1,0),
         xlab = "",
         ylab = "",
         col=plot_colors,
         ylim = c(0,120),
         #log = "y",
         axes = FALSE,
         las=2, #rotate names
         args.legend = list(x="topleft", bty="n", bty="n", ncol=2, cex=1.0, x.intersp=0.5, text.width=1.2),
         legend.text = c("Build", "Alloc", "Apply", "Meta"),
         cex.names = 1.0, #reduce name size
         line = -0.7
)

axis(2, las=2,) # horizontal y axis
mtext(2, text="Execution Time [s]",line=2.8)
#mtext(1, text="Number of Rows [Thousands]",line=2)
text(c(0.5,1.5,3.5,4.5,6.5,7.5), labels=c("RC-U","RC-B","DC-U","DC-B","BIN-U","BIN-B"), 
    par("usr")[3], adj=c(1.1,1.1), srt=40, xpd=TRUE, cex=0.9)

box()

dev.off()

