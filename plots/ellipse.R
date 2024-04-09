library(ggplot2)
library(reshape2)
library(ggforce)
library(RColorBrewer)
library(paletteer)

kappa <- read.csv('Kappa-ranks.csv')
gmean <- read.csv('G-Mean-ranks.csv')

kappa_melted = melt(kappa, id.vars=c(1))
gmean_melted = melt(gmean, id.vars=c(1))

colnames(kappa_melted)[3] = "Kappa"
colnames(gmean_melted)[3] = "Gmean"

kappa_melted$Gmean = gmean_melted$Gmean

instance = kappa_melted[1,]

colors = as.vector(paletteer_c("grDevices::RdYlGn", 30))

#Comment this when the data is not ranking
kappa_melted$Kappa = 1 - (kappa_melted$Kappa/ max(kappa_melted$Kappa))
kappa_melted$Gmean = 1 - (kappa_melted$Gmean/ max(kappa_melted$Gmean))
kappa_melted$balance = kappa_melted$Kappa * kappa_melted$Gmean
kappa_melted$Gmean = kappa_melted$Gmean * kappa_melted$Gmean 
kappa_melted$Kappa = kappa_melted$Kappa * kappa_melted$Kappa

kappa_melted$Ratio <- factor(kappa_melted$Ratio, levels = c(1, 5, 10, 20, 50, 100) )

g = ggplot(kappa_melted) + 
  geom_ellipse(aes(x0 = 0, y0 = 0, a = Kappa, b = Gmean, angle = pi/4, fill=balance)) + 
  #scale_fill_continuous(colours=colors) +
  scale_fill_gradient2(low="red",mid="yellow", high="green", midpoint = 2*median(kappa_melted$balance)) +
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
  facet_grid(Ratio ~ variable, switch = "both" ) +
  ylab("Imbalance ratio") +
  theme(strip.background = element_blank(),
        strip.text.y.left = element_text(angle=0, size=15 ),
        strip.text.x = element_text(size=11),
        axis.title.y = element_text(size=16)) 

ggsave("BC_SIR_ellipse.pdf", g, width = 24)

#g <- ggplot() + stat_ellipse()

