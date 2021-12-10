require(graphics)
require(Matrix)
options(warn = -1)

file = 
pdf(file="exp_9f.pdf",
    width=4.5, height=4.0, family="serif", pointsize=14)

DIR = "/home/aphani/sigmod_21_exp/revision/results"

l2svmSyn = rowMeans(matrix(as.matrix(read.table("..//results//resl2svmSyn.dat", sep="\t"))[,3],1,3,byrow=TRUE))
l2svmSyn_R = rowMeans(matrix(as.matrix(read.table("..//results//resl2svmSyn_reuse.dat", sep="\t"))[,3],1,3,byrow=TRUE))
l2svmKdd = rowMeans(matrix(as.matrix(read.table("..//results//resl2svmKdd.dat", sep="\t"))[,3],1,3,byrow=TRUE))
l2svmKdd_R = rowMeans(matrix(as.matrix(read.table("..//results//resl2svmKdd_reuse.dat", sep="\t"))[,3],1,3,byrow=TRUE))
l2svmKdd_np = rowMeans(matrix(as.matrix(read.table("..//results//resl2svmKdd_np.dat", sep="\t"))[,3],1,3,byrow=TRUE))
l2svmKdd_np_R = rowMeans(matrix(as.matrix(read.table("..//results//resl2svmKdd_np_reuse.dat", sep="\t"))[,3],1,3,byrow=TRUE))

exampleSyn = rowMeans(matrix(as.matrix(read.table("..//results//resexampleSyn.dat", sep="\t"))[,3],1,3,byrow=TRUE))
exampleSyn_R = rowMeans(matrix(as.matrix(read.table("..//results//resexampleSyn_reuse.dat", sep="\t"))[,3],1,3,byrow=TRUE))
exampleKdd = rowMeans(matrix(as.matrix(read.table("..//results//resexampleKdd.dat", sep="\t"))[,3],1,3,byrow=TRUE))
exampleKdd_R = rowMeans(matrix(as.matrix(read.table("..//results//resexampleKdd_reuse.dat", sep="\t"))[,3],1,3,byrow=TRUE))
exampleKdd_np = rowMeans(matrix(as.matrix(read.table("..//results//resexampleKdd_np.dat", sep="\t"))[,3],1,3,byrow=TRUE))
exampleKdd_np_R = rowMeans(matrix(as.matrix(read.table("..//results//resexampleKdd_np_reuse.dat", sep="\t"))[,3],1,3,byrow=TRUE))

exampleCVSyn = rowMeans(matrix(as.matrix(read.table("..//results//resexampleCVSyn.dat", sep="\t"))[,3],1,3,byrow=TRUE))
exampleCVSyn_R = rowMeans(matrix(as.matrix(read.table("..//results//resexampleCVSyn_reuse.dat", sep="\t"))[,3],1,3,byrow=TRUE))
exampleCVKdd = rowMeans(matrix(as.matrix(read.table("..//results//resexampleCVKdd.dat", sep="\t"))[,3],1,3,byrow=TRUE))
exampleCVKdd_R = rowMeans(matrix(as.matrix(read.table("..//results//resexampleCVKdd_reuse.dat", sep="\t"))[,3],1,3,byrow=TRUE))
exampleCVKdd_np = rowMeans(matrix(as.matrix(read.table("..//results//resexampleCVKdd_np.dat", sep="\t"))[,3],1,3,byrow=TRUE))
exampleCVKdd_np_R = rowMeans(matrix(as.matrix(read.table("..//results//resexampleCVKdd_np_reuse.dat", sep="\t"))[,3],1,3,byrow=TRUE))

ensSyn = rowMeans(matrix(as.matrix(read.table("..//results//resenswpSyn.dat", sep="\t"))[,3],1,3,byrow=TRUE))
ensSyn_R = rowMeans(matrix(as.matrix(read.table("..//results//resenswpSyn_reuse.dat", sep="\t"))[,3],1,3,byrow=TRUE))
ensAps = rowMeans(matrix(as.matrix(read.table("..//results//resenswpAps.dat", sep="\t"))[,3],1,3,byrow=TRUE))
ensAps_R = rowMeans(matrix(as.matrix(read.table("..//results//resenswpAps_reuse.dat", sep="\t"))[,3],1,3,byrow=TRUE))
ensAps_np = rowMeans(matrix(as.matrix(read.table("..//results//resenswpAps_np.dat", sep="\t"))[,3],1,3,byrow=TRUE))
ensAps_np_R = rowMeans(matrix(as.matrix(read.table("..//results//resenswpAps_np_reuse.dat", sep="\t"))[,3],1,3,byrow=TRUE))

pcaSyn = rowMeans(matrix(as.matrix(read.table("..//results//respcaSyn.dat", sep="\t"))[,3],1,3,byrow=TRUE))
pcaSyn_R = rowMeans(matrix(as.matrix(read.table("..//results//respcaSyn_reuse.dat", sep="\t"))[,3],1,3,byrow=TRUE))
pcaKdd = rowMeans(matrix(as.matrix(read.table("..//results//respcaKdd.dat", sep="\t"))[,3],1,3,byrow=TRUE))
pcaKdd_R = rowMeans(matrix(as.matrix(read.table("..//results//respcaKdd_reuse.dat", sep="\t"))[,3],1,3,byrow=TRUE))
pcaKdd_np = rowMeans(matrix(as.matrix(read.table("..//results//respcaKdd_np.dat", sep="\t"))[,3],1,3,byrow=TRUE))
pcaKdd_np_R = rowMeans(matrix(as.matrix(read.table("..//results//respcaKdd_np_reuse.dat", sep="\t"))[,3],1,3,byrow=TRUE))

data = matrix(0, 3, 5)
data[1,1] = l2svmSyn/l2svmSyn_R
data[2,1] = l2svmKdd/l2svmKdd_R
data[3,1] = l2svmKdd_np/l2svmKdd_np_R
data[1,2] = exampleSyn/exampleSyn_R
data[2,2] = exampleKdd/exampleKdd_R
data[3,2] = exampleKdd_np/exampleKdd_np_R
data[1,3] = exampleCVSyn/exampleCVSyn_R
data[2,3] = exampleCVKdd/exampleCVKdd_R
data[3,3] = exampleCVKdd_np/exampleCVKdd_np_R
data[1,4] = ensSyn/ensSyn_R
data[2,4] = ensAps/ensAps_R
data[3,4] = ensAps_np/ensAps_np_R
data[1,5] = pcaSyn/pcaSyn_R
data[2,5] = pcaKdd/pcaKdd_R
data[3,5] = pcaKdd_np/pcaKdd_np_R


line1 <- c("(a)","(b)","(c)","(d)","(e)")

plot_colors <- c("orange","cornflowerblue","red")

barplot( data, 
         space = c(0,2.5),
         xlab = "", 
         ylab = "",
         col=plot_colors,
         ylim = c(0,8.5),
         #log = "y",
         axes = FALSE, 
         names.arg = line1,
         args.legend = list(x="topright", bty="n", bty="n", ncol=1, x.intersp=0.5),
         legend.text = c("Synthetic", "Real", "RealNP"),
         beside = TRUE,
         #line = -0.7,
)

abline(h=1, lty=2, lwd=0.7)

axis(2, las=2) # horizontal y axis
mtext(2, text="Speed-up [X]",line=2.2) 
mtext(1, text="Pipelines (KDD98 & APS)", line=2)

#text(x=21.3, y=42, labels="#Rows: 20K")
#text(x=20.2, y=33, labels="#Ops/Iter:   40")

box()	

dev.off() 
