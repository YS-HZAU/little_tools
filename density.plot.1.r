library(ggplot2)
args=commandArgs(T)
mydat=read.table(args[1],header=F)
names(mydat)=c("length")
out=args[2]
avg=as.numeric(args[3])
pdf(out,width=18)
ggplot(mydat,mapping = aes(x = length)) +
  geom_histogram(binwidth=5, aes(y=..density..), colour="#f8b62b", fill="#f8b62b") +
  geom_density(alpha=.2,colour="#00a0e9",lwd=1) +
  scale_x_continuous(expand = c(0,0)) +
  scale_y_continuous(expand = c(0,0)) +
  geom_vline(xintercept=mean(mydat$length), linetype="dotted") +
  labs(title=args[1]) +
  labs(title="test") +
  theme_bw() +
  theme(panel.grid=element_blank(),axis.line=element_line(size=1,colour="black"))

ggplot(mydat,mapping = aes(x = length)) +
  geom_histogram(binwidth=5, aes(y=..density..), colour="#f8b62b", fill="#f8b62b") +
  geom_density(alpha=.2,colour="#00a0e9",lwd=1) +
  scale_x_continuous(expand = c(0,0)) +
  scale_y_continuous(expand = c(0,0)) +
  geom_vline(xintercept=avg, linetype="dotted") +
  geom_vline(xintercept=mean(mydat$length), linetype="dotted") +
  labs(title=args[1]) +
  labs(title="test") +
  theme_bw() +
  theme(panel.grid=element_blank(),axis.line=element_line(size=1,colour="black"))
dev.off()
