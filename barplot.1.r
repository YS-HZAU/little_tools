library(reshape2)
library(ggplot2)
sample = c("row1","row2","row3","row4")
col1 = c(145074618,147727479,119838375,137302673)
col2 = c(575596288,186597397,399216860,509472869)
col3 = c(8828138,2406567,8611785,5621498)
mydat = data.frame(sample=sample,col1=col1,col2=col2,col3=col3)
md = melt(mydat,id=c("sample"),measure=c("col1","col2","col3"))

sample = c("row1","row2","row3","row4","row1","row2","row3","row4","row1","row2","row3","row4")
variable = c("col1","col1","col1","col1","col2","col2","col2","col2","col3","col3","col3","col3")
value = c(145074618,147727479,119838375,137302673,575596288,186597397,399216860,509472869,8828138,2406567,8611785,5621498)
md = data.frame(sample=sample,variable=variable,value=value)

col = c("#f8b62b","#00a0e9","#009944")
ggplot(data = md, mapping = aes(x = sample, y = value, fill = variable)) + # 解析数据
  geom_bar(stat = 'identity', position = 'fill',colour = 'black') + # 画图
  scale_fill_manual(values = col) +
  ylab('percent') + 
  theme_bw() + 
  theme(panel.grid=element_blank(),axis.line=element_line(size=1,colour="black"))