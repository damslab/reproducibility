require(graphics)
require(Matrix)
options(warn = -1)

pdf(file="exp_8a.pdf",
    width=4.5, height=4.0, family="serif", pointsize=14)
#par(mar=c(3.5, 4, 2.5, 2) + 0.1)

base = as.matrix(read.table("..//results//resmicroeviction.dat", sep="\t"))
lru = as.matrix(read.table("..//results//resmicroeviction_lru.dat", sep="\t"))
cs = as.matrix(read.table("..//results//resmicroeviction_cs.dat", sep="\t"))
inf = as.matrix(read.table("..//results//resmicroeviction_inf.dat", sep="\t"))
base = colMeans(base)
lru = colMeans(lru)
cs = colMeans(cs)
inf = colMeans(inf)

data = matrix(0, 3, 4)
data[,1] = t(base)/1000
data[,2] = t(lru)/1000
data[,3] = t(cs)/1000
data[,4] = t(inf)/1000


plot_colors <- c("orange", "cornflowerblue", "grey30")

barplot( data, 
         space = c(0,1,1,1),
         xlab = "", 
         ylab = "",
         col=plot_colors,
         ylim = c(0,33),
         #log = "y",
         axes = FALSE, 
         names.arg = c("Base", "LRU", "C&S", "Infinite"),
         args.legend = list(x="topright", bty="n", bty="n", ncol=3, cex=1.0, x.intersp=0.5, text.width=0.4),
         legend.text = c("P1", "P2", "P3"),
         beside = FALSE,
         cex.names = 1.0,
         line = -0.7
)

#abline(v = 7.8) #vertical line seperator between groups
axis(2, las=2,) # horizontal y axis
mtext(2, text="Execution Time [s]",line=2.8) 
#mtext(1, text="Number of Rows [Thousands]",line=2) 

box()	

dev.off() 

