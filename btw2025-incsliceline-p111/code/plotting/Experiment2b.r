for(i in 1:7) {

  require(graphics)
  require(Matrix)

  pdf(file=paste("Experiment2b",i,".pdf",sep=""),
    width=7.3, height=3.0, family="serif", pointsize=14)

  numInit = (i-1)*4
  numInc = numInit + 1;


  data0 = readMM(paste("../results/Exp2b_1_debug.csv/",numInit,"_null.mtx",sep=""))[,2:3]
  data0 = t(as.matrix(data0))
  data1 = readMM(paste("../results/Exp2b_1_debug.csv/",numInc,"_null.mtx",sep=""))[,2:3]
  data1 = t(as.matrix(data1))

  data1 = rbind(data0, cbind(data1,matrix(0,2,ncol(data0)-ncol(data1))))

  plot_colors <- c("orange","black", "cornflowerblue","black")

  if( i==1 ) {
    barplot( data1,
             space = c(0, 0.3), xlab = "", ylab = "",
             col=plot_colors, ylim = c(0,12500),
             log = "", axes = FALSE,
             names.arg = c("1","2","3","4","5","6","7","8","9","10","11","12","13"),
             args.legend = list(x="topright", bty="n", bty="n", ncol=2, cex=0.95),
             legend.text = c("Init Enum", "Init Valid", "Inc Enum", "Inc Valid"),
             beside = TRUE, line=-0.9
    )

    mtext(1,text="Lattice Level L",line=1)
  }
  else{
    barplot( data1,
             space = c(0, 0.3), xlab = "", ylab = "",
             col=plot_colors, ylim = c(0,12500),
             log = "", axes = FALSE,
             beside = TRUE, line=-0.9
    )
  }

  axis(2, las=1)
  mtext(2,text="# Slices",line=3.1)

  numAdded=2^(i-1);
  text(4, 7000, paste("#added:",numAdded))


  box()	              # box around plot
  dev.off()

}
