library(ggplot2)
library(reshape2)
library(dplyr)

stream_name <- "concepts_multi_class_global_prune_growth_new_branch_ds_5000_c_10_ca_2_f_10_1_1" 

df <- read.csv(paste0("../output/concepts/", stream_name, ".csv"))

df_filter <- df[df$class == 9,]


selected_features <- c("eigenvalues.mean" , "iq_range.mean", "kurtosis.mean", "mean.mean",
                       "median.mean", "nr_outliers", "sd.mean", "skewess.mean", "t_mean.mean")



df_filter$concept = df_filter$index > 50

g <- ggplot(data = df_filter) + geom_point(aes(x=sd.mean, y=kurtosis.mean, colour=concept))
g