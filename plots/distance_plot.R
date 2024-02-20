library(ggplot2)
library(reshape2)
library(dplyr)



difficulties <- c("swap_cluster", "swap_leaves", "prune_growth_new_branch")

locality <- c("local", "global")

feature_number <- c(10)

ds_speed <- c(1, 5000)

for (l in locality){
  for (d in difficulties){
    for (f in feature_number){
      for (ds in ds_speed){
        stream_name <- paste0("drift_alerts_concepts_multi_class_", l,"_",d,"_ds_",ds,"_c_10_ca_2_f_",f,"_1_1")
        df <- read.csv(paste0("../output/", stream_name, ".csv"))
        #dd_alerts <- df[, c("idx", "drift", "class")]
        #dd_alerts <- dd_alerts[dd_alerts$drift == 1,]
        
        df <- df[, !(names(df) %in% c("drift"))]
        
        df_melt <- melt(df, id.vars = c("idx", "class", "type"))
        
        g <- ggplot(data=df_melt, aes(x=idx, y=value)) + geom_line(aes(color=type)) + 
          ggh4x::facet_grid2(class~variable,scales = "free_y", independent = "y")
          #geom_vline(aes(xintercept=idx, alpha=drift), linetype=3, color="red") 
        
        #ggsave(paste0("./distance_", stream_name, ".pdf"), height=10, width=18)
        #break;
      }
    }
  }
}



