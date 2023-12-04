import pandas as pd


df = pd.read_csv("./agg_metrics.csv")

df.groupby(["clf","n_classes","c_affected"]).agg(["mean"]).reset_index().to_csv("summarized_df.csv", index=None)