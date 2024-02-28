library(ggplot2)
library(reshape2)
library(dplyr)


stream_name <- paste0("distance_prune_growth_new_branch_global_sudden_5")
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
  ggh4x::facet_grid2(class~variable,scales = "free_y", independent = "y") 




g
