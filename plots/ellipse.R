library(ggplot2)
library(reshape2)
library(ggforce)
library(RColorBrewer)
library(paletteer)

data <- read.csv("../metric_agg/ranking_average_nb.csv")
data <- data[data$drift_type=="gradual",]

#kappa <- read.csv('Kappa-ranks.csv')
#gmean <- read.csv('G-Mean-ranks.csv')

#kappa_melted = melt(kappa, id.vars=c(1))
#gmean_melted = melt(gmean, id.vars=c(1))

#colnames(kappa_melted)[3] = "Kappa"
#colnames(gmean_melted)[3] = "Gmean"

#kappa_melted$Gmean = gmean_melted$Gmean

#instance = kappa_melted[1,]

colors = as.vector(paletteer_c("grDevices::RdYlGn", 30))

#Comment this when the data is not ranking
data$f1 = 1 - (data$f1/ max(data$f1))
data$delay = 1 - (data$delay/ max(data$delay))
data$balance = data$f1 * data$delay
data$f1 = data$f1 * data$f1
data$delay = data$delay * data$delay

data$n_class <- factor(data$n_class, levels = c(3, 5, 10, 15) )

g = ggplot(data) + 
  geom_ellipse(aes(x0 = 0, y0 = 0, a = f1, b = delay, angle = pi/4, fill=balance)) + 
  #scale_fill_continuous(colours=colors) +
  scale_fill_gradient2(low="red",mid="yellow", high="green", midpoint = 2*median(data$balance)) +
  coord_fixed() +
  theme_bw() + ylab("") + xlab("") +
  theme(panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank(), 
        panel.border = element_blank(),
        axis.text.x = element_blank(),
        axis.text.y = element_blank(),
        axis.ticks.x = element_blank(),
        axis.ticks.y = element_blank(),
        legend.position = "none") +
  facet_grid(n_class ~ dd, switch = "both" ) +
  ylab("# of classes") +
  theme(strip.background = element_blank(),
        strip.text.y.left = element_text(angle=0, size=15 ),
        strip.text.x = element_text(size=11),
        axis.title.y = element_text(size=16)) 

ggsave("NB_gradual_ellipse.pdf", g, width = 12, height=4.5)

#g <- ggplot() + stat_ellipse()

