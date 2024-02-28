library(ggplot2)
library(reshape2)
library(dplyr)



difficulties <- c("swap_cluster", "swap_leaves", "prune_growth_new_branch", "split_node")

locality <- c("local", "global")

feature_number <- c(10)

ds_speed <- c(1, 5000)

#for (l in locality){
#  for (d in difficulties){
#    for (f in feature_number){
#      for (ds in ds_speed){
#        stream_name <- paste0("concepts_multi_class_", l,"_",d,"_ds_",ds,"_c_10_ca_2_f_",f,"_1_1")
#        df <- read.csv(paste0("../output/concepts/", stream_name, ".csv"))
#        
#        #df_filter <- df[df$class > 7,]
#        df_filter <- df
        
#        selected_features <- c("eigenvalues.mean" , "iq_range.mean", "kurtosis.mean", "mean.mean",
#                               "median.mean", "sd.mean", "skewess.mean", "t_mean.mean")
#        df[,selected_features]
#        df_melt <- melt(df_filter, id.vars = c("index", "class"))
#        
#        df_melt <- df_melt[df_melt$variable %in% selected_features,]
        
#        g <- ggplot(data = df_melt) + geom_line(aes(x=index, y=value, color=variable)) + 
#          ggh4x::facet_grid2(class~variable,scales = "free_y", independent = "y") +
#          theme(legend.position = "none")
#        ggsave(paste0("./", stream_name, ".pdf"), height=18, width=15.10)
#      }
#    }
#  }
#}

library(zoo)


stream_name <- paste0("concepts_prune_growth_new_branch_local_sudden_5")
df <- read.csv(paste0("../output/", stream_name, ".csv"))
#        
#df_filter <- df[df$class > 4,]
df_filter <- df


#t(apply(df_filter, 1, rollmean, 3))

selected_features <- c("eigenvalues.mean" , "iq_range.mean", "kurtosis.mean", "mean.mean",
"median.mean", "sd.mean", "skewess.mean", "t_mean.mean")
#df[,selected_features]
df_melt <- melt(df_filter, id.vars = c("index", "class", "type"))
#        
df_melt <- df_melt[df_melt$variable %in% selected_features,]

#df_melt <- df_melt[df_melt$type == "concept",]

g <- ggplot(data = df_melt) + geom_line(aes(x=index, y=value, color=type)) + 
          ggh4x::facet_grid2(class~variable,scales = "free_y", independent = "y") +
          theme(legend.position = "none")




g

#15.10x3.76