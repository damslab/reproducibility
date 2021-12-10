require(graphics)
require(Matrix)

pdf(file="plots/Experiment2b.pdf",
  width=4.5, height=4.0, family="serif", pointsize=14)

data1 = read.table("results/Experiment2_Covtype.dat", sep=",")[,2:3]
data2 = read.table("results/Experiment2_USCensus.dat", sep=",")[,2:3]
data3 = read.table("results/Experiment2_KDD98.dat", sep=",")[,2:3]

data1 = t(rbind(as.matrix(data3),matrix(1,1,2),
      as.matrix(data2),matrix(1,1,2),as.matrix(data1)))

plot_colors <- c("cornflowerblue","black")

barplot( data1, 
         space = c(0, 0.3),
         xlab = "", 
         ylab = "",
         col=plot_colors,
         ylim = c(1,25000000),
         log = "y",
         axes = FALSE, 
         names.arg = c("1","2","3","","1","2","3","4","","1","2","3"),
         cex.names=0.96,
         args.legend = list(x="topright", bty="n", bty="n", ncol=1),
         legend.text = c("Evaluated Slices", expression(paste("Valid Slices (",sigma,")"))),
         beside = TRUE,
         line = -0.9
)

axis(2, las=1, at=c(1,10,100,1000,1e4,1e5,1e6,1e7), labels=c("1","10","100","1000","1e4","1e5","1e6","1e7")) 
mtext(2,text="# Enumerated Slices",line=2.7) 
axis(1, las=1, at=c(3.0,14,24.8), labels=c("KDD98","USCensus","Covtype") ) 
#mtext(1,text="Datasets",line=2) 


box()	              # box around plot       
dev.off() 
