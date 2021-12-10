require(graphics)
require(Matrix)

pdf(file="plots/Experiment5b.pdf",
  width=3.7, height=4.0, family="serif", pointsize=14)

data = as.matrix(read.table("results/Experiment5b_times.dat", sep=",")[3])/1000

plot_colors <- c("orangered","orange","cornflowerblue")

barplot( data, 
         space = c(0.1,0.1),
         xlab = "", 
         ylab = "",
         col=plot_colors,
         ylim = c(0,1350),
         log = "",
         axes = FALSE, 
         names.arg = c("MT-Ops","","Dist-PFor"),
         args.legend = list(x="topleft", bty="n", bty="n", ncol=1),
         beside = TRUE,
)

axis(2, las=1) 
mtext(2,text="Execution Time [s]",line=2.8) 
mtext(1,text="MT-PFor",line=0.2) 
mtext(1,text="Parallel Configurations",line=2) 

text(2.73,800,"scale-out")
text(2.5,1200,"1x USCensus")


box()	              # box around plot       
dev.off() 
