library(ggplot2)

length = c(1,2,3,4,5,6,7,8,9,10)
count = sample(1:10)
sample = c(rep("CTCF",5),rep("EZH2",5))
percentage = count/10
mydat = data.frame(length=length,count=count,sample=sample,percentage=percentage)
ggplot(mydat, aes(x = length, y=percentage, group = sample, fill = sample, colour = sample)) +
  geom_line(size=0.75,aes(linetype=sample)) +
  scale_color_manual( values = c("#da1c6f","#da1c6f","#f8b62b","#f8b62b","#00a0e9","#00a0e9","#009944","#009944")) +
  scale_linetype_manual(values = c("solid","dashed","solid","dashed","solid","dashed","solid","dashed")) +
  scale_x_continuous(expand = c(0,0),limits = c(-0.1,11), breaks = seq(0,11, by=2)) + 
  scale_y_continuous(expand = c(0,0)) +
  labs(title="test") + 
  geom_vline(xintercept=4, linetype="dotted") +
  theme_bw() + 
  theme(panel.grid=element_blank(),axis.line=element_line(size=1,colour="black"))

ggplot(mydat, aes(x = length, y=percentage, group = sample, fill = sample , colour = sample)) +
  # adjust 拟合参数.带宽，带宽越大，曲线越光滑，默认带宽为1，可以通过adjust参数进行调整。
  geom_line(size=0.75,adjust=2,aes(linetype=sample)) +
  scale_color_manual( values = c("#da1c6f","#da1c6f","#f8b62b","#f8b62b","#00a0e9","#00a0e9","#009944","#009944")) +
  scale_linetype_manual(values = c("solid","dashed","solid","dashed","solid","dashed","solid","dashed")) +
  scale_x_continuous(expand = c(0,0),limits = c(-0.1,11), breaks = seq(0,11, by=2)) + 
  scale_y_continuous(expand = c(0,0)) +
  labs(title="test") + 
  geom_vline(xintercept=4, linetype="dotted") +
  theme_bw() + 
  theme(panel.grid=element_blank(),axis.line=element_line(size=1,colour="black"))
