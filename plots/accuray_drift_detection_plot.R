library(ggplot2)
library(reshape2)
library(dplyr)
library(ggpubr)

ciddm <- read.csv("../output/alerts_prune_growth_new_branch_global_recurrent_20.csv")

ht_acc <- read.csv("../output/HT_ADWIN_prune_growth_new_branch_global_recurrent_20.csv")
ht_adwin <- read.csv("../output/drift_alerts_HT_ADWIN_prune_growth_new_branch_global_recurrent_20.csv")
nb_adwin <- read.csv("../output/drift_alerts_NB_ADWIN_prune_growth_new_branch_global_recurrent_20.csv")

columns <- c("idx", "accuracy", "class_9")

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

figure