require(graphics)
require(Matrix)

pdf(file="plots/Experiment2c2.pdf",
  width=5, height=4.5, family="serif", pointsize=14)

data = read.table("results/Exp2c_0.csv", sep=",")

plot_colors <- c("orangered","orange","cornflowerblue")

plot(   data[,1], data[,2],
        type="o",
        pch=15,
        cex=1.1,
        col=plot_colors[1],
        ylim = c(0,45),
		xlab="",
        ylab="",
        log="",
        axes=FALSE,
        bg=plot_colors[1],
        lwd=1.1,
	    lty=1
  )

lines(data[,1], data[,3], type="o", pch=18, lty=1, lwd=1.1, col=plot_colors[2], bg=plot_colors[1], cex=1.0)
lines(data[,1], data[,4], type="o", pch=17, lty=1, lwd=1.1, col=plot_colors[3], bg=plot_colors[2], cex=1.0)

axis(1, las=1)
axis(2, las=1)
mtext(2,text="Execution Time [s]",line=2.3)
mtext(1,text="Data Replication Factor",line=2)


box()	              # box around plot

legend( "topleft",
       c("SliceLine","IncSliceLine Init", "IncSliceLine"), ncol=1, col=plot_colors,
       pch=c(15,18,17), lty=c(1), lwd=c(1.1), bty="n", pt.bg=plot_colors);


dev.off()

