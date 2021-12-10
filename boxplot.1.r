library(ggpubr)
data("ToothGrowth")
meandata = aggregate(len ~ supp, data = ToothGrowth, mean)
meandata$length = seq(1:nrow(meandata))
ToothGrowth$supp = factor(ToothGrowth$supp, levels=meandata$supp)
aa = as.vector(meandata$supp)
my_comparisons = list()
tmpend = length(aa)-1
for(i in 1:tmpend){
    tmpstart = i+1
    for(j in tmpstart:length(aa)){
        my_comparisons = append(my_comparisons,list(c(aa[i],aa[j])))
    }
}

ggboxplot(ToothGrowth,x="supp",fill="supp",y="len",color = "black",palette=c("#feb6fd", "#ffb548", "#cde8ec"),width=0.6,outlier.colour=NA)+
# outlier.colour=NA 让离群点不着色
#  coord_flip()+
#  stat_compare_means(label = "p.signif",method="wilcox.test",comparisons=my_comparisons,label.y=c(10,12,14,16,18,20)) +
  stat_compare_means(label = "p.signif",method="wilcox.test",comparisons=my_comparisons) +
#  stat_compare_means(label.y = 10,label.x = 3) +
  geom_hline(yintercept = median(ToothGrowth$len), linetype=2) +
#  scale_y_continuous(limit=c(0,20),breaks=seq(0, 20, 5)) +
  geom_point(data=meandata,mapping=aes(x=supp,y=len),size=5) +
  theme_bw() +
  theme(panel.grid=element_blank(),axis.line=element_line(size=1,colour="black"))

ToothGrowth$normal = log2(ToothGrowth$len+1)
meandata$normal = log2(meandata$len+1)
ggboxplot(ToothGrowth,x="supp",fill="supp",y="len",color = "black",palette=c("#feb6fd", "#ffb548", "#cde8ec"),width=0.6,outlier.colour=NA)+
# outlier.colour=NA 让离群点不着色
#  coord_flip()+
#  stat_compare_means(label = "p.signif",method="wilcox.test",comparisons=my_comparisons,label.y=c(10,12,14,16,18,20)) +
  stat_compare_means(label = "p.signif",method="wilcox.test",comparisons=my_comparisons) +
#  stat_compare_means(label.y = 10,label.x = 3) +
  geom_hline(yintercept = median(ToothGrowth$len), linetype=2) +
#  scale_y_continuous(limit=c(0,20),breaks=seq(0, 20, 5)) +
  geom_point(data=meandata,mapping=aes(x=supp,y=len),size=5) +
  theme_bw() +
  theme(panel.grid=element_blank(),axis.line=element_line(size=1,colour="black"))

ggboxplot(ToothGrowth,x="supp",fill="supp",y="normal",color = "black",palette=c("#feb6fd", "#ffb548", "#cde8ec"),width=0.6,outlier.colour=NA)+
# outlier.colour=NA 让离群点不着色
#  coord_flip()+
#  stat_compare_means(label = "p.signif",method="wilcox.test",comparisons=my_comparisons,label.y=c(10,12,14,16,18,20)) +
  stat_compare_means(label = "p.signif",method="wilcox.test",comparisons=my_comparisons) +
#  stat_compare_means(label.y = 10,label.x = 3) +
  geom_hline(yintercept = log2(median(ToothGrowth$len)+1), linetype=2) +
#  scale_y_continuous(limit=c(0,20),breaks=seq(0, 20, 5)) +
  geom_point(data=meandata,mapping=aes(x=supp,y=normal),size=5) +
  theme_bw() +
  theme(panel.grid=element_blank(),axis.line=element_line(size=1,colour="black"))

compare_means(data=ToothGrowth,len~supp,method = "wilcox.test")