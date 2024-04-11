library(ggplot2)
library(reshape2)
library(ggforce)
library(RColorBrewer)
library(paletteer)


df <- read.csv("../metric_agg/agg_class_id_results.csv")

df_melt <- melt(df, id.vars = c("n_class", "class_affected"))


df_melt$n_class <- as.factor(df_melt$n_class)
df_melt$variable <-
  factor(
    paste(df_melt$class_affected, df_melt$variable, sep = "_"),
    levels = c("1_tp", "2_tp", "1_fn", "2_fn")
  )
df_melt <- df_melt[c("n_class", "variable", "value")]

g <- ggplot(df_melt, aes(y = n_class, x = value)) +
  geom_bar(
    aes(fill = variable),
    stat = "identity",
    position = position_fill(reverse = TRUE),
    colour = "black"
  ) +
  theme_bw() +
  theme(
    panel.grid.major = element_blank(),
    panel.border = element_blank(),
    legend.title = element_blank(),
    legend.position = "top",
    legend.text = element_text(size = 16),
    axis.text.x = element_blank(),
    axis.ticks.x = element_blank(),
    axis.text.y = element_text(size = 16, face = "bold"),
    axis.title.y = element_text(size = 18)
  ) +
  scale_x_continuous(expand = c(0.01, 0)) +
  scale_y_discrete(expand = c(0.15, 0.15)) +
  scale_fill_manual(
    values = c("#1a9641",
               "#a6d96a",
               "#fdae61",
               "#d7191c"),
    name = "Metric",
    labels = c(
      bquote("Detected C"[1]),
      bquote("Detected C"[2]),
      bquote("Not detected C"[1]),
      bquote("Not detected C"[2])
    ),
    expand = c(0, 0)
  ) +
  labs(x = "", y = "# of Classes")



g
ggsave("class_identification_bar.pdf",
       width = 8,
       height = 6)