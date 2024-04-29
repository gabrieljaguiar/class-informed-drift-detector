library(ggplot2)
library(reshape2)
library(dplyr)
library(ggpubr)

stream_name <- "swap_cluster_global_gradual_5.csv"

df_gt <- read.csv(paste0("../output/NB_RT_GT_", stream_name))
df_no_drift <-
  read.csv(paste0("../output/NB_RT_NO_DRIFT_", stream_name))

df_gt <- df_gt[c("idx", "accuracy", "class_4")]
df_no_drift <- df_no_drift[c("idx", "accuracy", "class_4")]
df_gt$detector <- "GT"
df_no_drift$detector <- "NO DRIFT"

df <- rbind(df_gt, df_no_drift)

df_point <- df[df$idx %in% seq(500, 400000, by=25000),]
# n_classes = c(3,5,10,15,20)

g <- ggplot(df, aes(x = idx, y = accuracy)) +
  geom_line(aes(color = detector)) +
  xlab("Instances") + ylab("Accuracy") +
  geom_point(data=df_point, aes(color=detector, shape=detector),size=2) +
  scale_color_manual(name = "Detector", values = c("#008837", "#b00404")) +
  scale_shape_manual(name = "Detector", values = c(19,18)) +
  scale_x_continuous(labels = scales::unit_format()) +
  scale_y_continuous(labels = scales::percent_format()) +
  theme_bw() + theme(legend.position = "top")

g
ggsave("NB_swap_cluster_gradual_5.pdf", width=5.20, height=3.92)
#7.6x3.92
# files <- list.files("../datasets/", pattern="*.csv")
#
# for (f in files){
#
#   ciddm <- read.csv(paste0("../output/alerts_", f))
#
#   ht_acc <- read.csv(paste0("../output/HT_ADWIN_",f))
#   ht_adwin <- read.csv(paste0("../output/drift_alerts_HT_ADWIN_",f))
#   #nb_adwin <- read.csv(paste0("../output/drift_alerts_NB_ADWIN_",f))
#
#   columns <- c("idx", "accuracy")
#
#   acc_df <- ht_acc[, columns]
#
#   acc_melt <- melt(acc_df, id.vars="idx")
#
#   g_ciddm <- ggplot(acc_melt, aes(x=idx, y=value)) +
#     geom_line(aes(color=variable)) +
#     scale_x_continuous(labels=scales::comma) +
#     geom_vline(xintercept = c(100000, 200000, 300000),
#                color="black", alpha=0.8, linetype=3, linewidth=1) +
#     geom_vline(xintercept = ciddm$idx,
#                color="red", alpha=0.8, linetype=3, linewidth=1) +
#     ggtitle("CIDDM") +
#     theme_bw()
#
#   g_adwin <- ggplot(acc_melt, aes(x=idx, y=value)) +
#     geom_line(aes(color=variable)) +
#     scale_x_continuous(labels=scales::comma) +
#     geom_vline(xintercept = c(100000, 200000, 300000),
#                color="black", alpha=0.8, linetype=3, linewidth=1) +
#     geom_vline(xintercept = ht_adwin$idx,
#                color="red", alpha=0.8, linetype=3, linewidth=1) +
#     ggtitle("ADWIN") +
#     theme_bw()
#
#
#   figure <- ggarrange(g_ciddm, g_adwin,
#                       labels = c("", ""),
#                       ncol = 2, nrow = 1)
#
#
#   ggsave(paste0(f,".pdf"),width=16.77, height=3)
#
# }