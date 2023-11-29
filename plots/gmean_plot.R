library(ggplot2)
library(reshape2)
library(dplyr)

#"NB_no_retrain", AdaNB(classifier=AdaGaussianNB(), drift_detector=NoDrift())), 
#("NB_retrain", AdaNB(classifier=AdaGaussianNB(), drift_detector=NoDrift(), retrain=True)),
#("NB_gt"

no_drift <- read.csv("../output/NB_no_retrain_ground_truth_multi_class_global_swap_cluster_ds_1_c_10_ca_2_f_2_1_1.csv")
retrain <- read.csv("../output/NB_retrain_ground_truth_multi_class_global_swap_cluster_ds_1_c_10_ca_2_f_2_1_1.csv")
gt_drift <- read.csv("../output/NB_gt_ground_truth_multi_class_global_swap_cluster_ds_1_c_10_ca_2_f_2_1_1.csv")

no_drift$method <- "no_drift"
gt_drift$method <- "gt"
retrain$method <- "retrain"

df <- rbind(no_drift, gt_drift,retrain)


ggplot(data=df, aes(x=idx, y=accuracy)) + geom_line(aes(color=method))


mean(no_drift$class_8)
mean(gt_drift$class_8)
mean(retrain$class_8)

mean(retrain[99:102,]$accuracy)
mean(gt_drift[99:102,]$accuracy)
