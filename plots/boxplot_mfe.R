library(ggplot2)
library(reshape2)
library(dplyr)


#data <- read.csv("../output/multi_class_global_prune_growth_new_branch_ds_1_c_10_ca_2_f_5_1_1.csv")
data <- read.csv("../output/multi_class_global_swap_leaves_ds_1_c_10_ca_5_f_2_1_1.csv")



df <- data
#df <- data[data$class_ref==7,]

feat <- c("kurtosis.mean", "eigenvalues.mean", "iq_range.mean", "nr_outliers", "sd.mean")

feats <- c("idx_ref", "class_ref",feat)

#df <- df[, colSums(is.na(df)) != nrow(df)]

#df <- df %>% select_if(~ var(.) != 0)

df <- df[, feats]

df[, feat] <- as.data.frame(scale(df[, feat]))

melted_df <- melt(df, id.vars = c("idx_ref", "class_ref"))
melted_df <- melted_df[melted_df$variable != "ns_ratio",]

g <- ggplot(data=melted_df, aes(x=idx_ref,y=value)) + 
  geom_line(aes(color=variable)) + 
  theme_bw() + 
  theme(legend.position = "none") + 
  ggh4x::facet_grid2(class_ref ~ variable, scales = "free_y", independent = "y")


ggsave(filename = "global_swap_leaves.pdf",g, height = 12, width=12)