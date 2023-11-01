library(ggplot2)
library(reshape2)
library(dplyr)

data <- read.csv("../output/multi_class_global_prune_growth_new_branch_ds_1_c_10_ca_5_f_2_1_1.csv")


df <- data[data$class_ref==7,]

df <- df[, colSums(is.na(df)) != nrow(df)]

df <- df %>% select_if(~ var(.) != 0)

melted_df <- melt(df, id.vars = "idx_ref")
melted_df <- melted_df[melted_df$variable != "ns_ratio",]

ggplot(data=melted_df, aes(x=idx_ref,y=value)) + 
  geom_line(aes(color=variable)) + 
  theme_bw() + 
  theme(legend.position = "none") + 
  facet_wrap( . ~ variable, ncol = 3, scales = "free")
