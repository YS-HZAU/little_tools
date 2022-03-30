rm(list=ls())
library(scatterplot3d)
library(DESeq2)
library(ggord)
library(ggplot2)
library(FactoMineR)
setwd("C:\\Users\\Dell\\Desktop")
mycounts <- read.table("c2_read.txt", header=T, row.names=1)
colData <- read.table("c2_group.txt", header=T, row.names=1)
dds <- DESeqDataSetFromMatrix(mycounts, colData, design=~condition)
vsd <- vst(dds, blind=FALSE)
df1 <- assay(vsd)
# df1 <- read.delim('c2_tpm.txt', row.names=1, sep='\t')
df2 <- log2(df1+1)
df3 <- t(df2)
df3.pca <- PCA(df3, ncp=3, scale.unit=TRUE, graph=FALSE)
plot(df3.pca)

pca_sample <- data.frame(df3.pca$ind$coord[ ,1:3])
pca_eig1 <- round(df3.pca$eig[1,2],2)
pca_eig2 <- round(df3.pca$eig[2,2],2)
pca_eig3 <- round(df3.pca$eig[3,2],2)

group <- read.delim('c2_group.txt', row.names=1, sep='\t', check.names=FALSE)
group <- group[rownames(pca_sample), ]
pca_sample <- cbind(pca_sample, group)
# pca_sample[4:33,]
my_color <- c('#f9c74f', '#d6f94f', '#4f81f9', '#f94fd6', '#4ff9c7', '#f9724f', '#4fd6f9', '#5f9ea0', '#a05f9e', '#5fa061')
colors <- my_color[as.numeric(factor(pca_sample[4:33,]$condition))]

p <- scatterplot3d(pca_sample[4:33,1:3], color=colors, main="3DPCA", pch=rep(c(11,17), c(15,15)), angle=40, cex.symbols=1.5, cex.axis=0.8, xlab=paste('PCA1: ', pca_eig1), ylab=paste('PCA2: ', pca_eig2), zlab=paste('PCA3: ', pca_eig3))
legend(p$xyz.convert(18, 5, 10), legend=levels(factor(pca_sample[4:33,]$condition)), col=colors, pch=rep(c(11,17), c(18,15)))

my_color <- c('#f94144','#f9c74f','#5390d9',"#66C2A5FF","#FC8D62FF","#8DA0CBFF",'#f9c74f','#5390d9',"#66C2A5FF","#FC8D62FF","#8DA0CBFF")
my_color <- c('#f9c74f', '#d6f94f', '#4f81f9', '#f94fd6', '#4ff9c7', '#f9724f', '#4fd6f9', '#5f9ea0', '#a05f9e', '#5fa061', '#FF0000')
colors <- my_color[as.numeric(factor(pca_sample$condition))]
p <- scatterplot3d(pca_sample[,1:3], color=colors, main="3DPCA", pch=rep(c(11,17), c(18,15)), angle=40, cex.symbols=1.5, cex.axis=0.8, xlab=paste('PCA1: ', pca_eig1), ylab=paste('PCA2: ', pca_eig2), zlab=paste('PCA3: ', pca_eig3))
legend(p$xyz.convert(18, 5, 10), legend=levels(factor(pca_sample$condition)), col=colors, pch=rep(c(11,17), c(18,15)))