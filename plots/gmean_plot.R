library(ggplot2)
library(reshape2)
library(dplyr)


no_drift <- read.csv("../output/NB_No_drift_multi_class_global_swap_cluster_ds_1_c_5_ca_3_f_5_1_1.csv")
gt_drift <- read.csv("../output/NB_ground_truth_multi_class_global_swap_cluster_ds_1_c_5_ca_3_f_5_1_1.csv")

no_drift$method <- "no_drift"
gt_drift$method <- "gt"

df <- rbind(no_drift, gt_drift)


ggplot(data=df, aes(x=idx, y=accuracy)) + geom_line(aes(color=method))