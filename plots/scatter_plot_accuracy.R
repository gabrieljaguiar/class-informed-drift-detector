library(Rcpp)
library(ggplot2)
library(reshape2)
library(ggrepel)

data <- read.csv("../metric_agg/rank_metrics_ht.csv")


data$balance = data$acc_rank  * data$gmean_rank


g = ggplot(data,  aes(x=acc_rank, y=gmean_rank)) 
g = g + geom_point(size=3, aes(x=acc_rank, y=gmean_rank, colour=balance)) #Without size
#g = g + geom_point( aes(x=Kappa, y=Gmean, colour=balance, size=1/balance)) #WithSize
g = g + scale_colour_gradient2(low="green",mid="yellow", high="red", midpoint = mean(data$balance))
g = g + geom_label_repel(aes(label = dd),
                         box.padding   = 0.35, 
                         point.padding = 0.5,
                         size = 5,
                         segment.color = 'grey50') + theme_bw() 

g = g + theme(panel.grid.major = element_blank(), 
              legend.position = "none", 
              plot.title = element_text(hjust = 0.5, size = 18)) +
  #ggtitle("Multi-class experiments - Kappa vs Runtime") + 
  ylab("Delay Rank") + xlab("F1 Rank") + ggtitle("HT") +
  scale_y_continuous(limits=c(1,11),breaks=seq(1, 11,by=2)) + 
  scale_x_continuous(limits=c(1,11),breaks=seq(1, 11,by=2))

ggsave("scatter_acc_HT.pdf", g, width = 8, height = 6.5)