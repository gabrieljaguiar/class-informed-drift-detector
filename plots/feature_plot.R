library(ggplot2)
library(reshape2)
library(dplyr)




stream_name <- paste0("concepts_multi_class_local_swap_cluster_ds_5000_c_10_ca_2_f_10_1_1")
df <- read.csv(paste0("../output/concepts/", stream_name, ".csv"))
#        
df_filter <- df[df$class %in% c(6,9),]



#t(apply(df_filter, 1, rollmean, 3))

selected_features <- c("eigenvalues.mean" , "iq_range.mean", "mean.mean",
"median.mean", "sd.mean")
#df[,selected_features]
df_melt <- melt(df_filter, id.vars = c("index", "class"))
#        
df_melt <- df_melt[df_melt$variable %in% selected_features,]

#df_melt <- df_melt[df_melt$type == "concept",]

df_melt$variable <- factor(df_melt$variable)
df_melt$class <- factor(df_melt$class, levels=c(6,9), labels=c("C1", "C2"))
df_melt$variable <- factor(df_melt$variable, labels=c("Eigenvalues", "IQ Range", "Mean", "Median", "STD"))

g <- ggplot(data = df_melt) + geom_line(aes(x=index, y=value), color="#7ea7d9") + 
          geom_point(aes(x=index, y=value), color="#7ea7d9") +
          geom_rect(aes(xmin = 8,xmax = 12,  ymin=-Inf, ymax=Inf),fill="gray", alpha=0.05) +
          ggh4x::facet_grid2(class~variable,scales = "free_y", independent = "y") +
          theme_bw() +
          ylab("") +
          xlab("") +
          theme(legend.position = "none")


ggsave("detection_features.pdf", plot = g, height = 4, width=11)

#15.10x3.76