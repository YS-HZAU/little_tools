library(ggplot2)
set.seed(123)
aa = runif(20,min=-1,max=1)
bb = runif(20,min=-1,max=1)
group = sample(c("A","B","C","D"),20,replace=T)
data = sample(1:4,20,replace=T)
mydat = data.frame(aa=aa,bb=bb,group=group,data=data)
ggplot(mydat,aes(x=aa,y=bb,group=group)) + 
  scale_shape_manual(values=c(0,1,2,3,4,5,6,7,8)) + 
  geom_point(size=6,aes(colour=group)) + 
  geom_text(label=paste(mydat$data),colour="black",size=4) +
  theme_bw() +
  theme(panel.grid=element_blank(),axis.line=element_line(size=1,colour="black"))