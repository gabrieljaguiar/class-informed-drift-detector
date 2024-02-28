library(ggplot2)
library(reshape2)
library(dplyr)
library(ggpubr)

n_classes = c(3,5,10,15,20)



files <- list.files("../datasets/", pattern="*.csv")

for (f in files){

  ciddm <- read.csv(paste0("../output/alerts_", f))
  
  ht_acc <- read.csv(paste0("../output/HT_ADWIN_",f))
  ht_adwin <- read.csv(paste0("../output/drift_alerts_HT_ADWIN_",f))
  #nb_adwin <- read.csv(paste0("../output/drift_alerts_NB_ADWIN_",f))
  
  columns <- c("idx", "accuracy")
  
  acc_df <- ht_acc[, columns]
  
  acc_melt <- melt(acc_df, id.vars="idx")
  
  g_ciddm <- ggplot(acc_melt, aes(x=idx, y=value)) + 
    geom_line(aes(color=variable)) +
    scale_x_continuous(labels=scales::comma) +
    geom_vline(xintercept = c(100000, 200000, 300000), 
               color="black", alpha=0.8, linetype=3, linewidth=1) +
    geom_vline(xintercept = ciddm$idx, 
               color="red", alpha=0.8, linetype=3, linewidth=1) +
    ggtitle("CIDDM") +
    theme_bw()
  
  g_adwin <- ggplot(acc_melt, aes(x=idx, y=value)) + 
    geom_line(aes(color=variable)) +
    scale_x_continuous(labels=scales::comma) +
    geom_vline(xintercept = c(100000, 200000, 300000), 
               color="black", alpha=0.8, linetype=3, linewidth=1) +
    geom_vline(xintercept = ht_adwin$idx, 
               color="red", alpha=0.8, linetype=3, linewidth=1) +
    ggtitle("ADWIN") +
    theme_bw()
  
  
  figure <- ggarrange(g_ciddm, g_adwin,
                      labels = c("", ""),
                      ncol = 2, nrow = 1)
  
  
  ggsave(paste0(f,".pdf"),width=16.77, height=3)

}