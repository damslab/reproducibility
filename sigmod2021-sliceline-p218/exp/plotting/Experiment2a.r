require(graphics)
require(Matrix)

pdf(file="plots/Experiment2a.pdf",
  width=4.5, height=4.0, family="serif", pointsize=14)

data0 = read.table("results/Experiment2_Adult.dat", sep=",")[,2:3]
data1 = t(as.matrix(data0))


plot_colors <- c("cornflowerblue","black")

print(ncol(data1))

barplot( data1, 
         space = c(0, 0.3),
         xlab = "", 
         ylab = "",
         col=plot_colors,
         ylim = c(0,12500),
         log = "",
         axes = FALSE, 
         names.arg = c("1","2","3","4","5","6","7","8","9","10","11","12","13"),
         args.legend = list(x="topright", bty="n", bty="n", ncol=1),
         legend.text = c("Evaluated", expression(paste("Valid (",sigma,")"))),
         beside = TRUE,
         line=-0.9
)

axis(2, las=1) 
mtext(2,text="# Enumerated Slices",line=3.1) 
mtext(1,text="Lattice Level L",line=1) 


box()	              # box around plot       
dev.off() 
