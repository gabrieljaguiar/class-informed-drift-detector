from glob import glob
import pandas as pd
import numpy as np

dd_data = pd.read_csv("./results_dd_update.csv")
dd_data_ciddm = pd.read_csv("./results_ciddm_updated.csv")
dd_data_ciddm["classif"] = "HT"
dd_data_ciddm["dd"] = "CIDDM"
dd_data = pd.concat([dd_data, dd_data_ciddm], axis=0)

dd_data = dd_data[dd_data["classif"]== "HT"]

dd_data = dd_data[dd_data["n_class"] < 20]

dd_data.drop(["stream"], inplace=True, axis=1)
sum_df = dd_data.groupby(["n_class", "drift_type", "classif", "dd"]).sum()
avg_df = dd_data.groupby(["n_class", "drift_type", "classif", "dd"]).mean()

final_df = sum_df
final_df["avg_delay"] = avg_df["avg_delay"]
final_df["precision"] = final_df["tp"]/(final_df["tp"]+final_df["fp"]) #if (final_df["tp"]+final_df["fp"]) > 0 else 0
final_df["precision"].fillna(0, inplace=True)
final_df["recall"] = final_df["tp"]/(final_df["tp"]+final_df["fn"]) #if (dd_data["tp"]+dd_data["fn"]) > 0 else 0
final_df["recall"].fillna(0, inplace=True)
final_df["f1"] = 2*final_df["precision"]*final_df["recall"]/(final_df["precision"]+final_df["recall"])
final_df["f1"].fillna(0, inplace=True)

final_df.reset_index(inplace=True)

final_df[final_df["drift_type"] == "gradual"].to_csv("ht_gradual_utd.csv")
final_df[final_df["drift_type"] == "sudden"].to_csv("ht_sudden_utd.csv")